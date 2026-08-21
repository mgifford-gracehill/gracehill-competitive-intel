"""Deep-dive evidence -> competitor record. The missing link.

A deep dive writes evidence to data/deepdive/{id}.json. That file is deliberately
NOT the record: research is evidence, the record is what a rep says. This script
is the bridge, and it enforces the one rule that matters — facts auto-apply with
a citation, claims queue for a human.

  python3 promote.py                 # show the queue for every deep dive
  python3 promote.py <id>            # one competitor
  python3 promote.py <id> --apply    # apply the FACT class only, never claims

Why the split is mechanical rather than a judgment call each time: a fact is
something a source URL settles (a price, a version list, a refresh cadence, a
dated model change). A claim is something a person decides (whether that makes
them stronger, what a rep should say about it, whether a gap is a real gap).
Auto-applying a claim is how a plausible-but-wrong line reaches a call.
"""
import json, pathlib, sys, datetime

DD = pathlib.Path('data/deepdive')
CPATH = pathlib.Path('data/competitors.json')

# Fields a sourced fact may write. Anything outside this list queues, by design.
FACT_FIELDS = {'pricing', 'snapshot', 'news', 'sources', 'health'}
# Fields that decide what a rep says. Never auto-written.
CLAIM_FIELDS = {'positioning', 'whyWeWin', 'verdict', 'play', 'doNotSay',
                'strengths', 'gaps', 'objections', 'whenItComesUp', 'spiced', 'askThis'}


def load_records():
    raw = json.loads(CPATH.read_text())
    recs = raw if isinstance(raw, list) else raw.get('competitors', raw)
    return raw, recs


def proposals(dd, rec):
    """Compare evidence against the record. Return (facts, claims)."""
    facts, claims = [], []
    when = dd.get('retrieved')

    # --- Pricing. The commonest and most consequential drift: a record that says
    # "no pricing published" while the vendor has since published a rate.
    price_facts = [f for f in dd.get('facts', []) if 'pricing' in f.get('area', '').lower()]
    if price_facts:
        cur = (rec.get('pricing') or {}).get('value') or ''
        published = [f for f in price_facts if any(t in f['fact'] for t in ('$', 'per month', 'per unit'))]
        if published and ('not published' in cur.lower() or 'discloses no rates' in cur.lower()):
            facts.append({
                'field': 'pricing.value',
                'was': cur,
                'now': ' '.join(f['fact'] for f in published),
                'source': published[0]['url'], 'date': when,
                'why': 'Record says pricing is not published. The deep dive found a published rate. '
                       'A rep repeating the old line is wrong on a call.'})

    # --- News. An empty news array on a Head-to-head record is a gap a rep feels.
    dated = [f for f in dd.get('facts', []) if f.get('date', '').startswith('20') and len(f.get('date', '')) == 10]
    if dated and not rec.get('news'):
        facts.append({
            'field': 'news',
            'was': '[] (empty)',
            'now': f'{len(dated)} dated items from the deep dive',
            'source': dated[0]['url'], 'date': when,
            'items': [{'title': f['fact'][:150], 'url': f['url'], 'retrievedOn': f['date']} for f in dated],
            'why': 'Record carries no news. Dated first-party items exist.'})

    # --- Sources. Widening the citation base is always safe.
    have = {s.get('url') for s in rec.get('sources', [])}
    new_urls = []
    for f in dd.get('facts', []):
        u = f.get('url')
        if u and u not in have and u not in {x['url'] for x in new_urls}:
            new_urls.append({'title': f"{dd['competitor']} — {f['area']}", 'url': u, 'retrievedOn': when})
    if new_urls:
        facts.append({'field': 'sources', 'was': f'{len(have)} sources', 'now': f'+{len(new_urls)} new',
                      'source': 'multiple', 'date': when, 'items': new_urls,
                      'why': 'More citable sources behind the same record.'})

    # --- Health. Record the deep dive so the next run can skip it.
    facts.append({'field': 'health', 'was': (rec.get('health') or {}).get('lastFullReview'),
                  'now': when, 'source': 'deep-dive protocol', 'date': when,
                  'why': 'Stamp the deep dive so the quarterly job skips this record for 180 days.'})

    # --- Contradiction check. The fact/claim split is right, but it creates one
    # failure mode: a fact promotion can leave an approved claim line stating the
    # opposite. That is worse than either alone, because the page now argues with
    # itself. Surface it at the top of the queue.
    for f in facts:
        if f['field'] != 'pricing.value':
            continue
        for cf in ('gaps', 'strengths', 'whyWeWin', 'objections'):
            for i, item in enumerate(rec.get(cf) or []):
                txt = item.get('text') if isinstance(item, dict) else (item if isinstance(item, str) else json.dumps(item))
                if txt and ('no pricing is published' in txt.lower() or 'pricing is not published' in txt.lower()):
                    claims.insert(0, {
                        'field': f'{cf}[{i}]  ⚠ CONTRADICTS AN APPLIED FACT',
                        'proposed': f'Currently reads: "{txt[:120]}" — this is now wrong. '
                                    f'Replace or delete. Suggested: "Entry pricing is published '
                                    f'(from $30 per month, four named tiers); per-tier feature '
                                    f'inclusions are not yet detailed on the page."',
                        'why': 'A fact was applied that this approved line contradicts. Until you resolve it '
                               'the record argues with itself, which is worse than either version alone. '
                               'Highest priority in this queue.'})

    # --- Everything below changes what a rep says. Queue it.
    for h in dd.get('highValueFinds', []):
        claims.append({'field': 'strengths or gaps (your call)', 'proposed': h,
                       'why': 'A high-value find. Whether it is a strength, a gap, or neither is a positioning call.'})
    for s in dd.get('roadmapSignals', []):
        claims.append({'field': 'roadmapSignals (new field)', 'proposed': f"{s['signal']} — {s['evidence']}",
                       'source': s.get('url'),
                       'why': 'Direction of travel. Useful to a rep, but it is an inference, not a fact.'})
    for t in dd.get('reviewThemes', []):
        if t.get('frequency') == 'recurring':
            claims.append({'field': 'gaps (candidate)', 'proposed': f"{t['theme']} ({t['source']}, {t['dates']})",
                           'why': 'A recurring customer complaint. Check the evidence base before treating it as a pattern — '
                                  + (dd.get('reviewThemesCaveat') or 'two reviews is not a trend.')})
    for a in dd.get('analystActions', []):
        claims.append({'field': '— decision needed —', 'proposed': a,
                       'why': 'Flagged by the research pass as needing a human.'})
    return facts, claims


