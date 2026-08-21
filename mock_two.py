"""Two more card types: Approach-to-Market (Klue's actual structure) and Account Management."""
import json, asyncio, pathlib
from playwright.async_api import async_playwright

C = {c['id']: c for c in json.load(open('data/competitors.json'))}
PATH = {p['id']: p for p in json.load(open('data/pathways.json'))['pathways']}
HEARD = json.load(open('data/heard.json'))['competitors']
SEG = json.load(open('data/segments.json'))
MSG = {m['id']: m for m in json.load(open('data/messages.json'))['messages']}

NAVY, RED, CER, CHAR, LINE, BG = '#262262', '#D31417', '#03B8EC', '#393A3C', '#E4E4EE', '#F7F7FB'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

# Competitor-claimed pain points. Derived from their own positioning and marketing.
# THIS WANTS TO BE A DATA FIELD — see the note on each card.
THEIR_PAIN = {
    'realpage-realconnect': [
        ("Training does not get done because people cannot reach it",
         "Mobile-first delivery and just-in-time access on the device already in their hand."),
        ("The wrong people get the wrong courses",
         "Learning pathways assignable by position, market type and location."),
        ("Onsite teams are not all English-first",
         "A fully translated English and Spanish learner interface."),
    ],
    'grow-by-inhabit': [
        ("Buying a whole platform to fix a content gap is too much",
         "Courses sold à la carte and in SCORM format, dropped into the LMS you already run."),
        ("Multifamily teams find generic corporate training irrelevant",
         "300+ short courses across 28+ multifamily topic areas, written for this industry."),
        ("Vendor sprawl across the property tech stack",
         "Bundled with Inhabit sibling products, so it arrives on an existing paper."),
    ],
    'satisfacts-apartmentratings': [
        ("We survey residents but never see it reflected publicly",
         "Surveys sold alongside the ApartmentRatings review site and epIQ Index, under one brand."),
        ("Nobody responds to our reviews",
         "A managed review response service rather than tooling alone."),
        ("We have no idea how our score compares",
         "A published, named industry index buyers already recognize."),
    ],
}

def esc(s):
    return str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def dq(s):
    s = str(s or '').strip().strip('"').strip('“”')
    return '&ldquo;%s&rdquo;' % esc(s) if s else ''

