"""Animated SVG diagrams. ANIM=True for the website (SMIL animation, started when scrolled into view).
ANIM=False for the printed handbook (static, complete at rest)."""
import html

ANIM = True

C = dict(bg="#070b12", panel="#0c121c", panel2="#101827", line="#2a4358", ice="#8fd3ff", amber="#ffb02e",
         text="#e8eef5", mute="#8da0b5", ok="#7fe0b0", bad="#ff7a7a", faint="#3a5166")


def e(s):
    return html.escape(s, quote=True)


def tx(x, y, s, size=15, fill=None, w=400, a="start", ls=None, mono=False):
    fill = fill or C["text"]
    fam = ' font-family="JetBrains Mono,Consolas,DejaVu Sans Mono,monospace"' if mono else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{w}" text-anchor="{a}"{l}{fam}>{e(s)}</text>'


def label(x, y, s, a="start", fill=None):
    return tx(x, y, s.upper(), 12, fill or C["amber"], 700, a, ls="2")


def box(x, y, w, h, title, sub=None, accent=None, fill=None, stroke=None, tsize=16, ssize=13, sub2=None):
    stroke = stroke or (accent or C["line"])
    fill = fill or C["panel"]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>']
    if accent:
        out.append(f'<rect x="{x}" y="{y}" width="34" height="3" fill="{accent}"/>')
    cx = x + w / 2
    if sub is None:
        out.append(tx(cx, y + h / 2 + 5, title, tsize, C["text"], 700, "middle"))
    else:
        ty = y + h / 2 - (6 if sub2 is None else 14)
        out.append(tx(cx, ty, title, tsize, C["text"], 700, "middle"))
        out.append(tx(cx, ty + 22, sub, ssize, C["mute"], 400, "middle"))
        if sub2:
            out.append(tx(cx, ty + 40, sub2, ssize, C["mute"], 400, "middle"))
    return "".join(out)


def chip(x, y, w, s, color=None, h=24, size=12.5, fill=None):
    color = color or C["ice"]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill or "none"}" stroke="{color}" stroke-width="1"/>'
            + tx(x + w / 2, y + h / 2 + 4.5, s, size, color, 600, "middle"))


def arrow(uid, d, color=None, dash=None, w=1.6):
    color = color or C["ice"]
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da} marker-end="url(#{uid}a)"/>'


def line(x1, y1, x2, y2, color=None, w=1, dash=None):
    color = color or C["line"]
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da}/>'


def packet(d, dur=3.0, begin=0.0, color=None, r=4.5):
    if not ANIM:
        return ""
    color = color or C["amber"]
    return (f'<circle r="{r}" fill="{color}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{d}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')


def pulse(inner, dur=3, begin=0, lo=0.35, hi=1.0):
    if not ANIM:
        return inner
    return (f'<g>{inner}<animate attributeName="opacity" values="{lo};{hi};{lo}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>')


def svg(uid, w, h, inner, desc):
    marker = (f'<marker id="{uid}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
              f'<path d="M0,0 L10,5 L0,10 z" fill="{C["ice"]}"/></marker>')
    play = ' data-play="1"' if ANIM else ""
    return (f'<figure class="fig"><svg class="dg" id="{uid}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{e(desc)}"{play} '
            f'style="font-family:Inter,\'Segoe UI\',Arial,sans-serif"><defs>{marker}</defs>'
            f'<rect width="{w}" height="{h}" fill="{C["bg"]}"/>{inner}</svg></figure>')


def caption(fig, text):
    return fig.replace("</figure>", f"<figcaption>{html.escape(text)}</figcaption></figure>")


# ------------------------------------------------------------------ 1. journey
def journey():
    u = "gj"
    xs = [170, 480, 790]
    days = [("Mon 2 Nov", "Day 1 | Ask", "Explore  Prompt  Retrieve  Query", "Copilot, Colab, Gemini, SQL"),
            ("Tue 3 Nov", "Day 2 | Build", "Measure  Agent  Tune  Attack", "Tools, loop, harness, tests"),
            ("Wed 4 Nov", "Day 3 | Prove", "Govern  Brief  Demo  Monday", "One verified page")]
    o = [line(60, 100, 900, 100, C["faint"], 2, "6 6")]
    if ANIM:
        o.append(f'<line x1="60" y1="100" x2="900" y2="100" stroke="{C["ice"]}" stroke-width="2" stroke-dasharray="16 700"><animate attributeName="stroke-dashoffset" values="0;-716" dur="5s" repeatCount="indefinite"/></line>')
    else:
        o.append(line(60, 100, 900, 100, C["ice"], 2))
    for i, (x, d) in enumerate(zip(xs, days)):
        col = C["amber"] if i == 2 else C["ice"]
        o.append(label(x, 46, d[0], "middle", C["mute"]))
        o.append(f'<circle cx="{x}" cy="100" r="30" fill="{C["panel"]}" stroke="{col}" stroke-width="2"/>')
        o.append(tx(x, 109, str(i + 1), 26, col, 700, "middle"))
        if ANIM:
            o.append(f'<circle cx="{x}" cy="100" r="30" fill="none" stroke="{col}" stroke-width="1"><animate attributeName="r" values="30;46;30" dur="3.6s" begin="{i*1.2}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0;0.7" dur="3.6s" begin="{i*1.2}s" repeatCount="indefinite"/></circle>')
        o.append(tx(x, 168, d[1], 22, C["text"], 700, "middle"))
        o.append(tx(x, 196, d[2], 14, C["mute"], 400, "middle"))
        o.append(tx(x, 218, d[3], 14, col, 600, "middle"))
    o.append(packet("M60,100 L900,100", 6, 0, C["amber"], 5))
    return svg(u, 960, 250, "".join(o), "Three days from Ask on Monday, to Build on Tuesday, to Prove on Wednesday")


