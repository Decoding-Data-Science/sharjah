"""Helper functions for the Airport Agent workshop.

This file holds the plumbing (API key, retries, loading files, printing). The ideas that you learn
in the workshop (prompts, SQL, RAG, agents) are written out in full inside the notebooks.
All data and documents are fictional.
"""
import getpass
import glob
import os
import random
import re
import sqlite3
import time
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from google import genai
from google.genai import types

# ----------------------------------------------------------------------------- locations
KIT = os.environ.get("AIRPORT_KIT", "/content/Airport_Agent_Workshop_Kit")
if not os.path.isdir(KIT):  # running from the kit folder on a laptop
    KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(KIT, "01_Database", "airport_ops.db")
DOCS_DIR = os.path.join(KIT, "02_Documents")

# ----------------------------------------------------------------------------- models
MODEL_CANDIDATES = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"]
EMBED_MODEL = "gemini-embedding-001"
EMBED_MODEL_NEW = "gemini-embedding-2"
THINKING_LEVELS = ["low", "medium", "high"]  # "minimal" is not supported by gemini-3.8-flash (it returns an error)

# Standard-tier prices in USD per 1 million tokens for gemini-3.8-flash (thinking tokens are billed as output).
PRICE_INTRO = {"input": 0.75, "output": 3.75}   # through 31 December 2026
PRICE_FROM_2027 = {"input": 1.50, "output": 7.50}  # from 1 January 2027


# ----------------------------------------------------------------------------- client and retries
def get_api_key():
    try:
        from google.colab import userdata
        return userdata.get("GEMINI_API_KEY")
    except Exception as e:  # not in Colab, or the secret is missing or notebook access is off
        key = os.environ.get("GEMINI_API_KEY")
        if key:
            return key
        print("Could not read the secret GEMINI_API_KEY from Colab Secrets (" + type(e).__name__ + ").")
        print("Fix: click the key icon on the left, add GEMINI_API_KEY, and switch on 'Notebook access'.")
        return getpass.getpass("Or paste your Gemini API key here (it will not be saved): ")


def make_client():
    return genai.Client(api_key=get_api_key())


