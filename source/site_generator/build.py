"""Build the static site and the illustrated handbook into ../site"""
import os, shutil, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import diagrams as D
import common
import pages_a, pages_b, handout, book

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
PKG = "/home/claude/pkg"
RELEASE = os.path.join(HERE, "..", "release_later", "downloads")
os.makedirs(os.path.join(SITE, "downloads"), exist_ok=True)


def all_pages():
    return {
        "index.html": pages_a.index(),
        "day-1.html": pages_a.day1(),
        "day-2.html": pages_a.day2(),
        "day-3.html": pages_a.day3(),
        "use-case.html": pages_b.usecase(),
        "models.html": pages_b.models(),
        "setup.html": pages_b.setup(),
        "tokens.html": pages_b.tokens(),
        "security.html": pages_b.security(),
        "exercises.html": pages_b.exercises(),
        "glossary.html": pages_b.glossary(),
        "downloads.html": pages_b.downloads(),
    }


# ---- pass 1: static content for the handbook
D.ANIM = False
all_pages()
STATIC = dict(common.BODIES)
pdf, total, nums = book.make(STATIC, SITE)
print("handbook pages:", total, nums)

# thumbnails for the handbook page
thumb_dir = os.path.join(SITE, "assets", "hb")
shutil.rmtree(thumb_dir, ignore_errors=True)
os.makedirs(thumb_dir)
picks = [1, 2, 4, 9, 14, 20, 28, 34, 40]
picks = [p for p in picks if p <= total]
for p in picks:
    subprocess.run(["pdftoppm", "-r", "60", "-png", "-f", str(p), "-l", str(p), "-singlefile", pdf, os.path.join(thumb_dir, f"p{p:02d}")], check=True)

# ---- pass 2: the live site
D.ANIM = True
pages = all_pages()
pages["handbook.html"] = pages_b.handbook_page(total, picks, nums)
pages["handout.html"] = handout.build()
for name, content in pages.items():
    with open(os.path.join(SITE, name), "w", encoding="utf-8") as f:
        f.write(content)
with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
    f.write(common.page("404.html", "Page not found", "Page not found.",
        '<section><div class="wrap"><h1>Page not found</h1><p class="lede">That page does not exist. <a href="index.html">Return to the home page</a>.</p></div></section>'))
open(os.path.join(SITE, ".nojekyll"), "w").close()

# ---- downloads
os.makedirs(RELEASE, exist_ok=True)
now = {
    "Students_All_Days/Airport_Workshop_Participant_Pack.zip": "Airport_Workshop_Participant_Pack.zip",
    "Students_All_Days/Airport_Copilot_Workbook.xlsx": "Airport_Copilot_Workbook.xlsx",
    "Students_All_Days/Copilot_Prompt_Pack_Participant.pdf": "Copilot_Prompt_Pack_Participant.pdf",
    "Day_1/Students/Participant_Guide_Day1.pdf": "Participant_Guide_Day1.pdf",
    "Day_1/Students/Day1_Explore_and_Ask_Slides.pdf": "Day1_Explore_and_Ask_Slides.pdf",
    "Day_1/Students/Day1_Notebooks.zip": "Day1_Notebooks.zip",
}
later = {
    "Day_2/Students/Participant_Guide_Day2.pdf": "Participant_Guide_Day2.pdf",
    "Day_2/Students/Day2_Build_the_Analyst_Slides.pdf": "Day2_Build_the_Analyst_Slides.pdf",
    "Day_2/Students/Day2_Notebooks.zip": "Day2_Notebooks.zip",
    "Day_3/Students/Participant_Guide_Day3.pdf": "Participant_Guide_Day3.pdf",
    "Day_3/Students/Day3_Put_It_Together_Slides.pdf": "Day3_Put_It_Together_Slides.pdf",
    "Day_3/Students/Day3_Notebooks.zip": "Day3_Notebooks.zip",
}
for src, dst in now.items():
    shutil.copy(os.path.join(PKG, src), os.path.join(SITE, "downloads", dst))
for src, dst in later.items():
    shutil.copy(os.path.join(PKG, src), os.path.join(RELEASE, dst))
print("built", len(pages) + 1, "pages")
