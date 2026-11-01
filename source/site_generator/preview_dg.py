import os, sys
sys.path.insert(0, os.getcwd())
import diagrams
from playwright.sync_api import sync_playwright
diagrams.ANIM = False
names = list(diagrams.ALL.keys())
html = "<html><body style='margin:0;background:#222'>" + "".join(f"<div id='{n}' style='width:960px;margin:10px'>{diagrams.ALL[n]()}</div>" for n in names) + "</body></html>"
open("/home/claude/work/shots/dg.html","w").write(html)
out="/home/claude/work/shots/dg"; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1000,"height":800}); pg.goto("file:///home/claude/work/shots/dg.html")
    for n in names:
        pg.locator("#"+n).screenshot(path=f"{out}/{n}.png")
    b.close()
print(names)
