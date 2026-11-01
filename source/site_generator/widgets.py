"""Interactive widgets for the site. Each one has a printed equivalent when diagrams.ANIM is False."""
import html
import diagrams as D


def _live():
    return D.ANIM


def watch(text):
    return f'<div class="watch"><b class="t">Watch out</b>{text}</div>'


def fig(f, cap):
    return D.caption(f, cap)


def prompt_builder():
    if not _live():
        rows = [("Role", "Who the model should be", "You are an operations analyst at a general international airport."),
                ("Context", "What it can see", "The workbook has hourly departure immigration waits. Weight by sampled_journeys."),
                ("Task", "What to do", "Compare Friday with Monday to Thursday, 17:00 to 22:59, Terminal 1."),
                ("Format", "How to answer", "A table with three columns, then two sentences for a manager."),
                ("Rules", "What is forbidden", "Use only the workbook. If something is unclear, say so instead of guessing.")]
        tr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
        return (f'<div class="tw"><table><thead><tr><th>Part</th><th>What it does</th><th>Airport example</th></tr></thead><tbody>{tr}</tbody></table></div>'
                '<p class="small">Try it: write your own five-part prompt for a task from your department.</p>')
    return """
<div class="wid" id="pb">
<div class="wid-h"><b>Prompt builder</b><span class="small">Edit the five parts. Watch the prompt and the score.</span>
<span class="wid-b"><button type="button" data-pb="vague">Vague</button><button type="button" data-pb="full">Five parts</button></span></div>
<div class="wid-g">
<div>
<label for="pb_role">1 | Role</label><input id="pb_role" type="text">
<label for="pb_ctx">2 | Context</label><input id="pb_ctx" type="text">
<label for="pb_task">3 | Task</label><input id="pb_task" type="text">
<label for="pb_fmt">4 | Format</label><input id="pb_fmt" type="text">
<label for="pb_rules">5 | Rules</label><input id="pb_rules" type="text">
</div>
<div>
<div class="meter"><span id="pb_score">5 of 5 parts</span><div class="progress"><i id="pb_bar"></i></div></div>
<pre id="pb_out"></pre>
<p class="small" id="pb_msg"></p>
</div>
</div></div>"""


def rag_sim():
    rows = [("GIA-DRAFT-11 v4.0", "DRAFT", "Proposes a maximum average wait of 12 minutes", "0.91", "draft"),
            ("GIA-SUP-12 v2.0", "SUPERSEDED", "Old standard: 20 minutes. Replaced on 31 Dec 2025", "0.89", "sup"),
            ("GIA-POL-01 v3.0, clause 2.3", "APPROVED", "15 minutes, no more than 5 percent over 30", "0.88", "ok")]
    if not _live():
        tr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d, _ in rows)
        return (f'<div class="tw"><table><thead><tr><th>Section</th><th>Status</th><th>Says</th><th>Similarity (illustrative)</th></tr></thead><tbody>{tr}</tbody></table></div>'
                '<p><b>Without a filter</b> the top match is the draft, and the answer is 12 minutes: wrong. <b>With the approved-only filter</b> the top match is clause 2.3: 15 minutes, cited. '
                'The scores here are illustrative; the point is that similar is not the same as valid.</p>')
    tr = "".join(
        f'<tr class="rs-row" data-k="{k}"><td><b>{a}</b></td><td><span class="tag {"free" if k=="ok" else ("paid" if k=="draft" else "no")}">{b}</span></td><td>{c}</td><td class="mono">{d}</td></tr>'
        for a, b, c, d, k in rows)
    return f"""
<div class="wid" id="rs">
<div class="wid-h"><b>Retrieval simulator</b><span class="small">Question: what is the maximum average departure immigration wait?</span>
<label class="sw"><input type="checkbox" id="rs_filter"><span>Approved-only filter</span></label></div>
<div class="tw" style="margin:12px 0 0"><table><thead><tr><th>Retrieved section</th><th>Status</th><th>Says</th><th>Similarity</th></tr></thead><tbody>{tr}</tbody></table></div>
<div class="rs-ans" id="rs_ans"></div>
<p class="small">Similarity scores are illustrative. The lesson is real: a draft can look like the best match.</p>
</div>"""


def model_chooser():
    if not _live():
        return """
<div class="tw"><table><thead><tr><th>Your situation</th><th>Choose</th></tr></thead><tbody>
<tr><td>Personal data</td><td>Never send it to an external model. Remove or mask it first.</td></tr>
<tr><td>Internal data</td><td>An approved service under paid terms only (GIA-POL-10). Not the free tier.</td></tr>
<tr><td>Fictional data, free tier</td><td><code>gemini-3.5-flash-lite</code> for prompts, RAG answers and text-to-SQL. For the agent, expect more errors.</td></tr>
<tr><td>Fictional data, paid key</td><td><code>gemini-3.8-flash</code> for the agent. Try Flash-Lite first for simple tasks and keep it if the test set passes.</td></tr>
</tbody></table></div>"""
    return """
<div class="wid" id="mc">
<div class="wid-h"><b>Model chooser</b><span class="small">Three questions, one recommendation.</span></div>
<div class="wid-g">
<div>
<label for="mc_data">What data will you send?</label>
<select id="mc_data"><option value="fict">Fictional or public</option><option value="int">Internal</option><option value="pers">Personal data</option></select>
<label for="mc_key">Which key do you have?</label>
<select id="mc_key"><option value="free">Free tier</option><option value="paid">Paid, billing on</option></select>
<label for="mc_task">What is the task?</label>
<select id="mc_task"><option value="simple">Prompts, classification, extraction</option><option value="rag">Answers from documents (RAG)</option><option value="agent">An agent with tools</option><option value="hard">Hard multi-step reasoning</option></select>
</div>
<div><div class="rec" id="mc_out"></div><p class="small" id="mc_note"></p></div>
</div></div>"""


