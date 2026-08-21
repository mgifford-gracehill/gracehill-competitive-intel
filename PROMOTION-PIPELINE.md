# Deep research → the app

The link that was missing. Research is evidence; the record is what a rep says. These are
deliberately different things, and `promote.py` is the only bridge between them.

```
data/deepdive/{id}.json        evidence — written by the quarterly deep dive, never by hand
        │
        │  python3 promote.py {id}            show the queue
        │  python3 promote.py {id} --apply    apply FACTS only
        ▼
data/competitors.json          the record — what a rep reads and says
        │
        │  python3 build.py                  (runs audit.py as a gate)
        ▼
the app                        evidence shown in About them, labelled as evidence
```

## The split, and why it is mechanical

**A fact is settled by a source URL.** A price, a version list, a refresh cadence, a dated
model change. `promote.py --apply` writes these itself, stamps `verifiedOn`, and marks the
field `via: deep-dive` so its provenance is visible.

Fields a fact may write: `pricing`, `snapshot`, `news`, `sources`, `health`. Anything else is
refused by the script, not by convention.

**A claim is settled by a person.** Whether a find makes them stronger, what a rep should say
about it, whether a recurring complaint is a real gap. These queue. Auto-applying a claim is
exactly how a plausible-but-wrong line reaches a live call.

## The contradiction check

The split is right but it creates one failure mode, so the script watches for it: an applied
fact can leave an approved claim line stating the opposite. On the first run this fired twice
on J Turner Research — a fact established that entry pricing *is* published, while two `gaps`
entries still read "No pricing is published."

That state is worse than either version alone, because the record now argues with itself in
front of a rep. Contradictions are inserted at the **top** of the claim queue with a suggested
replacement.

## What the first run produced

J Turner Research, deep dive 2026-08-21: **4 facts applied, 20 claims queued.**

Applied automatically:

| Field | Was | Now |
|---|---|---|
| `pricing.value` | "Not published as a rate card" | Published entry price from $30/month, four named tiers |
| `news` | empty | 5 dated first-party items |
| `sources` | 9 | 13 |
| `health.deepDive` | — | 2026-08-21, so the quarterly job skips it for 180 days |

The pricing one is the case for the whole pipeline. A rep working from the old record would
have told a prospect J Turner does not publish pricing. They do, and have for long enough that
the page is mid-redesign.

## Running it

```
python3 promote.py                    # queue for every deep dive on disk
python3 promote.py j-turner-research  # one record
python3 promote.py j-turner-research --apply
```

Idempotent. Re-running `--apply` after the facts are in proposes nothing new, because the
proposals are derived by comparing evidence against the current record rather than from a
changelog.
