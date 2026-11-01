"""Use case, models, setup, tokens, security, exercises, glossary, downloads."""
from common import *


def usecase():
    hero = pagehero("The use case", "The airport and its Friday Problem",
                    "One fictional airport, one database, twelve policy documents. Every lab uses the same case, so you never spend time learning a new one.")
    body = """
<section class="reveal"><div class="wrap">
<div class="kpis">
<div><div class="num">19,775</div><span>flights, 1 Oct 2025 to 30 Sep 2026</span></div>
<div><div class="num">108,488</div><span>sampled passenger journeys (a 4 percent sample)</span></div>
<div><div class="num">16</div><span>tables and views of operations, people, money, rules</span></div>
<div><div class="num">12</div><span>policy documents: 10 approved, 1 draft, 1 superseded</span></div>
</div>
<p style="margin-top:22px">Currency is the UAE dirham (AED). All airlines, outlets, people and policies are fictional. Do not mix real figures into your answers.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="read-first">Read this first</h2>
<p>These six facts stop most wrong answers. They appear in the data dictionary, in the standing rules and in the agent's system prompt.</p>
<ul class="facts">
<li><span><b>The passenger table is a sample.</b> <code>passenger_journeys</code> is a 4 percent random sample. Multiply counts by 25. Never multiply averages or percentages.</span></li>
<li><span><b>Time of day uses the immigration hour.</b> Use <code>immigration_hour</code>, not the scheduled flight hour. Peak hours are 17:00 to 22:59.</span></li>
<li><span><b>The roster has gaps.</b> <code>staffing_roster</code> has no rows for a few hours on days when the roster system was down (see incidents of type Roster system outage).</span></li>
<li><span><b>Feedback has duplicates.</b> Use the view <code>v_feedback_clean</code>, which removes exact duplicate submissions.</span></li>
<li><span><b>Shopping and dining revenue is estimated.</b> It is built from the passenger sample (sample spend x 25).</span></li>
<li><span><b>Cancelled flights are excluded</b> from delay percentages.</span></li>
</ul>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="tables">The database</h2>
<p>A SQLite file, <code>airport_ops.db</code>, with sixteen tables. The same tables are in the Copilot workbook.</p>
""" + table(["Table", "Rows", "What it holds"], [
        ["<code>meta</code>", "9", "Facts about the dataset itself: period, sampling rate, currency. Read this first"],
        ["<code>dim_date</code>", "365", "Calendar with weekend, holiday and event flags"],
        ["<code>dim_terminals</code>", "2", "T1 serves full-service airlines. T2 serves low-cost and regional airlines"],
        ["<code>dim_checkpoints</code>", "8", "Check-in, security and immigration points, with installed and standard counters"],
        ["<code>dim_airlines</code>", "6", "The six airlines"],
        ["<code>dim_routes</code>", "15", "The 15 routes, each flown in both directions"],
        ["<code>dim_concessions</code>", "17", "Shops, restaurants and services that pay rent"],
        ["<code>flights</code>", "19,775", "One row per scheduled flight. Full population, not a sample"],
        ["<code>passenger_journeys</code>", "108,488", "A 4 percent sample with measured waits and spend"],
        ["<code>staffing_roster</code>", "69,984", "Counters open per hour at every checkpoint"],
        ["<code>feedback</code>", "13,116", "Survey responses, one row per rated category. May hold duplicates"],
        ["<code>complaints</code>", "1,428", "Formal complaints with resolution time against the 10-day target"],
        ["<code>incidents</code>", "153", "Outages, faults, weather, security alerts"],
        ["<code>daily_revenue</code>", "365", "Daily revenue by stream, in AED"],
        ["<code>concession_monthly_sales</code>", "204", "Monthly sales and rent per outlet"],
        ["<code>airline_incentive_ledger</code>", "72", "Monthly landing-charge rebates paid to airlines"],
    ]) + """
<h3>Ready-made views (read-only)</h3>
""" + table(["View", "Use it for"], [
        ["<code>v_departure_immigration_hourly</code>", "Departure immigration by date, hour and terminal: sampled journeys, average wait, share waiting over 30 minutes, counters open"],
        ["<code>v_airline_month_delay</code>", "Monthly delayed-flight percentage per airline, cancelled flights excluded"],
        ["<code>v_route_month_performance</code>", "Monthly flights, passengers and average load factor per route and direction"],
        ["<code>v_feedback_clean</code>", "Feedback with exact duplicate submissions removed"],
    ]) + """
<h3>How the tables connect</h3>
<p><code>flights</code> links to airlines, routes, terminals and dates. <code>passenger_journeys</code> links to <code>flights</code>. <code>staffing_roster</code> joins to journeys on date, hour and checkpoint (<code>terminal_id || '-IMM-DEP'</code>). <code>feedback</code> and <code>complaints</code> link to journeys. The full data dictionary is in the participant pack.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="documents">The twelve documents</h2>
<p>Each document has a number, a version and a status. The status is data: an assistant that ignores it will quote the wrong rule.</p>
""" + table(["Document", "Title", "Version", "Status"], [
        ["GIA-POL-01", "Passenger Service Standards Policy", "v3.0", "<span class=\"tag free\">Approved</span>"],
        ["GIA-POL-02", "Airline Incentive and Route Development Policy", "v3.1", "<span class=\"tag free\">Approved</span>"],
        ["GIA-STD-03", "Counter Staffing and Roster Standard", "v2.0", "<span class=\"tag free\">Approved</span>"],
        ["GIA-SOP-04", "Delay Management SOP", "v2.2", "<span class=\"tag free\">Approved</span>"],
        ["GIA-SOP-05", "Complaint Handling Procedure", "v2.0", "<span class=\"tag free\">Approved</span>"],
        ["GIA-SOP-06", "Peak Period Operations and Queue Escalation SOP", "v1.3", "<span class=\"tag free\">Approved</span>"],
        ["GIA-GDL-07", "Passenger Feedback Survey Guideline", "v1.2", "<span class=\"tag free\">Approved</span>"],
        ["GIA-MAN-08", "KPI and Data Definitions Manual", "v1.1", "<span class=\"tag free\">Approved</span>"],
        ["GIA-POL-09", "Commercial and Concessions Policy", "v2.0", "<span class=\"tag free\">Approved</span>"],
        ["GIA-POL-10", "Responsible Use of AI and Data Policy", "v1.0", "<span class=\"tag free\">Approved</span>"],
        ["GIA-DRAFT-11", "Passenger Service Standards Policy", "v4.0", "<span class=\"tag paid\">Draft</span>"],
        ["GIA-SUP-12", "Passenger Service Standards PSS-01", "v2.0", "<span class=\"tag no\">Superseded</span>"],
    ]) + """
<h3>Three traps hidden in the documents</h3>
<div class="grid g3">
<div class="card"><span class="k">The draft</span><p>A proposed new version that sounds recent and may rank first in a similarity search. Not approved.</p></div>
<div class="card"><span class="k">The superseded version</span><p>The old rule, replaced on 31 December 2025. Still a good match for the question.</p></div>
<div class="card"><span class="k">The expired exception</span><p>An exception that expired on 30 June 2026 and was never renewed.</p></div>
</div>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="beats">The five beats</h2>
<p>The Friday Problem unfolds in five questions. You meet them on Day 1 by hand and on Day 2 with an agent.</p>
<ol>
<li><b>Is the feeling real?</b> Which weekday has the longest wait at Terminal 1?</li>
<li><b>When, and why?</b> Hour by hour: waits and counters.</li>
<li><b>What does it cost?</b> Lost spend, missed flights, estimated over the year.</li>
<li><b>What do the rules say?</b> Maximum wait and minimum counters, approved documents only.</li>
<li><b>The aha.</b> Which clauses are we breaching, what is the cost, what must we do next?</li>
</ol>
<p>On Day 3 the same data supports seven other questions: a late airline, where to add a flight, two problems in Terminal 2, the smart gates, shops under review, and complaints against the rulebook. See <a href="day-3.html#capstone">the capstone</a>.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="swap">Take the pattern to your own department</h2>
<p>Nothing here is about airports. The pattern is a database for facts, approved documents for rules, a model that can use both, and a harness that makes the answers checkable. Swap the case for HR, energy, finance or licensing and the same method applies.</p>
<div class="flow">
<div><b>Facts</b><span>Tables and views, queried with SQL</span></div>
<div><b>Rules</b><span>Approved documents, searched with RAG</span></div>
<div><b>Reasoning</b><span>A model with a clear job description</span></div>
<div><b>Checks</b><span>Read-only tools, logs, golden set, citations</span></div>
</div>
</div></section>
"""
    return page("use-case.html", "The airport use case", "The fictional airport database, the twelve policy documents and the five beats of the Friday Problem.", body, hero_html=hero,
                prev=("day-3.html", "Day 3: Put it together"), nxt=("models.html", "Models and the free tier"))