# ------------------------------------------------------------------ 2. four layers
def layers():
    u = "gl"
    rows = [("1", "Prompt", "The instruction you write: role, context, task, format, rules", "Day 1"),
            ("2", "Context", "What the model can see: files, documents, schema, examples", "Days 1 and 2"),
            ("3", "Harness", "Guardrails and tools: read-only, caps, filters, logs", "Day 2"),
            ("4", "Loop", "Plan, act, check, repeat. Test again after every change", "Days 2 and 3")]
    o = []
    for i, (n, t, d, day) in enumerate(rows):
        y = 16 + i * 78
        col = C["amber"] if i == 3 else C["ice"]
        o.append(f'<rect x="20" y="{y}" width="920" height="64" fill="{C["panel"]}" stroke="{C["line"]}"/>')
        bar = f'<rect x="20" y="{y}" width="6" height="64" fill="{col}"/>'
        if ANIM:
            bar = (f'<rect x="20" y="{y}" width="6" height="64" fill="{col}"><animate attributeName="width" values="6;900;6" keyTimes="0;0.12;1" dur="8s" begin="{i*1.6}s" repeatCount="indefinite" calcMode="spline" keySplines="0.2 0.8 0.2 1;0.4 0 0.2 1"/>'
                   f'<animate attributeName="opacity" values="1;0.12;1" keyTimes="0;0.12;1" dur="8s" begin="{i*1.6}s" repeatCount="indefinite"/></rect>')
        o.append(bar)
        o.append(tx(60, y + 41, n, 30, col, 700))
        o.append(tx(100, y + 28, t, 20, C["text"], 700))
        o.append(tx(100, y + 50, d, 14, C["mute"]))
        o.append(chip(820, y + 20, 100, day, col))
    return svg(u, 960, 340, "".join(o), "The four layers: prompt, context, harness and loop")


# ------------------------------------------------------------------ 3. RAG pipeline
def rag():
    u = "gr"
    X = [20 + i * 192 for i in range(5)]
    W = 152
    o = [label(20, 30, "Indexing, once"), label(20, 206, "Every question")]
    # lane 1
    l1 = [("12 documents", "10 approved", "1 draft, 1 superseded"), ("1 Split", "by section,", "status in the header"), ("2 Embed", "meaning to", "a list of numbers"), ("Vector store", "sections, vectors,", "document status")]
    for i, (t, s1, s2) in enumerate(l1):
        o.append(box(X[i], 46, W, 92, t, s1, C["ice"] if i else None, sub2=s2))
        if i:
            o.append(arrow(u, f"M{X[i-1]+W},92 L{X[i]-4},92"))
    # docs chips inside first box
    o.append(packet(f"M{X[0]+W},92 L{X[3]},92", 3.2, 0))
    # lane 2
    l2 = [("Question", "plain English", None), ("Embed", "question to", "numbers"), ("3 Compare", "top-k = 4", "closest sections"), ("Filter", "approved only", "status and date"), ("4 Answer", "cites document", "and clause")]
    for i, (t, s1, s2) in enumerate(l2):
        acc = C["amber"] if i == 3 else (C["ice"] if i else None)
        o.append(box(X[i], 222, W, 92, t, s1, acc, sub2=s2))
        if i:
            o.append(arrow(u, f"M{X[i-1]+W},268 L{X[i]-4},268"))
    # store to compare
    o.append(arrow(u, f"M{X[3]+W/2},138 L{X[3]+W/2},178 L{X[2]+W/2},178 L{X[2]+W/2},218", C["faint"], "5 4"))
    o.append(packet(f"M{X[3]+W/2},138 L{X[3]+W/2},178 L{X[2]+W/2},178 L{X[2]+W/2},218", 3.2, 1.0, C["ice"]))
    o.append(packet(f"M{X[0]+W},268 L{X[4]},268", 4.4, 0))
    # filter chips
    cy = 332
    o.append(chip(X[3], cy, W, "POL-01 passes", C["ok"]))
    o.append(chip(X[3], cy + 30, W, "DRAFT-11 held back", C["amber"]))
    o.append(chip(X[3], cy + 60, W, "SUP-12 held back", C["bad"]))
    o.append(chip(X[4], cy, W, "[GIA-POL-01 clause 2.3]", C["ok"]))
    o.append(tx(X[4] + W / 2, cy + 44, "15 minutes, no more", 13, C["mute"], 400, "middle"))
    o.append(tx(X[4] + W / 2, cy + 62, "than 5% over 30", 13, C["mute"], 400, "middle"))
    o.append(tx(20, 436, "Similar is not the same as valid. A filter beats a clever prompt.", 15, C["text"], 600))
    return svg(u, 960, 460, "".join(o), "RAG pipeline: split, embed, store, then for each question embed, compare, filter by status, and answer with a citation")


