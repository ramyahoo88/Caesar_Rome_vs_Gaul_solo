"""Real-browser test of the shipped Directive helper (print/Caesar_Solo_Deck.html).

Usage: python3 helper_browser.py REPO OUT_DIR

Runs the unmodified page in headless Google Chrome through Playwright, with the
browser's own localStorage (a persistent profile, so it survives a full browser
restart). Writes OUT_DIR/helper-browser.json and screenshots.
"""
import json, os, re, shutil, sys, tempfile
from playwright.sync_api import sync_playwright

REPO, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
URL = 'file://' + os.path.join(os.path.abspath(REPO), 'print', 'Caesar_Solo_Deck.html')
KEY = 'caesarSoloDeck2'
CHROME = '/usr/bin/google-chrome'
results, errors = [], []


def check(name, ok, detail=''):
    results.append({'check': name, 'pass': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail)


def state(pg):
    return pg.evaluate(f"()=>JSON.parse(localStorage.getItem('{KEY}'))")


def watch(pg):
    pg.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: errors.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)


def fresh(pg):
    pg.evaluate('()=>localStorage.clear()')
    pg.reload()
    pg.click('#reset')


def no_overflow(pg):
    return pg.evaluate('()=>document.documentElement.scrollWidth<=window.innerWidth')


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])

    # ---------------- desktop
    ctx = b.new_context(viewport={'width': 1000, 'height': 1250})
    pg = ctx.new_page(); watch(pg)
    pg.goto(URL); fresh(pg)
    check('loads with Imperator, turn 1, play 0',
          pg.inner_text('#title') == 'Imperator' and pg.inner_text('#turn') == '1' and pg.inner_text('#play') == '0')
    check('desktop: no horizontal overflow', no_overflow(pg))

    # full deck cycle and reshuffle
    seen = []
    for k in range(9):
        pg.click('#draw'); seen.append(state(pg)['cur']['i'])
    check('9 draws show all 9 Imperator Directives once', sorted(seen) == list(range(9)), str(seen))
    check('empty deck says it reshuffles', 'reshuffles' in pg.inner_text('#left'), pg.inner_text('#left'))
    check('history lists 9 plays', pg.inner_text('#hist').count('(') == 9)
    pg.click('#draw')
    check('10th draw reshuffles a fresh deck (8 left, play 10)',
          pg.inner_text('#left') == '8 left' and pg.inner_text('#play') == '10', pg.inner_text('#left'))
    card = pg.inner_text('#cardbox')
    i = state(pg)['cur']['i']
    check('card face shows ID, compass and before/after reminder',
          re.search(r'I-\d', card) and 'Ties go to the compass' in card and 'CONTINUE' in card, card[:80])
    pg.wait_for_timeout(700)
    check('card flip finishes flat and opaque',
          pg.evaluate("()=>{const c=getComputedStyle(document.querySelector('#cardbox .card'));return c.transform==='none'&&c.opacity==='1'}"))
    pg.screenshot(path=os.path.join(OUT, 'helper-desktop-imperator.png'), full_page=True)

    # reload keeps everything
    before = state(pg); pg.reload(); after = state(pg)
    check('reload restores the exact saved state', before == after)
    check('reload shows the same card and counters',
          pg.inner_text('#play') == '10' and pg.inner_text('#cardbox') == card)

    # separate side counters
    pg.click('#bG')
    check('Concilium has its own counter (0) and its own deck',
          pg.inner_text('#title') == 'Concilium' and pg.inner_text('#play') == '0' and pg.inner_text('#left') == '9 left')
    pg.click('#draw'); pg.click('#draw')
    gcard = pg.inner_text('#cardbox')
    check('Concilium card shows a C- ID and the AGITATE reminder', re.search(r'C-\d', gcard) and 'AGITATE' in gcard)
    pg.wait_for_timeout(700)
    pg.screenshot(path=os.path.join(OUT, 'helper-desktop-concilium.png'), full_page=True)
    pg.click('#bR')
    check('switching back keeps Imperator at 10 plays', pg.inner_text('#play') == '10')

    # undo a draw
    left0 = pg.inner_text('#left'); pg.click('#draw'); pg.click('#undo')
    check('Undo of a draw restores deck and counter', pg.inner_text('#left') == left0 and pg.inner_text('#play') == '10')

    # next turn up to 6, undo across a turn
    for t in range(5):
        pg.click('#next')
    check('turn 6 reached; Next turn disabled and labelled Last turn',
          pg.inner_text('#turn') == '6' and pg.is_disabled('#next') and pg.inner_text('#next') == 'Last turn')
    check('new turn clears counters and history', pg.inner_text('#play') == '0' and pg.inner_text('#hist') == '')
    for t in range(5):
        pg.click('#undo')
    check('Undo across five turns returns to turn 1 with its 10 plays and history',
          pg.inner_text('#turn') == '1' and pg.inner_text('#play') == '10' and pg.inner_text('#hist').count('(') == 10)

    # level texts and bonus boundaries
    lv_ok = True
    for side in ('R', 'G'):
        pg.click('#b' + side)
        for lv in range(1, 6):
            pg.select_option('#lvl', str(lv))
            lv_ok &= pg.inner_text('#lvltxt').startswith(f'Level {lv}:') and state(pg)['lvl'][side] == lv
    check('all 10 level selections save and display', lv_ok)

    def bonus_run(side, lv):
        fresh(pg); pg.click('#b' + side); pg.select_option('#lvl', str(lv))
        out = []
        for n in range(6):
            pg.click('#draw'); out.append('+1 AP' in pg.inner_text('#bonus'))
        return out
    check('Imperator L2: +1 AP on plays 1-4 only', bonus_run('R', 2) == [True] * 4 + [False] * 2)
    check('Imperator L1: never a bonus', bonus_run('R', 1) == [False] * 6)
    check('Imperator L3-5: bonus on every play', all(bonus_run('R', l) == [True] * 6 for l in (3, 4, 5)))
    check('Concilium L5: +1 AP on plays 1-4 only', bonus_run('G', 5) == [True] * 4 + [False] * 2)
    check('Concilium L1-4: never a bonus', all(bonus_run('G', l) == [False] * 6 for l in (1, 2, 3, 4)))

    # keyboard
    fresh(pg)
    order = []
    pg.locator('body').focus()
    for k in range(25):
        pg.keyboard.press('Tab'); order.append(pg.evaluate('()=>document.activeElement.id||document.activeElement.tagName'))
    check('Tab reaches side buttons, level, Draw, Undo, Next turn and Reset',
          all(x in order for x in ('bR', 'bG', 'lvl', 'draw', 'next', 'reset')), str(order))
    pg.focus('#draw'); pg.keyboard.press('Enter'); pg.keyboard.press('Space')
    check('Enter and Space on Draw each draw a card', pg.inner_text('#play') == '2')

    # damaged saved session
    pg.evaluate(f"()=>localStorage.setItem('{KEY}','{{not json')"); pg.reload()
    check('damaged session: notice shown, new game started, damaged copy kept',
          'could not be restored' in pg.inner_text('#notice') and pg.is_visible('#noticebox')
          and pg.inner_text('#turn') == '1' and pg.evaluate(f"()=>localStorage.getItem('{KEY}-damaged')") == '{not json')
    pg.click('#dismiss')
    check('Dismiss hides the notice', not pg.is_visible('#noticebox'))

    # damaged Undo history
    okprev = json.dumps({'side': 'G', 'lvl': {'R': 3, 'G': 2}, 'turn': 2, 'play': {'R': 1, 'G': 0},
                         'deck': {'R': [1, 2], 'G': [3]}, 'cur': None, 'hist': []})
    good = {'side': 'R', 'lvl': {'R': 3, 'G': 3}, 'turn': 3, 'play': {'R': 0, 'G': 0},
            'deck': {'R': list(range(9)), 'G': list(range(9))}, 'cur': None, 'hist': [], 'prev': [okprev, 'not JSON']}
    pg.evaluate("([k,v])=>localStorage.setItem(k,v)", [KEY, json.dumps(good)]); pg.reload()
    check('damaged Undo history: game restored, bad step dropped, notice shown',
          pg.inner_text('#turn') == '3' and 'Undo history was damaged' in pg.inner_text('#notice') and len(state(pg)['prev']) == 1)
    pg.click('#undo')
    check('Undo then reaches the surviving snapshot',
          pg.inner_text('#title') == 'Concilium' and pg.inner_text('#turn') == '2' and pg.is_disabled('#undo'))
    ctx.close()

    # reduced motion turns the flip off
    ctx = b.new_context(reduced_motion='reduce'); pg = ctx.new_page(); watch(pg); pg.goto(URL); pg.click('#draw')
    check('reduced motion: no flip animation',
          pg.evaluate("()=>getComputedStyle(document.querySelector('#cardbox .card')).animationName")=='none')
    ctx.close()

    # storage that refuses writes
    ctx = b.new_context()
    ctx.add_init_script("Storage.prototype.setItem=function(){throw new DOMException('QuotaExceededError','QuotaExceededError')}")
    pg = ctx.new_page(); watch(pg); pg.goto(URL)
    pg.click('#draw')
    check('storage refusing writes: page still works and warns',
          'not saving' in pg.inner_text('#notice') and pg.inner_text('#play') == '1')
    ctx.close()

    # shuffle sanity: first card after Reset over 180 resets
    ctx = b.new_context(); pg = ctx.new_page(); watch(pg); pg.goto(URL)
    counts = [0] * 9
    for k in range(180):
        pg.click('#reset'); pg.click('#draw'); counts[state(pg)['cur']['i']] += 1
    check('180 resets: every Directive appears as the first card', min(counts) > 0, str(counts))
    ctx.close()

    # phone viewport
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page(); watch(pg); pg.goto(URL)
    pg.tap('#draw')
    check('phone: tap draws; no horizontal overflow', pg.inner_text('#play') == '1' and no_overflow(pg))
    boxes = pg.evaluate("""()=>['draw','undo','next','reset','bR','bG'].map(id=>{const r=document.getElementById(id).getBoundingClientRect();return [id,r.width,r.height]})""")
    check('phone: main buttons at least 40 px tall', all(h >= 40 for _, w, h in boxes), str(boxes))
    pg.wait_for_timeout(700)
    pg.screenshot(path=os.path.join(OUT, 'helper-phone.png'), full_page=True)
    ctx.close()
    b.close()

    # real persistent storage across a full browser restart
    prof = tempfile.mkdtemp()
    ctx = p.chromium.launch_persistent_context(prof, executable_path=CHROME, args=['--no-sandbox'])
    pg = ctx.new_page(); watch(pg); pg.goto(URL)
    for k in range(3):
        pg.click('#draw')
    pg.click('#next'); pg.click('#bG'); pg.click('#draw')
    saved = state(pg); ctx.close()
    ctx = p.chromium.launch_persistent_context(prof, executable_path=CHROME, args=['--no-sandbox'])
    pg = ctx.new_page(); watch(pg); pg.goto(URL)
    check('browser restart: real localStorage restores the session',
          state(pg) == saved and pg.inner_text('#title') == 'Concilium' and pg.inner_text('#turn') == '2' and pg.inner_text('#play') == '1')
    pg.click('#undo')
    check('browser restart: Undo history survives', pg.inner_text('#play') == '0' and pg.inner_text('#turn') == '2')
    ctx.close(); shutil.rmtree(prof, ignore_errors=True)

check('no page errors or console errors/warnings in any run', not errors, '; '.join(errors[:5]))
res = {'url': URL, 'chrome': CHROME, 'checks': results,
       'passed': sum(r['pass'] for r in results), 'total': len(results), 'errors': errors}
json.dump(res, open(os.path.join(OUT, 'helper-browser.json'), 'w'), indent=1)
print(f"{res['passed']}/{res['total']} checks pass")