def models():
    hero = pagehero("Models", "Types of models, and which to use on the free tier",
                    "A large language model is one kind of model among several. This page sorts them by how you get them, how big they are and what they do, then shows the Gemini family and the choice that works on a free key.",
                    '<div class="callout"><b class="t">Check before you teach</b><p>Model names, prices and limits change often. This page reflects the Gemini documentation and public trackers as of 1 November 2026. Confirm on a fresh key the day before.</p></div>')
    body = """
<section class="reveal"><div class="wrap">
<h2 id="types">Types of large language models</h2>
<p>There is no single scale. The same model can be described along several axes at once.</p>
<h3>1. By access: closed, open-weight, open-source</h3>
""" + table(["Type", "What you get", "Examples", "Good for", "Watch out for"], [
        ["<span class=\"tag paid\">Closed</span> proprietary, API only", "Access through the provider's API or app. No weights.", "Gemini (Google), GPT (OpenAI), Claude (Anthropic)", "Best capability, no hardware, fastest start", "Data goes to the provider. Pay per token. Provider decides versions and prices"],
        ["<span class=\"tag open\">Open-weight</span>", "Downloadable weights. Training data and pipeline usually private.", "Llama (Meta), Qwen (Alibaba), DeepSeek, Mistral, Gemma (Google), Phi (Microsoft)", "Run on your own hardware, fine-tune, keep data in-house, offline or air-gapped use", "You run and secure it. Licences differ: Apache 2.0 and MIT are permissive; community licences add conditions"],
        ["<span class=\"tag open\">Fully open-source</span>", "Weights, training data and code.", "OLMo (Ai2)", "Research, audit and reproducibility", "Smaller choice. Often behind the frontier"],
    ]) + """
<p>Most models called "open source" are really open-weight: you can download and run them, but you cannot see everything they were trained on. For a government team, the question is rarely "open or closed?" It is which model, on what hardware, under which licence, with which data rules.</p>
<h3>2. By size and speed</h3>
""" + table(["Tier", "Typical role", "Gemini example"], [
        ["Frontier or Pro", "Hard reasoning, long analysis. Slowest and most expensive", "Gemini 4 Argon"],
        ["Flash", "Balanced: strong, fast, affordable. The everyday workhorse", "Gemini 3.8 Flash, 3.6 Flash"],
        ["Flash-Lite", "Cheapest and fastest. Classification, extraction, simple answers, high volume", "Gemini 3.5 Flash-Lite, 3.1 Flash-Lite"],
        ["Small open models", "Run on a laptop or a single GPU", "Gemma 4"],
    ]) + """
<h3>3. By what they do</h3>
<div class="grid g3">
<div class="card"><span class="k">Text and reasoning</span><p>Chat, writing, analysis, tool calling. "Thinking" models reason before they answer, and you pay for that reasoning.</p></div>
<div class="card"><span class="k">Embedding models</span><p>Turn text (or images, audio, PDFs) into numbers so you can search by meaning. They do not write answers. RAG needs one.</p></div>
<div class="card"><span class="k">Multimodal and media</span><p>Understand or generate images, video, audio and speech. Live and voice models handle real-time conversation.</p></div>
</div>
<h3>4. By where it runs</h3>
<p><b>Cloud API</b> (fast start, data leaves your network), <b>private cloud or approved enterprise service</b> (paid terms, governance), <b>on-premises or on-device</b> (open-weight models, full control, you operate it). Your data class decides which is allowed: see <a href="security.html#data">Secure AI</a>.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="gemini">The Gemini API family</h2>
<p>These are the models you can call with your key. IDs are what you type in code.</p>
""" + table(["Model", "ID", "Role", "Free tier"], [
        ["Gemini 4 Argon", "<code>gemini-4-argon</code>", "Flagship reasoning", "<span class=\"tag no\">No</span>"],
        ["Gemini 3.8 Flash", "<code>gemini-3.8-flash</code>", "Most capable Flash model. Our paid-key default", "<span class=\"tag free\">Yes</span> very small daily allowance reported"],
        ["Gemini 3.6 Flash", "<code>gemini-3.6-flash</code>", "Previous-generation Flash", "<span class=\"tag free\">Yes</span> very small daily allowance reported"],
        ["Gemini 3.5 Flash-Lite", "<code>gemini-3.5-flash-lite</code>", "Fastest, lowest-cost 3.5 model", "<span class=\"tag free\">Yes</span> larger daily allowance reported"],
        ["Gemini 3.1 Flash-Lite", "<code>gemini-3.1-flash-lite</code>", "Low-cost, high-throughput", "<span class=\"tag free\">Yes</span>"],
        ["Gemini 3.1 Pro (preview)", "<code>gemini-3.1-pro-preview</code>", "Pro-tier model", "<span class=\"tag no\">No</span>"],
        ["Gemini 2.5 Pro, Flash, Flash-Lite", "<code>gemini-2.5-*</code>", "Older family", "Limited to users who already used them. Avoid for new projects"],
        ["Gemini Embedding", "<code>gemini-embedding-001</code>", "Text embeddings. Our RAG default", "Check on your key"],
        ["Gemini Embedding 2", "<code>gemini-embedding-2</code>", "Multimodal embeddings (text, images, video, audio, PDFs)", "<span class=\"tag free\">Yes</span>"],
        ["Gemma 4", "<code>gemma-4-31b-it</code>, <code>gemma-4-26b-a4b-it</code>", "Open-weight models, also reachable with the same key", "<span class=\"tag free\">Yes</span>"],
    ]) + """
<p class="small">Preview models usually need billing and may have stricter limits. The 2.5 models are not deprecated, but access is limited, and Google recommends 3.5 Flash-Lite or 3.8 Flash for new projects.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="free">The free tier: what it is and what it costs you</h2>
<div class="grid g2">
<div class="card"><h3>What you get</h3><p>A key with no card and no billing account. Free input and output tokens on selected models, up to each model's rate limits.</p></div>
<div class="card"><h3>What you give up</h3><p>Lower limits, and your prompts and responses may be used by Google to improve its products. Use <b>fictional data only</b>. Real government data needs a paid project and approved data handling (GIA-POL-10).</p></div>
</div>
<h3>Three limits are checked on every call</h3>
""" + table(["Limit", "Meaning", "What you see when you hit it"], [
        ["RPM", "Requests per minute", "Error 429 immediately. Wait a minute"],
        ["TPM", "Input tokens per minute", "Error 429. Send less text per call, or wait"],
        ["RPD", "Requests per day", "Blocked until the daily counter resets (midnight Pacific Time)"],
    ]) + """
<div class="callout"><b class="t">The numbers are not fixed</b><p>Google no longer prints a table of free-tier limits in its documentation. Public trackers report about 20 requests per day for Gemini 3.8 Flash and 3.6 Flash, and about 500 per day plus 10 requests per minute for the Flash-Lite models, but other sources quote higher figures. Treat the Flash-Lite figures as a planning number only. Your own limits are shown in AI Studio, on the rate-limit page for your project.</p></div>
<p>Each participant has their own key and project, so limits are per person, not shared across the room. Shared keys are not allowed, and a shared key would be exhausted by 25 people at once.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="which">Which model for which lab</h2>
<p>The kit tries <code>gemini-3.8-flash</code> first. On a free key that model answers, but with a very small daily allowance it can run out before the second lab. Use a Flash-Lite model as the first choice on the free tier.</p>
""" + table(["Lab", "Free-tier choice", "Paid-key choice", "Notes"], [
        ["Notebook 01: prompting", "<code>gemini-3.5-flash-lite</code>", "<code>gemini-3.8-flash</code>", "Short prompts, simple answers. Flash-Lite is enough"],
        ["Notebook 02: RAG answers and embeddings", "<code>gemini-3.5-flash-lite</code> with <code>gemini-embedding-001</code> or <code>gemini-embedding-2</code>", "<code>gemini-3.8-flash</code>", "Embeddings are the only heavy step. Embed once and reuse"],
        ["Notebook 03: text-to-SQL", "<code>gemini-3.5-flash-lite</code>", "<code>gemini-3.8-flash</code>", "Compare its query with yours. Mistakes are the lesson"],
        ["Notebook 04: RAG deep dive", "Embeddings only, mostly", "Same", "Query rewriting uses one model call per question"],
        ["Notebook 05: the agent", "<code>gemini-3.5-flash-lite</code>, expect more errors", "<code>gemini-3.8-flash</code>", "Flash-Lite is weaker at multi-step tool use. Several calls per question"],
        ["Notebook 06: tune and attack", "Reduce the repeat count to 2", "<code>gemini-3.8-flash</code>", "The thinking-level experiment is the heaviest cell"],
        ["Notebook 07: capstone", "<code>gemini-3.5-flash-lite</code>", "<code>gemini-3.8-flash</code>", "Pace your questions to stay under the per-minute limit"],
    ]) + """
<div class="callout ice"><b class="t">Check the thinking setting</b><p>The kit sets <code>thinking_level</code> (low, medium, high). Support for this setting on Flash-Lite models has not been confirmed for this workshop. If a call fails with an error that mentions thinking, remove the <code>level</code> argument from that call and run it again.</p></div>
<h3 id="switch">How to switch the model</h3>
<p>Open <code>workshop_helpers.py</code> in the participant pack and change one line near the top. The helper tries the models in order and uses the first one that answers a tiny test call.</p>
""" + code("""# Free-tier order: lite models first
MODEL_CANDIDATES = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.6-flash"]

# Paid-key order (kit default)
# MODEL_CANDIDATES = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"]""", "workshop_helpers.py") + """
<p>Change it once and every notebook follows. Embedding models are set on the next lines: <code>EMBED_MODEL</code> and <code>EMBED_MODEL_NEW</code>.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="choose">How to choose in real work</h2>
""" + steps([
        ("Start with the data", "Fictional or public data: the free tier is fine. Internal data: approved service, paid terms. Personal data: it never goes to an external model."),
        ("Pick the smallest model that passes your test set", "Write ten questions with known answers. Run them on Flash-Lite, then on Flash. Pay for more capability only if the score improves."),
        ("Raise thinking only when it helps", "Measure low, medium and high on your own questions. Reasoning tokens cost money and time."),
        ("Match embeddings to the job", "Test the newer embedding model against your golden set before switching."),
        ("Consider open-weight when control matters", "On-premises use, data residency, offline work, or heavy volume. Budget for the people who will run it."),
        ("Re-test after every change", "A new model version is a change. Run the question set again."),
    ]) + """
<h3>Sources</h3>
<ul>
<li><a href="https://ai.google.dev/gemini-api/docs/models">Gemini API models (Google)</a></li>
<li><a href="https://ai.google.dev/gemini-api/docs/rate-limits">Gemini API rate limits (Google)</a></li>
<li><a href="https://apidog.com/blog/gemini-api-free-tier/">Gemini API free tier in 2026 (Apidog)</a></li>
<li><a href="https://www.scriptbyai.com/gemini-api-free-tier-limits/">Gemini API free tier limits (ScriptByAI)</a></li>
<li><a href="https://www.maximem.ai/blog/gemini-api-pricing-2026">Gemini API pricing 2026 (Maximem)</a></li>
<li><a href="https://www.layer3labs.io/guides/best-open-source-llm">Best open source LLMs, 2026 (Layer3 Labs)</a></li>
<li><a href="https://techjacksolutions.com/ai-tools/open-source/best-open-source-ai-models/">Best open source AI models (TechJack Solutions)</a></li>
</ul>
</div></section>
"""
    return page("models.html", "Models and the free tier", "Types of large language models, the Gemini family, and which model to use on the free tier.", body, hero_html=hero,
                prev=("use-case.html", "The airport use case"), nxt=("setup.html", "Setup"))


