"""Four Klue-style battlecard types, banded-section design, one competitor."""
import json, asyncio, pathlib
from playwright.async_api import async_playwright

C = {c['id']: c for c in json.load(open('data/competitors.json'))}
HEARD = json.load(open('data/heard.json'))['competitors']
PATH = json.load(open('data/pathways.json'))['pathways']
FEAT = {f['id']: f for line in json.load(open('data/features.json'))['lines'] for f in line['features']}
FLINE = {f['id']: line['line'] for line in json.load(open('data/features.json'))['lines'] for f in line['features']}
GHB = json.load(open('data/gh-baseline.json'))

SUBJECT = 'yardi-aspire'

NAVY, RED, CER, CHAR, LINE, BG = '#262262', '#D31417', '#03B8EC', '#393A3C', '#E4E4EE', '#F7F7FB'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

def esc(s):
    return str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def dq(s):
    s = str(s or '').strip().strip('"').strip('“”')
    return '&ldquo;%s&rdquo;' % esc(s) if s else ''

# Proof points that carry no customer name — safe on a forwardable card.
PROOF = [
    ('7.3M', 'residents and prospects surveyed a year'),
    ('92%', 'on-time mystery shop completion'),
    ('800+', 'prewritten policies, forms and job descriptions'),
    ('110+', 'Spanish-language courses'),
    ('21-30 days', 'published implementation window'),
    ('35 years', 'of multifamily benchmarking history behind the Kingsley Index'),
]

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
.body{padding:9px 11px}
.two{display:grid;grid-template-columns:1fr 1fr}
.two>div{padding:9px 11px}.two>div:first-child{border-right:1px solid %(LINE)s}
.ch{font-size:7.2pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
    text-align:center;padding-bottom:5px;margin-bottom:6px;border-bottom:1px solid %(LINE)s}