# ------------------------------------------------------------------ 4. embeddings map
def embeddings():
    u = "ge"
    o = [line(40, 260, 580, 260, C["faint"], 1), line(40, 260, 40, 20, C["faint"], 1),
         tx(580, 280, "meaning", 12, C["mute"], 400, "end"), tx(46, 30, "meaning", 12, C["mute"])]
    pts = [(170, 110, "The passport queue was too long", C["ice"]), (230, 160, "Waiting at immigration took forever", C["ice"]),
           (430, 210, "The coffee shop sells excellent dates", C["mute"])]
    o.append(f'<ellipse cx="200" cy="135" rx="120" ry="58" fill="none" stroke="{C["ice"]}" stroke-dasharray="4 5" opacity="0.6"/>')
    o.append(line(170, 110, 230, 160, C["ice"], 1.4))
    for x, y, s, col in pts:
        o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{col}"/>')
    o.append(tx(170, 92, pts[0][2], 13, C["text"], 500, "middle"))
    o.append(tx(262, 188, pts[1][2], 13, C["text"], 500, "middle"))
    o.append(tx(430, 240, pts[2][2], 13, C["mute"], 400, "middle"))
    o.append(f'<path d="M205,210 l5,-12 l5,12 l-13,-8 h16 z" fill="{C["amber"]}" transform="translate(0,0)"/>')
    o.append(tx(210, 232, "Your question", 12, C["amber"], 700, "middle"))
    o.append(tx(400, 40, "Close means similar meaning,", 14, C["text"], 600, "middle"))
    o.append(tx(400, 60, "even with no shared words.", 14, C["text"], 600, "middle"))
    if ANIM:
        o.append(f'<circle cx="200" cy="135" r="4" fill="none" stroke="{C["ice"]}"><animate attributeName="r" values="4;70;4" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0;0.8" dur="4s" repeatCount="indefinite"/></circle>')
    return svg(u, 620, 300, "".join(o), "Embedding map: two queue sentences sit close together, the coffee sentence is far away")


# ------------------------------------------------------------------ 5. the 4 percent sample
def sample():
    u = "gs"
    hot = {7, 34, 58, 91}
    o = [label(40, 28, "Every square is 1 percent of passengers")]
    for i in range(100):
        r, c = divmod(i, 10)
        x, y = 40 + c * 26, 44 + r * 26
        on = i in hot
        fill = C["amber"] if on else C["panel2"]
        sq = f'<rect x="{x}" y="{y}" width="22" height="22" fill="{fill}" stroke="{C["line"]}"/>'
        if on and ANIM:
            sq = f'<rect x="{x}" y="{y}" width="22" height="22" fill="{fill}" stroke="{C["amber"]}"><animate attributeName="opacity" values="1;0.35;1" dur="2.4s" begin="{(i%4)*0.4}s" repeatCount="indefinite"/></rect>'
        o.append(sq)
    o.append(tx(40, 330, "4 squares = the sample: 108,488 journeys", 14, C["amber"], 600))
    o.append(arrow(u, "M320,150 L420,150", C["amber"], None, 2.2))
    o.append(tx(370, 136, "x 25", 22, C["amber"], 700, "middle"))
    o.append(box(430, 100, 230, 100, "Estimated passengers", "COUNT(*) x 25", C["amber"], sub2="about 2.7 million"))
    o.append(box(690, 60, 250, 74, "Counts", "multiply by 25", C["ok"]))
    o.append(box(690, 150, 250, 74, "Averages, percentages", "never multiply", C["bad"]))
    o.append(tx(560, 270, "Always say: estimated from a 4 percent sample.", 15, C["text"], 600, "middle"))
    o.append(tx(560, 296, "Multiplying an average by 25 is the classic wrong answer.", 14, C["mute"], 400, "middle"))
    return svg(u, 960, 350, "".join(o), "A 4 percent sample: counts are multiplied by 25, averages and percentages are not")