def setup():
    hero = pagehero("Setup", "Get ready in ten minutes",
                    "A Google account, an API key, and one Colab Secret. Do it once, before Monday, and run the smoke test to prove it works.")
    body = """
<section class="reveal"><div class="wrap">
<h2 id="steps">Your API key and Colab</h2>
""" + steps([
        ("Sign in to Google AI Studio", "Go to <a href=\"https://aistudio.google.com\">aistudio.google.com</a> and sign in with your Google account."),
        ("Create an API key in a new project", "Use a new project, not one you use for other work. Copy the key once. Do not share it, and do not paste it into emails or chats."),
        ("Choose free or paid", "<b>Free tier:</b> no card, low limits, fictional data only, content may be used by Google to improve its products. <b>Paid:</b> enable billing on the project for reliable quota. The three days are estimated at about USD 10, which is a ceiling, not an expected spend. Set a budget alert."),
        ("Open any notebook in Colab", "Go to <a href=\"https://colab.research.google.com\">colab.research.google.com</a> and open a notebook (File, Upload notebook)."),
        ("Store the key as a Colab Secret", "Click the key icon on the left. Add a secret named <code>GEMINI_API_KEY</code>, paste your key, and switch on <b>Notebook access</b>."),
        ("Run the smoke test", "Open <code>00_Smoke_Test.ipynb</code>. Run the cells top to bottom with Shift and Enter. Upload the participant pack zip when asked. You want to see <b>all checks passed</b>."),
    ]) + """
<div class="callout"><b class="t">The three usual problems</b><p>A missing Colab Secret, Notebook access switched off, or a key from a project with no quota. These account for nearly all stuck participants. Check them first.</p></div>
<p>On the free tier, also read <a href="models.html#which">which model to use</a>. The first model in the kit's list can have a very small daily allowance.</p>
""" + checks("setup", [
        "I signed in to Google AI Studio and created a key in a new project",
        "I decided free tier (fictional data only) or paid (billing and a budget alert)",
        "I added the secret <code>GEMINI_API_KEY</code> in Colab and switched on Notebook access",
        "I ran <code>00_Smoke_Test.ipynb</code> and saw <b>all checks passed</b>",
        "I know my key is private: never in a cell, a chat, an email or Git",
    ], "su") + """
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="copilot">Copilot Notebook (5 minutes)</h2>
<p>For Day 1, Part 1 and Lab 1A. If you do not have Copilot, use any AI chat that accepts file uploads.</p>
""" + steps([
        ("Upload the workbook", "Upload <code>Airport_Copilot_Workbook.xlsx</code> to your OneDrive."),
        ("Create a notebook", "Open Microsoft 365 Copilot in your browser, open Notebooks, create a new notebook and name it <b>Airport Analyst</b>."),
        ("Add the source", "Add the workbook as a source. Do not add the PDFs yet."),
        ("Paste the standing rules", "Open More options, then Instructions. Paste the six <a href=\"day-1.html#lab1\">standing rules</a>. Save."),
        ("Check", "Ask: <em>What sources do you have, and what are your rules?</em> Copilot should list the workbook and your six rules."),
    ]) + """
<p class="small">Copilot in Excel needs each sheet to be an Excel Table. The workbook is already built that way.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="fix">If something breaks</h2>
""" + table(["Symptom", "Likely cause", "Fix"], [
        ["Could not read the secret <code>GEMINI_API_KEY</code>", "Secret missing, or Notebook access is off", "Add or enable it, then rerun the setup step"],
        ["400 or 403 mentioning the API key", "Wrong key, key restricted, or project disabled", "Create a new key"],
        ["429 RESOURCE_EXHAUSTED", "Quota or rate limit", "The helper retries by itself. If it persists, pause 60 seconds, switch to a Flash-Lite model, or use a funded key"],
        ["Model not found", "The model name is unavailable to your key", "The helper falls back. Otherwise edit <code>MODEL_CANDIDATES</code>"],
        ["<code>ModuleNotFoundError: workshop_helpers</code>", "The kit setup cell was not run", "Run the kit cell and check that the zip uploaded"],
        ["The agent loops or gives no answer", "A tool error, or too many calls", "Read the TOOLS CALLED log and the error text the tool returned"],
        ["My answer differs from my neighbour's", "Normal variation. The model is not deterministic", "Compare the SQL it ran, not the wording"],
        ["Colab disconnects", "Idle timeout", "Reconnect and rerun the setup cells. Use the catch-up cell in notebook 05"],
    ]) + """
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="after">After the workshop</h2>
<ul>
<li>Keep the notebooks, the prompt checklist and the data dictionary.</li>
<li>Fictional data only on free keys.</li>
<li>Delete or restrict the keys you created for the workshop. See <a href="security.html#rotation">key rotation</a>.</li>
</ul>
</div></section>
"""
    return page("setup.html", "Setup", "API key, Colab Secrets, smoke test and fixes for common errors.", body, hero_html=hero,
                prev=("models.html", "Models and the free tier"), nxt=("tokens.html", "Tokens and cost"))


