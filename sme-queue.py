"""Build the batch for the SVP of Content. Ranked, capped, and quiet when empty.

  python3 sme-queue.py            # show the round
  python3 sme-queue.py --approve tr-fair-housing tr-bilingual   # record sign-off

Why a ranking rather than a list: the first round has 22 items because the Training line was
just rewritten, and the cap is six. Sending 22 is how you turn a subject expert into someone
who skims. Sending the six where subject expertise actually changes the answer is how you get
a real review. The rest are not dropped — they come back next round.
"""
import json, re, sys, datetime, argparse

BASE = 'data/gh-baseline.json'

# What makes an item need HER specifically, rather than any careful reader. These are the
# subjects where she has already caught us being wrong, which is the best available evidence
# of where the nuance lives.
RISK = [
    (10, re.compile(r'\b(approval|approved|accredit|DPOR|TDHCA|NAAEI|CEC|credential)\b', re.I),
     'approvals and accreditation — the exact class that was fabricated on Yardi'),
    (9,  re.compile(r'\b(federal|state[- ]specific|jurisdiction|state coverage)\b', re.I),
     'federal versus state scope — flagged as overemphasized twice'),
    (8,  re.compile(r'\b(Spanish|Language Support|translat)\b', re.I),
     'Spanish versus Language Support — two capabilities people conflate'),
    (8,  re.compile(r'\b(legal monitoring|regulatory (?:change|currency)|compliance responsib)\b', re.I),
     'legal monitoring and where the compliance obligation sits'),
    (7,  re.compile(r'\b(content type|instructional|Spark|Booster|In the Know|Refresher)\b', re.I),
     'content types and instructional approach — designed to differ, not interchangeable'),
    (6,  re.compile(r'\b(\d{2,4}\+?\s*(?:courses|Sparks|modules|lessons)|course count|catalog)\b', re.I),
     'course counts — point-in-time and easy to quote stale'),
]

def score(k, v):
    txt = ' '.join(str(v.get(f) or '') for f in ('lead', 'limitLine', 'lookUp', 'note'))
    hits = [(w, why) for w, pat, why in RISK if pat.search(txt)]
    s = sum(w for w, _ in hits)
    # A claim that is not a plain Yes carries nuance by definition — that is what she reads for.
    if v.get('support') in ('Partial', 'No'):
        s += 4
    # Something we generalized this round: shortening can drop a load-bearing nuance.
    if v.get('formVersion') == '3-line':
        s += 3
    return s, [why for _, why in hits]

def load():
    return json.load(open(BASE))

def queue(G):
    out = []
    for k, v in G.items():
        if not isinstance(v, dict) or not k.startswith('tr-'):
            continue
        reviewed, changed = v.get('smeReviewedOn') or '', v.get('verifiedOn') or ''
        if reviewed and reviewed >= changed:
            continue
        s, why = score(k, v)
        out.append((s, k, v, why))
    out.sort(key=lambda x: (-x[0], x[1]))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--approve', nargs='*', default=None)
    ap.add_argument('--cap', type=int, default=6)
    a = ap.parse_args()
    G = load()

    if a.approve:
        today = datetime.date.today().isoformat()
        for k in a.approve:
            if k in G:
                G[k]['smeReviewedOn'] = today
                G[k]['smeReviewedBy'] = 'SVP of Content'
                print(f'  signed off: {k}')
            else:
                print(f'  ! unknown claim id: {k}')
        json.dump(G, open(BASE, 'w'), indent=2, ensure_ascii=False)
        return

    q = queue(G)
    if not q:
        print('Nothing for the SME this round. Send nothing.')
        return
    show, held = q[:a.cap], q[a.cap:]
    print(f'SME review round — {len(show)} to send, {len(held)} held for next round\n')
    for i, (s, k, v, why) in enumerate(show, 1):
        print(f'{i}. {k}  [{v.get("support")}]   priority {s}')
        print(f'   needs her because: {"; ".join(why) or "content claim not yet reviewed"}')
        print(f'   now reads: {(v.get("lead") or v.get("note") or "")[:190]}')
        if v.get('limitLine'):
            print(f'   limit: {v["limitLine"][:170]}')
        print()
    if held:
        print(f'HELD ({len(held)}): ' + ', '.join(k for _, k, _, _ in held))
        print('Not dropped — they return next round. Say so in the message so nobody assumes they were reviewed.')

if __name__ == '__main__':
    main()