def retry(fn, *args, tries=5, **kwargs):
    """Call fn, and retry with a growing pause when the service is busy or the rate limit is reached."""
    for attempt in range(tries):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            text = str(e)
            transient = any(s in text for s in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE", "500", "INTERNAL", "DEADLINE"))
            if not transient or attempt == tries - 1:
                raise
            wait = min(60, 2 ** attempt * 3) + random.random()
            print(f"[retry] the service is busy or the rate limit was reached. Waiting {wait:.0f} seconds (attempt {attempt + 1} of {tries - 1}).")
            time.sleep(wait)


def pick_model(client, candidates=None):
    """Return the first model in the list that answers a tiny test call."""
    for m in candidates or MODEL_CANDIDATES:
        try:
            retry(client.models.generate_content, model=m, contents="Reply with the single word OK.",
                  config=types.GenerateContentConfig(max_output_tokens=200))
            print(f"Using model: {m}")
            return m
        except Exception as e:
            print(f"Model {m} not available ({str(e)[:120]}). Trying the next one.")
    raise RuntimeError("No Gemini model answered. Check the API key, the billing status of the project and your internet access.")


# ----------------------------------------------------------------------------- generate
@dataclass
class Result:
    text: str
    parsed: object = None
    usage: dict = field(default_factory=dict)
    seconds: float = 0.0
    truncated: bool = False
    raw: object = None


def usage_of(resp):
    u = getattr(resp, "usage_metadata", None)
    if u is None:
        return {"prompt": 0, "output": 0, "thinking": 0, "total": 0}
    return {"prompt": u.prompt_token_count or 0, "output": u.candidates_token_count or 0,
            "thinking": getattr(u, "thoughts_token_count", 0) or 0, "total": u.total_token_count or 0}


def generate(client, model, prompt, system=None, level=None, max_tokens=None, schema=None, **extra):
    """One call to Gemini. level = thinking level (low, medium, high). schema = a pydantic class for JSON output."""
    cfg = dict(extra)
    if system:
        cfg["system_instruction"] = system
    if level:
        cfg["thinking_config"] = types.ThinkingConfig(thinking_level=level)
    if max_tokens:
        cfg["max_output_tokens"] = max_tokens
    if schema is not None:
        cfg["response_mime_type"] = "application/json"
        cfg["response_schema"] = schema
    t0 = time.time()
    resp = retry(client.models.generate_content, model=model, contents=prompt, config=types.GenerateContentConfig(**cfg))
    secs = time.time() - t0
    finish = ""
    try:
        finish = str(resp.candidates[0].finish_reason)
    except Exception:
        pass
    return Result(text=resp.text or "", parsed=getattr(resp, "parsed", None), usage=usage_of(resp), seconds=secs,
                  truncated="MAX_TOKENS" in finish, raw=resp)


def show_usage(r):
    u = r.usage
    print(f"[tokens] prompt {u['prompt']}, answer {u['output']}, thinking {u['thinking']}, total {u['total']} | {r.seconds:.1f} s"
          + ("  | ANSWER WAS CUT OFF (max_output_tokens too small)" if r.truncated else ""))


def cost_usd(usage, prices=None):
    prices = prices or PRICE_INTRO
    return (usage["prompt"] * prices["input"] + (usage["output"] + usage["thinking"]) * prices["output"]) / 1e6


# ----------------------------------------------------------------------------- database
def sql(query, params=None):
    """Run a read-only SQL query and return a table."""
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        return pd.read_sql_query(query, con, params=params)
    finally:
        con.close()


def schema_text():
    """Plain-text description of the database, built from the data_dictionary table. This is the model's map."""
    dd = sql("SELECT * FROM data_dictionary")
    meta = sql("SELECT key, value, note FROM meta")
    lines = ["DATABASE airport_ops.db (SQLite). Fictional general international airport, 1 Oct 2025 to 30 Sep 2026. Currency AED.", ""]
    for _, r in meta.iterrows():
        lines.append(f"- {r['key']}: {r['value']} ({r['note']})")
    lines.append("")
    for t in dd["table_name"].unique():
        part = dd[dd["table_name"] == t]
        head = part[part["column_name"].isin(["(table)", "(view)"])].iloc[0]
        kind = "VIEW" if head["column_name"] == "(view)" else "TABLE"
        lines.append(f"{kind} {t}: {head['description']}")
        for _, c in part[~part["column_name"].isin(["(table)", "(view)"])].iterrows():
            lines.append(f"  {c['column_name']} ({c['data_type']}): {c['description']}")
        lines.append("")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- documents and embeddings
def load_chunks(docs_dir=DOCS_DIR):
    """Read every policy document and split it into sections. Each section keeps its document, version and status."""
    chunks = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "GIA-*.txt"))):
        text = open(path, encoding="utf-8").read()
        lines = text.split("\n")
        source = lines[0].strip()
        doc_no = re.search(r"Document (GIA-[A-Z]+-\d+)", lines[1]).group(1)
        version = re.search(r"Version (.*)$", lines[1]).group(1).strip()
        status = re.search(r"Status: (.*?) \|", lines[2]).group(1).strip()
        effective = re.search(r"Effective: (.*?) \|", lines[2]).group(1).strip()
        review = re.search(r"Next review: (.*)$", lines[2]).group(1).strip()
        title = source.split(" (version")[0]
        for part in re.split(r"\n(?=Section \d+\.)", text)[1:]:
            part = part.strip()
            head = part.split("\n")[0]
            chunks.append(dict(doc_no=doc_no, title=title, version=version, status=status, effective=effective,
                               review=review, in_force=status.startswith("APPROVED"), source=source, section=head,
                               section_no=int(re.match(r"Section (\d+)\.", head).group(1)), text=part,
                               file=os.path.basename(path)))
    return chunks


def embed(client, texts, kind="document", model=EMBED_MODEL, dims=768, normalize=True, titles=None):
    """Turn texts into vectors. kind is 'document' or 'query'. Works for gemini-embedding-001 and gemini-embedding-2."""
    is_new = model.startswith("gemini-embedding-2")
    vectors = []
    for i in range(0, len(texts), 50):
        batch = texts[i:i + 50]
        if is_new:  # no task_type for this model: the task goes into the text, one Content per text
            if kind == "query":
                items = [f"task: search result | query: {t}" for t in batch]
            else:
                items = [f"title: {(titles[i + j] if titles else 'none')} | text: {t}" for j, t in enumerate(batch)]
            contents = [types.Content(parts=[types.Part(text=t)]) for t in items]
            cfg = types.EmbedContentConfig(output_dimensionality=dims)
        else:
            contents = batch
            cfg = types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT" if kind == "document" else "RETRIEVAL_QUERY",
                                           output_dimensionality=dims)
        res = retry(client.models.embed_content, model=model, contents=contents, config=cfg)
        vectors += [e.values for e in res.embeddings]
    v = np.array(vectors, dtype="float32")
    if normalize:  # gemini-embedding-001 needs this for any size other than 3072
        v = v / np.linalg.norm(v, axis=1, keepdims=True)
    return v


class Index:
    """A small vector index over document sections."""

    def __init__(self, client, chunks, model=EMBED_MODEL, dims=768, texts=None):
        self.client, self.chunks, self.model, self.dims = client, chunks, model, dims
        texts = texts or [c["source"] + "\n" + c["text"] for c in chunks]
        self.vecs = embed(client, texts, "document", model, dims, titles=[c["title"] for c in chunks])

    def search(self, question, k=3, only_in_force=False, qvec=None):
        q = qvec if qvec is not None else embed(self.client, [question], "query", self.model, self.dims)[0]
        scores = self.vecs @ q
        out = []
        for i in np.argsort(-scores):
            c = self.chunks[i]
            if only_in_force and not c["in_force"]:
                continue
            out.append((float(scores[i]), c))
            if len(out) == k:
                break
        return out