def tokens():
    hero = pagehero("Tokens and cost", "Understanding tokenomics",
                    "You do not pay for answers. You pay for tokens. Knowing what a token is, what is counted and how an agent multiplies it lets you predict a bill before it arrives.")
    body = """
<section class="reveal"><div class="wrap">
<h2 id="what">What is a token?</h2>
<p>A model reads and writes tokens, not words. A token can be a single character or a whole word, and long words are split into several tokens. For Gemini, a token is about 4 characters, and 100 tokens is roughly 60 to 80 English words.</p>
<div class="grid g3">
<div class="card"><span class="k">Rule of thumb</span><p>1,000 tokens is about 750 English words, or one and a half pages of text.</p></div>
<div class="card"><span class="k">Not equal for every text</span><p>Other languages, code, tables and numbers often use more tokens per word than plain English. Count them, do not guess.</p></div>
<div class="card"><span class="k">Not only text</span><p>Images, audio and video are tokenised too. A small image costs a fixed number of tokens, and video and audio are counted per second.</p></div>
</div>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="pay">What you pay for</h2>
""" + table(["Counted as", "What it includes", "Why it matters"], [
        ["<b>Input tokens</b>", "Your prompt, the system instruction, tool definitions, retrieved document sections, the schema, earlier chat turns, and tool results sent back to the model", "Everything the model reads, every call. A long system prompt is paid on every call"],
        ["<b>Output tokens</b>", "The answer the model writes", "Priced several times higher than input. Ask for brevity in the prompt"],
        ["<b>Thinking tokens</b>", "The hidden reasoning before the answer", "Billed as output, and they count toward <code>max_output_tokens</code>. Higher thinking levels cost more and take longer"],
    ]) + """
<div class="callout ice"><b class="t">Output costs more than input</b><p>On <code>gemini-3.8-flash</code>, output is priced five times higher than input (3.75 against 0.75 USD per million tokens until 31 December 2026). A short, focused answer saves more than a short prompt.</p></div>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="agents">Why agents cost more than chats</h2>
<p>A chat answer is one call. An agent is a loop, and every turn of the loop is a call that re-sends the context.</p>
<div class="flow">
<div><b>Turn 1</b><span>System prompt, schema, question go in. The model asks for a SQL call.</span></div>
<div><b>Turn 2</b><span>All of that goes in again, plus the SQL result. The model asks for a document search.</span></div>
<div><b>Turn 3</b><span>Everything so far goes in again, plus the sections. The model writes the answer.</span></div>
</div>
<p>The figure printed after a call in a notebook covers the last model turn. A question with several tool calls costs more than the displayed figure, and notebook 06 multiplies by a rough factor to estimate it. That is why you measure.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="prices">Prices used in this workshop</h2>
""" + table(["Model", "Input per million tokens", "Output per million tokens (including thinking)", "Note"], [
        ["<code>gemini-3.8-flash</code>, paid, until 31 Dec 2026", "USD 0.75", "USD 3.75", "Used in the notebooks"],
        ["<code>gemini-3.8-flash</code>, paid, from 1 Jan 2027", "USD 1.50", "USD 7.50", "Prices double after the introductory period"],
        ["<code>gemini-3.5-flash-lite</code>, paid", "USD 0.30", "USD 2.50", "Indicative, from a public tracker"],
        ["Free tier, eligible models", "USD 0", "USD 0", "Within rate limits. Fictional data only"],
    ]) + """
<p class="small">Prices change. Compare with the official pricing page the day before you teach or buy.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="calculator">Estimate a pilot</h2>
<p>These are example numbers. Replace them with the <code>[tokens]</code> line printed under your own notebook calls: prompt, answer, thinking.</p>
<div class="calc" id="calc">
<div>
<label for="c_model">Price set</label>
<select id="c_model"><option value="flash38a">gemini-3.8-flash, until 31 Dec 2026</option><option value="flash38b">gemini-3.8-flash, from 1 Jan 2027</option><option value="lite35">gemini-3.5-flash-lite (indicative)</option></select>
<label for="c_in">Input tokens per model call</label><input id="c_in" type="number" min="0" value="5000">
<label for="c_out">Answer tokens per model call</label><input id="c_out" type="number" min="0" value="600">
<label for="c_th">Thinking tokens per model call</label><input id="c_th" type="number" min="0" value="1200">
<label for="c_calls">Model calls per question (agent loop)</label><input id="c_calls" type="number" min="1" value="4">
<label for="c_users">Users</label><input id="c_users" type="number" min="0" value="25">
<label for="c_q">Questions per user per day</label><input id="c_q" type="number" min="0" value="20">
<label for="c_days">Days</label><input id="c_days" type="number" min="0" value="3">
</div>
<div>
<div class="small" id="r_note"></div>
<div class="row2"><span>Cost per model call</span><b id="r_call"></b></div>
<div class="row2"><span>Cost per question</span><b id="r_q"></b></div>
<div class="row2"><span>Total tokens</span><b id="r_tok"></b></div>
<div class="row2"><span>Cost per user</span><b id="r_user"></b></div>
<p style="margin-top:18px" class="small">Total for everyone</p>
<div class="res" id="r_tot"></div>
</div>
</div>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="levers">Eight ways to spend fewer tokens</h2>
""" + steps([
        ("Retrieve, do not paste", "Pasting all twelve documents works but is costly and does not scale. RAG sends only the four best sections."),
        ("Keep top-k small", "Four sections gave enough context with little noise in the workshop test."),
        ("Ask for brevity in the prompt", "Do not use a tiny output cap to shorten answers. Thinking tokens count toward the cap, and a small cap cuts the answer off."),
        ("Match thinking to the task", "Low for classification and extraction. Medium for the agent. High only if your test set shows it helps."),
        ("Pick the smallest model that passes", "Test Flash-Lite against Flash on your golden set."),
        ("Trim the system prompt and schema", "They are paid on every call. Keep rules short and numbered."),
        ("Embed once, reuse", "Embedding all sections is done once per session and cached."),
        ("Look at caching and batch options", "Cached input is cheaper, and batch processing suits jobs that are not urgent. Check the pricing page for current terms."),
    ]) + """
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="measure">Measure, then multiply</h2>
<p>Before sending, <code>count_tokens</code> returns the input count. After sending, the usage fields on the response report input, output, thinking and total tokens. The workshop helper prints them under each call as a <code>[tokens]</code> line, with the time taken and a warning if the answer was cut off.</p>
<p>Run one full pass through notebooks 01 to 06 on your own key, count the calls and tokens, then multiply by the number of people. That figure beats any estimate on this page.</p>
<h3>Rate limits are part of the economics</h3>
<p>Requests per minute, tokens per minute and requests per day are checked on every call. A 429 error means you hit one. The helper waits and retries with a growing pause. If many people hit it at once, stagger the heavy cells. See <a href="models.html#free">the free tier</a>.</p>
</div></section>
"""
    return page("tokens.html", "Tokens and cost", "What a token is, what you pay for, why agents cost more, and a pilot cost calculator.", body, hero_html=hero,
                prev=("setup.html", "Setup"), nxt=("security.html", "Secure AI"))