def qa(title, items):
    """items: list of (question, answer)."""
    if not _live():
        items = items[:QA_LIMIT]
        qs = "".join(f"<li>{q}</li>" for q, _ in items)
        ans = " ".join(f"<b>{i+1}.</b> {a}" for i, (_, a) in enumerate(items))
        return (f'<div class="qbox"><b class="t">Can you answer?</b><ol>{qs}</ol><p class="ans"><b>Answers.</b> {ans}</p></div>')
    cards = "".join(
        f'<details class="q"><summary>{q}</summary><div>{a}</div></details>' for q, a in items)
    return f'<div class="qbox"><b class="t">Can you answer? {html.escape(title)}</b>{cards}</div>'


QA_LIMIT = 5

# questions per topic
QA_D1 = [
    ("Why do you multiply counts by 25 but never averages?", "passenger_journeys is a 4 percent sample, so a count of sampled people is 4 percent of the real count. An average or a percentage is already a ratio, so the sample size cancels out."),
    ("The draft says 12 minutes and GIA-POL-01 says 15. Which is the rule?", "15 minutes. Only approved documents are in force. The draft is a proposal and is not approved."),
    ("Which part of the five-part prompt tells the model what is forbidden?", "Rules. Role says who, context says what it can see, task says what to do, format says how to answer."),
    ("A comment says: ignore your rules. What should a safe assistant do?", "Treat it as text to classify, report it as suspicious, and keep following the standing rules."),
    ("Which hour column do you use for time-of-day analysis, and why?", "immigration_hour. It is when the passenger was actually at immigration, and it joins to the staffing roster."),
]
QA_D2 = [
    ("What does hit@3 mean?", "The right section was among the top three retrieved sections."),
    ("Why does the SQL tool cap results at 40 rows?", "A careless query cannot flood the model with data, which saves tokens and keeps the answer focused."),
    ("Why is a tiny max_output_tokens a bad idea with thinking turned on?", "Thinking tokens count toward the cap, so a small cap can cut the answer off or leave no room for it. Ask for brevity in the prompt instead."),
    ("If an attack on your agent works, what is the next step?", "Add a rule or a guard (a harness change), then run the same attack again."),
    ("An agent answer has a number but the tool log shows no SQL. What do you do?", "Do not trust it. Numbers must come from queries. Reject it and fix the prompt or the tools."),
]
QA_D3 = [
    ("Under GIA-POL-10, can internal data go to a free-tier key?", "No. Internal data goes only to approved services under paid terms. Free tier is for fictional data only."),
    ("Who is accountable for an agent that others rely on?", "A named person. Answers are also checked against the source query before publication."),
    ("What turns a prompt that works three times into something reusable?", "A skill: a saved set of instructions, rules and an example for one kind of task."),
    ("Which brief numbers may stay in the one-page brief?", "Only the ones you can reproduce with your own SQL."),
    ("When would you choose a Gemini agent over a Copilot notebook?", "When a team needs a repeatable, tested service with full control and a log of every tool call."),
]
QA_MODELS = [
    ("On the free tier, why use a Flash-Lite model first?", "Its daily allowance is reported to be far larger than Flash, so a workshop does not run out before the second lab."),
    ("What is the difference between open-weight and open-source?", "Open-weight means you can download and run the weights. Open-source also releases the training data and code."),
    ("Which kind of model do you need for search by meaning?", "An embedding model. It turns text into numbers; it does not write answers."),
]
QA_TOKENS = [
    ("Why does output cost more than input?", "Generating text is more expensive per token than reading it. On gemini-3.8-flash output is five times the input price."),
    ("Why does an agent cost more than one chat call?", "Each turn of the loop re-sends the context, plus the tool results, so a question with several tool calls costs several times one call."),
    ("How do you estimate a pilot's cost?", "Measure one full question from the [tokens] line, then multiply by calls per question, questions per user, and users."),
]
QA_SEC = [
    ("Where should your API key live in Colab?", "In Colab Secrets, read with userdata.get. Never in a cell, a chat, an email or Git."),
    ("Why is a prompt rule against injection not enough?", "The model cannot always tell your instructions from the data it reads. Add a harness: read-only tools, caps, logs, and output checks."),
    ("Your key leaks. What are the four steps?", "Create a new key, switch your code to it, disable the old key, then check usage and billing."),
]
