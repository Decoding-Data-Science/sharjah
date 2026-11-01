import os
from playwright.sync_api import sync_playwright
SITE=os.path.abspath("../site"); out=os.path.abspath("../shots")
jobs=[("tokens","#calculator",1280),("models","#gemini",1280),("models","#which",1280),("day-1","#lab1",1280),("security","#keys",1280),("downloads","#before",1280),("day-2","#lab5",1280),("use-case","#read-first",1280)]
with sync_playwright() as p:
    b=p.chromium.launch()
    msgs=[]
    for name,sel,w in jobs:
        pg=b.new_page(viewport={"width":w,"height":900})
        pg.on("console", lambda m: msgs.append((name,m.type,m.text)) if m.type in("error","warning") else None)
        pg.on("pageerror", lambda e: msgs.append((name,"pageerror",str(e))))
        pg.goto("file://%s/%s.html"%(SITE,name)); pg.wait_for_timeout(500)
        pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))"); pg.wait_for_timeout(700)
        el=pg.locator("section:has(%s)"%sel).first
        el.screenshot(path=os.path.join(out,"%s_%s.png"%(name,sel.strip('#'))))
        pg.close()
    b.close()
print(msgs)