def security():
    hero = pagehero("Secure AI", "What to do while you code",
                    "A model that is accurate on Monday can leak a key on Tuesday. These are the habits that protect your keys, your data and your users, in the order you will meet them.")
    body = """
<section class="reveal"><div class="wrap">
<h2 id="keys">1. Your API key is a password</h2>
<p>Anyone who holds your key can spend your money and read what you send. Treat it like a bank PIN.</p>
<div class="grid g2">
<div class="card"><h3>Do</h3>
<ul>
<li>Store it in Colab Secrets (key icon, name <code>GEMINI_API_KEY</code>, Notebook access on).</li>
<li>Read it from a secret or an environment variable in code.</li>
<li>Use a separate key for each project.</li>
<li>In production, use a secret manager.</li>
<li>Set a budget alert on the project.</li>
<li>Restrict the key to the Gemini API only.</li>
</ul></div>
<div class="card"><h3>Never</h3>
<ul>
<li>Paste the key into a notebook cell, a chat, an email or a screenshot.</li>
<li>Print it, even to "check it works".</li>
<li>Commit it to Git, even in a private repository.</li>
<li>Put it in a web page or mobile app. Users can extract it from client-side code.</li>
<li>Share one key between people.</li>
</ul></div>
</div>
""" + code("""# Right: the key comes from a secret, never from the code
from google import genai
from google.colab import userdata

client = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))

# Wrong: the key is now in the file, in the history and in every copy
# client = genai.Client(api_key="AIza...")""", "Colab pattern") + """
<div class="callout ice"><b class="t">Colab hygiene</b><p>Colab Secrets keep the key outside the notebook file. The notebook can still leak it if a cell prints it. Before you share a notebook, clear all outputs and search the cells for the word "key".</p></div>
<h3 id="rotation">Rotating and responding to a leak</h3>
""" + steps([
        ("Create a new key", "In AI Studio or the Google Cloud console."),
        ("Switch your code to the new key", "Update the secret or variable, deployments and configuration, then test."),
        ("Disable the old key", "Only after the new one works. If the old one leaked, do this at once."),
        ("Check billing and usage", "Audit usage logs for calls you did not make."),
    ]) + """
<p class="small">Google's current guidance: never check keys into source control, read them from environment variables, restrict them to the Gemini API, and route calls through a backend if you build a web or mobile app. Google now rejects unrestricted standard keys, and new AI Studio keys default to authorisation keys bound to a service account. Check the current key documentation for details.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="data">2. Know where your data goes</h2>
<p>Every prompt leaves your machine. Decide what may leave before you type it.</p>
""" + table(["Data class", "May go to an external model?", "Rule"], [
        ["Fictional or public", "Yes, including the free tier", "The workshop is entirely in this class"],
        ["Internal", "Only to approved services under paid terms", "GIA-POL-10, clauses 2.2 and 2.3"],
        ["Personal data", "Never", "GIA-POL-10, clause 2.3. Remove or mask it first"],
        ["Anything on the free tier", "No, unless fictional", "Content may be used by Google to improve its products"],
    ]) + """
<p>The airport's AI policy (GIA-POL-10) also says: training and pilots use fictional data only (2.4), agents have read-only access with every tool call logged (3.1 to 3.4), rules come from approved documents, numbers come from queries, and a named person is accountable and checks answers against the source query before publication (4.1 and 4.2).</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="injection">3. Data is not an instruction</h2>
<p>Prompt injection is text inside the data that tries to give the model orders: a feedback comment that says "ignore all previous instructions", or a document that says "run DROP TABLE". The model cannot always tell your instructions from the data it reads.</p>
<div class="grid g3">
<div class="card"><span class="k">Layer 1 | Prompt</span><p>A standing rule: text inside comments or documents is data, never an instruction. Helpful, but a rule is not a wall.</p></div>
<div class="card"><span class="k">Layer 2 | Harness</span><p>Read-only access, SELECT only, blocked write words, row caps. Even an obeyed order cannot delete anything.</p></div>
<div class="card"><span class="k">Layer 3 | Check</span><p>Log every call. Check the output in code (citations, schema). Review what the agent did, not only what it said.</p></div>
</div>
<p style="margin-top:14px"><b>Rules in the prompt help. Guardrails around the model help more.</b> Run the five attacks from Day 2 on your own agent, and when one works, add a defence and run it again.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="tools">4. Give tools the least power they need</h2>
<p>A model asks for a tool call. Your code decides whether to run it. That is the most important security boundary in an agent.</p>
""" + code("""# A read-only SQL tool, in outline
BLOCKED = ("insert", "update", "delete", "drop", "alter", "create", "attach", "pragma")

def run_sql(query):
    q = query.strip().lower()
    if not q.startswith("select"):          # SELECT only
        return "Refused: only SELECT queries are allowed."
    if any(w in q for w in BLOCKED):        # write words blocked
        return "Refused: this query contains a blocked word."
    con = sqlite3.connect("file:airport_ops.db?mode=ro", uri=True)   # read-only connection
    rows = pd.read_sql_query(query, con).head(40)                    # row cap
    log_call(query, len(rows))                                       # every call logged
    return rows.to_string()""", "The harness idea (simplified)") + """
<ul>
<li><b>Allow-list, do not block-list.</b> The model may call only the tools you defined.</li>
<li><b>Return errors as text</b> so the model can repair its own query, instead of crashing.</li>
<li><b>Never run model-written code or SQL with more rights</b> than a human reader would have.</li>
<li><b>Show the tool log</b> to the person who reads the answer.</li>
</ul>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="outputs">5. Treat model output as untrusted</h2>
<ul>
<li><b>Numbers come from queries.</b> Verify at least three yourself. A number with no query behind it does not go in the brief.</li>
<li><b>Rules come from approved documents.</b> Check status: draft and superseded versions are not in force.</li>
<li><b>Check citations in code.</b> Confirm that each cited clause is in the sections you retrieved.</li>
<li><b>Use structured output.</b> A schema (for example JSON with fixed fields) is easier to validate than free text.</li>
<li><b>Say what you do not know.</b> Honest "not found" beats a confident invention.</li>
<li><b>Re-test after every change</b> to the model, the prompt, the tools or the documents.</li>
</ul>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="hygiene">6. Everyday coding hygiene</h2>
""" + table(["Habit", "Why"], [
        ["Keep keys out of Git: add secret files to <code>.gitignore</code>, turn on secret scanning and push protection on your repository", "A key committed once is public forever in the history"],
        ["Install only packages you recognise, and pin their versions", "A mistyped or hijacked package can steal secrets"],
        ["Do not paste unknown code that reads environment variables or secrets", "Notebooks run with your access"],
        ["Log calls, but never log keys or personal data", "Logs are shared and kept"],
        ["Set timeouts, retries with a growing pause, and a maximum number of tool turns", "A looping agent can burn your budget"],
        ["Set a budget alert on every project", "You find out about a leak from the alert, not the bill"],
        ["Delete keys you no longer use", "Old keys are the ones nobody watches"],
        ["Name one accountable person for every agent that others rely on", "No owner, no audit"],
    ]) + """
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="checklist">Secure AI checklist</h2>
""" + checks("sec", [
        "My key is a Colab Secret or an environment variable, never in a cell",
        "I have not printed, pasted, committed or emailed my key",
        "I know the data class of everything I send, and I used fictional data on the free tier",
        "My tools are read-only, allow-listed, row-capped and logged",
        "Text inside data is treated as data, and I tested at least one injection",
        "I verified key numbers with my own query and checked citations",
        "I set a budget alert, and I know how to rotate the key",
        "A named person is accountable for anything others will use",
    ], "sc") + """
<h3>Sources</h3>
<ul>
<li><a href="https://ai.google.dev/gemini-api/docs/api-key">Using Gemini API keys (Google)</a></li>
<li><a href="https://ai.google.dev/gemini-api/docs/tokens">Understand and count tokens (Google)</a></li>
</ul>
</div></section>
"""
    return page("security.html", "Secure AI", "API key safety, data rules, prompt injection, safe tools and coding hygiene for AI projects.", body, hero_html=hero,
                prev=("tokens.html", "Tokens and cost"), nxt=("exercises.html", "All exercises"))