def format_hits(hits):
    return "\n\n".join(f"[{c['doc_no']} | {c['section']} | {c['status']}] (relevance {s:.2f})\n{c['text']}" for s, c in hits)


# ----------------------------------------------------------------------------- agent helpers
@dataclass
class Answer:
    text: str
    tools: list
    seconds: float
    usage: dict


def ask(chat, question, log, show=True):
    """Send a question to the agent, then print which tools it used and its answer."""
    log.clear()
    t0 = time.time()
    resp = retry(chat.send_message, question)
    secs = time.time() - t0
    text = resp.text or "(no text returned)"
    if show:
        print("QUESTION:", question, "\n")
        print(f"TOOLS CALLED ({len(log)}):")
        for name, arg, _ in log:
            print(f"  - {name}: {str(arg)[:400]}")
        print(f"\nANSWER ({secs:.0f} s):\n{text}")
    return Answer(text=text, tools=list(log), seconds=secs, usage=usage_of(resp))


def numbers_in(text):
    """All numbers written in a text (thousands separators allowed), as floats."""
    return [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", text)]


def contains_number(text, truth, tol=0.5):
    return any(abs(n - truth) <= tol for n in numbers_in(text))


# ----------------------------------------------------------------------------- smoke test
def smoke_test(client, model=None):
    """Check every Gemini feature the workshop uses. Takes about two minutes. Returns a table of PASS/FAIL."""
    rows = []

    def run(name, fn):
        t0 = time.time()
        try:
            note = fn()
            rows.append((name, "PASS", str(note)[:110], round(time.time() - t0, 1)))
        except Exception as e:
            rows.append((name, "FAIL", f"{type(e).__name__}: {str(e)[:150]}", round(time.time() - t0, 1)))
        print(rows[-1][0], "->", rows[-1][1], "|", rows[-1][2])

    chosen = {}

    def t_model():
        chosen["m"] = model or pick_model(client)
        return chosen["m"]
    run("1 A Gemini model answers", t_model)
    m = chosen.get("m") or MODEL_CANDIDATES[0]

    def t_text():
        r = generate(client, m, "Name one airport service in five words.", max_tokens=300)
        return r.text.strip()[:60]
    run("2 Plain text call", t_text)

    def t_levels():
        out = []
        for lv in THINKING_LEVELS:
            r = generate(client, m, "What is 17 x 23? Answer with the number only.", level=lv, max_tokens=800)
            out.append(f"{lv}: thinking tokens {r.usage['thinking']}")
        return "; ".join(out)
    run("3 thinking_level low, medium, high", t_levels)

    def t_minimal():
        try:
            generate(client, m, "Hi", level="minimal", max_tokens=100)
        except Exception as e:
            return "minimal is rejected as expected: " + str(e)[:60]
        return "minimal was accepted by this model (fine, but do not rely on it)"
    run("4 thinking_level minimal (expected to be rejected by 3.8)", t_minimal)

    def t_json():
        from pydantic import BaseModel

        class Ticket(BaseModel):
            category: str
            severity: str
        r = generate(client, m, "Complaint: the passport queue was 50 minutes and I missed my flight.", schema=Ticket, max_tokens=500)
        return f"parsed={r.parsed}"
    run("5 JSON output with a schema", t_json)

    def t_embed1():
        v = embed(client, ["passport queue", "baggage belt"], "document", EMBED_MODEL, 768)
        return f"{EMBED_MODEL}: shape {v.shape}, norm {np.linalg.norm(v[0]):.2f}"
    run("6 Embeddings gemini-embedding-001", t_embed1)

    def t_embed2():
        v = embed(client, ["passport queue", "baggage belt"], "document", EMBED_MODEL_NEW, 768)
        return f"{EMBED_MODEL_NEW}: shape {v.shape} (must be 2 rows)"
    run("7 Embeddings gemini-embedding-2", t_embed2)

    def t_tool():
        calls = []

        def count_flights(day: str) -> str:
            """Return the number of flights on a given day.

            Args:
                day: Date in YYYY-MM-DD format.
            """
            calls.append(day)
            return "There were 53 flights on that day."
        chat = client.chats.create(model=m, config=types.GenerateContentConfig(tools=[count_flights]))
        resp = retry(chat.send_message, "How many flights were there on 2026-03-02? Use the tool.")
        assert calls, "the model never called the tool"
        assert "53" in (resp.text or ""), "the answer did not use the tool result"
        return f"tool called with {calls[0]}, answer: {resp.text.strip()[:50]}"
    run("8 Function calling (the agent loop)", t_tool)

    def t_burst():
        for _ in range(6):
            generate(client, m, "Say OK.", max_tokens=100)
        return "6 quick calls without a rate-limit error"
    run("9 Six calls in a row (rate limit check)", t_burst)

    df = pd.DataFrame(rows, columns=["check", "result", "detail", "seconds"])
    print("\nPASSED", int((df.result == "PASS").sum()), "of", len(df))
    return df