def apply_facts(raw, recs, rec, facts):
    for f in facts:
        fld = f['field'].split('.')[0]
        if fld not in FACT_FIELDS:
            print(f'  REFUSED {f["field"]} — not a fact field'); continue
        if f['field'] == 'pricing.value':
            rec['pricing'] = {'value': f['now'], 'source': f['source'],
                              'verifiedOn': f['date'], 'via': 'deep-dive'}
        elif f['field'] == 'news':
            rec['news'] = f['items']
        elif f['field'] == 'sources':
            rec.setdefault('sources', []).extend(f['items'])
        elif f['field'] == 'health':
            rec.setdefault('health', {})
            rec['health']['lastFullReview'] = f['now']
            rec['health']['deepDive'] = f['now']
        print(f'  applied {f["field"]}')
    CPATH.write_text(json.dumps(raw, indent=2, ensure_ascii=False))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    do_apply = '--apply' in sys.argv
    raw, recs = load_records()
    by = {c['id']: c for c in recs}
    files = sorted(DD.glob('*.json'))
    if args:
        files = [f for f in files if f.stem in args]
    if not files:
        print('no deep-dive files found in data/deepdive/'); return
    for path in files:
        dd = json.loads(path.read_text())
        cid = dd.get('competitorId', path.stem)
        rec = by.get(cid)
        if not rec:
            print(f'{cid}: no matching competitor record — skipping'); continue
        facts, claims = proposals(dd, rec)
        print(f'\n=== {dd["competitor"]} · deep dive {dd.get("retrieved")} · confidence {dd.get("confidenceOverall")}')
        print(f'--- {len(facts)} FACTS (auto-appliable, each with a source)')
        for f in facts:
            print(f'  · {f["field"]}')
            print(f'      was: {str(f.get("was"))[:120]}')
            print(f'      now: {str(f.get("now"))[:160]}')
            print(f'      why: {f["why"]}')
        print(f'--- {len(claims)} CLAIMS (queued — a person decides)')
        for c in claims:
            print(f'  · {c["field"]}: {c["proposed"][:150]}')
        if do_apply:
            print('applying facts only:')
            apply_facts(raw, recs, rec, facts)


if __name__ == '__main__':
    main()
