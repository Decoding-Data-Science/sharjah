import os
from playwright.sync_api import sync_playwright
SITE=os.path.abspath("../site"); out=os.path.abspath("../shots/v2"); os.makedirs(out,exist_ok=True)
import http.server, threading, socketserver, functools
H=functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
H=functools.partial(Q, directory=SITE)
srv=socketserver.TCPServer(("127.0.0.1",8771),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
msgs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    def open_(path,w=1280):
        pg=b.new_page(viewport={"width":w,"height":900})
        pg.on("pageerror",lambda e:msgs.append((path,str(e))))
        pg.on("console",lambda m: msgs.append((path,m.text)) if m.type=="error" else None)
        pg.goto("http://127.0.0.1:8771/"+path); pg.wait_for_timeout(600)
        pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        return pg
    pg=open_("index.html"); pg.wait_for_timeout(1500); pg.screenshot(path=out+"/index_top.png"); 
    pg.locator("#days").scroll_into_view_if_needed(); pg.wait_for_timeout(800)
    pg.evaluate("document.querySelectorAll('svg[data-play]').forEach(s=>{s.unpauseAnimations();s.setCurrentTime(2.4)})"); pg.wait_for_timeout(300)
    pg.locator("section:has(#days)").screenshot(path=out+"/index_days.png")
    pg.close()
    pg=open_("day-1.html")
    # prompt builder
    pg.locator("#pb").scroll_into_view_if_needed(); pg.click("[data-pb=vague]"); pg.wait_for_timeout(200)
    pg.locator("#pb").screenshot(path=out+"/pb_vague.png")
    pg.click("[data-pb=full]"); pg.locator("#pb").screenshot(path=out+"/pb_full.png")
    pg.locator("#rs").scroll_into_view_if_needed(); pg.locator("#rs").screenshot(path=out+"/rs_off.png")
    pg.check("#rs_filter"); pg.wait_for_timeout(400); pg.locator("#rs").screenshot(path=out+"/rs_on.png")
    pg.locator("details.q").first.scroll_into_view_if_needed()
    pg.locator("details.q").first.click(); pg.locator(".qbox").last.screenshot(path=out+"/qa.png")
    pg.close()
    pg=open_("models.html"); pg.locator("#mc").scroll_into_view_if_needed(); pg.select_option("#mc_task","agent"); pg.locator("#mc").screenshot(path=out+"/mc.png"); pg.close()
    pg=open_("handbook.html"); pg.wait_for_timeout(800); pg.screenshot(path=out+"/handbook.png",full_page=False); pg.close()
    pg=open_("day-2.html"); pg.evaluate("document.querySelectorAll('svg[data-play]').forEach(s=>{s.unpauseAnimations();s.setCurrentTime(1.7)})"); pg.locator("section:has(#lab5)").locator("svg").first.screenshot(path=out+"/agent_anim.png"); pg.close()
    b.close()
print(msgs)