def exercises():
    hero = pagehero("Exercises", "Every exercise, in one place",
                    "Core checklists for each lab, with your progress saved in this browser, followed by optional stretch tasks for when you finish early.")
    body = """
<section class="reveal"><div class="wrap">
<h2 id="day1">Day 1 | Explore and ask</h2>
<h3>Core</h3>
""" + checks("ex1", [
        "<b>Lab 1A</b> (Copilot, 50 min): notebook \"Airport Analyst\" created with the workbook as a source",
        "Standing rules pasted into Instructions",
        "Round 1 (vague) and Round 2 (five parts) compared",
        "Round 4: ten comments classified, English and Arabic",
        "Round 5: I know what happened with the comment that gives orders",
        "<b>Lab 1B</b> (Colab, 40 min): sections 1 to 5, 7, 9 and 11 done",
        "My code returns a structured table of classified comments",
        "<b>Lab 2</b>: I added the 12 PDFs in Copilot and noted which document it quoted",
        "I can say why we split first and compare numbers second",
        "I found which draft or old rule slips in",
        "<b>Lab 3</b> (Colab, 50 min): I wrote my own queries",
        "My query shows waiting time and counters open for Friday evenings",
        "I scaled counts by 25",
    ], "e1_") + """
<h3>Stretch (optional)</h3>
<ul>
<li>Rewrite a task from your own department as a five-part prompt. Test it on a public document.</li>
<li>Classify twenty comments instead of ten. Which fail, and what example would fix them?</li>
<li>Ask three document questions where the draft would give a wrong answer. Does your status rule hold?</li>
<li>Write three more SQL queries: delayed share by airline, estimated passengers by terminal (use 25), counters open by hour on a weekday of your choice.</li>
<li>Ask Gemini to write a query for a question of your own, then fix it by hand.</li>
</ul>
<p><b>Homework:</b> finish the optional sections in notebooks 01 to 03. Bring one question from your own department that could be answered with data and documents.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="day2">Day 2 | Build the analyst</h2>
<h3>Core</h3>
""" + checks("ex2", [
        "<b>Lab 4</b> (90 min): baseline hit@1 and hit@3 written down",
        "Compared chunking and embedding sizes",
        "Turned on the status filter and saw the draft question change",
        "Added keyword search and saw which questions improved",
        "Added three golden questions of my own",
        "<b>Lab 5</b> (120 min): tested the SQL tool with a good query and a bad query (DROP)",
        "Tested the document tool, with and without the draft flag",
        "Read the nine rules in the system prompt",
        "Ran the five beats and read the tool log after each",
        "Verified at least three numbers with my own SQL",
        "<b>Lab 6</b> (80 min): compared low, medium and high thinking levels on four questions",
        "Saw the effect of a tiny output cap",
        "Ran five safety attacks and recorded each result",
        "Estimated monthly cost for 25 users",
    ], "e2_") + """
<h3>Stretch (optional)</h3>
<ul>
<li>Test <code>gemini-embedding-2</code> against the default on your golden set. Does the score change?</li>
<li>Run the same four questions on a Flash-Lite model and on a Flash model. Compare correctness, seconds, tool calls and tokens.</li>
<li>Invent a sixth attack and add a defence. Run all six again.</li>
<li>Write a golden question that needs both tools. Does the agent call both?</li>
<li>Measure the tokens of one full question and use the <a href="tokens.html#calculator">calculator</a> to estimate a pilot of five users.</li>
</ul>
<p><b>Homework:</b> notebook 06 sections 7 and 10. Choose the capstone scenario you would like to take.</p>
</div></section>

<section class="reveal"><div class="wrap">
<h2 id="day3">Day 3 | Put it together, then prove it</h2>
<h3>Core</h3>
""" + checks("ex3", [
        "<b>Lab 7</b>: scenario chosen, three starter questions run",
        "Own follow-up questions asked: why, by month, by terminal, what do the rules say",
        "Three numbers verified with my own SQL",
        "One-page brief filled in: headline, numbers, rules, three actions with owners and deadlines, assumptions and limits",
        "Brief downloaded, and demo rehearsed once",
        "Quiz done and demo given: finding, evidence, how we checked, the ask, one limit",
    ], "e3_") + """
<h3>My Monday-morning plan</h3>
""" + checks("mon", [
        "One repeated question in my department:",
        "The data and documents I would need:",
        "The rule I must check first (data class, approved service):",
        "Ten golden questions I will write:",
        "Five pilot users:",
    ], "m_") + """
<p class="small">Write the answers on the printable <a href="handout.html">handout</a>.</p>
</div></section>
"""
    return page("exercises.html", "All exercises", "Core checklists and stretch tasks for every lab, with saved progress.", body, hero_html=hero,
                prev=("security.html", "Secure AI"), nxt=("glossary.html", "Glossary"))


