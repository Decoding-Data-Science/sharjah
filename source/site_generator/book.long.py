"""Illustrated participant handbook (A4 PDF) built from the same content as the site."""
import math, os, re, subprocess, html as _h
import diagrams as D
from common import esc


# ----------------------------------------------------------------- static wireframe art
def wire(cls="wire", w=600, h=600, rot=(0.7, 0.9)):
    p = (1 + math.sqrt(5)) / 2
    V = [(-1, p, 0), (1, p, 0), (-1, -p, 0), (1, -p, 0), (0, -1, p), (0, 1, p), (0, -1, -p), (0, 1, -p), (p, 0, -1), (p, 0, 1), (-p, 0, -1), (-p, 0, 1)]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    E = set()
    for f in F:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            E.add((min(a, b), max(a, b)))
    ax, ay = rot
    ca, sa, cb, sb = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay)
    P = []
    for x, y, z in V:
        y1, z1 = y * ca - z * sa, y * sa + z * ca
        x2, z2 = x * cb + z1 * sb, -x * sb + z1 * cb
        s = 1 / (1 + z2 * 0.12)
        P.append((w / 2 + x2 * w * 0.16 * s, h / 2 + y1 * w * 0.16 * s, z2))
    out = [f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    for a, b in sorted(E):
        d = (P[a][2] + P[b][2]) / 2
        op = 0.3 + 0.45 * (d + 2) / 4
        out.append(f'<line x1="{P[a][0]:.1f}" y1="{P[a][1]:.1f}" x2="{P[b][0]:.1f}" y2="{P[b][1]:.1f}" stroke="#8fd3ff" stroke-opacity="{op:.2f}" stroke-width="1.6"/>')
    for i, q in enumerate(P):
        if i % 4 == 0:
            out.append(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="4" fill="#ffb02e"/>')
    out.append("</svg>")
    return "".join(out)


def grid_art():
    w, h = 794, 450
    hz = 40
    out = [f'<svg class="grid" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">']
    for i in range(-14, 15):
        x = w / 2 + i * 70
        out.append(f'<line x1="{w/2 + i*6}" y1="{hz}" x2="{w/2 + (x - w/2)*2.4}" y2="{h}" stroke="#8fd3ff" stroke-opacity="{0.06 + 0.12*(1-abs(i)/14):.2f}"/>')
    for j in range(1, 14):
        k = j / 14
        y = hz + (h - hz) * k ** 2.2
        out.append(f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}" stroke="#8fd3ff" stroke-opacity="{0.05 + 0.2*k:.2f}"/>')
    for d in range(8):
        k1, k2 = d / 8, (d + 0.45) / 8
        out.append(f'<line x1="{w/2}" y1="{hz + (h-hz)*k1**2.2:.1f}" x2="{w/2}" y2="{hz + (h-hz)*k2**2.2:.1f}" stroke="#ffb02e" stroke-opacity="0.6" stroke-width="2"/>')
    out.append("</svg>")
    return "".join(out)


# ----------------------------------------------------------------- pieces
def cover():
    return f"""<div class="cover">{grid_art()}{wire('wire', 600, 600, (0.55, 0.8))}
<div class="in">
<div class="eyebrow">Corporate Workshop | 2 to 4 November 2026</div>
<h1>Participant <em>handbook</em></h1>
<div class="sub">Data and AI with Gemini. Three days, one airport, one problem. Your take-away notes: the ideas, the diagrams, the lab steps and the habits to keep.</div>
<div class="who">Instructor: Mohammad Arshad</div>
<div class="meta"><div><b>Dates</b>Mon 2 to Wed 4 Nov</div><div><b>Hours</b>08:30 to 15:00 (Wed 12:45)</div><div><b>Tools</b>Copilot, Colab, Gemini</div><div><b>Data</b>Fictional airport</div></div>
</div></div>"""


def banner(day, title, theme, when, skills, art_rot):
    items = "".join(f'<div><b>{a}</b>{b}</div>' for a, b in skills)
    return f"""<div class="banner">{wire('wire', 400, 400, art_rot)}
<div class="k">{day}</div><h1>{title}</h1><p>{theme}</p>
<div class="row"><div><b>When</b>{when}</div>{items}</div></div>"""


def part_head(n, title, sub, mk):
    return f'<div class="break"></div><span class="mk">@@{mk}@@</span><span class="kicker">Part {n}</span><h1 class="big">{title}</h1><p class="small" style="margin-bottom:3mm">{sub}</p>'


def clean(body, keep_sections=None):
    b = body
    # drop interactive-only remnants
    b = re.sub(r'<div class="toc".*?</div>', "", b, flags=re.S)
    b = re.sub(r'<div class="prevnext">.*?</div>\s*$', "", b, flags=re.S)
    # card links become plain cards, other internal links become plain text
    b = re.sub(r'<a class="card link"[^>]*>(.*?)</a>', r'<div class="card">\1</div>', b, flags=re.S)
    b = re.sub(r'<a [^>]*href="(?!https?:)[^"]*"[^>]*>(.*?)</a>', r"\1", b, flags=re.S)
    b = b.replace("<details>", "<details open>")
    return b


def drop_section(body, anchor_id):
    parts = re.split(r'(?=<section class="reveal">)', body)
    return "".join(p for p in parts if f'id="{anchor_id}"' not in p)


def notes_pages():
    lines = '<div class="lines">' + "<i></i>" * 26 + "</div>"
    plan = ("<table><tbody>"
            + "".join(f'<tr><td style="width:40%"><b>{i}. {t}</b></td><td style="height:19mm">&nbsp;</td></tr>' for i, t in enumerate(
                ["One repeated question in my department", "The data and documents I would need", "The rule I must check first (data class, approved service)", "Ten golden questions I will write", "Five pilot users"], 1))
            + "</tbody></table>")
    return (f'<div class="break"></div><span class="mk">@@N@@</span><span class="kicker">Notes</span><h1 class="big">My Monday-morning plan</h1>'
            f'<p>Small, measured, governed. Then grow.</p>{plan}<h3>My notes</h3>'
            f'<div class="lines">{"<i></i>" * 8}</div>'
            f'<div class="break"></div><h2 style="margin-top:0">More notes</h2>{lines}')


def contents(parts):
    rows = ""
    for i, (title, desc, mk) in enumerate(parts, 1):
        rows += f'<div class="r"><b>{i:02d}</b><div>{esc(title)}<span class="d">{esc(desc)}</span></div><em data-mk="{mk}">__{mk}__</em></div>'
    return f"""<span class="kicker">Contents</span><h1 class="big">What is inside</h1>
<div class="toc2">{rows}</div>
<div class="callout ice" style="margin-top:8mm"><b class="t">How to use this handbook</b><p>Read the part for the day you are in. Do the lab steps with your notebook open. Use the <b>Watch out</b> boxes to avoid the traps. Answer the <b>Can you answer?</b> questions to check yourself; the answers are printed small below each box. Keep the Secure AI and Tokens parts on your desk when you build your own project.</p></div>"""


PARTS = [
    ("Welcome and the story", "The manager's problem, the three days, the Four-Layer Shift, the ground rules", "P1"),
    ("Setup", "Your key, Colab Secrets, Copilot, the smoke test, and a fix for each common error", "P2"),
    ("The airport case", "The database, the twelve documents, the traps, the five beats", "P3"),
    ("Day 1: Explore and ask", "Copilot, prompt engineering, documents (RAG) and SQL", "D1"),
    ("Day 2: Build the analyst", "Measured RAG, the agent, tuning, testing and attacking it", "D2"),
    ("Day 3: Put it together, then prove it", "Governance, Monday actions and the capstone brief", "D3"),
    ("Models and the free tier", "Types of models, the Gemini family, which one to pick", "M1"),
    ("Tokens and cost", "What a token is, what you pay for, why agents cost more", "M2"),
    ("Secure AI", "Keys, data, injection, safe tools and coding hygiene", "M3"),
    ("Exercises and glossary", "Every lab checklist and the words you will meet", "M4"),
    ("My Monday-morning plan and notes", "Your plan for your own department", "N"),
]


def build_html(B, nums=None):
    """B: dict fname -> body html (static diagrams)."""
    css = '<link rel="stylesheet" href="assets/book.css">'
    toc = contents(PARTS)
    if nums:
        for mk, n in nums.items():
            toc = toc.replace(f"__{mk}__", str(n))
    toc = re.sub(r"__[A-Z0-9]+__", "", toc)

    welcome = drop_section(drop_section(clean(B["index.html"]), "site"), "prework")
    jr = D.journey()
    parts = []
    parts.append(f'<div class="break"></div><span class="mk">@@C@@</span>{toc}')
    parts.append(part_head(1, "Welcome and the story", "Where we are going, and how we will get there.", "P1") + welcome)
    parts.append(part_head(2, "Setup", "Ten minutes, done once, before Monday.", "P2") + clean(B["setup.html"]))
    parts.append(part_head(3, "The airport case", "One fictional airport, one database, twelve documents.", "P3") + clean(trim_case(B["use-case.html"])))
    parts.append('<div class="break"></div><span class="mk">@@D1@@</span>' + banner("Day 1 | Monday 2 November", "Explore and ask", "Three ways to ask a question: a Copilot assistant with your files, Gemini in code, and SQL.", "08:30 to 15:00",
                 [("Labs", "3"), ("Notebooks", "00 to 03"), ("Ends with", "Quiz")], (0.5, 0.7)) + clean(B["day-1.html"]))
    parts.append('<div class="break"></div><span class="mk">@@D2@@</span>' + banner("Day 2 | Tuesday 3 November", "Build the analyst", "One assistant that reads the documents and queries the data, and a way to prove it can be trusted.", "08:30 to 15:00",
                 [("Labs", "3"), ("Notebooks", "04 to 06"), ("Ends with", "Wrap-up")], (0.9, 0.4)) + clean(B["day-2.html"]))
    parts.append('<div class="break"></div><span class="mk">@@D3@@</span>' + banner("Day 3 | Wednesday 4 November", "Put it together, then prove it", "See the whole system in one picture, leave with five actions, and deliver a verified one-page brief.", "08:30 to 12:45",
                 [("Lab", "1"), ("Notebook", "07"), ("Ends with", "Demos")], (0.3, 1.1)) + clean(B["day-3.html"]))
    parts.append(part_head(7, "Models and the free tier", "Types of models, the Gemini family, and the choice that works on a free key.", "M1") + clean(B["models.html"]))
    parts.append(part_head(8, "Tokens and cost", "You do not pay for answers. You pay for tokens.", "M2") + clean(drop_calc(B["tokens.html"])))
    parts.append(part_head(9, "Secure AI", "What to do while you code.", "M3") + clean(B["security.html"]))
    parts.append(part_head(10, "Exercises and glossary", "Every lab checklist, then the words you will meet.", "M4") + clean(trim_ex(B["exercises.html"])) + "<h2>Glossary</h2>" + clean(B["glossary.html"]))
    parts.append(notes_pages())
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Participant handbook | Data and AI with Gemini</title>{css}</head><body>' + "".join(parts) + "</body></html>"


def trim_case(body):
    b = re.sub(r'(<h2 id="tables">.*?</h2>\s*<p>.*?</p>\s*)<div class="tw">.*?</div>\s*(?=<h3>)', r"\1", body, count=1, flags=re.S)
    return b


def trim_ex(body):
    b = re.sub(r'<div data-progress="[^"]*">.*?</div></div>\s*<ul class="check"[^>]*>.*?</ul>', "", body, flags=re.S)
    b = re.sub(r'<h3>Core</h3>\s*', "", b)
    b = re.sub(r'<h3>My Monday-morning plan</h3>\s*', "", b)
    return b


def drop_calc(body):
    parts = re.split(r'(?=<section class="reveal">)', body)
    out = []
    for p in parts:
        if 'id="calculator"' in p:
            out.append('<section><div class="wrap"><h2 id="calculator">Estimate a pilot</h2><p><b>Cost per call</b> = (input tokens x input price + (answer tokens + thinking tokens) x output price) / 1,000,000. '
                       '<b>Cost per question</b> = cost per call x calls per question. <b>Pilot cost</b> = cost per question x questions per user x users x days.</p>'
                       '<div class="callout ice"><b class="t">Worked example (illustrative numbers)</b><p>5,000 input, 600 answer and 1,200 thinking tokens per call on <code>gemini-3.8-flash</code> (0.75 and 3.75 USD per million): about USD 0.011 per call. Four calls per question: about USD 0.042. 20 questions a day for 3 days: about USD 2.52 per person. Replace the numbers with the <code>[tokens]</code> line from your own notebook.</p></div></div></section>')
        else:
            out.append(p)
    return "".join(out)


def render_pdf(html_path, pdf_path, total_label=True, cover_only=False):
    from playwright.sync_api import sync_playwright
    foot = ('<div style="font:7.5pt Inter,Arial,sans-serif;color:#52627a;width:100%;padding:0 15mm;display:flex;justify-content:space-between">'
            '<span>Data and AI with Gemini | Participant handbook | All data and documents are fictional</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + os.path.abspath(html_path))
        pg.wait_for_timeout(600)
        if cover_only:
            pg.pdf(path=pdf_path, format="A4", print_background=True, prefer_css_page_size=True)
        else:
            pg.pdf(path=pdf_path, format="A4", print_background=True, prefer_css_page_size=True, display_header_footer=True,
                   header_template="<span></span>", footer_template=foot)
        b.close()


def page_of_markers(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    found = {}
    for i in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), pdf, "-"], capture_output=True, text=True).stdout
        for m in re.findall(r"@@([A-Z0-9]+)@@", t):
            found.setdefault(m, i)
    return found, n


def make(B, site_dir):
    """Two-pass build. Returns (pdf_path, page_count)."""
    work = site_dir
    cover_html = os.path.join(work, "_cover.html")
    open(cover_html, "w", encoding="utf-8").write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="assets/book.css"></head><body>{cover()}</body></html>')
    body_html = os.path.join(work, "_book.html")
    open(body_html, "w", encoding="utf-8").write(build_html(B))
    tmp = os.path.join(work, "_book.pdf")
    render_pdf(body_html, tmp)
    found, n = page_of_markers(tmp)
    nums = {k: v for k, v in found.items()}
    open(body_html, "w", encoding="utf-8").write(build_html(B, nums))
    render_pdf(body_html, tmp)
    found2, n2 = page_of_markers(tmp)
    if found2 != found:
        nums = found2
        open(body_html, "w", encoding="utf-8").write(build_html(B, nums))
        render_pdf(body_html, tmp)
    cov = os.path.join(work, "_cover.pdf")
    render_pdf(cover_html, cov, cover_only=True)
    out = os.path.join(work, "downloads", "Participant_Handbook.pdf")
    subprocess.run(["pdfunite", cov, tmp, out], check=True)
    for f in (cover_html, body_html, tmp, cov):
        os.remove(f)
    total = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout).group(1))
    return out, total, nums
