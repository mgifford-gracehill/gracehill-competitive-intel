"""Repackage the CI data as a Claude skill. Run after any build that changed the data.

  python3 build-skill.py

Why a skill and not an MCP connector: the data is read-only reference that changes weekly.
A connector means a server to host, authenticate and keep running; a skill is a zip that
works in any Claude conversation with no infrastructure at all. If this ever needs to be
live rather than a weekly snapshot — a rep asking "what changed since this morning" — that
is the point to revisit it, and not before.
"""
import json, pathlib, shutil, subprocess, sys

SRC = pathlib.Path('data'); STAGE = pathlib.Path('_skill'); OUT = pathlib.Path('grace-hill-competitive-intel.skill')
KEEP = ('id','name','aka','parent','website','toolCategory','ciCategory','play','verdict','overlaps',
        'positioning','whyWeWin','gaps','strengths','objections','askThis','doNotSay','spiced',
        'whenItComesUp','pricing','snapshot','news','sources','health','features')
PREFIX = {'tr-':'training','po-':'policies','sv-':'surveys','rm-':'reputation','ms-':'mystery-shopping',
          'md-':'market-data','ai-':'intelligence-plus','rl-':'realync'}

def main():
    if STAGE.exists(): shutil.rmtree(STAGE)
    ref = STAGE/'reference'; (ref/'competitors').mkdir(parents=True); (ref/'grace-hill').mkdir()
    # SKILL.md and the hand-written reference pages are kept in skill-src/ and copied verbatim.
    src = pathlib.Path('skill-src')
    for f in ('SKILL.md',):
        shutil.copy(src/f, STAGE/f)
    for f in ('rules.md',):
        shutil.copy(src/f, ref/f)

    C = json.load(open(SRC/'competitors.json'))
    recs = C if isinstance(C, list) else C.get('competitors', C)
    F = json.load(open(SRC/'features.json'))
    FEAT = {x['id']: x['label'] for l in F['lines'] for x in l['features']}

    rows = ['# Competitor index', '',
            'One line per competitor. Find what you need here, then read only that file from',
            '`reference/competitors/<id>.json`. Do not load them all — the full set is over a megabyte.', '',
            '| id | name | also called | what it is | how we play it |', '|---|---|---|---|---|']
    for c in sorted(recs, key=lambda x: x['name'].lower()):
        rows.append(f"| `{c['id']}` | {c['name']} | {', '.join((c.get('aka') or [])[:3])} | "
                    f"{c.get('toolCategory') or ''} | {c.get('play') or ''} |")
        d = {k: c[k] for k in KEEP if k in c}
        if 'features' in d:
            d['features'] = {FEAT.get(k, k): v for k, v in d['features'].items()}
        (ref/'competitors'/f"{c['id']}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
    (ref/'competitor-index.md').write_text('\n'.join(rows))

    G = json.load(open(SRC/'gh-baseline.json'))
    byline = {}
    for k, v in G.items():
        if not isinstance(v, dict): continue
        byline.setdefault(next((n for p, n in PREFIX.items() if k.startswith(p)), 'other'), {})[k] = v
    for line, claims in byline.items():
        (ref/'grace-hill'/f'{line}.json').write_text(json.dumps(claims, indent=1, ensure_ascii=False))

    for name, fn in (('pitch.md', build_pitch), ('partners.md', build_partners)):
        (ref/name).write_text(fn())

    if OUT.exists(): OUT.unlink()
    subprocess.run(['zip', '-qr', str(OUT.resolve()), '.', '-x', '.*'], cwd=STAGE, check=True)
    print(f'{OUT} — {OUT.stat().st_size//1024} KB · {len(recs)} competitors · '
          f'{sum(len(v) for v in byline.values())} Grace Hill claims')

def build_pitch():
    P = json.load(open(SRC/'pitch.json')); M = json.load(open(SRC/'messages.json'))
    L = [f"# The Grace Hill pitch\n\n*{P.get('source','')}*\n",
         f"**Theme.** {P.get('theme','')}\n", f"**Anchor promise.** {P.get('anchorPromise','')}\n",
         "## Thirty seconds\n", P.get('thirtySecond','') + "\n"]
    for k, v in (P.get('threeMinute') or {}).items():
        L.append(f"**{k}** — {v}\n")
    if P.get('proof'):
        L.append("## Proof points\n")
        L += [f"- **{x.get('stat')}** — {x.get('label')}" for x in P['proof']] + ['']
    if P.get('objections'):
        L.append("## Objections and responses\n")
        L += [f"**\"{o.get('objection')}\"**\n\n{o.get('response')}\n" for o in P['objections']]
    if P.get('stories'):
        L.append("## Customer stories\n")
        L += [f"**{s.get('role','')}** — use when: {s.get('useWhen','')}\n\n"
              f"{s.get('situation','')} {s.get('pain','')} {s.get('impact','')}\n" for s in P['stories']]
    L.append("## Message by deal type\n"); L.append(M.get('theBigIdea','') + "\n")
    for m in (M.get('messages') or []):
        L.append(f"### {m.get('name')}\n\n*{m.get('use','')}*\n\n**Goal.** {m.get('goal','')}\n")
        L += [f"- {st}" for st in (m.get('steps') or [])] + ['']
    if P.get('languageToAvoid'):
        L.append("## Language to avoid\n"); L += [f"- {x}" for x in P['languageToAvoid']]
    return '\n'.join(L)

def build_partners():
    PA = json.load(open(SRC/'partners.json'))
    L = ["# Partners\n", PA.get('rule','') + "\n", "## Standing rules\n"]
    L += [f"- {r}" for r in PA.get('standingRules', [])]
    L.append("\n## Programs\n")
    for pr in PA['programs']:
        L.append(f"### {pr.get('short', pr.get('id'))} — {pr.get('posture')}\n\n{pr.get('whatItMeans','')}\n\n"
                 f"**Your move.** {pr.get('repMove','')}\n\n**Watch for.** {pr.get('watchFor','')}\n")
    L.append("## Companies\n")
    L += [f"- **{c['company']}** ({', '.join(c.get('programs', []))}) — {c.get('line','')}" for c in PA['companies']]
    return '\n'.join(L)

if __name__ == '__main__':
    main()