GLOSS = [
    ("Agent", "A model plus tools plus a loop. It decides what to do, calls a tool, reads the result and repeats until the answer is ready."),
    ("API key", "A secret string that identifies your project to the Gemini API. Treat it like a password."),
    ("Approved, draft, superseded", "Document statuses. Only approved documents are in force."),
    ("Chunk", "A piece of a document that is stored and searched on its own. In this workshop, one section."),
    ("Context", "Everything the model can see when it answers: your prompt, files, documents, schema, examples, chat history."),
    ("Context window", "The maximum number of tokens a model can read in one call."),
    ("Cosine similarity", "A score for how close two embeddings are in meaning."),
    ("Embedding", "Meaning turned into a list of numbers. Similar meanings give similar numbers."),
    ("Few-shot", "Giving the model a few worked examples inside the prompt."),
    ("Golden set", "Questions with known answers, used to test every change."),
    ("Hallucination", "A confident answer that is not supported by facts or sources."),
    ("Harness", "The guardrails around the model: read-only access, row caps, filters, logs, checks."),
    ("Hit at 1 or 3", "The right section was ranked first, or was in the top three."),
    ("Hybrid search", "Meaning search (embeddings) combined with keyword search."),
    ("Large language model (LLM)", "A model trained on large amounts of text that predicts and generates text."),
    ("Loop engineering", "Testing and re-testing so that quality does not silently drop after a change."),
    ("Metadata filter", "A rule on the search, such as status equals approved."),
    ("Open-weight model", "A model whose weights you can download and run yourself. Not always fully open source."),
    ("Prompt", "The instruction you give the model."),
    ("Prompt injection", "Text in the data that tries to give the model orders."),
    ("RAG", "Retrieval Augmented Generation: find the right text, then answer from it."),
    ("Rate limit", "A cap on requests or tokens per minute or per day. Exceeding it returns error 429."),
    ("Reciprocal rank fusion", "A way to merge two ranked lists so items ranked well in both rise to the top."),
    ("Sample", "A part of the data standing for the whole. Here, 4 percent of passengers: multiply counts by 25."),
    ("Skill", "A saved set of instructions, rules and examples for one kind of task."),
    ("SQL", "The language used to ask a database exact questions."),
    ("System instruction", "Standing rules the model follows in every answer."),
    ("Thinking level", "How much hidden reasoning the model does before answering: low, medium or high."),
    ("Token", "The unit a model reads and writes and the unit you pay for. About 4 characters of English."),
    ("Tool", "A function the model may ask your code to run, such as a database query or a document search."),
    ("Tool calling", "The model returns a request to call a tool. Your code runs it and returns the result."),
    ("Top-k", "How many sections the document tool returns for each question."),
    ("Free tier", "Access to selected models at no charge within rate limits. Content may be used to improve the provider's products."),
]


