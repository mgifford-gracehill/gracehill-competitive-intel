# Competitor record schema — v2

One record per competitor, whether or not a battlecard was ever written. A battlecard is a
*rendered view* of a record, never a separate document.

## Field ownership

- **machine** — research pipelines may overwrite freely. Carries `verifiedOn` + `source`.
- **human** — only a person changes these. Research may *propose* but never overwrite.
- **derived** — computed at build time.

```jsonc
{
  "id": "kebab-case",                    // stable key, never changes
  "name": "Yardi Aspire",                // machine
  "aka": ["Aspire LMS"],                 // machine — other names reps may hear
  "parent": "Yardi Systems",             // machine
  "website": "https://…",                // machine

  // ---------- CLASSIFICATION (the "what is this" answer) ----------
  "toolCategory": "Learning management system",   // human — what KIND of tool this is
  "ciCategory": "Indirect",              // human — Direct | Indirect | Replacement | Potential | Status Quo | Partner-Competitor
  "tier": "Tier 1",                      // human — Tier 1 | Tier 2 | Tier 3 | Watchlist

  // ---------- THE COMPETE VERDICT (shown first, always) ----------
  "verdict": {
    "stance": "Compete",                 // human — Compete | Partial overlap | Do not compete | Partner
    "line": "Bundled into the PMS your buyer already pays for. Compete on content depth and regulatory currency, never on platform breadth.",  // human — ONE sentence a rep reads in 5 seconds
    "doInstead": null                    // human — required when stance is "Do not compete" or "Partner": what the rep should do instead
  },

  // ---------- OVERLAP ----------
  "overlaps": [                          // human
    { "product": "Training", "degree": "High" },      // High | Partial | None
    { "product": "Policies", "degree": "High" }
  ],

  // ---------- FACTS (machine-owned, each dated) ----------
  "snapshot": {
    "hq":        { "value": "Santa Barbara, CA", "source": "https://…", "verifiedOn": "2026-08-11" },
    "founded":   { "value": "1984", "source": "…", "verifiedOn": "2026-08-11" },
    "ownership": { "value": "Private", "source": "…", "verifiedOn": "2026-08-11" },
    "size":      { "value": "8,000+ employees", "source": "…", "verifiedOn": "2026-08-11" },
    "funding":   { "value": null, "source": null, "verifiedOn": null }
  },
  "pricing": { "value": "Quote-only, not published. Tiered Plus/Premium.", "source": "…", "verifiedOn": "2026-08-11" },
  "positioning": { "value": "How they describe themselves, in their words.", "source": "…", "verifiedOn": "2026-08-11" },

  // ---------- SALES CONTENT ----------
  "strengths":  [ { "text": "…", "source": "…", "verifiedOn": "…" } ],   // machine — honest, sourced
  "gaps":       [ { "text": "…", "source": "…", "verifiedOn": "…" } ],   // machine — MUST be sourced; no subjective judgments
  "whyWeWin":   [ "…" ],                 // human — approved claims only
  "askThis":    [ "…" ],                 // human — trap-setting questions, phrased for a live call
  "objections": [ { "objection": "…", "response": "…" } ],  // human
  "doNotSay":   [ "…" ],                 // human — claims that are false, unsourced, or legally risky

  // ---------- FEATURE MATRIX ----------
  "features": {                          // machine — keyed to the canonical feature ids in features.json
    "multifamily-specific-content": { "support": "Partial", "note": "General multifamily plus PMS product training.", "source": "…", "verifiedOn": "2026-08-11" }
    // support: "Yes" | "No" | "Partial" | "Unknown"   —  Unknown is a real answer. Never guess.
  },

  // ---------- FRESHNESS ----------
  "health": {
    "lastFullReview": "2026-08-11",      // machine
    "confidence": "High",                // derived — from source count and age
    "owner": null,                       // human
    "autoUpdated": false,                // derived — true if a pipeline changed a field since last human review
    "pendingReview": []                  // derived — proposed changes awaiting approval
  },

  "news": [ { "headline": "…", "date": "…", "url": "…", "impact": "…" } ],  // machine — last 90 days
  "sources": [ { "title": "…", "url": "…", "retrievedOn": "…" } ]           // machine
}
```

## Rules

1. **Unknown is a valid answer.** Never infer a feature value, a price, or a headcount.
2. **Every `gap` needs a source.** Subjective judgments ("support is poor", "reporting is unreliable")
   are not gaps — convert them to a question in `askThis`.
3. **No absolute negatives** unless a named public source supports it. "They have no X" is the single
   highest-liability sentence a rep can say.
4. **`verdict.line` is the product.** If a rep reads nothing else, they read this. One sentence.
5. **Grace Hill companies are not competitors** — Edge2Learn, Ellis Partners, EPMS, HelloData, Realync,
   SkillCat, Visto, Kingsley. If one appears, it is an error.
6. Auto-applied machine fields render with an "unverified" badge until a human reviews.
