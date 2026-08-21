# The admin layer — how to change anything in the app

There are two ways to change the competitive intelligence app. Use whichever fits the moment.

---

## 1. The sheet — for structured edits and bulk changes

**`Grace-Hill-CI-Admin.xlsx`** → drop it into Google Drive and it converts to a Google Sheet
automatically. Share it with whoever should be able to edit records.

Eleven tabs, in two groups.

**Records** — one row per thing:

| Tab | Rows | What it's for |
|---|---|---|
| **README** | — | The rules, plus live counts of competitors, stances and open requests |
| **Competitors** | 98 | The main working surface |
| **Our Capabilities** | 77 | The Grace Hill column of the us-vs-them matrix |
| **Grace Hill** | 20 | Our own products and named capabilities (Ask Gracie, Capture Wizard, …) |
| **Requests** | — | Add a competitor, flag an error, ask for a change |

**Content** — one row per field, all sharing the same `key · Section · Field · Value` layout:

| Tab | Rows | What it controls |
|---|---|---|
| **Pitch** | 150 | The 30/3/30 pitch — anchor promise, resolution loop, insight stats, alternatives, perfect world, packaging, objections, language to avoid |
| **SPICED** | 77 | Ask-it-live questions, the deal-review checklist, fit indicators, the Stage 2 exit bar |
| **Plays** | 73 | The 11 demand plays and the two rules |
| **Framework** | 138 | The six categories, the tiers, the four forms of status quo, live-deal cautions |
| **Personas** | 449 | All nine personas — pains, objections, metrics, buying role, competitors they raise |
| **ICP** | 73 | Core profile, fit signals, the four problem segments, market context |

On a content tab, edit the **Value** column and leave **key** alone — the key is how the sync
finds the field, so changing it breaks the link. Numbered rows (`…[0]`, `…[1]`) are list items;
add a row with the next number to add an item to the list.

### The color rule

**Yellow means you own it.** Type in a yellow cell and your text wins permanently — automated
research will never overwrite it.

**Gray means don't touch.** Keys and machine-maintained fields.

### What's yours vs. what research maintains

| You own | Research maintains |
|---|---|
| Stance, tier, competitive category | Company facts, HQ, ownership, funding |
| The verdict line and "do instead" | Pricing |
| All four when-it-comes-up fields | Their published strengths and gaps |
| Win with · Ask this · Do not say | Competitor capability values |
| Overlaps and degree | News and sources |
| Owner and status | Last-reviewed dates |
| Grace Hill capability scores and notes | |

That split is the whole point. Facts go stale and should update themselves. Judgment — whether
we compete, what a rep should say — is yours and should never be silently rewritten.

### Multi-value cells

One item per line (Alt+Enter inside a cell). Overlaps use `Product:Degree`, so:

```
Training:High
Policies:Partial
```

### Adding a competitor

Use the **Requests** tab. Name and a URL is enough — research fills in the rest, and it comes
back with a full record, a verdict and a battlecard.

### Retiring one

Set **Status** to `Retire` on the Competitors tab. It leaves the app; the record is kept in
`data/retired.json` in case you want it back.

---

## 2. Just ask — for anything else

Open a session and say what you want:

> "The Yardi verdict line is too soft — make it sharper."
> "Add Elevate Mystery Shopping."
> "Rilla should be Tier 1, not Tier 2."
> "Refresh the RealPage record, their pricing page changed."

No file, no syntax. Good for one-off corrections and anything that needs judgment or research
rather than a field edit.

---

## Applying sheet edits

Say **"sync the admin sheet."** What happens:

1. The sheet is read and every human-owned field is applied.
2. Open requests on the Requests tab are picked up and worked.
3. Anything in **Notes for Claude** is surfaced.
4. Integrity checks run — the most important being that a competitor marked *Do not compete* or
   *Partner* must have "Do instead" filled in. A rep who opens that card otherwise is left with
   nothing to say.
5. The app rebuilds and is republished.

The sync is idempotent: running it on an unedited sheet changes nothing.

Under the hood it's `sync_admin.py`, which only ever writes human-owned fields.

---

## A note on the guidance quality flag

Every competitor has when-it-comes-up guidance. 43 of 98 are hand-written — all 22 Tier 1
records and all 21 "do not compete" records. The other 55 are derived from that record's own
verdict and gaps, and the app labels them as a starting point rather than approved language.

Rewrite one in the sheet and it's automatically promoted to hand-written. That flag is the
honest measure of how much of the library is actually yours versus scaffolding, so it's worth
watching as a number.
