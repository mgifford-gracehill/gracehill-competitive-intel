# Grace Hill Competitive Intelligence

Internal competitive intelligence for sales and customer success. Live at
**ci-gracehill.com** behind Cloudflare Access.

## What this is

A single self-contained HTML file — all CSS, JavaScript, data and the logo inlined, no
external requests — built from JSON in `data/` by `build.py`.

## Build and publish

```
python3 build.py          # runs the editorial gate, builds, writes public/index.html
```

`public/` is the deploy directory. It is committed on purpose: Cloudflare Pages serves it
with no build command, so a push is a deploy.

## The editorial gate

`audit.py` runs inside every build and blocks it on must-fix findings. Each detector exists
because something went wrong once — a fabricated regulator, a promised regulatory currency
our policy refuses to promise, an unshipped capability leaking to the field. Read the header
comment on each before changing one.

```
python3 audit.py          # detail on every finding
python3 sme-queue.py      # what needs the SVP of Content, ranked and capped
python3 weekly-report.py  # what changed this week, and what feedback is unanswered
python3 build-skill.py    # repackage the data as a Claude skill
```

## Who approves what

`policy.json` is the authority. The rule in one line: **the direction of a change decides who
approves it.** Changes toward caution apply and get reported; changes toward confidence wait
for the VP of Product Marketing. Content-truth changes route to the SVP of Content.

`data/claim-hierarchy.json` decides how much detail a claim carries.
`data/evidence-hierarchy.json` decides what a piece of evidence is good for.
`data/gh-conflicts.json` records where our own sources disagree, and which won.

## Data

| File | What it holds |
|---|---|
| `data/competitors.json` | 98 competitor records |
| `data/gh-baseline.json` | Grace Hill capability claims, sourced |
| `data/partners.json` | Partner programs. Partners compete; partnership is context |
| `data/pitch.json`, `data/messages.json` | The company pitch and message by deal type |
| `data/news.json` | Weekly feed. Refreshed by the Sunday sweep |

## Setup

See `SETUP-AUTO-DEPLOY.md` for GitHub and Cloudflare Pages.
