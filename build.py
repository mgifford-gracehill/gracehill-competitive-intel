import json, base64, pathlib
A = pathlib.Path('/root/.claude/skills/synced/gracehill-branding-official/assets')
L = lambda n: json.load(open(f'data/{n}.json'))

# Every key the template reads. Keep this list in sync with `grep -o "D\.[a-zA-Z]*" template.html`.
data = {
    'competitors': L('competitors'),
    'features':    L('features'),
    'news':        L('news'),
    'ghBaseline':  L('gh-baseline'),
    'ghIndex':     L('gh-index'),
    'pitch':       L('pitch'),
    'spiced':      L('spiced'),
    'plays':       L('plays'),
    'personas':    L('personas'),
    'icp':         L('icp'),
    'framework':   L('framework'),
    'stack':       L('stack'),
    'heard':       L('heard'),
    'roles':       L('roles'),
    'segments':    L('segments'),
    'pathways':    L('pathways'),
    'committee':   L('committee'),
    'messages':    L('messages'),
    'jtbd':        L('jtbd'),
    'partners':    L('partners'),
    'ghContext':   L('gh-context'),
    # Deep-dive evidence, keyed by competitor id. Evidence, not approved copy —
    # the app labels it as such and a person promotes facts via promote.py.
    'evidence':   json.load(open('data/evidence-hierarchy.json')),
    'conflicts':  json.load(open('data/gh-conflicts.json')),
    'deepdive':    {p.stem: json.load(open(p)) for p in sorted(pathlib.Path('data/deepdive').glob('*.json'))},
    'built':       'August 18, 2026',
}

# Fail loudly rather than shipping a half-empty app.
import re
needed = set(re.findall(r'D\.([a-zA-Z]+)', pathlib.Path('template.html').read_text()))
missing = needed - set(data)
if missing:
    raise SystemExit(f'template.html reads keys the build does not supply: {sorted(missing)}')
empty = [k for k, v in data.items() if k != 'built' and not v]
if empty:
    raise SystemExit(f'these data files loaded empty: {empty}')

# ---- Editorial gate. Ruth's review, as a test suite. -------------------------
# Runs before every build. Must-fix classes print a warning with counts; the
# build still completes so a fix cycle is possible, but the counts are loud and
# a rising number is a regression. Set CI_STRICT=1 to make them fatal.
import os, subprocess
try:
    r = subprocess.run(['python3', 'audit.py'], capture_output=True, text=True, timeout=120)
    findings = json.load(open('audit-findings.json'))
    MUST = ['J_customer_named', 'C_obligation', 'D_fear', 'A_absolute', 'H_no_note']
    must_n = sum(len(findings.get(k, [])) for k in MUST)
    sme_n = len(findings.get('N_sme_queue', []))
    iter_n = sum(len(v) for k, v in findings.items() if k not in MUST and k != 'N_sme_queue')
    print(f'editorial gate: {must_n} must-fix, {iter_n} iterative, {sme_n} awaiting SME  (python3 audit.py for detail)')
    if must_n and os.environ.get('CI_STRICT'):
        raise SystemExit(f'CI_STRICT set and {must_n} must-fix findings remain — see audit-findings.json')
except FileNotFoundError:
    print('editorial gate: audit.py not found — skipping (this should not happen)')

logo = 'data:image/svg+xml;base64,' + base64.b64encode((A / 'GH-CorporateLogo-AllWhite.svg').read_bytes()).decode()
p = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</script>', '<\\/script>')
out = pathlib.Path('template.html').read_text().replace('__DATA__', p).replace('__LOGO__', logo)
f = pathlib.Path('Grace-Hill-Competitive-Intelligence.html')
f.write_text(out, encoding='utf-8')
print(f'built {f} — {f.stat().st_size/1024/1024:.2f} MB · {len(data["competitors"])} competitors · keys: {", ".join(sorted(k for k in data if k != "built"))}')
