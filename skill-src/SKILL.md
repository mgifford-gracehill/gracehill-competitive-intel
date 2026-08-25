---
name: grace-hill-competitive-intel
description: Answer questions and build content using Grace Hill's competitive intelligence — 98 competitor records, Grace Hill's own sourced capability claims, the company pitch, and partner rules. Use when writing or planning anything that touches a competitor or our own positioning: competitive takeover campaigns, battlecards, internal enablement and training, sales plays, comparison content, objection handling, win-loss narratives, launch messaging, or answering "how do we compete with X". Also use when someone asks what Grace Hill can and cannot claim about its own products.
---

# Grace Hill competitive intelligence

The reference set behind ci-gracehill.com, packaged so it can be used in a conversation.

## What is here

| File | What it holds |
|---|---|
| `reference/competitor-index.md` | One line per competitor. **Read this first.** |
| `reference/competitors/<id>.json` | One competitor in full. Read only what you need. |
| `reference/grace-hill/<line>.json` | What Grace Hill can claim, by product line, with sources |
| `reference/pitch.md` | The company pitch, proof points, objections, stories |
| `reference/partners.md` | Partner programs and how to behave in a partner deal |
| `reference/rules.md` | The guardrails, and why each exists |

## How to use it

**Always start with the index, never with the full set.** The competitor files total over a
megabyte. Grep the index for the name, then read only that record.

```
grep -i "yardi" reference/competitor-index.md      # find the id
cat reference/competitors/yardi-aspire.json        # read only that one
```

For a question about what *Grace Hill* does, read the relevant product line from
`reference/grace-hill/`. Training, policies, surveys, reputation, mystery-shopping,
market-data, intelligence-plus.

**Read `reference/rules.md` before writing anything.** It is short, and every rule in it
exists because something went wrong once.

## Reading a competitor record

- `verdict` — the one-line read. `claimType: "positioning"` means it is our judgment, not a
  sourced fact about them. Say so if you use it.
- `whyWeWin`, `askThis`, `doNotSay` — approved rep-facing language. `doNotSay` is a hard stop.
- `strengths` / `gaps` — each carries a `source` URL when it has one. **A line with no source
  is our reading, not a published fact.** That difference must survive into anything you write.
- `features` — capability comparison. `Unknown` is not `No`.
- `health.lastFullReview` — how stale the record is. Say so if it is old.

## What good output looks like

**Building a competitive takeover campaign.** Start from `verdict` and `gaps` for the target,
then `pitch.md` for the proof points and the objection responses. The campaign angle should be
built on their published limits and our sourced strengths — never on a characterization of
their product as bad. Check `partners.md` first: if they are a partner, the angle changes and
some lines are off limits.

**Building internal enablement or training.** Use `askThis` and `objections` as the practice
material — they are the questions and pushback reps actually meet. `whenItComesUp` is the
natural script. Teach the `doNotSay` list explicitly; those are the lines that create exposure.
Include the sourced/our-read distinction in the training itself, because a rep who does not
know which is which will present both with the same confidence.

**Answering "how do we compete with X".** `verdict.line` is the answer. Everything else is
supporting material. Lead with it, then the two or three `whyWeWin` entries that fit the deal.

**Answering "can we say X about ourselves".** Read the product line file. If the claim is
`Partial`, the limit next to it is the thing that matters. If it is `Unknown` or absent, say
we cannot support it rather than reasoning toward a yes.

## Rules that override anything else

Read `reference/rules.md` in full. The four that get broken most often:

1. **Unknown is never No.**
2. **Do not widen what a source says** — one named state is not "state-approved".
3. **Never name a regulator, agency or statute the source does not name.**
4. **Never name a Grace Hill customer or prospect.**

## Freshness

This data is a point-in-time copy. Each record carries `health.lastFullReview`, and news items
carry dates. For anything going to a customer or a large internal audience, check the live app
at ci-gracehill.com or ask Product Marketing before publishing. Say plainly when a fact you are
relying on is undated or old — that is a finding, not a gap to paper over.

Competitive positioning and messaging decisions belong to the VP of Product Marketing. This
skill helps you draft and reason; it does not approve anything.
