# What feeds the Grace Hill side, and what should

Written 2026-08-20, after testing each source rather than assuming.

---

## 1. What the tool uses today — the exact audit

**Competitor side.** Every claim carries a public source URL and a verification date, visible on
each record's Sources tab. This part is sound.

**Our side is two files, and they are not equally trustworthy.**

| File | What it drives | Provenance |
|---|---|---|
| `gh-baseline.json` — 77 entries | Every Yes / Partial / No / Unknown in *Us vs them* and *Compare features* | **75 of 77 carry a public URL** — 68 gracehill.com, 7 hellodata.ai. Two cite internal documents. One is now flagged for SME review. |
| `gh-index.json` — 20 products | The product pages: what it is, why it matters, differentiators, objections, personas | **No record-level source, owner, or review date.** The 123 proof points inside them *do* each name an internal document — playbooks, enablement decks, case-study collections. |

So the honest summary: **our capability answers are sourced; our product prose is not.** The prose
is what a reader hits first, and it is the layer that produced the Docebo errors.

The internal documents named in those proof points are things like "PerformanceHQ Playbook,"
"Grace_Hill_Case_Studies_ROI_Proof_Points," and "Internal Enablement: Release Notes + Sales Talk
Track + Objection FAQ — Intelligence+ Launch." Those are real sources — they were just pasted in
as file names rather than linked, so nobody can check them.

---

## 2. Ask Gracie — what it actually runs on

**Tested, and the answer is better than expected.**

Gracie is live in **#product_help** as a Slack bot, and **it cites its sources.** Every answer
ends with links like:

```
Sources:
• https://adminhq.performancehq.gracehill.com/manuals/18017/policies/1180047
  "Manage Locations Users Accounts"
```

So the original data source behind Ask Gracie is **AdminHQ** — `adminhq.performancehq.gracehill.com`
— structured as *manuals* containing *policies*. Manual 18017 holds admin guides, 18022 holds the
Test Out guides, 19822 holds release notes.

**That is the source of truth you were asking about.** Not a mystery model, a documentation library.

**I can read #product_help today.** No new access needed — it is a public channel and I have it.
What is in there is arguably better than Gracie alone, because the channel is the *human correction
layer on top of Gracie*. The recurring pattern:

- *"So Gracie tells me that we can add Canada properties — is that true?"*
- *"Gracie thinks this may be intentional. Is that correct?"*
- *"Gracie is not clearly certain, nor am I."*

Product managers then confirm or correct. That gives us Q&A pairs with a verdict attached, which is
exactly the nuance the stakeholder review said was missing. It also surfaces roadmap answers, known
gaps, and — usefully — Gracie flagging its own limits: *"here's what the docs tell us, and where
there's a gap."*

**The constraint.** That channel is full of named customers and prospects. Anything pulled from it
has to be aggregated to patterns before it goes near the app, exactly like the Gong pass. This is a
real risk, not a formality.

---

## 3. Jira — not today, and probably not the right source anyway

**Two separate problems.**

First, the Atlassian connector is **currently disconnected** from this workspace. It was available
earlier in this project and dropped out; it is not in the connected server list now. So I cannot
open either of those links.

Second, and more important: **release notes are no longer in Jira.** From #product_help, June 4:

> "We are leveling up how we handle and share Release Notes. Moving forward, we are retiring the old
> process of using a monthly PDF in the PerformanceHQ Resource Center."

They now live in **AdminHQ as policies**, with a `Released` date and an `Impacted Customers` field.
Example: `/manuals/19822/policies/1284214` = "April Release Notes." A Grace Hill CSM skill already
pulls them from there via an `AdminHQ:Search_Policies` tool — so a working access pattern exists in
the org, just not connected to this workspace.

The two links you sent are **Jira Product Discovery** views (`/jira/polaris/projects/GHP/ideas/`).
That is the roadmap and ideas backlog, which is a genuinely useful and *different* thing — what is
coming, not what shipped. Worth connecting for the "is X on the roadmap" questions that come up
constantly in #product_help. But it needs the connector back, and JPD ideas are a different entity
type from Jira issues, so it needs a five-minute test rather than an assumption.

---

## 4. What I would connect, in priority order

**1. AdminHQ. This is the one that matters.**
It is Gracie's own source, it contains both the product guides and the release notes, it is
structured and dated, and a working access pattern already exists in another Grace Hill skill.
Connecting it would let the tool answer product questions from the same library Gracie uses, and
keep the 20 product records current instead of frozen. Ask whoever set up the connector for the CSM
roadmap skill.

**2. #product_help — no access needed, start now.**
I would mine it for three things: corrections where a human overruled Gracie, questions that came up
more than twice (those are the real gaps in our own documentation), and roadmap answers. Aggregated,
never verbatim, no customer names.

**3. Jira Product Discovery — after the connector is back.**
For roadmap answers only. Worth it because "is this on the roadmap" is one of the most common
questions in #product_help, and reps get asked it in deals.

**4. The internal enablement documents already cited but not linked.**
The 123 proof points name real files. Getting those into Drive where the tool can read them turns
123 unverifiable claims into checkable ones. Cheapest large win after AdminHQ.

**5. Salesforce, for two things we are not using it for.**
`Product2.Family` gives the authoritative product list, which would stop the product records drifting
from what is actually sold. Closed-lost reasons would put evidence under "why we lose," which is
currently reasoning rather than data.

---

## 5. On a demo environment — I would not, and here is why

It answers a different question than the one causing errors.

