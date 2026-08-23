"""Append one entry to the changelog. The Friday report reads this.

Git tells you WHAT bytes changed. It cannot tell you WHY, or who asked. That
gap is the whole reason this file exists: a weekly note to the beta group is
made of causes, not diffs. "Ruth said About them felt light, so we added an
evidence panel" is the sentence people want. Git can only produce "template.html
+142 -18".

  python3 changelog.py heard   "Ruth: About them felt light"        --who "Ruth (SME)" --via "review doc"
  python3 changelog.py changed "Added a deep-dive evidence panel"   --records "docebo,j-turner" --because "Ruth: About them felt light"
  python3 changelog.py shipped "Deployed to ci-gracehill.com"

Three kinds, deliberately. `heard` is input we did not generate. `changed` is
something we did about it. `shipped` is a release boundary. A week with `heard`
entries and no `changed` entries is a real signal worth seeing, which is why
they are separate rather than one blob.
"""
import json, sys, argparse, datetime, pathlib

LOG = pathlib.Path('CHANGELOG.jsonl')
KINDS = ('heard', 'changed', 'shipped')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=KINDS)
    ap.add_argument('summary')
    ap.add_argument('--who', default='', help='who said it (role, never a customer name)')
    ap.add_argument('--via', default='', help='where it arrived: DM, beta channel, form, Gong, audit')
    ap.add_argument('--because', default='', help='the feedback this change answers — links changed back to heard')
    ap.add_argument('--records', default='', help='comma-separated competitor or claim ids touched')
    ap.add_argument('--tier', default='', choices=['','1','2','3','4'],
                    help='approval tier from policy.json. 2 = applied without asking, must be '
                         'reported in the Friday note so she can veto it.')
    ap.add_argument('--date', default='', help='YYYY-MM-DD, defaults to today')
    a = ap.parse_args()

    e = {'date': a.date or datetime.date.today().isoformat(), 'kind': a.kind, 'summary': a.summary}
    for k in ('who', 'via', 'because', 'tier'):
        if getattr(a, k): e[k] = getattr(a, k)
    if a.records: e['records'] = [x.strip() for x in a.records.split(',') if x.strip()]

    with LOG.open('a') as f:
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
    print(f'logged {a.kind}: {a.summary}')

if __name__ == '__main__':
    main()
