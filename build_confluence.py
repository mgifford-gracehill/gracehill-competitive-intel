import json, html, pathlib
E=lambda s: html.escape(str(s or ''))
L=lambda n: json.load(open(f'data/{n}.json'))
C=L('competitors'); GHB=L('gh-baseline'); P=L('pitch'); SP=L('spiced'); N=L('news')
FEAT={}
for l in L('features')['lines']:
    for f in l['features']: FEAT[f['id']]={**f,'line':l['line']}
STATUS={'Compete':'red','Partial overlap':'yellow','Do not compete':'neutral','Partner':'purple'}
def chip(s): return f'<span data-type="status" data-color="{STATUS.get(s,"neutral")}">{E(s)}</span>'
def ul(a): return '<ul>'+''.join(f'<li><p>{E(x)}</p></li>' for x in a)+'</ul>' if a else ''
order={'Tier 1':0,'Tier 2':1,'Tier 3':2,'Watchlist':3}
srt=sorted(C,key=lambda c:(order.get(c.get('tier'),9),c['name']))
APPNOTE='<div data-type="panel-info"><p><strong>This is the reference copy.</strong> The full app — search, the us-vs-them capability matrix, downloadable battlecards — is a separate file. This page is here so anyone can find the answer without it.</p></div>'

# ---------- 1. PARENT ----------
st=lambda s: sum(1 for c in C if (c.get('verdict') or {}).get('stance')==s)
parent=f'''<div data-type="panel-info"><p><strong>{len(C)} competitors, and for each one a straight answer to two questions: do we compete, and what do I say.</strong></p></div>
<p>Built from public research, the Jira competitor register and the field-intel Slack channel. Company facts are re-verified on a schedule; the judgment — stance, tier, what a rep should say — is owned by marketing and edited in the admin sheet.</p>
<h2>Start here</h2>
<table><tbody>
<tr><th><p>If you want to know…</p></th><th><p>Go to</p></th></tr>
<tr><td><p>Do we compete with this vendor?</p></td><td><p><strong>Competitor index</strong></p></td></tr>
<tr><td><p>They just named a competitor on a call — what do I say?</p></td><td><p><strong>When it comes up</strong></p></td></tr>
<tr><td><p>How do I tell the Grace Hill story?</p></td><td><p><strong>The pitch</strong></p></td></tr>
<tr><td><p>What do I ask in discovery?</p></td><td><p><strong>SPICED discovery</strong></p></td></tr>
<tr><td><p>What happened in the market this week?</p></td><td><p><strong>Weekly digest</strong></p></td></tr>
</tbody></table>
<h2>The shape of the competitive set</h2>
<table><tbody>
<tr><th><p>Stance</p></th><th><p>Count</p></th><th><p>What it means</p></th></tr>
<tr><td><p>{chip('Compete')}</p></td><td><p>{st('Compete')}</p></td><td><p>Same buyer, same budget line. A real head-to-head.</p></td></tr>
<tr><td><p>{chip('Partial overlap')}</p></td><td><p>{st('Partial overlap')}</p></td><td><p>Overlaps on part of the job. Concede the part they own.</p></td></tr>
<tr><td><p>{chip('Do not compete')}</p></td><td><p>{st('Do not compete')}</p></td><td><p>Not a fight to pick. Each says what to do instead.</p></td></tr>
<tr><td><p>{chip('Partner')}</p></td><td><p>{st('Partner')}</p></td><td><p>Confirm posture before using competitive language.</p></td></tr>
</tbody></table>
<div data-type="panel-warning"><p><strong>A fifth of the register is not a fight.</strong> Before you build a case against a vendor, check the stance. Pitching against a partner or a tool that solves a different problem costs credibility you need later.</p></div>
{APPNOTE}'''

