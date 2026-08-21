# audit.py — Ruth's review as a test suite

Runs automatically inside `build.py` before every build. Also runs standalone.

```
python3 audit.py                    # report
python3 audit.py --emit-allowlist   # write audit-open.json for triage
CI_STRICT=1 python3 build.py        # make must-fix findings fatal
```

## The eight detectors

| Class | Catches | Gate |
|---|---|---|
| `C_obligation` | Grace Hill implying it owns the customer's compliance | must fix |
| `D_fear` | Confrontational or fear-framed question | must fix |
| `A_absolute` | Nuance stated as an absolute, unsourced absolute negative | must fix |
| `H_no_note` | A Yes/Partial/No/Unknown value with no note to hold the nuance | must fix |
| `B_aphorism` | Punchy claim-field line that reads as generated | iterative |
| `I_jargon` | Jargon from the brand voice and Punchy lists | iterative |
| `F_fairhousing_heavy` | Over-indexed on Fair Housing as the differentiator | iterative |
| `G_unsourced_GH` | Grace Hill claim not yet sourced to AdminHQ | iterative |

Must-fix classes share one property: **the cost of being wrong lands on a person outside the room.**

## Two design decisions that make it usable

**Guardrail fields are excluded.** `doNotSay`, `avoid`, `reviewNote` and `languageToAvoid` exist to *prohibit* these patterns, so a match there is the control working. Without this exclusion the absolute-language detector reported 66 hits instead of 11, and a linter that cries wolf gets switched off.

**Reviewed-and-correct hits are allowlisted by content hash.** A detector matches words, not meaning — a sentence can contain "obligation" while correctly stating the obligation is the customer's. Confirmed-fine hits go into `audit-allowlist.json` keyed on `[class, competitor id, field path, sha1(text)[:10]]`.

The hash is the point: **if someone later edits that text, the hash changes and the hit resurfaces for re-review.** An allowlist keyed on the field alone would silently bless whatever replaced it.

## Adding a detector

When the next reviewer finds something new, add a pattern rather than fixing the one record. That is what makes review #2 raise the floor for all 98 instead of fixing record #2.

## Settled policy (2026-08-21)

Two rules that were open questions and are now decided, recorded here so they are not re-litigated:

**Customer-name URLs — cite the page, withhold the link.** A fact whose only source names a Grace Hill customer or prospect in its URL is reported with the link withheld rather than discarded. The name never appears; the competitive point survives. Cycle one of the deep dive lost six first-party sources on a single record by dropping the fact along with the link.

**JavaScript rendering — yes on publicly served pages, never on robots-disallowed paths.** Rendering a page the site serves to any visitor is ordinary reading. A robots-disallowed path is an explicit instruction and is not overridden by any means.

**Legal default is not-cleared.** When a finding turns on contract terms, liability, or redistribution rights, the rep-facing instruction is a hard stop until Legal rules — not carefully hedged wording. Careful wording around an unruled question is still a decision, and it is not ours to make.