def clip(s, n):
    s = str(s or '').strip()
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0].rstrip(' ,.;:—-') + '…'

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
.sec.warn>h2{background:%(RED)s}.sec.gap>h2{background:#8A8A96}.sec.grow>h2{background:#0E7C7B}
.body{padding:9px 11px}
.pp{margin-bottom:8px}.pp:last-child{margin-bottom:0}
.pp .n{font-size:6.8pt;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:%(RED)s}
.pp .t{font-weight:700;color:%(NAVY)s}
.pp .h{margin-top:2px}
.two{display:grid;grid-template-columns:1fr 1fr}
.two>div{padding:9px 11px}.two>div:first-child{border-right:1px solid %(LINE)s}
.ch{font-size:7.2pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;text-align:center;
    padding-bottom:5px;margin-bottom:6px;border-bottom:1px solid %(LINE)s}
.row{display:grid;grid-template-columns:118px 1fr;gap:3px 10px}.row b{color:%(NAVY)s}
ul{padding-left:14px}li{margin-bottom:3px}
.tick li{list-style:none;position:relative;padding-left:15px}
.tick li:before{content:'';position:absolute;left:0;top:4px;width:9px;height:9px;border-radius:50%%;background:%(NAVY)s}
.cross li:before{background:%(RED)s}
.act{background:#FFF6F6;border-left:3px solid %(RED)s;padding:8px 11px}
.ok{background:#F2FAFA;border-left:3px solid #0E7C7B;padding:8px 11px}
.chip{display:inline-block;font-size:6.6pt;font-weight:700;text-transform:uppercase;letter-spacing:.05em;
      padding:2px 7px;border-radius:3px;background:#E7E7F2;color:%(NAVY)s;margin:0 4px 4px 0}
table{width:100%%;border-collapse:collapse}
th{background:%(BG)s;font-size:7pt;letter-spacing:.06em;text-transform:uppercase;text-align:left;
   padding:4px 8px;border-bottom:1px solid %(LINE)s;color:#6B6B72}
td{padding:5px 8px;border-bottom:1px solid #F0F0F5;vertical-align:top}
.kpi{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.kpi .n{font-size:13pt;font-weight:700;color:%(NAVY)s;line-height:1.1}
.kpi .l{font-size:7pt;color:#6B6B72}
.q{font-style:italic;color:%(NAVY)s}
.foot{font-size:6.4pt;color:#8A8A96;border-top:1px solid %(LINE)s;padding-top:5px;margin-top:7px}
.note{font-size:7pt;color:#8A8A96;margin-top:5px}
""" % dict(F=FONT, NAVY=NAVY, RED=RED, CER=CER, CHAR=CHAR, LINE=LINE, BG=BG)

def sec(t, inner, two=False, cls=''):
    return '<div class="sec %s"><h2>%s</h2>%s</div>' % (cls, t, inner if two else '<div class="body">%s</div>' % inner)

def ways_for(c):
    mine = {o['product'] for o in (c.get('overlaps') or []) if o.get('degree') != 'None'}
    return [p for p in PATH.values() if any(o in mine for o in (p.get('overlaps') or []))]

def head(c, kind, tag):
    return ('<div class="title"><h1>%s</h1><span class="kind">%s</span></div>'
            '<div class="sub">%s</div>') % (esc(c['name']), esc(kind), tag)

def foot(c, extra=''):
    return ('<div class="foot">Grace Hill Competitive Intelligence &middot; reviewed %s%s</div>' %
            (esc((c.get('health') or {}).get('lastFullReview', '—')), extra))

# ---------------- Approach to Market, Klue structure ----------------
def card_atm(c):
    pains = THEIR_PAIN.get(c['id'], [])
    pp = ''.join('<div class="pp"><div class="n">Pain point %d</div><div class="t">%s</div>'
                 '<div class="h"><span style="color:#8A8A96">How they solve it:</span> %s</div></div>' % (
                     i + 1, esc(a), esc(b)) for i, (a, b) in enumerate(pains)) or \
         '<div style="color:#8A8A96">Not yet researched.</div>'
    uvp = esc(clip((c.get('positioning') or {}).get('value'), 300))
    msg = ''.join('<li>%s</li>' % esc(s['text']) for s in (c.get('strengths') or [])[:3])
    counter = ''.join('<li>%s</li>' % esc(g['text']) for g in (c.get('gaps') or [])[:2])
    return '<div class="pg">' + \
        head(c, 'Approach to market', 'What they tell the buyer &middot; owned by %s' % esc(c.get('parent') or 'independent')) + \
        sec('Pain points they claim to solve', pp) + \
        sec('Their unique value proposition', uvp) + \
        sec('Positioning and messaging', '<div class="two" style="border:0">'
            '<div style="border-right:1px solid %s"><div class="ch" style="color:%s">What they lead with</div>'
            '<ul class="tick">%s</ul></div>'
            '<div><div class="ch" style="color:%s">What that message leaves out</div>'
            '<ul class="tick cross">%s</ul></div></div>' % (LINE, NAVY, msg or '<li>—</li>', RED, counter or '<li>—</li>'), two=True) + \
        sec('So expect this in the deal', '<div class="act">%s</div>' % esc(
            (HEARD.get(c['id']) or {}).get('useIt') or (c.get('verdict') or {}).get('line'))) + \
        sec('Not yet researched', '<ul><li>Target verticals beyond multifamily</li>'
            '<li>Named clients and logos they lead with</li><li>Channel and reseller partners</li>'
            '<li>Sales motion: pilots, proofs of concept, free trials, discount patterns</li></ul>'
            '<div class="note">Pain points above are derived from their own positioning and marketing, not from a named source. '
            'They want to become a maintained field so the weekly sweep keeps them current.</div>', cls='gap') + \
        foot(c) + '</div>'

# ---------------- Account Management ----------------
def card_am(c):
    ways = ways_for(c)
    mine = {o['product'] for o in (c.get('overlaps') or []) if o.get('degree') != 'None'}
    nxt = None
    for p in PATH.values():
        if p not in ways and p['id'] in ('workforce', 'sentiment', 'market'):
            nxt = p; break
    stay, evolve = MSG['stay'], MSG['evolve']
    wl = SEG['whyWeLose']
    hd = HEARD.get(c['id'])

    risk = ('<div class="row"><b>Why accounts leave</b><div>%s</div>'
            '<b>Where this one bites</b><div>%s</div>'
            '<b>Live signal</b><div>%s</div></div>') % (
        esc(wl['headline'] + ' ' + wl['points'][0]),
        esc(wl['points'][2] if 'consolidation' in ' '.join(wl['points'][2:3]).lower() else wl['points'][2]),
        ('Named in %d open deal%s. %s' % (hd['deals'], '' if hd['deals'] == 1 else 's', esc(hd.get('pricingSignal') or ''))) if hd
        else 'Not named in an open deal this month.')

    staycard = '<ol class="q" style="padding-left:16px">%s</ol><div class="ok" style="margin-top:7px">%s</div>' % (
        ''.join('<li style="font-style:normal">%s</li>' % esc(s) for s in stay['steps']), esc(stay['evidence']))

    grow = ('<div class="row"><b>They own today</b><div>%s</div>'
            '<b>Natural next step</b><div>%s</div>'
            '<b>Why it lands</b><div>%s</div></div>') % (
        ' '.join('<span class="chip">%s</span>' % esc(m) for m in mine) or '—',
        ('<strong style="color:%s">%s</strong> &mdash; %s' % (NAVY, esc(nxt['name']), esc(', '.join((nxt.get('products') or [])[:3])))) if nxt else '—',
        esc(SEG['migration']['points'][2]))

    evolvecard = '<ol class="q" style="padding-left:16px">%s</ol><div class="ok" style="margin-top:7px">%s</div>' % (
        ''.join('<li style="font-style:normal">%s</li>' % esc(s) for s in evolve['steps']), esc(evolve['evidence']))

    warn = ('Do not use a disruptive, challenge-the-status-quo message on an existing customer. '
            'It raises the chance they leave by at least 10%. You are the status quo now — do not displace yourself.')

    gaps = ''.join('<li>%s</li>' % esc(g['text']) for g in (c.get('gaps') or [])[:2]) or '<li>—</li>'

    return '<div class="pg">' + \
        head(c, 'Account management', 'Renewal and expansion &middot; %s' % (
            ' &middot; '.join(esc(w['name']) for w in ways) or esc(c.get('play')))) + \
        sec('Churn risk', risk, cls='warn') + \
        sec('If they threaten to switch &mdash; the Why Stay message', staycard) + \
        sec('If they evaluate this competitor instead', '<ul class="tick cross">%s</ul>'
            '<div class="note">Ask them to verify one of these with the vendor in writing. Do not argue it yourself — '
            'the incumbent is trusted at 79%%, a rep at 58%%.</div>' % gaps) + \
        sec('Where the expansion is', grow, cls='grow') + \
        sec('The Why Evolve message', evolvecard, cls='grow') + \
        sec('The rule that matters most', '<div class="act">%s</div>' % esc(warn), cls='warn') + \
        foot(c, ' &middot; churn data from RML baseline, message models from Corporate Visions') + '</div>'

async def render(name, body):
    html = "<!doctype html><meta charset='utf-8'><style>@page{size:letter;margin:11mm}%s</style>%s" % (CSS, body)
    pathlib.Path('/tmp/x.html').write_text(html, encoding='utf-8')
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file:///tmp/x.html'); await pg.wait_for_timeout(250)
        await pg.pdf(path=name, format='Letter', print_background=True)
        from pypdf import PdfReader
        print('%s: %d pages, errors=%s' % (name, len(PdfReader(name).pages), errs))
        await b.close()

async def main():
    await render('Battlecard-Approach-to-Market-v2.pdf',
                 ''.join(card_atm(C[i]) for i in ['realpage-realconnect', 'grow-by-inhabit']))
    await render('Battlecard-Account-Management.pdf',
                 ''.join(card_am(C[i]) for i in ['realpage-realconnect', 'satisfacts-apartmentratings']))

asyncio.run(main())
