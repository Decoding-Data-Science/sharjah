"""Shared template and helpers for the workshop site."""
import html

NAV = [
    ("index.html", "Home"),
    ("day-1.html", "Day 1"),
    ("day-2.html", "Day 2"),
    ("day-3.html", "Day 3"),
    ("use-case.html", "Use case"),
    ("models.html", "Models"),
    ("setup.html", "Setup"),
    ("tokens.html", "Tokens"),
    ("security.html", "Security"),
    ("exercises.html", "Exercises"),
    ("glossary.html", "Glossary"),
    ("handbook.html", "Handbook"),
    ("downloads.html", "Downloads"),
]

SITE = "Data and AI with Gemini"
BODIES = {}


def esc(s):
    return html.escape(s, quote=False)


def code(s, label=None):
    """A copyable code block. s is plain text (escaped here)."""
    lab = f'<span class="plabel">{esc(label)}</span>' if label else ""
    return f'{lab}<pre data-copy><code>{esc(s.strip(chr(10)))}</code></pre>'


def checks(group, items, prefix):
    """A saved checklist. items is a list of strings (HTML allowed)."""
    lis = "".join(
        f'<li><input type="checkbox" id="{prefix}{i}"><label for="{prefix}{i}">{t}</label></li>'
        for i, t in enumerate(items)
    )
    return (
        f'<div data-progress="{group}"><div class="small"><span class="ptxt"></span></div><div class="progress"><i></i></div></div>'
        f'<ul class="check" data-group="{group}">{lis}</ul>'
    )


def timeline(rows):
    """rows: (time, title, where, kind) kind in '', 'lab', 'brk'."""
    out = ['<div class="tl">']
    for t, title, where, kind in rows:
        cls = "row brk" if kind == "brk" else "row"
        ttl = f'<span class="lab">{title}</span>' if kind == "lab" else title
        out.append(f'<div class="{cls}"><span class="t">{t}</span><span>{ttl}</span><span class="w">{where}</span></div>')
    out.append("</div>")
    return "".join(out)


def steps(items):
    """items: (title, text)"""
    lis = "".join(f"<li><div><b>{t}</b><br>{d}</div></li>" for t, d in items)
    return f'<ol class="steps">{lis}</ol>'


def done(text):
    return f'<div class="done"><b>Done when</b>{text}</div>'


def callout(title, body, ice=False):
    return f'<div class="callout{" ice" if ice else ""}"><b class="t">{title}</b>{body}</div>'


def table(head, rows, raw=True):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def page(fname, title, desc, body, hero_html=None, prev=None, nxt=None):
    BODIES[fname] = body
    cur = ' aria-current="page"'
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (f, cur if f == fname else "", l) for f, l in NAV
    )
    pn = ""
    if prev or nxt:
        p = f'<a href="{prev[0]}"><small>Previous</small>{prev[1]}</a>' if prev else "<span></span>"
        n = f'<a class="n" href="{nxt[0]}"><small>Next</small>{nxt[1]}</a>' if nxt else "<span></span>"
        pn = f'<div class="prevnext">{p}{n}</div>'
    hero = hero_html or ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {SITE}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#06080c">
<script>document.documentElement.className+=' js'</script>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="top-in">
<a class="brand" href="index.html">Data and AI with <b>Gemini</b></a>
<nav class="main" aria-label="Site">{nav}</nav>
</div></header>
{hero}
<main id="main">
{body}
<div class="wrap">{pn}</div>
</main>
<footer><div class="wrap">
<div>{SITE} | Corporate Workshop | 2 to 4 November 2026<br>All airlines, people, data and documents in this workshop are fictional.</div>
<div>Instructor: Mohammad Arshad</div>
</div></footer>
<script src="assets/app.js"></script>
</body>
</html>
"""


def pagehero(eyebrow, h1, lede, extra=""):
    return f"""<div class="pagehero"><div class="wrap">
<span class="eyebrow">{eyebrow}</span>
<h1>{h1}</h1>
<p class="lede">{lede}</p>{extra}
<div class="toc" id="toc"><h4>On this page</h4><ul></ul></div>
</div></div>"""