# ------------------------------------------------------------------ 6. agent
def agent():
    u = "ga"
    o = []
    o.append(f'<rect x="580" y="30" width="360" height="360" fill="none" stroke="{C["amber"]}" stroke-dasharray="7 6" opacity="0.8"/>')
    o.append(label(598, 54, "Harness"))
    o.append(box(20, 170, 160, 90, "Manager asks", "plain English"))
    o.append(box(300, 120, 200, 190, "Gemini", "the reasoning engine", C["ice"], fill=C["panel2"], tsize=22, sub2="reads, decides, repeats"))
    o.append(box(610, 76, 300, 112, "SQL tool", "facts from the database", C["ice"], sub2="SELECT only | read-only | 40 rows"))
    o.append(box(610, 236, 300, 112, "Document tool", "rules from approved documents", C["ice"], sub2="top 4 sections | cited"))
    o.append(box(300, 360, 200, 60, "Answer", "numbers, clauses, limits", C["amber"]))
    o.append(arrow(u, "M180,215 L296,215"))
    o.append(arrow(u, "M500,170 C540,170 560,132 606,132"))
    o.append(arrow(u, "M606,152 C560,152 540,190 500,190", C["faint"], "5 4"))
    o.append(arrow(u, "M500,260 C540,260 560,292 606,292"))
    o.append(arrow(u, "M606,312 C560,312 540,280 500,280", C["faint"], "5 4"))
    o.append(arrow(u, "M400,310 L400,356", C["amber"]))
    o.append(tx(400, 96, "The loop", 13, C["amber"], 700, "middle", "2"))
    o.append(tx(400, 112, "call, read, decide again", 12, C["mute"], 400, "middle"))
    o.append(packet("M180,215 L296,215", 2.4, 0, C["amber"]))
    o.append(packet("M500,170 C540,170 560,132 606,132", 2.4, 0.8, C["ice"]))
    o.append(packet("M606,152 C560,152 540,190 500,190", 2.4, 1.6, C["ok"]))
    o.append(packet("M500,260 C540,260 560,292 606,292", 2.4, 0.4, C["ice"]))
    o.append(packet("M606,312 C560,312 540,280 500,280", 2.4, 1.2, C["ok"]))
    o.append(packet("M400,310 L400,356", 2.4, 2.0, C["amber"]))
    o.append(tx(20, 300, "Agent = Model + Tools + Loop", 16, C["text"], 700))
    o.append(tx(20, 324, "Facts from SQL. Rules from documents.", 14, C["mute"]))
    o.append(tx(20, 344, "The loop joins them.", 14, C["mute"]))
    return svg(u, 960, 440, "".join(o), "An agent: the manager asks, Gemini decides, calls the SQL tool and the document tool inside a harness, then answers")


# ------------------------------------------------------------------ 7. harness gates
def gates():
    u = "gh"
    gx = [290, 405, 520, 635, 750]
    names = ["SELECT only", "Writes blocked", "Read-only file", "40-row cap", "Every call logged"]
    o = []
    o.append(label(20, 28, "A good query"))
    o.append(box(20, 70, 190, 56, "SELECT AVG(wait) ...", None, None, tsize=14))
    o.append(line(210, 98, 880, 98, C["faint"], 2, "5 5"))
    for x, n in zip(gx, names):
        o.append(f'<rect x="{x-5}" y="52" width="10" height="92" fill="{C["ice"]}" opacity="0.9"/>')
        o.append(tx(x, 168, n, 12, C["text"], 600, "middle"))
    o.append(box(800, 64, 140, 68, "Result", "max 40 rows", C["ok"]))
    o.append(packet("M210,98 L800,98", 4.2, 0, C["ok"], 5))
    o.append(packet("M210,98 L800,98", 4.2, 2.1, C["ok"], 5))
    o.append(label(20, 214, "A bad query", fill=C["bad"]))
    o.append(box(20, 250, 190, 56, "DROP TABLE flights", None, None, tsize=14))
    o.append(line(210, 278, 430, 278, C["faint"], 2, "5 5"))
    o.append(f'<rect x="{gx[1]-5}" y="232" width="10" height="92" fill="{C["bad"]}"/>')
    o.append(tx(gx[1], 346, "Blocked at gate 2", 13, C["bad"], 700, "middle"))
    o.append(f'<g stroke="{C["bad"]}" stroke-width="3"><line x1="{gx[1]+20}" y1="262" x2="{gx[1]+44}" y2="286"/><line x1="{gx[1]+44}" y1="262" x2="{gx[1]+20}" y2="286"/></g>')
    o.append(arrow(u, f"M{gx[1]+60},306 C{gx[1]+120},330 {gx[1]+180},330 {gx[1]+240},306", C["bad"], "5 4"))
    o.append(box(690, 250, 250, 56, "Refused: only SELECT", "queries are allowed", C["bad"], tsize=14, ssize=13))
    if ANIM:
        o.append(f'<circle r="5" cx="210" cy="278" fill="{C["bad"]}"><animate attributeName="cx" values="210;405;210" keyTimes="0;0.5;1" dur="4.2s" repeatCount="indefinite"/></circle>')
    o.append(tx(20, 372, "The model asks. Your code decides. A blocked query returns text, so the model can try again.", 14, C["mute"]))
    return svg(u, 960, 392, "".join(o), "Harness gates: a SELECT passes five gates, a DROP TABLE is blocked at gate two")


