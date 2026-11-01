"""Day 1 opening deck: AI in thirty minutes. Executive style: near-black, ice-blue lines, one amber node, hairlines, sharp corners.
Every block is a group that fades in on its own click. Speaker notes are word for word."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree
import copy

BG, PANEL, LINE = "05070B", "0A0F17", "2A4358"
ICE, AMB, WHITE, MUTE, DIM = "9FD6FF", "FFB454", "F2F6FA", "B4C3D3", "6F8296"
HEAD, BODY, MONO = "Arial", "Arial", "Consolas"
TOTAL = 16
FOOT = "Corporate Workshop | Day 1 / 3"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def rgb(h):
    return RGBColor.from_string(h)


def text(shapes, x, y, w, h, s, size=14, color=WHITE, bold=False, font=BODY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, name=None, spacing=None):
    tb = shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = s if isinstance(s, list) else [s]
    for i, ptxt in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.space_after = Pt(spacing)
        r = p.add_run()
        r.text = ptxt
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, font
        r.font.color.rgb = rgb(color)
    return tb


def rect(shapes, x, y, w, h, fill=PANEL, line=LINE, lw=0.75, name=None):
    sh = shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        sh.name = name
    if fill:
        sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def new_slide(label, title, notes, n=None):
    n = len(prs.slides) + 1
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(BG)
    text(s.shapes, 0.7, 0.42, 9, 0.3, label.upper(), 11, ICE, True, MONO)
    text(s.shapes, 0.7, 0.78, 11.9, 0.9, title, 34, WHITE, True, HEAD, name="Title")
    rect(s.shapes, 0.7, 1.72, 0.9, 0.04, ICE, None)           # the short ice-blue rule (house style)
    ln = s.shapes.add_connector(1, Inches(0.7), Inches(7.0), Inches(12.63), Inches(7.0))
    ln.line.color.rgb = rgb(LINE); ln.line.width = Pt(0.75)
    text(s.shapes, 0.7, 7.08, 6, 0.25, FOOT, 10, DIM, False, MONO)
    text(s.shapes, 11.63, 7.08, 1.0, 0.25, f"{n:02d}", 10, DIM, False, MONO, PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes
    s._clicks = []
    return s


def block(s, x, y, w, h, title, body=None, num=None, big=None, tsize=18, bsize=14, node=False):
    """One equal-size block, built as a group so it fades in as a single unit."""
    g = s.shapes.add_group_shape()
    g.name = f"Block {len(s._clicks) + 1}: {title[:30]}"
    rect(g.shapes, x, y, w, h)
    cy = y + 0.2
    if num:
        text(g.shapes, x + 0.25, cy, w - 0.5, 0.22, num, 11, ICE, True, MONO)
        cy += 0.32
    if big:
        text(g.shapes, x + 0.25, cy, w - 0.5, 0.75, big, 40, ICE, True, HEAD)
        cy += 0.85
    text(g.shapes, x + 0.25, cy, w - 0.5, 0.6, title, tsize, WHITE, True, HEAD)
    th = 0.34 * (1 + (len(title) * tsize * 0.0095 > (w - 0.5)))      # rough title height
    if body:
        text(g.shapes, x + 0.25, cy + th + 0.12, w - 0.5, h - (cy - y) - th - 0.3, body, bsize, MUTE, False, BODY)
    if node:
        n = g.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + w - 0.3), Inches(y + 0.2), Inches(0.1), Inches(0.1))
        n.fill.solid(); n.fill.fore_color.rgb = rgb(AMB); n.line.fill.background()
    s._clicks.append(g.shape_id)
    return g


def grid(cols, rows, x0=0.7, y0=2.15, w=11.93, h=4.55, gap=0.25):
    bw = (w - gap * (cols - 1)) / cols
    bh = (h - gap * (rows - 1)) / rows
    return [(x0 + c * (bw + gap), y0 + r * (bh + gap), bw, bh) for r in range(rows) for c in range(cols)]


def add_timing(slide):
    """A fade entrance on every block, one click each."""
    ids = slide._clicks
    if not ids:
        return
    P = "http://schemas.openxmlformats.org/presentationml/2006/main"
    n = [2]

    def nid():
        n[0] += 1
        return n[0]

    clicks = ""
    for spid in ids:
        a, b, c, d, e = nid(), nid(), nid(), nid(), nid()
        clicks += (f'<p:par><p:cTn id="{a}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
                   f'<p:par><p:cTn id="{b}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                   f'<p:par><p:cTn id="{c}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                   f'<p:set><p:cBhvr><p:cTn id="{d}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
                   f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
                   f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{e}" dur="500"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
                   f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    xml = (f'<p:timing xmlns:p="{P}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
           f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{clicks}</p:childTnLst></p:cTn>'
           f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
           f'<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
           f'</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
    el = etree.fromstring(xml)
    sld = slide._element
    clr = sld.find(f"{{{P}}}clrMapOvr")
    (clr.addnext(el) if clr is not None else sld.append(el))


def source(s, txt):
    text(s.shapes, 0.7, 6.72, 11.9, 0.22, txt, 10, DIM, False, MONO)


# ============================================================================== 1. title
s = prs.slides.add_slide(BLANK)
s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(BG)
s.shapes.add_picture("hero.png", 0, 0, prs.slide_width, prs.slide_height)
text(s.shapes, 0.7, 0.95, 9, 0.3, "DAY 1  |  MONDAY 2 NOVEMBER 2026", 12, ICE, True, MONO)
text(s.shapes, 0.7, 1.45, 7.6, 2.4, "Artificial intelligence in thirty minutes", 46, WHITE, True, HEAD, name="Title")
rect(s.shapes, 0.7, 3.7, 0.9, 0.04, ICE, None)
text(s.shapes, 0.7, 3.95, 6.6, 0.9, "What is happening, what it means for government work, and what we will build over the next three days.", 18, MUTE)
for i, (t, b) in enumerate([("What AI is", "and how a language model works"), ("What is happening", "in the world, the UAE and Sharjah"), ("What it means", "strengths, limits and responsible use")]):
    bx = 0.7 + i * 4.1
    g = s.shapes.add_group_shape(); g.name = f"Block {i + 1}: {t}"
    rect(g.shapes, bx, 5.55, 3.85, 1.15)
    text(g.shapes, bx + 0.25, 5.75, 3.4, 0.3, t, 18, WHITE, True)
    text(g.shapes, bx + 0.25, 6.15, 3.4, 0.4, b, 14, MUTE)
    s._clicks = getattr(s, "_clicks", []) + [g.shape_id]
text(s.shapes, 0.7, 7.08, 6, 0.25, FOOT, 10, DIM, False, MONO)
s.notes_slide.notes_text_frame.text = (
    "Good morning, and welcome. Before we open a single notebook, I want to spend half an hour on the big picture, so that everything we do for the next three days sits on one shared idea of what AI is and what it is not. "
    "I will keep this practical. We will cover three things. First, what AI actually is, and how a language model works in plain words. Second, what is happening in the world right now, and in the UAE and Sharjah in particular, because your government is moving faster than most. "
    "Third, what that means for you: the AI ecosystem, where AI is strong and where it fails, and how to write prompts that work, using our airport case. Please interrupt me at any point. If something is unclear to you, it is unclear to someone else in the room.")
slides = [s]

# ============================================================================== 2. agenda
s = new_slide("Overview", "What we will cover in the next half hour",
              "Here is the plan for the next thirty minutes. Six short parts. We start with a plain definition of AI, then look at how a language model really works, because that one idea explains most of its strengths and weaknesses. "
              "Then we look at what is happening now in the world, and what the UAE and Sharjah are doing. After that, an honest look at what AI does well and where it fails, a map of the three days, and finally we move into your hands-on labs. "
              "Notice that nothing here requires any technical background. If you can follow a news article, you can follow this.", 2)
items = [("01", "What AI is", "A plain definition, and the family tree of terms you keep hearing."),
         ("02", "How language models work", "Tokens, prediction and context, in three minutes."),
         ("03", "The AI ecosystem today", "Who builds what, the six shifts, and the numbers."),
         ("04", "The UAE and Sharjah", "The 2026 agentic AI programmes and what they mean for you."),
         ("05", "Strengths, limits, safety", "What AI does well, where it fails, and how to use it responsibly."),
         ("06", "Prompt engineering", "Prompt, context and harness, on our airport case, then the labs.")]
for (x, y, w, h), (n, t, b) in zip(grid(3, 2), items):
    block(s, x, y, w, h, t, b, num=n)
slides.append(s)

# ============================================================================== 3. what is AI
s = new_slide("01  What AI is", "What is artificial intelligence?",
              "A simple definition: AI is software that learns patterns from data, and then uses those patterns to predict, classify, generate or decide. That is all. It is not magic, and it is not a person. "
              "On the right you see the family tree. The biggest circle is artificial intelligence, any machine doing a task that normally needs human intelligence. Inside it is machine learning, systems that learn from examples instead of fixed rules. "
              "Inside that is deep learning, which uses very large neural networks. And at the centre is generative AI, the models that write, summarise, translate, draw and code. When people say AI today, they almost always mean this centre circle. "
              "One important point: a model knows nothing about your organisation unless you give it context. That is the theme of the whole workshop.", 3)
block(s, 0.7, 2.15, 5.7, 2.15, "A simple definition", "Software that learns patterns from data and uses them to predict, classify, generate or decide.")
block(s, 0.7, 4.55, 5.7, 2.15, "Not magic, not a person", "It finds patterns. It knows nothing about your organisation unless you give it context.")
rings = [(6.9, 2.15, 5.73, 4.55, "Artificial intelligence"), (7.35, 2.7, 4.83, 3.9, "Machine learning"), (7.8, 3.25, 3.93, 3.25, "Deep learning"), (8.25, 3.8, 3.03, 2.6, "Generative AI")]
for i, (x, y, w, h, lab) in enumerate(rings):
    r = rect(s.shapes, x, y, w, h, fill=PANEL if i < 3 else "0F1A26", line=ICE if i == 3 else LINE, lw=1.0 if i == 3 else 0.75)
    r.name = f"Ring {i + 1}: {lab}"
    tf = r.text_frame
    tf.margin_left, tf.margin_top = Inches(0.2), Inches(0.12)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    run = p.add_run(); run.text = lab
    run.font.size, run.font.bold, run.font.name = Pt(14), True, BODY
    run.font.color.rgb = rgb(ICE if i == 3 else WHITE)
    if i == 3:
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.LEFT
        r2 = p2.add_run(); r2.text = "writes, summarises, translates, draws and codes"
        r2.font.size, r2.font.name = Pt(14), BODY; r2.font.color.rgb = rgb(MUTE)
    s._clicks.append(r.shape_id)
slides.append(s)

# ============================================================================== 4. eras
s = new_slide("01  What AI is", "How we got here: five eras",
              "AI is not new. It has moved through five eras. In the first, people wrote the rules by hand: if this, then that. Useful, but brittle. In the second, machine learning, systems learned rules from examples, which is how your spam filter and recommendations work. "
              "In the third, deep learning from about 2012, very large neural networks became good at images, speech and text. In the fourth, from 2022, generative AI arrived and AI became something everyone could talk to. "
              "And now, from 2025, we are in the agentic era: models that do not only answer, but plan, use tools and take actions, always with human oversight. The UAE programmes we will see in a few minutes are about this last era. "
              "Each era did not replace the previous one. They stack, and a real system uses all of them.", 4)
eras = [("01", "Rules", "1950s to 1980s", "People write the rules. If this, then that."),
        ("02", "Machine learning", "1990s to 2010s", "Systems learn rules from examples: spam filters, recommendations."),
        ("03", "Deep learning", "2012 onward", "Large neural networks read images, speech and text."),
        ("04", "Generative AI", "2022 onward", "Models write, summarise, translate, draw and code."),
        ("05", "Agentic AI", "2025 onward", "Models plan, use tools and act, with human oversight.")]
for (x, y, w, h), (n, t, yr, b) in zip(grid(5, 1, h=4.3, gap=0.2), eras):
    block(s, x, y, w, h, t, yr + "\n" + b if False else b, num=f"{n}  {yr}", node=(n == "05"))
slides.append(s)

# ============================================================================== 5. how a language model works
s = new_slide("02  How language models work", "A language model predicts the next token",
              "Here is the one idea that explains most of what you will see. A language model does not look things up. It predicts the next piece of text. You give it text. It cuts the text into tokens, small pieces of about four characters of English. "
              "It then predicts the most likely next token, adds it, and repeats, token by token, until the answer is complete. It learned how to do this by reading an enormous amount of text. "
              "Two practical consequences. First, it sounds fluent even when it is wrong, because fluent text is exactly what it was trained to produce. Second, it can only use what it can see in one go, called the context window. "
              "If the fact is not in its training or in its context, it will invent something plausible. That is why, later today, we will give the model facts from your data and your documents.", 5)
flow = [("01", "Text in", "Your prompt, and any facts you add."), ("02", "Tokens", "Text is cut into pieces of about four characters."),
        ("03", "Prediction", "The model picks the likeliest next token, again and again."), ("04", "Text out", "A fluent answer. Fluent is not the same as correct.")]
for (x, y, w, h), (n, t, b) in zip(grid(4, 1, h=2.4), flow):
    block(s, x, y, w, h, t, b, num=n, node=(n == "03"))
facts = [("Trained on text", "It learned patterns from a huge amount of writing."), ("Context window", "It only sees what is in the prompt: instructions, files, data."), ("It does not look up", "No fact in its context means a plausible guess.")]
for (x, y, w, h), (t, b) in zip(grid(3, 1, y0=4.8, h=1.9), facts):
    block(s, x, y, w, h, t, b)
slides.append(s)

# ============================================================================== 6. what is happening
s = new_slide("03  What is happening now", "Six shifts shaping AI in 2026",
              "So what is happening right now? Six shifts. One: agents. Models are being given tools and memory so they can act, not only answer. Two: reasoning models that think step by step before they reply, which makes fewer mistakes on hard problems. "
              "Three: multimodal. One model reads text, images, audio and video together. Four: smaller and open models. Open-weight models have become competitive, and smaller specialised models are growing, which matters for cost and for data control. "
              "Five: AI built into the tools you already use, such as your office suite and your browser. And six: governance. Organisations are learning that rules, logs and accountability are not a brake on AI. They are what allows it to go live. "
              "You will touch four of these six in your labs: reasoning settings, tools, context and governance.", 6)
six = [("01", "Agents", "Models with tools and memory that plan and act, not only answer."), ("02", "Reasoning models", "They think step by step first, and make fewer errors on hard tasks."),
       ("03", "Multimodal", "One model reads text, images, audio and video together."), ("04", "Smaller and open models", "Open-weight and specialised models: more choice on cost and control."),
       ("05", "AI inside every tool", "Assistants built into office suites, browsers and business systems."), ("06", "Governance", "Rules, logs and named owners are what let AI go live.")]
for (x, y, w, h), (n, t, b) in zip(grid(3, 2), six):
    block(s, x, y, w, h, t, b, num=n, node=(n == "01"))
slides.append(s)


# ============================================================================== ecosystem
s = new_slide("03  The AI ecosystem", "The AI ecosystem: five layers, many players",
              "To make sense of the news, it helps to see AI as a stack of five layers. At the bottom, compute: chips and data centres, from companies like NVIDIA and Google's own TPUs, hosted by cloud providers. "
              "Above that, foundation models: Gemini, GPT, Claude, and open-weight families like Llama, Qwen, Mistral and Gemma. Above that, platforms and APIs, such as Google AI Studio and Vertex AI, where organisations reach the models. "
              "Above that, tools and agents: frameworks that give a model memory, search, databases and actions. And at the top, applications: the assistants and services people actually use. "
              "Why does this matter? Because when you choose AI for a government service, you are choosing at every layer: where the data goes, which model, who governs it. In this workshop we touch the middle three, using Gemini through AI Studio, with our own tools around it.", 0)
eco = [("05", "Applications", "Assistants and services people use: chat, copilots, citizen services, internal tools.", "Your airport assistant"),
       ("04", "Tools and agents", "Memory, search, databases and actions that let a model do work.", "Days 2 and 3"),
       ("03", "Platforms and APIs", "How organisations reach models: Google AI Studio, Vertex AI, cloud services.", "Gemini API, today"),
       ("02", "Foundation models", "Gemini, GPT, Claude; open-weight Llama, Qwen, Mistral, Gemma.", "Gemini Flash-Lite"),
       ("01", "Compute", "Chips and data centres: GPUs, TPUs and the clouds that host them.", "Provided by the cloud")]
for i, (n, t, b, w) in enumerate(eco):
    y = 2.1 + i * 0.93
    g = s.shapes.add_group_shape(); g.name = f"Layer {n}: {t}"
    rect(g.shapes, 0.7, y, 11.93, 0.8, fill="0F1A26" if i in (0, 1, 2, 3) and False else PANEL)
    text(g.shapes, 0.95, y + 0.26, 0.5, 0.3, n, 13, ICE, True, MONO)
    text(g.shapes, 1.5, y + 0.22, 3.0, 0.4, t, 18, WHITE, True)
    text(g.shapes, 4.6, y + 0.16, 5.4, 0.55, b, 14, MUTE)
    text(g.shapes, 10.2, y + 0.26, 2.3, 0.3, w, 12, AMB if i in (1, 2, 3) else DIM, True, MONO)
    s._clicks.append(g.shape_id)
slides.append(s)

# ============================================================================== 7. numbers
s = new_slide("03  What is happening now", "The scale of adoption is historic",
              "The numbers tell the same story. The Stanford AI Index 2026, published in April, reports global corporate AI investment of 581.7 billion dollars in 2025, up 130 percent in one year. "
              "Organisational adoption reached 88 percent, up from 78. Generative AI reached 53 percent of the population within three years, which is faster than the personal computer or the internet. "
              "And the UAE is among the world leaders on adoption, at about 54 percent in the Index, behind Singapore at 61. One caution: other commentators quote different UAE figures, so treat 54 percent as the Stanford figure, not the final word. "
              "The message for this room is simple. AI is not a future topic. Your colleagues, your citizens and your suppliers are already using it.", 7)
stats = [("581.7B", "Global corporate AI investment in 2025 (USD)", "Up 130 percent in one year"), ("88%", "Organisations using AI", "Up from 78 percent a year earlier"),
         ("53%", "Population using generative AI", "Within three years: faster than the PC or the internet"), ("54%", "UAE generative AI adoption", "Among the highest worldwide; Singapore 61 percent")]
for (x, y, w, h), (big, t, b) in zip(grid(4, 1, h=3.9, y0=2.3), stats):
    block(s, x, y, w, h, t, b, big=big, tsize=16, node=(big == "54%"))
source(s, "Source: Stanford HAI, AI Index Report 2026 (published 13 April 2026)")
slides.append(s)

# ============================================================================== 8. UAE and Sharjah
s = new_slide("04  The UAE and Sharjah", "The UAE and Sharjah are moving fast",
              "Now closer to home. In April 2026 the UAE Cabinet approved a framework to move fifty percent of federal government sectors, services and operations onto agentic AI within two years. "
              "The first four government AI agents are already live, covering procurement, tax audit, customer happiness and technical support. In June, His Highness the Crown Prince of Sharjah directed the acceleration of the transition to a government powered by agentic AI, "
              "and the Sharjah Digital Department is leading the Sharjah Agentic AI Programme, alongside the Digital Transformation Strategy for 2026 to 2028. "
              "Why does this matter to you? Because the people who understand how to ask, check and govern these systems will be the ones who shape them. That is what this workshop trains. "
              "Everything we build uses fictional data, but the method is exactly what a real service needs.", 8)
uae = [("UAE framework, April 2026", "Agentic AI across 50 percent of federal government sectors, services and operations within two years."),
       ("First federal AI agents", "Live in procurement, tax audit, customer happiness and technical support."),
       ("Sharjah, June 2026", "The Crown Prince directed a faster move to a government powered by agentic AI."),
       ("Sharjah Agentic AI Programme", "Led by the Sharjah Digital Department, with the 2026 to 2028 digital strategy.")]
for (x, y, w, h), (t, b) in zip(grid(4, 1, h=3.9, y0=2.3), uae):
    block(s, x, y, w, h, t, b, tsize=17, node=(t.startswith("Sharjah, June")))
source(s, "Sources: UAE Media Office (23 April 2026), WAM (2 June 2026), Middle East AI News")
slides.append(s)

# ============================================================================== 9. strengths and limits
s = new_slide("05  Strengths, limits, safety", "What AI does well, and where it fails",
              "Let us be honest about both sides. On the top row, what it does well: drafting and rewriting, summarising and extracting, translating and classifying, including Arabic, and explaining and brainstorming. "
              "On the bottom row, where it fails. It can invent facts with total confidence, which we call hallucination. It is weak at exact arithmetic and counting, so numbers must come from a database, not from the model. "
              "It cannot see your private data unless you give it. And it can be steered by instructions hidden inside the data it reads, which we call prompt injection. "
              "Every lab today is built around turning the bottom row into something manageable: facts from data, rules from approved documents, and checks around both.", 9)
text(s.shapes, 0.7, 2.0, 3, 0.22, "STRENGTHS", 11, ICE, True, MONO)
text(s.shapes, 0.7, 4.38, 3, 0.22, "LIMITS", 11, AMB, True, MONO)
good = [("Draft and rewrite", "Emails, reports and briefs in minutes."), ("Summarise and extract", "Long documents into key points and fields."),
        ("Translate and classify", "English and Arabic, comments into topics."), ("Explain and brainstorm", "A patient partner for ideas.")]
bad = [("Invents facts", "Fluent and confident, even when wrong."), ("Weak at exact numbers", "Counts and sums must come from data."),
       ("Blind to private data", "It only knows what you put in front of it."), ("Can be steered", "Hidden instructions in data can hijack it.")]
for (x, y, w, h), (t, b) in zip(grid(4, 1, y0=2.3, h=1.95, gap=0.2), good):
    block(s, x, y, w, h, t, b, tsize=16, bsize=14)
for (x, y, w, h), (t, b) in zip(grid(4, 1, y0=4.7, h=1.95, gap=0.2), bad):
    block(s, x, y, w, h, t, b, tsize=16, bsize=14, node=(t == "Invents facts"))
slides.append(s)

# ============================================================================== 10. models
s = new_slide("05  Strengths, limits, safety", "Models differ: closed, open, small, large",
              "A quick word on the models themselves. Closed models, like Gemini, GPT and Claude, are used through a provider's service. They are the most capable and the easiest to start with, but your data travels to the provider. "
              "Open-weight models, such as Llama, Qwen, DeepSeek, Mistral and Google's Gemma, can be downloaded and run on your own hardware, which helps with data control, but you operate them. "
              "Models also come in sizes. Large models reason better and cost more. Small models are fast and cheap. In this workshop we use the Gemini family, starting with the small and cheap Flash-Lite, because the free tier allows it. "
              "The rule to remember: choose the smallest model that passes your own test, and let your data rules decide where it may run.", 10)
mods = [("Closed models", "Gemini, GPT, Claude. Most capable, easiest start. Data goes to the provider."), ("Open-weight models", "Llama, Qwen, DeepSeek, Mistral, Gemma. You can run them yourself."),
        ("Large and small", "Pro and Flash for harder work. Flash-Lite and small open models for speed and cost."), ("How to choose", "The smallest model that passes your test, within your data rules.")]
for (x, y, w, h), (t, b) in zip(grid(4, 1, y0=2.3, h=3.9), mods):
    block(s, x, y, w, h, t, b, tsize=17, node=(t == "How to choose"))
slides.append(s)

# ============================================================================== 11. four-layer shift
s = new_slide("06  The road ahead", "The map for three days: the Four-Layer Shift",
              "Here is the map for the next three days. Every problem with an AI assistant sits in one of four layers. Layer one, the prompt: the instruction you write. Layer two, the context: the files, documents and data the model can see. "
              "Layer three, the harness: the guardrails and tools around the model, such as read-only access and logs. Layer four, the loop: testing, measuring and improving, again and again. "
              "Today we work on layers one and two. Tomorrow we add the harness and build an agent. On Wednesday we prove it with the loop. When something goes wrong, ask which layer it belongs to, and fix it there. Quality is usually fixed in context. Safety is fixed in the harness.", 11)
four = [("01  Day 1", "Prompt", "The instruction you write: role, task, format, rules."), ("02  Days 1 and 2", "Context", "What the model can see: files, documents, data, examples."),
        ("03  Day 2", "Harness", "Guardrails around the model: read-only tools, caps, logs."), ("04  Days 2 and 3", "Loop", "Test, measure, improve, and test again after every change.")]
for (x, y, w, h), (n, t, b) in zip(grid(4, 1, y0=2.3, h=3.9), four):
    block(s, x, y, w, h, t, b, num=n, tsize=22, node=(t == "Loop"))
slides.append(s)


# ============================================================================== prompt anatomy
s = new_slide("06  Prompt engineering", "A good prompt has five parts",
              "Now the practical heart of today: prompt engineering. Forget tricks. A good prompt has five parts. Role: who the model should act as. Task: exactly what to do. Context: the facts it must use. Format: how the answer should look. And rules: what it must never do. "
              "Look at our airport case. The weak prompt is: why are Friday evenings slow? The model has to guess everything. The strong prompt says: you are an airport operations analyst; explain the Friday evening queue at Terminal 1; here are the numbers from our database; answer in three bullets and one recommendation; use only these facts, and say if something is missing. "
              "Same model, same question, completely different quality. Notice that three of the five parts, context, format and rules, are not clever wording. They are information and guardrails. That leads us to the three layers.", 0)
parts = [("01", "Role", "You are an airport operations analyst."), ("02", "Task", "Explain the Friday evening queue at Terminal 1."),
         ("03", "Context", "Friday 17:00 to 22:59: average wait 36.1 min, 5 counters open."), ("04", "Format", "Three bullets and one recommendation."),
         ("05", "Rules", "Use only these facts. If something is missing, say so.")]
for (x, y, w, h), (n, t, b) in zip(grid(5, 1, h=2.6, gap=0.2), parts):
    block(s, x, y, w, h, t, b, num=n, node=(n == "03"))
block(s, 0.7, 4.95, 5.85, 1.75, "Weak prompt", "Why are Friday evenings slow? The model must guess everything, so it invents a plausible story.", tsize=17)
block(s, 6.78, 4.95, 5.85, 1.75, "Strong prompt", "All five parts present. Same model, same question, a grounded and checkable answer.", tsize=17, node=True)
slides.append(s)

# ============================================================================== three layers on the case
s = new_slide("06  Prompt engineering", "Three layers, on our airport case",
              "Here are the three layers, each with its airport example. Layer one, the prompt: the instruction. Role, task, format, tone. Layer two, the context: what the model can see. For us: the twelve policy documents and the facts from the airport database, but only the approved policies, never the draft or the superseded one. "
              "Layer three, the harness: the safety frame around the model. For us: the model may only run read-only SQL, SELECT statements only, results capped at forty rows, every query logged, and answers that cite their source. "
              "A useful rule for the whole workshop: when an answer is wrong, ask which layer failed. A vague answer is usually a prompt problem. An invented number is a context problem. An unsafe or unlogged action is a harness problem. Fix it in the layer where it belongs.", 0)
lay = [("LAYER 1", "Prompt", "The instruction you write.", "Role: operations analyst. Task: explain the Friday queue. Format: three bullets and a recommendation."),
       ("LAYER 2", "Context", "What the model can see.", "Approved policy clauses, never draft or superseded, plus facts from the database: waits, counters, delays."),
       ("LAYER 3", "Harness", "The frame around the model.", "Read-only SQL, SELECT only, 40-row cap, every query logged, answers cite their source.")]
for (x, y, w, h), (n, t, b, ex) in zip(grid(3, 1, y0=2.2, h=4.5), lay):
    g = block(s, x, y, w, h, t, b, num=n, tsize=22)
    text(g.shapes, x + 0.25, y + 2.2, w - 0.5, 0.25, "AIRPORT EXAMPLE", 11, AMB, True, MONO)
    text(g.shapes, x + 0.25, y + 2.55, w - 0.5, 1.7, ex, 14, WHITE)
slides.append(s)

# ============================================================================== same question three answers
s = new_slide("06  Prompt engineering", "One question, three answers",
              "Let us watch the layers work on one question: why is Friday evening so slow at Terminal 1? "
              "With the prompt only, the model answers from general knowledge. It will say something sensible and generic, like staffing shortages or peak travel, but it has no idea about our airport. It sounds right and it is a guess. "
              "Now add context, the facts from our database: between five and eleven on Friday evening, the average wait is 36.1 minutes against 9.2 on other days, with five counters open instead of nine. Now the answer names the real cause and the real numbers. "
              "Finally add the harness. The numbers are fetched by a read-only query, the answer cites the policy clause that sets the staffing standard, and the query is logged, so a colleague can check it. Now the answer is not only correct, it is trustworthy. "
              "That is the journey of the next three days: from a guess, to a grounded answer, to an answer you can defend.", 0)
three = [("01  PROMPT ONLY", "A fluent guess", "Probably staffing or peak travel. Sounds right. Nothing is checked, and none of it is about our airport."),
         ("02  + CONTEXT", "A grounded answer", "Friday 17:00 to 22:59 at Terminal 1: average wait 36.1 min against 9.2, with 5 counters open instead of 9."),
         ("03  + HARNESS", "An answer you can defend", "Numbers come from a read-only query, the standard cites its policy clause, and every step is logged.")]
for (x, y, w, h), (n, t, b) in zip(grid(3, 1, y0=2.2, h=4.5), three):
    block(s, x, y, w, h, t, b, num=n, tsize=22, node=(n.startswith("03")))
slides.append(s)

# ============================================================================== 12. responsible use
s = new_slide("05  Strengths, limits, safety", "Responsible use starts today",
              "Before you touch any tool, four principles. Privacy: in this workshop we use fictional data only. In your real work, personal data never goes to an external model, and internal data goes only to approved services under paid terms. "
              "Accuracy: verify every number and cite every rule. Fairness: look for bias, and keep a human in the loop for decisions that affect people. And accountability: every AI service has a named owner, and every answer can be traced to its source. "
              "You will see these again on Wednesday, in the responsible AI policy of our case study. For now, one habit: if you would not put it on a public website, do not paste it into an AI tool.", 12)
resp = [("Privacy", "Fictional data only here. Personal data never goes to an external model."), ("Accuracy", "Verify every number. Cite every rule. Say what you do not know."),
        ("Fairness", "Look for bias. Keep a person in the loop for decisions about people."), ("Accountability", "A named owner, a log of every action, a traceable source.")]
for (x, y, w, h), (t, b) in zip(grid(4, 1, y0=2.3, h=3.9), resp):
    block(s, x, y, w, h, t, b, tsize=20, node=(t == "Privacy"))
slides.append(s)

# ============================================================================== 13. data kinds
s = new_slide("06  The road ahead", "Data comes in three kinds",
              "One last concept, which is the bridge to your first two labs. Data comes in three kinds. Structured data lives in tables with fixed columns: flights, passengers, rosters. It is easy to count and to chart. "
              "Semi-structured data has some structure and some free text, like an incident record with a type, a severity and a short description. "
              "Unstructured data is free text: policies, emails, feedback comments, reports. Most organisational knowledge lives here, and this is where language models are strongest. "
              "In Lab one you will understand structured data with Python. In Lab two you will turn unstructured documents into something you can analyse. In Lab three you will bring both together for Gemini.", 13)
kinds = [("Structured", "Tables with fixed columns: flights, passengers, rosters. Easy to count and chart.", "Lab 1"),
         ("Semi-structured", "Some fields, some free text: an incident with a type, a severity and a root cause.", "Labs 1 and 2"),
         ("Unstructured", "Free text: policies, emails, feedback comments. Where language models are strongest.", "Lab 2")]
for (x, y, w, h), (t, b, lab) in zip(grid(3, 1, y0=2.3, h=3.9), kinds):
    block(s, x, y, w, h, t, b, num=lab, tsize=22)
slides.append(s)

# ============================================================================== 14. labs
s = new_slide("06  The road ahead", "Your three labs today",
              "Now to what you will do with your own hands. Lab one: understand the airport database with Python. You will list the tables, check the quality of the data, understand the four percent sample, and build a dashboard. "
              "Lab two: understand the policy documents. You will read them from PDF or text, turn them into a table, compare the approved, draft and superseded versions of one rule, and search them. "
              "Lab three: talk to Gemini. You will change the model, set a system prompt, and add context from a document and from your data, and see how a guess becomes a grounded answer. "
              "You do not need to be a programmer. You run a cell, read the result, and change one thing. By three o'clock you will have your own key, a dashboard, a document table and a grounded Gemini answer.", 14)
labs = [("Lab 1", "Understand the data", "Open the airport database with Python, check its quality, and build a dashboard."),
        ("Lab 2", "Understand the documents", "Read twelve policies from PDF, turn them into a table, and compare three versions of one rule."),
        ("Lab 3", "Talk to Gemini", "Change the model, set a system prompt, and add context from a document and from the data.")]
for (x, y, w, h), (n, t, b) in zip(grid(3, 1, y0=2.3, h=3.9), labs):
    block(s, x, y, w, h, t, b, num=n.upper(), tsize=22, node=(n == "Lab 3"))
slides.append(s)

# ============================================================================== 15. quick check
s = new_slide("Check", "Quick check before we build",
              "Four quick questions, to show hands. Question one: what does a language model do? It predicts the next token. Question two: a draft policy says twelve minutes, the approved one says fifteen. Which is the rule? The approved one, fifteen. "
              "Question three: a table holds a four percent sample of passengers. To estimate the number of passengers, what do you multiply the count by? Twenty-five. And do you multiply an average? No, never. "
              "Question four: where should an API key live? In a secret store, never in a notebook cell, a chat or an email. If most of the room got these right, we are ready. If not, we pause and look at that question again.", 15)
qs = [("Question 1", "What does a language model do?", "A  Looks facts up    B  Predicts the next token    C  Thinks like a person"),
      ("Question 2", "The draft says 12 minutes, the approved policy says 15. Which is the rule?", "A  12    B  15    C  The newest one"),
      ("Question 3", "A 4 percent sample of passengers. What do you multiply a count by?", "A  4    B  25    C  100"),
      ("Question 4", "Where should an API key live?", "A  In the notebook    B  In an email    C  In a secret store")]
for (x, y, w, h), (n, t, b) in zip(grid(2, 2, h=4.45, gap=0.22), qs):
    block(s, x, y, w, h, t, b, num=n.upper(), tsize=17, bsize=14)
slides.append(s)

# ============================================================================== 16. closing
s = prs.slides.add_slide(BLANK)
s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(BG)
s.shapes.add_picture("hero.png", 0, 0, prs.slide_width, prs.slide_height)
text(s.shapes, 0.7, 0.95, 9, 0.3, "NEXT", 12, ICE, True, MONO)
text(s.shapes, 0.7, 1.45, 7.6, 2.0, "Now let us build", 46, WHITE, True, HEAD, name="Title")
rect(s.shapes, 0.7, 2.55, 0.9, 0.04, ICE, None)
text(s.shapes, 0.7, 2.8, 6.4, 0.9, "Three steps, and you will have asked Gemini your first grounded question.", 18, MUTE)
s._clicks = []
for i, (n, t, b) in enumerate([("01", "Create your free key", "AI Studio, then a Colab Secret."), ("02", "Understand the data", "Lab 1: the airport database and a dashboard."), ("03", "Ask Gemini with context", "Lab 3: model, system prompt, facts.")]):
    bx = 0.7 + i * 4.1
    g = s.shapes.add_group_shape(); g.name = f"Block {i + 1}: {t}"
    rect(g.shapes, bx, 5.4, 3.85, 1.3)
    text(g.shapes, bx + 0.25, 5.57, 3.4, 0.22, n, 11, ICE, True, MONO)
    text(g.shapes, bx + 0.25, 5.86, 3.4, 0.3, t, 18, WHITE, True)
    text(g.shapes, bx + 0.25, 6.25, 3.4, 0.35, b, 14, MUTE)
    s._clicks.append(g.shape_id)
text(s.shapes, 0.7, 7.08, 6, 0.25, FOOT, 10, DIM, False, MONO)
s.notes_slide.notes_text_frame.text = (
    "That is the big picture. AI is software that learns patterns, a language model predicts the next token, the world and your government are moving toward agents, and the skill that matters is asking, checking and governing. "
    "Now we build. First step: create your free key. I will show you on the screen, and I want to see every hand with a green card within twenty minutes. Then Lab one: the airport data. "
    "Questions before we start? Good. Let us begin.")
slides.append(s)

for sl in slides:
    add_timing(sl)

prs.save("/home/claude/work/deck/Day1_AI_in_30_Minutes.pptx")
print("saved", len(slides), "slides")
