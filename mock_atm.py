"""Approach-to-Market card — how a competitor reaches and sells to our buyer."""
import json, asyncio, pathlib, re
from playwright.async_api import async_playwright

C = {c['id']: c for c in json.load(open('data/competitors.json'))}
HEARD = json.load(open('data/heard.json'))['competitors']
PATH = json.load(open('data/pathways.json'))['pathways']
ROLES = {r['id']: r for r in json.load(open('data/roles.json'))['roles']}
SEG = json.load(open('data/segments.json'))

SUBJECTS = ['realpage-realconnect', 'grow-by-inhabit']

NAVY, RED, CER, CHAR, LINE, BG = '#262262', '#D31417', '#03B8EC', '#393A3C', '#E4E4EE', '#F7F7FB'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

def esc(s):
    return str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def clip(s, n):
    s = str(s or '').strip()
    if len(s) <= n: return s
    return s[:n].rsplit(' ', 1)[0].rstrip(' ,.;:—-') + '…'

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:%(F)s;color:%(CHAR)s;font-size:8.4pt;line-height:1.4;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{page-break-after:always}.pg:last-child{page-break-after:auto}
.title{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:3px}
.title h1{font-size:16pt;color:%(NAVY)s;letter-spacing:-.3px}
.sub{color:#6B6B72;font-size:7.4pt;margin-bottom:11px}
.kind{display:inline-block;background:%(RED)s;color:#fff;font-size:6.6pt;font-weight:700;
      letter-spacing:.1em;text-transform:uppercase;padding:3px 9px;border-radius:3px}
.sec{margin-bottom:9px;border:1px solid %(LINE)s;border-radius:5px;overflow:hidden}
.sec>h2{background:%(NAVY)s;color:#fff;font-size:8pt;font-weight:700;letter-spacing:.13em;
        text-transform:uppercase;text-align:center;padding:5px 8px}
.sec.gap>h2{background:#8A8A96}
.body{padding:9px 11px}
.two{display:grid;grid-template-columns:1fr 1fr}
.two>div{padding:9px 11px}.two>div:first-child{border-right:1px solid %(LINE)s}
.ch{font-size:7.2pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
    text-align:center;padding-bottom:5px;margin-bottom:6px;border-bottom:1px solid %(LINE)s;color:%(NAVY)s}
.row{display:grid;grid-template-columns:132px 1fr;gap:3px 10px}
.row b{color:%(NAVY)s}
ul{padding-left:14px}li{margin-bottom:3px}
.tick li{list-style:none;position:relative;padding-left:15px}
.tick li:before{content:'';position:absolute;left:0;top:4px;width:9px;height:9px;border-radius:50%%;background:%(NAVY)s}
.chip{display:inline-block;font-size:6.6pt;font-weight:700;text-transform:uppercase;letter-spacing:.05em;
      padding:2px 7px;border-radius:3px;background:#E7E7F2;color:%(NAVY)s;margin:0 4px 4px 0}
.chip.hi{background:%(NAVY)s;color:#fff}
.act{background:#FFF6F6;border-left:3px solid %(RED)s;padding:8px 11px;margin-top:2px}
.miss{color:#6B6B72}
.foot{font-size:6.4pt;color:#8A8A96;border-top:1px solid %(LINE)s;padding-top:5px;margin-top:7px}
.note{font-size:7pt;color:#8A8A96;margin-top:5px}
""" % dict(F=FONT, NAVY=NAVY, RED=RED, CHAR=CHAR, LINE=LINE, BG=BG)

def sec(title, inner, two=False, gap=False):
    return '<div class="sec%s"><h2>%s</h2>%s</div>' % (
        ' gap' if gap else '', title, inner if two else '<div class="body">%s</div>' % inner)

# --- derivations -------------------------------------------------------------
MOTION_HINTS = [
    (r'installed platform base|inside an installed|existing .* clients it is an add-on|single sign-on across',
     'Rides an existing platform relationship — an add-on, not a new procurement.'),
    (r'SCORM format for one-time purchase|delivery inside a client', 'Sells content into the LMS they already run — low-commitment entry point.'),
    (r'[Bb]undleable|bundle with partner|discounting lever', 'Bundled with sibling products, giving the parent a discounting lever.'),
    (r'a la carte|per[- ]course|individual courses', 'A la carte course purchase alongside subscription.'),
    (r'self[- ]serve|per month|\$\d+', 'Published price and self-serve entry.'),
    (r'free|included at no', 'Given away or included to block a paid vendor.'),
]

def motions(c):
    blob = ' '.join([(c.get('pricing') or {}).get('value') or ''] +
                    [s['text'] for s in (c.get('strengths') or [])] +
                    [g['text'] for g in (c.get('gaps') or [])])
    out = []
    for pat, label in MOTION_HINTS:
        if re.search(pat, blob) and label not in out:
            out.append(label)
    return out

def who(c):
    mine = {o['product'] for o in (c.get('overlaps') or []) if o.get('degree') != 'None'}
    hits = [p for p in PATH if any(o in mine for o in (p.get('overlaps') or []))]
    roles, ways = [], []
    for p in hits:
        ways.append(p['name'])
        for rid in (p.get('roles') or []):
            if rid in ROLES and ROLES[rid]['name'] not in roles:
                roles.append(ROLES[rid]['name'])
    return roles, ways

def card(c):
    hd = HEARD.get(c['id'])
    roles, ways = who(c)
    pr = (c.get('pricing') or {}).get('value') or 'Not published.'
    mo = motions(c)
    posture = (hd or {}).get('posture')

    reach = '<div class="row">'
    reach += '<b>Owned by</b><div>%s</div>' % esc(c.get('parent') or 'Independent')
    reach += '<b>What they sell</b><div>%s</div>' % esc(c.get('toolCategory'))
    reach += '<b>Their claim</b><div>%s</div>' % esc(clip((c.get('positioning') or {}).get('value'), 190))
    reach += '<b>How they price</b><div>%s</div>' % esc(clip(pr, 210))
    reach += '</div>'

    sell = ('<ul class="tick">%s</ul>' % ''.join('<li>%s</li>' % esc(m) for m in mo)) if mo else \
           '<div class="miss">No distribution or pricing motion recorded yet.</div>'

    targ = ('<div class="two" style="border:0"><div style="border-right:1px solid %s">'
            '<div class="ch">Departments they reach</div>%s</div>'
            '<div><div class="ch">Budget line they compete for</div>%s</div></div>') % (
        LINE,
        ''.join('<span class="chip hi">%s</span>' % esc(r) for r in roles) or '<span class="miss">—</span>',
        ''.join('<span class="chip">%s</span>' % esc(w) for w in ways) or '<span class="miss">—</span>')

    inmkt = ('<div><strong>Named in %d open deal%s.</strong> %s %s</div>' % (
        hd['deals'], '' if hd['deals'] == 1 else 's', esc(posture or ''), esc(hd['whatBuyersSay'][0]))
        + ('<div class="note">%s</div>' % esc(hd.get('pricingSignal')) if hd.get('pricingSignal') else '')) if hd else \
        '<div class="miss">Not named in an open deal this month, so no live read on how they are selling.</div>'

    act = '<div class="act">%s</div>' % esc(
        (hd or {}).get('useIt') or (c.get('verdict') or {}).get('doInstead') or (c.get('verdict') or {}).get('line'))

    missing = []
    if not any(k in (c.get('toolCategory') or '').lower() for k in ['multifamily', 'property']):
        missing.append('Target verticals beyond multifamily — not recorded.')
    missing += ['Named clients and logos they lead with — not tracked, by policy and by gap.',
                'Formal channel or reseller partners — not recorded.',
                'Sales motion detail: pilots, proofs of concept, free trials, discount patterns — not recorded.']

    return '<div class="pg">' + \
        ('<div class="title"><h1>%s</h1><span class="kind">Approach to market</span></div>'
         '<div class="sub">How they reach our buyer &middot; %s</div>') % (esc(c['name']), esc(c.get('play'))) + \
        sec('How they reach the buyer', reach) + \
        sec('How they sell', sell) + \
        sec('Who they target', targ, two=True) + \
        sec('What we see in live deals', inmkt) + \
        sec('So do this', act) + \
        sec('Not yet researched', '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(m) for m in missing) +
            '<div class="note">These are the fields an Approach-to-Market card wants that the database does not yet carry. '
            'Add them to the weekly sweep and this section shrinks.</div>', gap=True) + \
        ('<div class="foot">Grace Hill Competitive Intelligence &middot; reviewed %s &middot; full record at ci-gracehill.com</div>' %
         esc((c.get('health') or {}).get('lastFullReview', '—'))) + \
        '</div>'

async def main():
    body = ''.join(card(C[i]) for i in SUBJECTS)
    html = "<!doctype html><meta charset='utf-8'><style>@page{size:letter;margin:11mm}%s</style>%s" % (CSS, body)
    pathlib.Path('/tmp/atm.html').write_text(html, encoding='utf-8')
    out = 'Battlecard-Approach-to-Market.pdf'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file:///tmp/atm.html'); await pg.wait_for_timeout(250)
        await pg.pdf(path=out, format='Letter', print_background=True)
        from pypdf import PdfReader
        print('%s: %d pages, errors=%s' % (out, len(PdfReader(out).pages), errs))
        await b.close()

asyncio.run(main())