# ---------- 2. COMPETITOR INDEX ----------
rows=''.join(f'''<tr><td><p><strong>{E(c["name"])}</strong>{f'<br /><em>{E(c.get("parent"))}</em>' if c.get('parent') else ''}</p></td>
<td><p>{chip((c.get("verdict") or {}).get("stance"))}</p></td><td><p>{E(c.get("tier"))}</p></td>
<td><p>{E(c.get("toolCategory"))}</p></td><td><p>{E((c.get("verdict") or {}).get("line"))}</p></td>
<td><p>{E(", ".join(o["product"] for o in (c.get("overlaps") or []) if o.get("degree")in("High","Partial")) or "—")}</p></td></tr>''' for c in srt)
index=f'''<p>Every competitor tracked, ordered by tier. Use your browser find (Ctrl+F) or Confluence search — this page is indexed, so searching a vendor name from anywhere in Confluence lands you here.</p>
<div data-type="panel-note"><p><strong>Overlaps</strong> lists only the Grace Hill lines where the overlap is High or Partial. Blank means we do not meaningfully overlap.</p></div>
<table data-layout="full-width"><tbody>
<tr><th><p>Competitor</p></th><th><p>Stance</p></th><th><p>Tier</p></th><th><p>What it is</p></th><th><p>The one-line read</p></th><th><p>Overlaps</p></th></tr>
{rows}</tbody></table>{APPNOTE}'''

# ---------- 3. WHEN IT COMES UP (authored only) ----------
auth=[c for c in srt if not (c.get('whenItComesUp') or {}).get('derived')]
def block(c):
    w=c.get('whenItComesUp') or {}; v=c.get('verdict') or {}
    return f'''<h2>{E(c["name"])} &nbsp; {chip(v.get("stance"))}</h2>
<p><em>{E(c.get("toolCategory"))}{" · owned by "+E(c.get("parent")) if c.get("parent") else ""}</em></p>
<div data-type="panel-info"><p>{E(v.get("line"))}</p></div>
<p><strong>Why this is / isn't a fight.</strong> {E(w.get("why"))}</p>
<div data-type="panel-success"><p><strong>Say this.</strong> {E(w.get("say"))}</p></div>
<div data-type="panel-error"><p><strong>Avoid.</strong> {E(w.get("avoid"))}</p></div>
<p><strong>Then redirect:</strong> <em>&ldquo;{E(w.get("redirect"))}&rdquo;</em></p>
{"<p><strong>Do instead.</strong> "+E(v.get("doInstead"))+"</p>" if v.get("doInstead") else ""}
{"<p><strong>Ask this:</strong> <em>&ldquo;"+E((c.get("askThis") or [""])[0])+"&rdquo;</em></p>" if c.get("askThis") else ""}'''
comes=f'''<p>Hand-written guidance for the {len(auth)} competitors that matter most — every Tier 1 record and every one we have decided not to compete with. Words you can say out loud, not a feature list.</p>
<div data-type="panel-warning"><p>The other {len(C)-len(auth)} competitors have starter guidance derived from their own record, marked as such in the app. Rewrite one in the admin sheet and it is promoted to hand-written here.</p></div>
{''.join(block(c) for c in auth)}{APPNOTE}'''

# ---------- 4. THE PITCH ----------
loop=''.join(f'<tr><td><p><strong>{r["n"]}. {E(r["step"])}</strong></p></td><td><p>{E(r["detail"])}</p></td></tr>' for r in P['resolutionLoop'])
alts=''.join(f'<tr><td><p><strong>{E(a["approach"])}</strong></p></td><td><p>{E(a["goodFor"])}</p></td><td><p>{E(a["stops"])}</p></td></tr>' for a in P['alternatives'])
pw=''.join(f'<tr><td><p><strong>{x["n"]}. {E(x["title"])}</strong></p></td><td><p>{E(x["detail"])}</p></td></tr>' for x in P['perfectWorld'])
objs=''.join(f'<p><strong>&ldquo;{E(o["objection"])}&rdquo;</strong><br />{E(o["response"])}</p>' for o in P['objections'])
stats=''.join(f'<tr><td><p><strong>{E(s["stat"])}</strong></p></td><td><p>{E(s["label"])}</p></td></tr>' for s in P['insight']['stats'])
pitch=f'''<div data-type="panel-info"><p><strong>{E(P["theme"])}</strong></p><p>{E(P["anchorPromise"])}</p></div>
<h2>The 30-second pitch</h2><blockquote><p>{E(P["thirtySecond"])}</p></blockquote>
<h2>The market shift</h2>
<table><tbody><tr><th><p>What changed</p></th><td><p>{E(P["marketShift"]["whatChanged"])}</p></td></tr>
<tr><th><p>What didn't</p></th><td><p>{E(P["marketShift"]["whatDidNot"])}</p></td></tr>
<tr><th><p>What it means</p></th><td><p>{E(P["marketShift"]["whatItMeans"])}</p></td></tr></tbody></table>
<p><strong>{E(P["marketShift"]["line"])}</strong></p>
<h2>The resolution loop</h2><table><tbody>{loop}</tbody></table>
<div data-type="panel-warning"><p>{E(P["loopNote"])}</p></div>
<h2>Our point of view</h2><p><strong>{E(P["insight"]["headline"])}</strong> {E(P["insight"]["sub"])}</p>
<table><tbody>{stats}</tbody></table><p><em>{E(P["insight"]["sources"])}</em></p>
<p>{E(P["insight"]["close"])}</p>
<h2>Their options — be fair to all four</h2>
<table><tbody><tr><th><p>Approach</p></th><th><p>Good for</p></th><th><p>Where it stops</p></th></tr>{alts}</tbody></table>
<div data-type="panel-note"><p>{E(P["alternativesNote"])}</p></div>
<h2>What good would look like</h2><table><tbody>{pw}</tbody></table>
<div data-type="panel-warning"><p>{E(P["perfectWorldNote"])}</p></div>
<h2>The moat</h2>
<p><strong>Evidence:</strong> {E(', '.join(P['connectsBothSides']['evidence']))}<br />
<strong>Context:</strong> {E(', '.join(P['connectsBothSides']['context']))}<br />
<strong>Improvement:</strong> {E(', '.join(P['connectsBothSides']['improvement']))}</p>
<div data-type="panel-success"><p><strong>{E(P["connectsBothSides"]["moat"])}</strong></p><p>{E(P["connectsBothSides"]["note"])}</p></div>
<h2>Where AI fits</h2><p><strong>What AI changed.</strong> {E(P["ai"]["changed"])}</p>
<p><strong>What it hasn't.</strong> {E(P["ai"]["unchanged"])}</p><p>{E(P["ai"]["close"])}</p>
<h2>Fair questions</h2>{objs}
<h2>Language to avoid</h2><div data-type="panel-error">{ul(P["languageToAvoid"])}</div>
<p><em>{E(P["closingLine"])}</em></p>{APPNOTE}'''

