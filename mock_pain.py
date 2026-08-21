"""Pain & Outcome card — the job the buyer is hiring for, and what to say when you hear it."""
import json, asyncio, pathlib
from playwright.async_api import async_playwright

C = {c['id']: c for c in json.load(open('data/competitors.json'))}
PATH = {p['id']: p for p in json.load(open('data/pathways.json'))['pathways']}
JOBS = json.load(open('data/jtbd.json'))['jobs']
HEARD = json.load(open('data/heard.json'))['competitors']

SUBJECTS = ['yardi-aspire', 'satisfacts-apartmentratings']

NAVY, RED, CER, CHAR, LINE, BG = '#262262', '#D31417', '#03B8EC', '#393A3C', '#E4E4EE', '#F7F7FB'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
PROOF = [('7.3M', 'residents and prospects surveyed a year'),
         ('92%', 'on-time mystery shop completion'),
         ('35 years', 'of multifamily benchmarking behind the Kingsley Index')]

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
.body{padding:9px 11px}
.job{border-left:3px solid %(CER)s;padding:1px 0 1px 10px;margin-bottom:8px}
.job .j{font-size:9.6pt;color:%(NAVY)s;font-style:italic;line-height:1.35}
.job .p{margin-top:3px}.job .o{margin-top:3px}
.lbl{font-size:6.8pt;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#8A8A96}
table{width:100%%;border-collapse:collapse}
th{background:%(BG)s;font-size:7pt;letter-spacing:.06em;text-transform:uppercase;text-align:left;
   padding:4px 8px;border-bottom:1px solid %(LINE)s;color:#6B6B72}
td{padding:5px 8px;border-bottom:1px solid #F0F0F5;vertical-align:top}
.two{display:grid;grid-template-columns:1fr 1fr}
.two>div{padding:9px 11px}.two>div:first-child{border-right:1px solid %(LINE)s}
.ch{font-size:7.2pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;text-align:center;
    padding-bottom:5px;margin-bottom:6px;border-bottom:1px solid %(LINE)s}
.kpi{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.kpi .n{font-size:13pt;font-weight:700;color:%(NAVY)s;line-height:1.1}
.kpi .l{font-size:7pt;color:#6B6B72}
.q{font-style:italic;color:%(NAVY)s}
.foot{font-size:6.4pt;color:#8A8A96;border-top:1px solid %(LINE)s;padding-top:5px;margin-top:7px}
""" % dict(F=FONT, NAVY=NAVY, RED=RED, CER=CER, CHAR=CHAR, LINE=LINE, BG=BG)

def sec(t, inner, two=False):
    return '<div class="sec"><h2>%s</h2>%s</div>' % (t, inner if two else '<div class="body">%s</div>' % inner)

def ways_for(c):
    mine = {o['product'] for o in (c.get('overlaps') or []) if o.get('degree') != 'None'}
    return [p for p in PATH.values() if any(o in mine for o in (p.get('overlaps') or []))]

def card(c):
    ways = ways_for(c)
    wids = {w['id'] for w in ways}
    jobs = [j for j in JOBS if j['pathway'] in wids][:3]

    jb = ''.join(
        '<div class="job"><div class="j">%s</div>'
        '<div class="p"><span class="lbl">Where it hurts today</span> %s</div>'
        '<div class="o"><span class="lbl">What good looks like</span> %s</div></div>' % (
            esc(j['job']), esc(j['pain']), esc(j['outcome'])) for j in jobs) or '<div style="color:#8A8A96">—</div>'

    claim = ('<div class="two" style="border:0"><div style="border-right:1px solid %s">'
             '<div class="ch" style="color:%s">What they promise</div>%s</div>'
             '<div><div class="ch" style="color:%s">Where that stops short</div><div>%s</div></div></div>') % (
        LINE, NAVY, esc(clip((c.get('positioning') or {}).get('value'), 300)),
        RED, esc(((c.get('gaps') or [{}])[0]).get('text', '—')))

    rows = ''
    for w in ways[:3]:
        hear = (w.get('hearThis') or ['—'])[0]
        rows += ('<tr><td style="width:36%%" class="q">%s</td>'
                 '<td style="width:20%%"><strong style="color:%s">%s</strong><br>'
                 '<span style="color:#8A8A96;font-size:7pt">%s</span></td>'
                 '<td>%s</td></tr>') % (dq(hear), NAVY, esc(w['name']), esc(w['goal']), esc(w['sayThat']))
    ask = ('<table><thead><tr><th>If you hear this</th><th>The outcome in play</th><th>Say this</th></tr></thead>'
           '<tbody>%s</tbody></table>' % rows) if rows else '<div style="color:#8A8A96">—</div>'

    win = '<ul>%s</ul>' % (''.join('<li>%s</li>' % esc(x) for x in (c.get('whyWeWin') or [])[:3]) or '<li>—</li>')
    k = ''.join('<div><div class="n">%s</div><div class="l">%s</div></div>' % (a, b) for a, b in PROOF)

    return '<div class="pg">' + \
        ('<div class="title"><h1>%s</h1><span class="kind">Pain &amp; outcome</span></div>'
         '<div class="sub">The job the buyer is hiring for &middot; %s</div>') % (
            esc(c['name']), ' &middot; '.join(esc(w['name']) for w in ways) or esc(c.get('play'))) + \
        sec('The job they are trying to get done', jb) + \
        sec('What this competitor promises against that job', claim, two=True) + \
        sec('Hear this, say that', ask) + \
        sec('The outcome we can commit to', win) + \
        sec('Proof behind it', '<div class="kpi">%s</div>' % k) + \
        ('<div class="foot">Grace Hill Competitive Intelligence &middot; jobs from the JTBD session, outcomes from the RML pathways &middot; '
         'reviewed %s</div>' % esc((c.get('health') or {}).get('lastFullReview', '—'))) + '</div>'

async def main():
    body = ''.join(card(C[i]) for i in SUBJECTS)
    html = "<!doctype html><meta charset='utf-8'><style>@page{size:letter;margin:11mm}%s</style>%s" % (CSS, body)
    pathlib.Path('/tmp/pain.html').write_text(html, encoding='utf-8')
    out = 'Battlecard-Pain-and-Outcome.pdf'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file:///tmp/pain.html'); await pg.wait_for_timeout(250)
        await pg.pdf(path=out, format='Letter', print_background=True)
        from pypdf import PdfReader
        print('%s: %d pages, errors=%s' % (out, len(PdfReader(out).pages), errs))
        await b.close()

asyncio.run(main())