# ------------------------------------------------------------------ 8. tokens
def tokens():
    u = "gt"
    o = [label(20, 28, "In: input tokens"), label(520, 28, "Out: output tokens")]
    ins = ["System rules", "Tool definitions", "Schema and examples", "Retrieved sections", "Question and history", "Tool results"]
    for i, s in enumerate(ins):
        o.append(chip(20, 44 + i * 32, 200, s, C["ice"], 26))
    o.append(box(300, 80, 150, 100, "Gemini", "reads, thinks,", C["ice"], sub2="writes"))
    o.append(arrow(u, "M222,104 L296,126"))
    o.append(arrow(u, "M222,200 L296,150"))
    o.append(arrow(u, "M450,130 L516,100"))
    o.append(arrow(u, "M450,150 L516,170"))
    o.append(box(520, 44, 200, 92, "Thinking tokens", "hidden reasoning", C["amber"], sub2="billed as output"))
    o.append(box(520, 150, 200, 70, "Answer tokens", "what you read", C["amber"]))
    o.append(packet("M222,104 L296,126", 2.6, 0, C["ice"]))
    o.append(packet("M222,200 L296,150", 2.6, 0.7, C["ice"]))
    o.append(packet("M450,130 L516,100", 2.6, 1.4, C["amber"]))
    # price bars
    o.append(label(20, 262, "Price per million tokens"))
    o.append(tx(20, 292, "Input", 14, C["text"], 600)); o.append(f'<rect x="90" y="278" width="60" height="18" fill="{C["ice"]}"/>'); o.append(tx(160, 292, "USD 0.75", 14, C["ice"], 700))
    o.append(tx(20, 322, "Output", 14, C["text"], 600)); o.append(f'<rect x="90" y="308" width="280" height="18" fill="{C["amber"]}"/>'); o.append(tx(380, 322, "USD 3.75 (5x)", 14, C["amber"], 700))
    # agent loop multiplier
    o.append(label(520, 262, "An agent re-sends the context every turn"))
    for i, (w, t) in enumerate([(90, "Turn 1"), (170, "Turn 2"), (250, "Turn 3")]):
        y = 276 + i * 30
        o.append(f'<rect x="520" y="{y}" width="{w}" height="22" fill="{C["panel2"]}" stroke="{C["ice"]}"/>')
        o.append(tx(526 + w + 8, y + 16, f"{t}: input grows", 13, C["mute"]))
    o.append(tx(20, 372, "Pay for tokens, not answers. Measure one question, then multiply by calls and users.", 14, C["text"], 600))
    return svg(u, 960, 392, "".join(o), "Token flow: input tokens cost less than output tokens, and an agent loop re-sends the context each turn")


# ------------------------------------------------------------------ 9. model taxonomy
def taxonomy():
    u = "gm"
    cols = [
        ("By access", [("Closed, API only", ["Gemini", "GPT", "Claude"], 0), ("Open-weight", ["Llama", "Qwen", "DeepSeek", "Mistral", "Gemma", "Phi"], 0), ("Fully open", ["OLMo"], 0)]),
        ("By size and speed", [("Frontier or Pro", ["Gemini 4 Argon"], 0), ("Flash", ["Gemini 3.8 Flash", "Gemini 3.6 Flash"], 0), ("Flash-Lite", ["Gemini 3.5 Flash-Lite", "Gemini 3.1 Flash-Lite"], 1), ("Small open", ["Gemma 4"], 0)]),
        ("By job", [("Text and reasoning", ["chat, analysis, tools"], 0), ("Embeddings", ["search by meaning"], 0), ("Multimodal and media", ["image, video, audio, live"], 0)]),
        ("By where it runs", [("Cloud API", ["fast start"], 0), ("Approved service", ["paid terms, governed"], 0), ("On premises or device", ["open-weight, you operate"], 0)]),
    ]
    o = [box(300, 14, 360, 46, "Large language models", None, C["ice"], fill=C["panel2"], tsize=18)]
    cw = 226
    for i, (head, groups) in enumerate(cols):
        x = 14 + i * (cw + 12)
        cx = x + cw / 2
        o.append(line(480, 60, 480, 78, C["faint"], 1.2)); o.append(line(14 + cw / 2 + 0, 78, 14 + 3 * (cw + 12) + cw / 2, 78, C["faint"], 1.2))
        o.append(line(cx, 78, cx, 96, C["faint"], 1.2))
        o.append(f'<rect x="{x}" y="96" width="{cw}" height="34" fill="{C["panel"]}" stroke="{C["ice"]}"/>')
        o.append(tx(cx, 118, head, 15, C["text"], 700, "middle"))
        y = 146
        for g, items, star in groups:
            n = len(items)
            h = 34 + n * 24
            o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{h}" fill="none" stroke="{C["line"]}"/>')
            o.append(tx(x + 12, y + 22, g, 13.5, C["amber"] if star else C["ice"], 700))
            for j, it in enumerate(items):
                o.append(tx(x + 12, y + 44 + j * 24, it, 13.5, C["text"] if not star else C["amber"], 500 if star else 400))
            if star and ANIM:
                pass
            y += h + 10
    o.append(tx(14, 600 - 10, "Amber: the free-tier choice for this workshop.", 13, C["amber"], 600))
    return svg(u, 960, 600, "".join(o), "Taxonomy of language models by access, by size, by job and by where they run")


