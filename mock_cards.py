"""Generate two battlecard design directions as 1-page PDFs, from real records."""
import json, asyncio, io, pathlib
from playwright.async_api import async_playwright

C = {c['id']: c for c in json.load(open('data/competitors.json'))}
HEARD = json.load(open('data/heard.json'))['competitors']
PATH = json.load(open('data/pathways.json'))['pathways']
ROLES = {r['id']: r for r in json.load(open('data/roles.json'))['roles']}
LADDER = {'risk':'workforce','workforce':'sentiment','leasing':'sentiment','sentiment':'workforce','market':'workforce'}
SUBJECTS = ['yardi-aspire', 'siro']

NAVY, RED, CER, CHAR, LINE = '#262262', '#FF0000', '#03B8EC', '#393A3C', '#E4E4EE'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

def esc(s):
    return (str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def dq(s):
    s = str(s or '').strip().strip('"').strip('“”')
    return f'&ldquo;{esc(s)}&rdquo;' if s else ''

def bits(c):
    """Normalise a record into the fields a card needs, whatever its play."""
    v, w = c.get('verdict') or {}, c.get('whenItComesUp') or {}
    fight = c.get('play') != 'Not our fight'
    say = [x for x in (c.get('whyWeWin') or [])][:3]
    if not say and w.get('say'):
        say = [w['say']]
    ask = (c.get('askThis') or [])[:3] or ([w['redirect']] if w.get('redirect') else [])
    never = (c.get('doNotSay') or [])[:2] or ([w['avoid']] if w.get('avoid') else [])
    obj = (c.get('objections') or [None])[0]
    ov = [o for o in (c.get('overlaps') or []) if o.get('degree') not in (None, 'None')]
    hd = HEARD.get(c['id'])
    mine = {o['product'] for o in ov}
    hits = [p for p in PATH if any(o in (p.get('overlaps') or []) for o in mine)]
    ways = [p['name'] for p in hits]
    who = []
    for p in hits:
        for rid in (p.get('roles') or []):
            if rid in ROLES and ROLES[rid]['name'] not in who:
                who.append(ROLES[rid]['name'])
    pair = []
    for p in hits:
        for pr in (p.get('products') or []):
            if not any(m.lower() in pr.lower() for m in mine) and pr not in pair:
                pair.append(pr)
    if hits:
        nxt = next((p for p in PATH if p['id'] == LADDER.get(hits[0]['id'])), None)
        if nxt and nxt not in hits:
            for pr in (nxt.get('products') or [])[:2]:
                if pr not in pair: pair.append(pr)
    return dict(v=v, w=w, fight=fight, say=say, ask=ask, never=never, obj=obj, ov=ov, hd=hd,
                ways=ways, who=who[:3], pair=pair[:5])

BASE = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{FONT};color:{CHAR};font-size:8.6pt;line-height:1.38;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.card{{width:100%;page-break-after:always;padding:0}}
.card:last-child{{page-break-after:auto}}
h1{{font-size:17pt;letter-spacing:-.3px}} h2{{font-size:8pt;letter-spacing:.11em;text-transform:uppercase}}
.chip{{display:inline-block;font-size:6.4pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:2px 6px;border-radius:3px}}
.q{{font-style:italic;color:{NAVY}}}
ul{{padding-left:13px}} li{{margin-bottom:3px}}
.foot{{font-size:6.4pt;color:#8A8A96;border-top:1px solid {LINE};padding-top:5px;margin-top:8px}}
"""

# ---------------- DESIGN A — the call card ----------------
A_CSS = BASE + f"""
.hero{{background:{NAVY};color:#fff;padding:13px 15px;border-radius:7px}}
.hero .top{{display:flex;justify-content:space-between;align-items:baseline;gap:10px}}
.hero h1{{color:#fff}} .hero .ln{{font-size:10.5pt;line-height:1.34;margin-top:6px}}
.cols{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin-top:10px}}
.col{{border:1px solid {LINE};border-radius:6px;padding:9px 10px;border-top:3px solid {NAVY}}}
.col.ask{{border-top-color:{CER}}} .col.never{{border-top-color:{RED}}}
.col h2{{color:{NAVY};margin-bottom:5px}} .col.never h2{{color:{RED}}}
.strip{{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:9px}}
.box{{border:1px solid {LINE};border-radius:6px;padding:9px 10px}}
.obj{{margin-top:9px;border:1px solid {LINE};border-left:4px solid {RED};border-radius:6px;padding:9px 11px}}
"""

def design_a(c):
    b = bits(c)
    playbg = RED if b['fight'] else '#EFEFF3'
    playfg = '#fff' if b['fight'] else '#5A5A66'
    hd = b['hd']
    return f"""<div class="card">
  <div class="hero">
    <div class="top"><h1>{esc(c['name'])}</h1>
      <span class="chip" style="background:{playbg};color:{playfg}">{esc(c.get('play'))}</span></div>
    <div class="ln">{esc((b['v'].get('line') if b['fight'] else b['v'].get('doInstead')) or b['v'].get('line'))}</div>
  </div>
  <div class="cols">
    <div class="col"><h2>Say this</h2><ul>{''.join(f'<li>{esc(x)}</li>' for x in b['say']) or '<li>—</li>'}</ul></div>
    <div class="col ask"><h2>Ask this</h2><ul>{''.join(f'<li class="q">{dq(x)}</li>' for x in b['ask']) or '<li>—</li>'}</ul></div>
    <div class="col never"><h2>Never say</h2><ul>{''.join(f'<li>{esc(x)}</li>' for x in b['never']) or '<li>—</li>'}</ul></div>
  </div>
  <div class="strip">
    <div class="box"><h2 style="color:{NAVY}">Where we overlap</h2>
      <div style="margin-top:5px">{''.join(f'<span class="chip" style="background:{NAVY if o["degree"]=="High" else "#E7E7F2"};color:{"#fff" if o["degree"]=="High" else NAVY};margin:0 4px 4px 0">{esc(o["product"])}</span>' for o in b['ov']) or '<span style="color:#8A8A96">No product overlap</span>'}</div>
      {f'<div style="margin-top:6px;font-size:7.4pt;color:#6B6B72">Outcome: {esc(" · ".join(b["ways"]))}</div>' if b['ways'] else ''}</div>
    <div class="box" style="border-left:3px solid {CER}"><h2 style="color:{NAVY}">What we're hearing</h2>
      {f'<div style="margin-top:4px"><strong>In {hd["deals"]} open deal{"s" if hd["deals"]!=1 else ""}.</strong> {esc(hd["whatBuyersSay"][0])}</div>' if hd else '<div style="margin-top:4px;color:#8A8A96">Not named in an open deal this month.</div>'}</div>
  </div>
  {f'''<div class="obj"><h2 style="color:{RED}">The objection you will get</h2>
    <div style="font-weight:700;color:{NAVY};margin-top:4px">{dq(b['obj']['objection'])}</div>
    <div style="margin-top:4px">{esc(b['obj'].get('response'))}</div></div>''' if b['obj'] else ''}
  <div class="strip">
    <div class="box"><h2 style="color:{NAVY}">Who raises this</h2>
      <div style="margin-top:4px">{esc(' · '.join(b['who'])) or '<span style="color:#8A8A96">—</span>'}</div></div>
    <div class="box"><h2 style="color:{NAVY}">Best paired with</h2>
      <div style="margin-top:4px">{esc(' · '.join(b['pair'])) or '<span style="color:#8A8A96">—</span>'}</div>
      <div style="font-size:7pt;color:#8A8A96;margin-top:3px">What completes the outcome once you have won this.</div></div>
  </div>
  <div class="foot">Grace Hill Competitive Intelligence · reviewed {esc((c.get('health') or {}).get('lastFullReview','—'))} · full record and us-vs-them matrix at ci-gracehill.com</div>
</div>"""

# ---------------- DESIGN B — the brief ----------------
B_CSS = BASE + f"""
.hdr{{border-bottom:3px solid {RED};padding-bottom:8px;margin-bottom:11px}}
.hdr .meta{{color:#6B6B72;font-size:7.4pt;margin-top:3px}}
.grid{{display:grid;grid-template-columns:33% 1fr;gap:14px}}
.rail{{background:#F7F7FB;border-radius:6px;padding:11px 12px}}
.rail h2{{color:{NAVY};margin:0 0 4px}} .rail .sec{{margin-bottom:10px}}
.main h2{{color:{RED};margin:0 0 4px}}
.lead{{border-left:3px solid {NAVY};padding:2px 0 2px 11px;font-size:11pt;line-height:1.35;color:{NAVY};margin-bottom:11px}}
.blk{{margin-bottom:10px}}
.blk .lbl{{font-size:7pt;letter-spacing:.1em;text-transform:uppercase;color:#8A8A96;font-weight:700;margin-bottom:3px}}
.neg{{border-left:3px solid {RED};padding-left:9px;margin-bottom:3px}}
"""

def design_b(c):
    b = bits(c)
    hd = b['hd']
    s = (c.get('strengths') or [])[:2]
    g = (c.get('gaps') or [])[:2]
    li = lambda rows: ''.join('<li>%s</li>' % esc(x.get('text')) for x in rows)
    srail = ('<div class="sec"><h2>What is real about them</h2><ul style="padding-left:12px">%s</ul></div>' % li(s)) if s else ''
    grail = ('<div class="sec"><h2>Where they stop</h2><ul style="padding-left:12px">%s</ul></div>' % li(g)) if g else ''
    return f"""<div class="card">
  <div class="hdr">
    <div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px">
      <h1 style="color:{NAVY}">{esc(c['name'])}</h1>
      <span class="chip" style="background:{RED if b['fight'] else '#EFEFF3'};color:{'#fff' if b['fight'] else '#5A5A66'}">{esc(c.get('play'))}</span></div>
    <div class="meta">{esc(c.get('toolCategory'))}{' · owned by ' + esc(c.get('parent')) if c.get('parent') else ''}</div>
  </div>
  <div class="grid">
    <div class="rail">
      <div class="sec"><h2>Where we overlap</h2>
        {''.join(f'<div>{esc(o["product"])} <span style="color:#8A8A96">— {esc(o["degree"])}</span></div>' for o in b['ov']) or '<div style="color:#8A8A96">No product overlap</div>'}
        {f'<div style="margin-top:5px;color:#6B6B72">Outcome: {esc(" · ".join(b["ways"]))}</div>' if b['ways'] else ''}</div>
      {srail}
      {grail}
      <div class="sec"><h2>What we're hearing</h2>
        {f'<div><strong>{hd["deals"]} open deal{"s" if hd["deals"]!=1 else ""}.</strong> {esc(hd["whatBuyersSay"][0])}</div>' if hd else '<div style="color:#8A8A96">Not named in an open deal this month.</div>'}</div>
    </div>
    <div class="main">
      <div class="lead">{esc((b['v'].get('doInstead') if not b['fight'] and b['v'].get('doInstead') else b['v'].get('line')))}</div>
      <div class="blk"><div class="lbl">Say this</div>
        <ul>{''.join(f'<li>{esc(x)}</li>' for x in b['say']) or '<li>—</li>'}</ul></div>
      <div class="blk"><div class="lbl">Ask this</div>
        <ul>{''.join(f'<li class="q">{dq(x)}</li>' for x in b['ask']) or '<li>—</li>'}</ul></div>
      <div class="blk"><div class="lbl">Never say</div>
        {''.join(f'<div class="neg">{esc(x)}</div>' for x in b['never']) or '<div>—</div>'}</div>
      {f'''<div class="blk"><div class="lbl">The objection you will get</div>
        <div style="font-weight:700;color:{NAVY}">{dq(b['obj']['objection'])}</div>
        <div>{esc(b['obj'].get('response'))}</div></div>''' if b['obj'] else ''}
      <div class="blk" style="border-top:1px solid #E4E4EE;padding-top:8px">
        <div class="lbl">Who raises this</div><div>{esc(' · '.join(b['who'])) or '—'}</div>
        <div class="lbl" style="margin-top:7px">Best paired with</div><div>{esc(' · '.join(b['pair'])) or '—'}</div></div>
    </div>
  </div>
  <div class="foot">Grace Hill Competitive Intelligence · reviewed {esc((c.get('health') or {}).get('lastFullReview','—'))} · full record at ci-gracehill.com</div>
</div>"""

def page(css, body, title):
    return f"<!doctype html><meta charset='utf-8'><title>{title}</title><style>@page{{size:letter;margin:11mm}}{css}</style>{body}"

async def main():
    docs = {
        'Battlecard-Design-A-call-card.pdf': page(A_CSS, ''.join(design_a(C[i]) for i in SUBJECTS), 'Design A'),
        'Battlecard-Design-B-the-brief.pdf': page(B_CSS, ''.join(design_b(C[i]) for i in SUBJECTS), 'Design B'),
    }
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, html in docs.items():
            pathlib.Path('/tmp/card.html').write_text(html, encoding='utf-8')
            pg = await b.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file:///tmp/card.html')
            await pg.wait_for_timeout(250)
            await pg.pdf(path=name, format='Letter', print_background=True)
            from pypdf import PdfReader
            n = len(PdfReader(name).pages)
            print(f'{name}: {n} pages (expect {len(SUBJECTS)}) errors={errs}')
            await pg.close()
        await b.close()

asyncio.run(main())
