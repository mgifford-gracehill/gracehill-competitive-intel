"""Assemble the factual base for the Friday beta note. Facts only, no prose.

Run this first on a Friday. It gives you what actually happened, so the note you
write is reporting rather than remembering. Everything here is mechanical: git
for what changed, CHANGELOG.jsonl for why, the data files for the current state.

  python3 weekly-report.py            # last 7 days
  python3 weekly-report.py --days 14

The output is your input. Do not paste it to anyone — it is a worksheet.
"""
import json, subprocess, argparse, datetime, pathlib, collections

def sh(*a):
    try:
        return subprocess.run(a, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        return f'(failed: {e})'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=7)
    a = ap.parse_args()
    since = (datetime.date.today() - datetime.timedelta(days=a.days)).isoformat()
    print(f'=== Week of {since} to {datetime.date.today().isoformat()} ===\n')

    # ---- Why it changed. The only source for cause. -------------------------
    entries = []
    p = pathlib.Path('CHANGELOG.jsonl')
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line: continue
            try:
                e = json.loads(line)
                if e.get('date', '') >= since: entries.append(e)
            except json.JSONDecodeError:
                print(f'  ! unparseable changelog line, skipped: {line[:80]}')
    by = collections.defaultdict(list)
    for e in entries: by[e['kind']].append(e)

    # Tier-2 changes were applied without asking. She has to be able to veto them, so they
    # are pulled out separately rather than buried in the general change list.
    t2 = [e for e in by['changed'] if str(e.get('tier')) == '2']
    print(f'--- APPLIED WITHOUT ASKING — she must be able to veto these  ({len(t2)})')
    for e in t2:
        print(f"  · {e['summary']}")
        if e.get('because'): print(f"      answers: {e['because']}")
    print('  (none this week)' if not t2 else '')
    print()

    for kind, head in (('heard', 'WHAT WE HEARD'), ('changed', 'WHAT WE CHANGED'), ('shipped', 'SHIPPED')):
        print(f'--- {head}  ({len(by[kind])})')
        for e in by[kind]:
            bits = [e['summary']]
            if e.get('who'): bits.append(f"— {e['who']}")
            if e.get('via'): bits.append(f"[{e['via']}]")
            print(f"  · {e['date']}  {' '.join(bits)}")
            if e.get('because'): print(f"      answers: {e['because']}")
            if e.get('records'): print(f"      records: {', '.join(e['records'])}")
        print()

    # ---- Unanswered feedback. The number that matters most in a beta. -------
    # Match loosely: a --because is usually a paraphrase of the heard item, not a copy.
    # An exact-prefix match reported items as unanswered when they had in fact been fixed,
    # which is the one number in this report that must not lie.
    def norm(t): return ' '.join(str(t or '').lower().split())
    answered = [norm(e.get('because')) for e in by['changed'] if e.get('because')]
    def is_answered(h):
        n = norm(h)
        return any(a and (a[:30] in n or n[:30] in a) for a in answered)
    open_items = [e for e in by['heard'] if not is_answered(e['summary'])]
    print(f'--- HEARD BUT NOT YET ANSWERED  ({len(open_items)})')
    for e in open_items:
        print(f"  · {e['summary']}" + (f"  — {e['who']}" if e.get('who') else ''))
    print('  (nothing outstanding)' if not open_items else '')
    print()

    # ---- What changed, mechanically. The backstop if nobody logged. ---------
    print('--- COMMITS')
    log = sh('git', 'log', f'--since={since}', '--pretty=format:  %h %ad %s', '--date=short')
    print(log or '  (none — either a quiet week or nobody committed, check the diff below)')
    print()
    print('--- DATA FILES TOUCHED')
    stat = sh('git', 'diff', '--stat', f'HEAD@{{{a.days} days ago}}', 'HEAD', '--', 'data/')
    print(stat or '  (no data changes recorded in git)')
    print()

    # ---- Current state. The two or three numbers worth reporting. -----------
    print('--- STATE NOW')
    try:
        b = json.load(open('data/gh-baseline.json'))
        claims = [v for v in b.values() if isinstance(v, dict) and 'support' in v]
        sourced = sum(1 for v in claims if v.get('proof'))
        flagged = sum(1 for v in claims if v.get('needsReview'))
        limits = sum(1 for v in claims if v.get('statedLimit'))
        pct = round(100 * sourced / len(claims)) if claims else 0
        print(f'  Grace Hill claims: {len(claims)}  ·  first-party-sourced: {sourced} ({pct}%)  '
              f'·  awaiting approval: {flagged}  ·  carrying a stated limit: {limits}')
    except Exception as e:
        print(f'  ! could not read gh-baseline.json: {e}')
    try:
        C = json.load(open('data/competitors.json'))
        recs = C if isinstance(C, list) else C.get('competitors', C)
        import collections as _c
        plays = _c.Counter(c.get('play') or 'unset' for c in recs)
        print(f'  Competitor records: {len(recs)}  ·  ' +
              '  ·  '.join(f'{k}: {v}' for k, v in plays.most_common()))
    except Exception as e:
        print(f'  ! could not read competitors.json: {e}')
    try:
        f = json.load(open('audit-findings.json'))
        MUST = ['J_customer_named', 'C_obligation', 'D_fear', 'A_absolute', 'H_no_note']
        must = sum(len(f.get(k, [])) for k in MUST)
        it = sum(len(v) for k, v in f.items() if k not in MUST)
        print(f'  Editorial gate: {must} must-fix  ·  {it} iterative')
    except Exception as e:
        print(f'  ! could not read audit-findings.json: {e}')
    print()
    print('Read the beta channel and the form responses before writing. This file only knows')
    print('what somebody logged plus what git saw — it does not know what came in today.')

if __name__ == '__main__':
    main()