# ---------- 5. SPICED ----------
sp=''.join(f'''<h2>{E(s["letter"])} &nbsp;&mdash;&nbsp; {E(s["stage"])}</h2><p><em>{E(s["objective"])}</em></p>
<p><strong>Ask it live</strong></p>{ul(s["askItLive"])}
<details><summary>Deal review — what you must be able to answer</summary>{ul(s["dealReview"])}</details>''' for s in SP['stages'])
exit_rows=''.join(f'<tr><td><p><strong>{E(c["item"])}</strong></p></td><td><p>{E(c["detail"])}</p></td></tr>' for c in SP['stage2Exit']['criteria'])
spiced=f'''<p>{E(SP["note"])}</p>{sp}
<h2>Fit indicators to listen for</h2>{ul(SP["fitIndicators"])}
<h2>{E(SP["stage2Exit"]["title"])}</h2><table><tbody>{exit_rows}</tbody></table>
<div data-type="panel-warning"><p>{E(SP["stage2Exit"]["note"])}</p></div>{APPNOTE}'''

# ---------- 6. WEEKLY DIGEST ----------
items=sorted(N['items'],key=lambda i:str(i.get('date')),reverse=True)[:14]
dig=''.join(f'''<h3>{E(i["headline"])}</h3><p><em>{E(i["date"])} &middot; {E(i["source"])}</em></p><p>{E(i["summary"])}</p>
<div data-type="panel-info"><p><strong>Why it matters.</strong> {E(i["soWhat"])}</p></div>
<p><a href="{E(i["url"])}">Read the source</a></p>''' for i in items)
news=f'''<div data-type="panel-info"><p><strong>This week's talk track</strong></p><p>{E(N["talkTrack"])}</p></div>
<p><em>{E(N["weekOf"])} &middot; coverage {E(N["coverageWindow"])}</em></p>{dig}{APPNOTE}'''

pages={'00-parent':('Competitive Intelligence',parent),
 '01-index':('Competitor index — do we compete?',index),
 '02-comes-up':('When it comes up — what to say',comes),
 '03-pitch':('The pitch',pitch),
 '04-spiced':('SPICED discovery',spiced),
 '05-news':('Weekly digest',news)}
pathlib.Path('confluence').mkdir(exist_ok=True)
for k,(t,b) in pages.items():
    pathlib.Path(f'confluence/{k}.html').write_text(b)
    print(f'{k}: "{t}" — {len(b):,} chars')
json.dump({k:v[0] for k,v in pages.items()}, open('confluence/titles.json','w'), indent=2)