def glossary():
    hero = pagehero("Glossary", "Plain-language definitions",
                    "Every term used in the workshop, in alphabetical order.")
    rows = "".join(f"<tr><td><b>{t}</b></td><td>{d}</td></tr>" for t, d in sorted(GLOSS, key=lambda x: x[0].lower()))
    body = f"""
<section class="reveal"><div class="wrap">
<div class="tw"><table><thead><tr><th>Term</th><th>Meaning</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
"""
    return page("glossary.html", "Glossary", "Definitions of the terms used in the workshop.", body, hero_html=hero,
                prev=("exercises.html", "All exercises"), nxt=("handout.html", "Printable handout"))


def downloads():
    hero = pagehero("Downloads", "Notebooks, slides, guides and data",
                    "Files are released day by day. A file that is not yet available shows as released on the day.")

    def row(title, desc, path, label="Download"):
        return f'<div class="dl" data-file="{path}"><div><b>{title}</b><span class="small">{desc}</span></div><a class="go" href="{path}">{label}</a></div>'

    body = f"""
<section class="reveal"><div class="wrap">
<h2 id="before">Before Monday</h2>
<div class="tw">
{row("Take-home handout (PDF, A4)", "Notes for all three days, ready to print", "downloads/Workshop_Handout.pdf")}
{row("Participant pack (zip)", "Database, 12 policy documents in text and PDF, data dictionary, helper files. Upload it when a notebook asks", "downloads/Airport_Workshop_Participant_Pack.zip")}
{row("Copilot workbook (xlsx)", "The airport data as Excel tables, for the Copilot labs", "downloads/Airport_Copilot_Workbook.xlsx")}
{row("Copilot prompt pack (PDF)", "Setup steps, standing rules, prompts 1 to 8 and the lab rounds", "downloads/Copilot_Prompt_Pack_Participant.pdf")}
</div>
</div></section>
<section class="reveal"><div class="wrap">
<h2 id="d1">Day 1 | Monday</h2>
<div class="tw">
{row("Participant guide, Day 1 (PDF)", "Agenda, lab checklists, glossary, homework", "downloads/Participant_Guide_Day1.pdf")}
{row("Slides, Day 1 (PDF)", "Explore and ask, 41 slides", "downloads/Day1_Explore_and_Ask_Slides.pdf")}
{row("Notebooks, Day 1 (zip)", "00 smoke test, 01 prompt engineering, 02 intro to RAG, 03 intro to SQL", "downloads/Day1_Notebooks.zip")}
</div>
</div></section>
<section class="reveal"><div class="wrap">
<h2 id="d2">Day 2 | Tuesday</h2>
<div class="tw">
{row("Participant guide, Day 2 (PDF)", "Agenda, lab checklists, the five beats, glossary", "downloads/Participant_Guide_Day2.pdf")}
{row("Slides, Day 2 (PDF)", "Build the analyst, 35 slides", "downloads/Day2_Build_the_Analyst_Slides.pdf")}
{row("Notebooks, Day 2 (zip)", "04 RAG deep dive, 05 build the agent, 06 tuning and reliability", "downloads/Day2_Notebooks.zip")}
</div>
</div></section>
<section class="reveal"><div class="wrap">
<h2 id="d3">Day 3 | Wednesday</h2>
<div class="tw">
{row("Participant guide, Day 3 (PDF)", "Scenarios, the one-page brief, scoring, Monday-morning plan", "downloads/Participant_Guide_Day3.pdf")}
{row("Slides, Day 3 (PDF)", "Put it together, then prove it, 21 slides", "downloads/Day3_Put_It_Together_Slides.pdf")}
{row("Notebook, Day 3 (zip)", "07 capstone template", "downloads/Day3_Notebooks.zip")}
</div>
<div class="callout ice"><b class="t">For the instructor</b><p>Day 2 and Day 3 files are kept in a separate folder, <code>release_later</code>. Copy them into <code>downloads</code> on the morning of each day and the links switch on by themselves. Facilitator-only material (answer key, speaker notes, facilitator guides, quiz answers) is not part of this site and should not be added.</p></div>
</div></section>
"""
    return page("downloads.html", "Downloads", "Notebooks, slides, guides and the data pack, released day by day.", body, hero_html=hero,
                prev=("handout.html", "Printable handout"))
