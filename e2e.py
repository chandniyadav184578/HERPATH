# Optional end-to-end test (Playwright + OpenCV): pip install playwright opencv-python-headless && playwright install chromium && python3 tests/e2e.py
import os,re,tempfile
T=tempfile.gettempdir()
from playwright.sync_api import sync_playwright
U='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','index.html'));errs=[];res=[]
def ok(n,c):res.append((n,bool(c)));print(('PASS ' if c else 'FAIL ')+n)
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':1280,'height':900});pg=ctx.new_page()
    pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda x:errs.append('PAGEERR '+str(x)))
    C=lambda s:(pg.click(s),pg.wait_for_timeout(250))
    pg.goto(U);pg.wait_for_selector('.hero')
    ok('fresh visit is dark',pg.evaluate("document.documentElement.dataset.theme")=='dark')
    C('[data-w=set]');ok('settings dialog opens',pg.locator('dialog[open] .themes').count()==1)
    C('dialog [data-v=light]');ok('light applies',pg.evaluate("document.documentElement.dataset.theme")=='light')
    C('dialog [data-v=hi]');ok('dialog reopened after language switch',pg.locator('dialog[open] .themes').count()==1)
    ok('theme kept after language switch',pg.evaluate("document.documentElement.dataset.theme")=='light')
    ok('hindi nav',pg.locator('.nav').inner_text().find('होम')>=0)
    pg.keyboard.press('Escape');pg.reload();pg.wait_for_selector('.hero')
    ok('persist theme+lang',pg.evaluate("[document.documentElement.dataset.theme,document.documentElement.lang]")==['light','hi'])
    C('[data-w=set]');C('dialog [data-v=en]');C('dialog [data-v=dark]');pg.keyboard.press('Escape')
    ok('independent switching',pg.evaluate("[document.documentElement.dataset.theme,JSON.parse(localStorage.herpath_v1).set.lang]")==['dark','en'])
    pg.click('.hero a.btn.p');pg.click('button[data-m=private]');pg.wait_for_selector('#view')
    ok('chip rewritten','demo' not in pg.locator('.chipmode').inner_text().lower())
    pg.goto(U+'#/app/passport');pg.wait_for_selector('.pcover')
    ok('passport cover shown, no records exposed',pg.locator('.paper').count()==0 and pg.locator('.pc-chip').first.inner_text().find('Passcode not set')>=0)
    pg.screenshot(path=T+'/s_cover_dark.png')
    C('.pc-act [data-a=paview]');pg.fill('#pa1','abc');pg.fill('#pa2','abc');C('dialog button[type=submit]');ok('short passcode rejected',pg.locator('#paerr').inner_text()!='')
    pg.fill('#pa1','secret1');pg.fill('#pa2','secret1');C('dialog button[type=submit]');pg.wait_for_timeout(800)
    ok('passcode set -> builder opens',pg.locator('.paper').count()==1)
    C('[data-a=palock]');ok('lock returns to cover',pg.locator('.pcover').count()==1 and pg.locator('.paper').count()==0)
    C('.pc-act [data-a=paview]');pg.fill('#pa1','wrong');C('dialog button[type=submit]');pg.wait_for_timeout(600);ok('wrong passcode denied',pg.locator('#paerr').inner_text().find('isn’t correct')>=0 and pg.locator('.paper').count()==0)
    pg.fill('#pa1','secret1');C('dialog button[type=submit]');pg.wait_for_timeout(800);ok('correct passcode unlocks',pg.locator('.paper').count()==1)
    pg.screenshot(path=T+'/s_open.png');C('[data-a=palock]')
    # QR payload
    svg=pg.locator('.pc-qr svg').evaluate("e=>e.outerHTML");url=pg.evaluate("location.href.split('#')[0]")
    pg.screenshot(path=T+'/s_cover_dark.png')
    p2=ctx.new_page();p2.set_content('<body style="margin:0;background:#fff">'+svg.replace('class="qr"','width="700" height="700"')+'</body>');p2.screenshot(path=T+'/qr.png');p2.close()
    import cv2;img=cv2.imread(T+'/qr.png');txt=''
    for fx in (1,1.5,2,3):
        im=cv2.copyMakeBorder(cv2.resize(img,None,fx=fx,fy=fx,interpolation=cv2.INTER_NEAREST),40,40,40,40,cv2.BORDER_CONSTANT,value=(255,255,255))
        txt,_,_=cv2.QRCodeDetector().detectAndDecode(im)
        if txt:break;print('QR payload:',txt)
    ok('QR decodes to access URL with opaque token',bool(re.search(r'#/access/[A-Za-z0-9_-]{24}$',txt)))
    store=pg.evaluate("localStorage.herpath_v1");ok('QR holds no personal data',all(w not in txt for w in['Pain','symptom','allerg','name']))
    # gate
    tok=txt.split('/access/')[1]
    pg.goto(U+'#/access/'+'x'*24);pg.wait_for_selector('.gate');ok('invalid code state',pg.locator('.gate h2').inner_text().find('isn’t valid')>=0)
    pg.goto(U+'#/access/'+tok);pg.wait_for_selector('.gate');ok('consent state, no data shown',pg.locator('.gate h2').inner_text()=='Access request' and pg.locator('.paper').count()==0)
    pg.fill('#gpw','nope');C('[data-f=paapprove] button[type=submit]');pg.wait_for_timeout(500);ok('bad approval denied',pg.locator('#gerr').inner_text()!='' and pg.locator('.paper').count()==0)
    pg.fill('#gpw','secret1');pg.select_option('#gdur','5');C('[data-f=paapprove] button[type=submit]');pg.wait_for_timeout(900)
    ok('approved shows read-only passport + timer',pg.locator('.gate .paper').count()==1 and 'left' in pg.locator('#gcount').inner_text())
    pg.screenshot(path=T+'/s_gate.png')
    pg.evaluate("GRANT.exp=Date.now()+1500");pg.wait_for_timeout(3000);ok('expired state',pg.locator('.gate h2').inner_text()=='Access expired')
    C('[data-a=gaterefresh]');pg.fill('#gpw','secret1');C('[data-f=paapprove] button[type=submit]');pg.wait_for_timeout(800);C('[data-a=gateend]');ok('end access works',pg.locator('.gate h2').inner_text()=='Access request')
    # scanner modal
    pg.goto(U+'#/app/passport');pg.wait_for_selector('.pcover');C('.pc-act [data-a=pasecure]');C('[data-a=pascan]');pg.screenshot(path=T+'/s_scan.png')
    C('[data-a=pacam]');ok('camera unsupported/denied message shown, no crash',pg.locator('#scanmsg').inner_text()!='')
    pg.fill('#pam','garbage');pg.press('#pam','Enter');pg.wait_for_timeout(300);ok('manual invalid code',pg.locator('#pamerr').inner_text()!='')
    pg.fill('#pam',url+'#/access/'+tok);pg.press('#pam','Enter');pg.wait_for_timeout(500);ok('manual code opens gate',pg.locator('.gate h2').inner_text()=='Access request')
    # replace code revokes
    pg.goto(U+'#/app/passport');pg.wait_for_selector('.pcover');C('.pc-act [data-a=pasecure]');C('[data-a=paregen]');C('dialog [data-a=myes]');pg.wait_for_timeout(300)
    pg.goto(U+'#/access/'+tok);pg.wait_for_selector('.gate');ok('old code revoked after replace',pg.locator('.gate h2').inner_text().find('isn’t valid')>=0)
    # light theme + mobile
    pg.goto(U+'#/app/passport');pg.evaluate("S.set.theme='light';save();applyPrefs()");pg.wait_for_timeout(300);pg.screenshot(path=T+'/s_cover_light.png')
    pg.set_viewport_size({'width':390,'height':800});pg.wait_for_timeout(300);pg.screenshot(path=T+'/s_cover_mobile.png',full_page=True)
    ok('no horizontal overflow on mobile',pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1"))
    for v in['overview','timeline','log','patterns','prep','library','settings','profile','notifications']:
        pg.goto(U+'#/app/'+v);pg.wait_for_timeout(250);ok('view '+v,pg.locator('#view').inner_text().strip()!='')
    b.close()
print('JS errors:',errs);print(sum(1 for _,c in res if c),'/',len(res),'passed')