# ------------------------------------------------------------------ 10. free tier
def freetier():
    u = "gf"
    o = [label(20, 28, "Three limits, checked on every call")]
    names = [("RPM", "requests per minute"), ("TPM", "tokens per minute"), ("RPD", "requests per day")]
    for i, (n, d) in enumerate(names):
        x = 40 + i * 150
        o.append(f'<rect x="{x}" y="50" width="100" height="130" fill="{C["panel"]}" stroke="{C["ice"]}"/>')
        lvl = [70, 45, 90][i]
        h = 130 * lvl / 100
        if ANIM:
            o.append(f'<rect x="{x+2}" y="{50+130-h}" width="96" height="{h}" fill="{C["ice"]}" opacity="0.25"><animate attributeName="height" values="{h*0.5};{h};{h*0.5}" dur="{4+i}s" repeatCount="indefinite"/><animate attributeName="y" values="{180-h*0.5};{180-h};{180-h*0.5}" dur="{4+i}s" repeatCount="indefinite"/></rect>')
        else:
            o.append(f'<rect x="{x+2}" y="{50+130-h}" width="96" height="{h}" fill="{C["ice"]}" opacity="0.25"/>')
        o.append(tx(x + 50, 108, n, 24, C["text"], 700, "middle"))
        o.append(tx(x + 50, 132, d, 11.5, C["mute"], 400, "middle"))
        o.append(tx(x + 50, 204, "full = 429", 13, C["bad"], 600, "middle"))
    o.append(tx(40, 232, "Hit any one and you wait.", 14, C["mute"])); o.append(tx(40, 252, "Each person has their own key.", 14, C["mute"]))
    o.append(label(540, 28, "Daily allowance on a free key (reported)"))
    o.append(tx(540, 70, "gemini-3.8-flash", 14, C["text"], 600)); o.append(f'<rect x="540" y="80" width="16" height="20" fill="{C["bad"]}"/>'); o.append(tx(566, 96, "about 20 a day", 14, C["bad"], 700))
    o.append(tx(540, 140, "gemini-3.5-flash-lite", 14, C["text"], 600)); o.append(f'<rect x="540" y="150" width="380" height="20" fill="{C["ok"]}"/>'); o.append(tx(540, 192, "about 500 a day, 10 a minute", 14, C["ok"], 700))
    o.append(tx(540, 226, "Reported by public trackers, not by Google.", 13, C["mute"]))
    o.append(tx(540, 246, "Check your own limits in AI Studio.", 13, C["mute"]))
    return svg(u, 960, 270, "".join(o), "Free tier limits: three limits per call, and a daily allowance that is far larger for Flash-Lite than for Flash")


# ------------------------------------------------------------------ 11. security layers
def security():
    u = "gx"
    cx, cy = 190, 170
    o = []
    rings = [(150, "4", C["amber"]), (115, "3", C["ice"]), (80, "2", C["ice"]), (45, "1", C["ice"])]
    for r, n, col in rings:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{C["panel"] if r == 150 else "none"}" stroke="{col}" stroke-width="1.5"/>')
    if ANIM:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{C["ice"]}"><animate attributeName="r" values="20;152;20" dur="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0;0.8" dur="6s" repeatCount="indefinite"/></circle>')
    o.append(tx(cx, cy + 5, "Answer", 14, C["text"], 700, "middle"))
    for (r, n, col) in rings:
        o.append(f'<circle cx="{cx - r}" cy="{cy}" r="11" fill="{C["bg"]}" stroke="{col}"/>')
        o.append(tx(cx - r, cy + 5, n, 13, col, 700, "middle"))
    leg = [("4", "People and policy", "POL-10, a named owner, verified numbers", C["amber"]),
           ("3", "Checks", "Citations in code, logs, golden set, structured output", C["ice"]),
           ("2", "Harness", "Least-power tools: read-only, allow-listed, row-capped", C["ice"]),
           ("1", "Prompt rules", "Data is never an instruction. Helpful, not a wall", C["ice"])]
    for i, (n, t, d, col) in enumerate(leg):
        y = 40 + i * 70
        o.append(f'<circle cx="420" cy="{y+14}" r="13" fill="none" stroke="{col}"/>')
        o.append(tx(420, y + 19, n, 14, col, 700, "middle"))
        o.append(tx(448, y + 14, t, 17, C["text"], 700))
        o.append(tx(448, y + 36, d, 13.5, C["mute"]))
    # key path
    o.append(label(20, 372, "Your key, the safe path"))
    path = [("Colab Secret", "the vault"), ("userdata.get()", "read at run time"), ("client", "in memory only"), ("Gemini API", "your project")]
    for i, (a, b) in enumerate(path):
        x = 20 + i * 190
        o.append(box(x, 388, 150, 58, a, b, C["ok"] if i == 0 else C["ice"], tsize=14, ssize=12))
        if i:
            o.append(arrow(u, f"M{x-38},417 L{x-2},417"))
    o.append(packet("M170,417 L770,417", 5, 0, C["ok"]))
    o.append(chip(790, 388, 150, "key in a cell", C["bad"], 26))
    o.append(chip(790, 418, 150, "key in Git or email", C["bad"], 26))
    o.append(tx(790, 462, "Never: any of these", 12.5, C["bad"], 600))
    return svg(u, 960, 480, "".join(o), "Four layers of protection around an answer, and the safe path for an API key from Colab Secret to the API")


