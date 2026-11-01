import sys, os
from playwright.sync_api import sync_playwright
SITE = os.path.abspath("../site")
out = os.path.abspath("../shots"); os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    # handout pdf
    pg = b.new_page()
    pg.goto("file://%s/handout.html" % SITE)
    pg.wait_for_timeout(500)
    foot = '<div style="font:7pt Inter,Arial,sans-serif;color:#566577;width:100%;padding:0 13mm;display:flex;justify-content:space-between"><span>Data and AI with Gemini | Corporate Workshop | 2 to 4 November 2026 | All data and documents are fictional</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>'
    pg.pdf(path=os.path.join(SITE, "downloads", "Workshop_Handout.pdf"), format="A4", print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template="<span></span>", footer_template=foot)
    pg.close()
    # screenshots
    for name, w, full in [("index",1280,False),("day-1",1280,False),("models",1280,False),("tokens",1280,False),("security",1280,False),("downloads",1280,False),("use-case",1280,False),("index",390,False)]:
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto("file://%s/%s.html" % (SITE, name))
        pg.wait_for_timeout(800)
        # reveal everything for screenshot
        pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(out, "%s_%d.png" % (name, w)), full_page=full)
        errs = []
        pg.close()
    b.close()
print("ok")