.snap{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px 14px}
.snap b{color:%(NAVY)s}
ul{padding-left:14px}li{margin-bottom:3px}
.tick li{list-style:none;position:relative;padding-left:15px}
.tick li:before{content:'';position:absolute;left:0;top:4px;width:9px;height:9px;border-radius:50%%;background:%(NAVY)s}
.cross li:before{background:%(RED)s}
.q{font-style:italic;color:%(NAVY)s}
.qa{margin-bottom:8px}.qa:last-child{margin-bottom:0}
.qa .qq{font-weight:700;color:%(NAVY)s}
.qa .aa{margin-top:2px}
table{width:100%%;border-collapse:collapse}
th{background:%(BG)s;font-size:7pt;letter-spacing:.06em;text-transform:uppercase;text-align:left;
   padding:4px 7px;border-bottom:1px solid %(LINE)s;color:#6B6B72}
td{padding:4px 7px;border-bottom:1px solid #F0F0F5;vertical-align:top}
.pill{display:inline-block;font-size:6.4pt;font-weight:700;text-transform:uppercase;
      padding:2px 6px;border-radius:3px;letter-spacing:.05em}
.yes{background:%(NAVY)s;color:#fff}.no{background:%(RED)s;color:#fff}
.part{background:#E7E7F2;color:%(NAVY)s}.unk{background:#EFEFF3;color:#8A8A96}
.kpi{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.kpi .n{font-size:13pt;font-weight:700;color:%(NAVY)s;line-height:1.1}
.kpi .l{font-size:7pt;color:#6B6B72}
.foot{font-size:6.4pt;color:#8A8A96;border-top:1px solid %(LINE)s;padding-top:5px;margin-top:7px}
.note{font-size:7pt;color:#8A8A96;margin-top:5px}
""" % dict(F=FONT, NAVY=NAVY, RED=RED, CHAR=CHAR, LINE=LINE, BG=BG)

def sec(title, inner, two=False):
    return '<div class="sec"><h2>%s</h2>%s</div>' % (
        title, inner if two else '<div class="body">%s</div>' % inner)

def head(c, kind, tag):
    return ('<div class="title"><h1>%s</h1><span class="kind">%s</span></div>'
            '<div class="sub">%s &middot; %s</div>') % (esc(c['name']), esc(kind), tag, esc(c.get('toolCategory')))

def foot(c, extra=''):
    return ('<div class="foot">Grace Hill Competitive Intelligence &middot; reviewed %s &middot; '
            'full record at ci-gracehill.com%s</div>') % (
        esc((c.get('health') or {}).get('lastFullReview', '—')), extra)

def clip(s, n):
    s = str(s or '').strip()
    if len(s) <= n: return s
    cut = s[:n].rsplit(' ', 1)[0]
    return cut.rstrip(' ,.;:—-') + '…'

def snapshot(c):
    sn = c.get('snapshot') or {}
    got = [(k.title(), (sn.get(k) or {}).get('value')) for k in ['hq', 'founded', 'ownership', 'size', 'funding']]
    got = [(k, v) for k, v in got if v]
    pr = (c.get('pricing') or {}).get('value')
    cells = ''.join('<div><b>%s:</b> %s</div>' % (esc(k), esc(clip(v, 78))) for k, v in got)
    cells += '<div><b>Pricing:</b> %s</div>' % esc(clip(pr or 'Not published', 78))
    return '<div class="snap">%s</div>' % cells

def lists(c, n=3):
    s = ''.join('<li>%s</li>' % esc(x['text']) for x in (c.get('strengths') or [])[:n])
    g = ''.join('<li>%s</li>' % esc(x['text']) for x in (c.get('gaps') or [])[:n])
    return ('<div class="two"><div><div class="ch" style="color:%s">What is genuinely true</div>'
            '<ul class="tick">%s</ul></div>'
            '<div><div class="ch" style="color:%s">Where they stop</div>'
            '<ul class="tick cross">%s</ul></div></div>') % (NAVY, s or '<li>—</li>', RED, g or '<li>—</li>')

def objections(c, n=2):
    out = ''
    for o in (c.get('objections') or [])[:n]:
        out += '<div class="qa"><div class="qq">Q: %s</div><div class="aa">A: %s</div></div>' % (
            dq(o.get('objection')), esc(o.get('response')))
    return out or '<div style="color:#8A8A96">None recorded.</div>'

def traps(c, n=3):
    return '<ul class="q">%s</ul>' % (''.join('<li>%s</li>' % dq(x) for x in (c.get('askThis') or [])[:n]) or '<li>—</li>')

def positioning(c):
    theirs = (c.get('positioning') or {}).get('value') or '—'
    ours = ((c.get('whyWeWin') or ['—'])[0])
    return ('<div class="two"><div><div class="ch" style="color:%s">Their pitch</div>%s</div>'
            '<div><div class="ch" style="color:%s">Our counter</div>%s</div></div>') % (
        NAVY, esc(theirs), RED, esc(ours))

def matrix(c, only_diff=True, n=12):
    rows = ''
    for k, f in (c.get('features') or {}).items():
        if k not in FEAT: continue
        g = GHB.get(k) or {'support': 'Unknown'}
        if only_diff and g.get('support') == f.get('support'): continue
        cls = {'Yes': 'yes', 'No': 'no', 'Partial': 'part'}.get
        rows += ('<tr><td style="width:38%%"><strong>%s</strong><br><span style="color:#8A8A96;font-size:7pt">%s</span></td>'
                 '<td style="width:13%%"><span class="pill %s">%s</span></td>'
                 '<td style="width:13%%"><span class="pill %s">%s</span></td>'
                 '<td>%s</td></tr>') % (
            esc(FEAT[k].get('label')), esc(FLINE.get(k, '')),
            cls(g.get('support'), 'unk'), esc(g.get('support')),
            cls(f.get('support'), 'unk'), esc(f.get('support')),
            esc(clip(f.get('note'), 118)))
        n -= 1
        if n == 0: break
    return ('<table><thead><tr><th>Capability</th><th>Us</th><th>Them</th><th>What their source says</th></tr></thead>'
            '<tbody>%s</tbody></table>' % (rows or '<tr><td colspan=4>No differences recorded.</td></tr>'))

def hearing(c):
    hd = HEARD.get(c['id'])
    if not hd:
        return '<div style="color:#8A8A96">Not named in an open deal this month.</div>'
    return ('<div><strong>Named in %d open deal%s.</strong> %s</div>'
            '<div class="note">Aggregated from recorded calls. Patterns only, no accounts.</div>') % (
        hd['deals'], '' if hd['deals'] == 1 else 's', esc(hd['whatBuyersSay'][0]))

# ---------------- the four types ----------------
def buyer_lines(c, n=3):
    '''Actual buyer phrasing, from the outcome pathways this competitor plays in.'''
    mine = {o['product'] for o in (c.get('overlaps') or []) if o.get('degree') != 'None'}
    out = []
    for p in PATH:
        if any(o in mine for o in (p.get('overlaps') or [])):
            for h in (p.get('hearThis') or []):
                if h not in out: out.append(h)
    return out[:n]

def card_bdr(c):
    w = c.get('whenItComesUp') or {}
    return '<div class="pg">' + head(c, 'BDR card', 'Early calls &middot; qualify and route') + \
        sec('What you will hear from the buyer', '<ul class="q">%s</ul>' % (
            ''.join('<li>%s</li>' % dq(x) for x in buyer_lines(c)) or '<li>—</li>')) + \
        sec('Trap questions &mdash; ask before they name a vendor', traps(c, 3)) + \
        sec('Say this / never say', '<div class="two"><div><div class="ch" style="color:%s">Say this</div>%s</div>'
            '<div><div class="ch" style="color:%s">Never say</div><ul class="tick cross">%s</ul></div></div>' % (
                NAVY, esc(w.get('say')), RED,
                ''.join('<li>%s</li>' % esc(x) for x in (c.get('doNotSay') or [])[:2]) or '<li>—</li>'), two=True) + \
        sec('When to escalate', esc(w.get('redirect') or '—') +
            '<div class="note">If they are already in a formal evaluation, hand to the AE with the trap-question answers.</div>') + \
        foot(c) + '</div>'

def card_sales(c):
    return '<div class="pg">' + head(c, 'Sales card', 'Live deal &middot; the workhorse') + \
        sec('Competitor snapshot', snapshot(c)) + \
        sec('Positioning', positioning(c), two=True) + \
        sec('Strengths &amp; weaknesses', lists(c, 3), two=True) + \
        sec('Common objections', objections(c, 2)) + \
        sec('Trap questions', traps(c, 3)) + \
        sec('What we are hearing in deals', hearing(c)) + \
        foot(c) + '</div>'

def card_exec(c):
    v = c.get('verdict') or {}
    hd = HEARD.get(c['id'])
    k = ''.join('<div><div class="n">%s</div><div class="l">%s</div></div>' % (a, b) for a, b in PROOF[:3])
    return '<div class="pg">' + head(c, 'Executive card', 'Leadership briefing &middot; one minute') + \
        sec('The position in one line', '<div style="font-size:10.5pt;line-height:1.35;color:%s">%s</div>' % (NAVY, esc(v.get('line')))) + \
        sec('Why they matter', '<div class="two" style="border:0"><div style="border-right:1px solid %s"><div class="ch" style="color:%s">Where we meet them</div>%s</div>'
            '<div><div class="ch" style="color:%s">Deal presence</div>%s</div></div>' % (
                LINE, NAVY,
                ' &middot; '.join(esc(o['product']) for o in (c.get('overlaps') or []) if o.get('degree') != 'None') or '—',
                NAVY, ('Named in %d open deal%s this month.' % (hd['deals'], '' if hd['deals'] == 1 else 's')) if hd else 'Not named in an open deal this month.'), two=True) + \
        sec('Their strongest card, and ours', lists(c, 2), two=True) + \
        sec('What we lead with', '<ul class="tick">%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in (c.get('whyWeWin') or [])[:2])) + \
        sec('Proof we can put behind it', '<div class="kpi">%s</div>' % k) + \
        foot(c) + '</div>'

def card_product(c):
    return '<div class="pg">' + head(c, 'Product card', 'Where we actually differ') + \
        sec('Capability comparison &mdash; differences only', matrix(c, True, 12)) + \
        sec('What their own sources do not state', '<ul class="tick cross">%s</ul>' % (
            ''.join('<li>%s</li>' % esc(x['text']) for x in (c.get('gaps') or [])[:3]) or '<li>—</li>')) + \
        sec('How to use this', 'Never present <span class="pill unk">Unknown</span> as a No. It means no public source states it either way &mdash; '
            'ask the buyer to have them confirm it in writing.'
            '<div class="note">Full 77-capability matrix, with sources and verification dates, is in the app.</div>') + \
        foot(c) + '</div>'

async def main():
    c = C[SUBJECT]
    body = card_bdr(c) + card_sales(c) + card_exec(c) + card_product(c)
    html = "<!doctype html><meta charset='utf-8'><style>@page{size:letter;margin:11mm}%s</style>%s" % (CSS, body)
    pathlib.Path('/tmp/types.html').write_text(html, encoding='utf-8')
    out = 'Battlecard-Types-Yardi-Aspire.pdf'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file:///tmp/types.html'); await pg.wait_for_timeout(300)
        await pg.pdf(path=out, format='Letter', print_background=True)
        from pypdf import PdfReader
        print('%s: %d pages, errors=%s' % (out, len(PdfReader(out).pages), errs))
        await b.close()

asyncio.run(main())