# ------------------------------------------------------------------ 12. ER diagram
def er():
    u = "gd"
    N = {  # name: (x, y, w, accent)
        "dim_airlines": (30, 28, 150), "dim_routes": (200, 28, 140), "dim_terminals": (370, 28, 150), "dim_date": (550, 28, 120),
        "dim_concessions": (700, 28, 170),
        "flights": (250, 150, 150), "passenger_journeys": (450, 150, 230),
        "staffing_roster": (470, 262, 200), "dim_checkpoints": (700, 262, 170),
        "feedback": (180, 262, 130), "complaints": (180, 330, 130),
        "airline_incentive_ledger": (6, 150, 205), "concession_monthly_sales": (715, 150, 230),
        "incidents": (20, 400, 130), "daily_revenue": (180, 400, 150), "meta": (360, 400, 90),
    }
    H = 38
    E = [("flights", "dim_airlines"), ("flights", "dim_routes"), ("flights", "dim_terminals"), ("flights", "dim_date"),
         ("passenger_journeys", "flights"), ("passenger_journeys", "dim_date"), ("staffing_roster", "dim_checkpoints"),
         ("staffing_roster", "passenger_journeys"), ("feedback", "passenger_journeys"), ("complaints", "passenger_journeys"),
         ("dim_checkpoints", "dim_terminals"), ("concession_monthly_sales", "dim_concessions"), ("airline_incentive_ledger", "dim_airlines")]
    def ctr(n):
        x, y, w = N[n]
        return x + w / 2, y + H / 2
    o = []
    for a, b in E:
        x1, y1 = ctr(a); x2, y2 = ctr(b)
        dash = "5 4" if (a, b) in [("staffing_roster", "passenger_journeys"), ("complaints", "passenger_journeys")] else None
        o.append(line(x1, y1, x2, y2, C["ice"], 1.2, dash))
    for n, (x, y, w) in N.items():
        big = n in ("flights", "passenger_journeys")
        col = C["amber"] if n == "passenger_journeys" else (C["ice"] if big else C["line"])
        fill = C["panel2"] if big else C["panel"]
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{H}" fill="{fill}" stroke="{col}" stroke-width="{1.6 if big else 1}"/>')
        o.append(tx(x + w / 2, y + 24, n, 13, C["text"], 700 if big else 500, "middle", mono=True))
    # notes
    o.append(tx(20, 480, "Solid line: a key links the tables. Dashed line: join on date, hour and checkpoint, or optional.", 13, C["mute"]))
    o.append(tx(20, 504, "passenger_journeys is a 4 percent sample (amber): multiply counts by 25. flights is the full population.", 13, C["amber"], 600))
    # views
    o.append(label(20, 548 - 22, "Ready-made views", fill=C["ice"]))
    vx = 20
    for v in ["v_departure_immigration_hourly", "v_airline_month_delay", "v_route_month_performance", "v_feedback_clean"]:
        w = 7.6 * len(v) + 18
        o.append(chip(vx, 536, w, v, C["ice"], 26, 11.5))
        vx += w + 8
    return svg(u, 960, 580, "".join(o), "Entity diagram of the airport database: flights, passenger journeys, roster, feedback, complaints, revenue and dimensions")


# ------------------------------------------------------------------ 13. five beats
def beats():
    u = "gb"
    xs = [96, 288, 480, 672, 864]
    items = [("Is the feeling", "real?", "Copilot, SQL"), ("When, and", "why?", "SQL"), ("What does", "it cost?", "SQL, x 25"), ("What do the", "rules say?", "RAG, approved"), ("The aha", "facts vs rules", "Agent")]
    o = [line(96, 90, 864, 90, C["faint"], 2, "6 6")]
    if ANIM:
        o.append(f'<line x1="96" y1="90" x2="864" y2="90" stroke="{C["ice"]}" stroke-width="2" stroke-dasharray="16 700"><animate attributeName="stroke-dashoffset" values="0;-716" dur="5s" repeatCount="indefinite"/></line>')
    for i, (x, (a, b, t)) in enumerate(zip(xs, items)):
        col = C["amber"] if i == 4 else C["ice"]
        o.append(f'<circle cx="{x}" cy="90" r="24" fill="{C["panel"]}" stroke="{col}" stroke-width="2"/>')
        o.append(tx(x, 99, str(i + 1), 22, col, 700, "middle"))
        o.append(tx(x, 148, a, 16, C["text"], 700, "middle"))
        o.append(tx(x, 168, b, 16, C["text"], 700, "middle"))
        o.append(chip(x - 62, 186, 124, t, col, 24, 12))
    o.append(label(480, 36, "The Friday Problem, one beat at a time", "middle"))
    o.append(packet("M96,90 L864,90", 6, 0, C["amber"], 5))
    return svg(u, 960, 230, "".join(o), "The five beats of the Friday Problem, from is the feeling real to the aha")