A demo tenant shows what the UI *does*. It cannot tell you that fully translated Spanish courses and
the Language Support Tool are different capabilities, that compliance content is federal-first with
named exceptions, or that we do not assume the customer's compliance responsibility. Every error in
the stakeholder review was that second kind — framing and nuance, not screen behavior. AdminHQ guides
describe intended behavior authoritatively and in text, which is both more accurate and far cheaper
to read than a live environment.

The one case where a demo environment earns its place is **screenshots for battlecards and comparison
pages** — showing rather than describing. That is a real need, but it is a design job, not a data
source, and it should not be the reason we connect anything.

If a live environment ever does become the source, the risk to watch is that a demo tenant is
configured, not canonical. Somebody's demo settings become "how the product works" in the tool, and
that is a worse failure than a missing source because it looks authoritative.

---

# ADDENDUM — 2026-08-20, after Atlassian was reconnected

Everything below was tested live, not inferred.

## The finding that changes the plan: Grace Hill already ships an MCP connector

Confluence page *"Using the PerformanceHQ MCP Tools in Claude"* (PHQ space, page 1523253250)
documents a **PerformanceHQ MCP connector, supported in Claude specifically.** Two of its tools are
exactly what this tool needs:

| Tool | Requires | What it returns |
|---|---|---|
| `Search_Policies` | Policies product | Semantic search across policies, SOPs and rules — excerpts **with source links back to PerformanceHQ** |
| `Search_Training` | Training product | Semantic search across the training catalog — courses with descriptions and source links |

There are thirteen more behind Intelligence+, HelloData and admin roles (training compliance,
survey rankings, mystery shop scores, rental comps, executive overview).

**This is the same class of source Ask Gracie cites.** Gracie's answers link to AdminHQ policies;
`Search_Policies` searches that library and returns the links. Nobody has to build anything — it is
Settings → Connectors → Grace Hill PerformanceHQ, and access is enforced server-side by product
subscription and role.

**Two things to check before relying on it.** First, results are scoped to *your organization's*
content, so what a Grace Hill employee sees is Grace Hill's own tenant — worth confirming that is the
full master catalog rather than an internal instance. Second, `Employees`, `Groups` and `Regions`
need a system administrator role. The [MCP Connector Reference](https://gracehill-app.atlassian.net/wiki/spaces/PHQ/pages/1551368197)
has the full access matrix.

## Where release notes actually live — the definitive answer

Confluence page *"Release Notes Update Guide"* documents the real pipeline:

1. Copy the **Jira** link(s) for the feature
2. Generate the note in Claude with `/release-note-generator`
3. Open **Release Notes** in the AdminHQ **Manuals** table
4. Open the row for the month, click **Create New Revision**

So: **Jira is the input, AdminHQ is the publication.** The two links you sent are the source side of
that pipeline, which is why they read as discovery work rather than finished notes.

There is also a third form: **customer-facing PDFs hosted publicly** at
`info.gracehill.com/hubfs/Customer Facing Hosted Docs/` (e.g. "April 2026 Release Notes.pdf"),
referenced from ticket TCP-344. Those are the *best* source for a competitive tool, because they are
public — quotable without any confidentiality question.

## What the GHP project actually contains

`GHP` = "Grace Hill Portfolio", project type **product_discovery**, ~100 issues of type **Solution**,
with statuses like *4. Problem Validation* and *5. Business Design*. These are forward-looking: problem
definitions, assumptions, knowledge gaps, key features, success metrics.

**Good for:** "is X on the roadmap" — the single most common question in #product_help — and content
currency signals. **Not** a record of what shipped.

## Three hard constraints on automating any of it

1. **Named customers throughout.** Individual accounts appear with assignment counts. Nothing from
   Jira can reach the app or a channel without stripping them, same rule as the Gong pass.
2. **Internal metrics that must never be published.** Per-course client counts, assignment and
   completion volumes, and NPS by course. Publishing "our Hoarding course NPS is 19" would be an own
   goal, and course-level client counts are exactly what our own editorial rules forbid us reporting
   about competitors.
3. **Cost.** Each Solution description runs 4,000–5,000 characters and the API ignores field
   restrictions on this project type, so a full sweep is roughly half a million characters. Any
   scheduled pull needs a tight JQL filter, not a project-wide read.

## Two things worth acting on immediately

**A material competitive fact.** From GHP-1073: *"our NAA partnership ends after Q1 2027."* Visto is
NAA-partnered and sits in our product index. That changes the positioning and belongs in the record
now, not whenever someone notices.

**Direct evidence for the SME's corrections.** Jira repeatedly describes *"Grace Hill's annual legal
monitoring review"* checking courses for regulatory currency, and states the federal-versus-state
pattern plainly — *"mold remains guidance-only at the federal level, while states have begun
introducing their own regulations."* That is sourceable evidence for the two statements we rewrote:
we maintain content against regulatory change, and compliance content is federal-first with named
exceptions. Confluence also has a page titled **"SCORM-Only Experience in PerformanceHQ"** — worth
pointing him at for the SCORM nuance he flagged.

## Revised source priority

1. **PerformanceHQ MCP connector** — add it. Same source as Gracie, returns links, no build required.
2. **Public release-note PDFs** on info.gracehill.com — citable, dated, safe.
3. **Confluence PHQ space** — accessible now, product documentation, PRDs, integration details.
4. **#product_help** — accessible now, Gracie's answers plus human corrections.
5. **Jira GHP** — roadmap answers only, with a tight filter and a redaction pass.