# ------------------------------------------------------------------ 14. brief anatomy
def brief():
    u = "gp"
    o = [f'<rect x="30" y="16" width="440" height="408" fill="#0e1520" stroke="{C["ice"]}" stroke-width="1.4"/>']
    o.append(f'<rect x="46" y="32" width="408" height="52" fill="{C["panel2"]}" stroke="{C["amber"]}"/>')
    o.append(tx(60, 52, "HEADLINE", 11, C["amber"], 700, ls="2")); o.append(line(60, 68, 400, 68, C["faint"], 5))
    o.append(tx(46, 108, "KEY NUMBERS", 11, C["ice"], 700, ls="2"))
    for i in range(3):
        x = 46 + i * 140
        o.append(f'<rect x="{x}" y="118" width="128" height="54" fill="{C["panel"]}" stroke="{C["line"]}"/>')
        o.append(line(x + 12, 136, x + 70, 136, C["faint"], 4)); o.append(tx(x + 12, 160, "verified by SQL", 11.5, C["ok"], 600))
    o.append(tx(46, 198, "RULES: document | clause | requirement | observed", 11, C["ice"], 700, ls="1"))
    for i in range(3):
        o.append(line(46, 216 + i * 18, 454, 216 + i * 18, C["faint"], 1))
    o.append(tx(46, 288, "THREE ACTIONS: owner | deadline", 11, C["ice"], 700, ls="1"))
    for i in range(3):
        o.append(f'<circle cx="56" cy="{306 + i*20}" r="5" fill="none" stroke="{C["ice"]}"/>'); o.append(line(70, 306 + i * 20, 330, 306 + i * 20, C["faint"], 3))
    o.append(tx(46, 384, "ASSUMPTIONS AND LIMITS", 11, C["ice"], 700, ls="1")); o.append(line(46, 400, 400, 400, C["faint"], 3))
    callouts = [("Headline", "the finding and why it matters, one sentence", 56), ("Key numbers", "each verified by your own SQL", 140), ("Rules", "approved documents only, with the clause", 222),
                ("Actions", "three, each with an owner and a deadline", 306), ("Limits", "say what you are not sure about", 394)]
    for t, d, y in callouts:
        o.append(line(472, y, 540, y, C["ice"], 1.2, "3 3")); o.append(f'<circle cx="540" cy="{y}" r="4" fill="{C["ice"]}"/>')
        o.append(tx(556, y - 4, t, 16, C["text"], 700)); o.append(tx(556, y + 16, d, 13, C["mute"]))
    o.append(f'<rect x="556" y="418" width="370" height="0" fill="none"/>')
    o.append(tx(700, 438, "A number you cannot reproduce does not go in the brief.", 13.5, C["amber"], 700, "middle"))
    return svg(u, 960, 456, "".join(o), "Anatomy of the one-page brief: headline, key numbers, rules, three actions, assumptions and limits")


# ------------------------------------------------------------------ 15. improve loop
def improve():
    u = "gi"
    items = [("Golden set", "18 questions,", "known answers"), ("Score", "hit@1 and", "hit@3"), ("Change one thing", "filter, hybrid,", "rewrite"), ("Re-run", "compare the", "scores")]
    o = []
    for i, (t, a, b) in enumerate(items):
        x = 20 + i * 232
        col = C["amber"] if i == 2 else C["ice"]
        o.append(box(x, 40, 190, 100, t, a, col, sub2=b))
        if i:
            o.append(arrow(u, f"M{x-40},90 L{x-2},90"))
    o.append(arrow(u, "M855,142 C855,200 120,200 115,144", C["amber"], "6 5"))
    o.append(tx(480, 196, "Keep what improves the score. Undo what does not.", 14, C["amber"], 600, "middle"))
    o.append(packet("M115,90 L855,90", 6, 0, C["amber"]))
    return svg(u, 960, 226, "".join(o), "Measure then fix loop: golden set, score, change one thing, re-run")


# ------------------------------------------------------------------ 16. data model summary: three ways to ask
def threeways():
    u = "gw"
    cols = [("Copilot", "a chat assistant with your files", "no code, fast to start", "good for the first look", "you cannot see behind the screen"),
            ("Gemini in Colab", "code, full control, tools", "every step visible and testable", "good for building and checking", "needs a key and a little code"),
            ("SQL", "exact questions to a database", "counts and averages, not guesses", "good for numbers you can defend", "needs the right table and the right hour")]
    o = []
    for i, (t, a, b, c, d) in enumerate(cols):
        x = 20 + i * 312
        col = C["amber"] if i == 2 else C["ice"]
        o.append(f'<rect x="{x}" y="16" width="296" height="210" fill="{C["panel"]}" stroke="{C["line"]}"/><rect x="{x}" y="16" width="40" height="3" fill="{col}"/>')
        o.append(tx(x + 18, 52, t, 22, C["text"], 700)); o.append(tx(x + 18, 80, a, 14, C["mute"]))
        o.append(tx(x + 18, 118, b, 14, C["text"])); o.append(tx(x + 18, 146, c, 14, col, 600)); o.append(tx(x + 18, 186, d, 13, C["mute"]))
    return svg(u, 960, 242, "".join(o), "Three ways to ask a question: Copilot, Gemini in Colab, and SQL")


ALL = dict(journey=journey, layers=layers, rag=rag, embeddings=embeddings, sample=sample, agent=agent, gates=gates, tokens=tokens,
           taxonomy=taxonomy, freetier=freetier, security=security, er=er, beats=beats, brief=brief, improve=improve, threeways=threeways)
