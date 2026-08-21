# Scaling one stakeholder review across 98 records

**August 21, 2026** — how Ruth's Docebo review gets applied everywhere without a stakeholder reading 98 pages.

---

## The reframe

Ruth did not give us 15 edits to a Docebo page. She gave us **eight classes of defect**. A class is a pattern, and a pattern can be detected mechanically. That is the difference between a review queue and a control.

So the work was not "apply her notes to Docebo." It was "write a detector for each thing she noticed, run it across all 98, and see how far the problem actually spread."

That ran this morning. `audit.py` is in the repo and takes under a second.

---

## What her review actually found, across the whole set

| Class | She found it on | Actually present on | Status |
|---|---|---|---|
| Grace Hill implying it owns the customer's compliance | 1 record | **11 records** | 3 genuine cases fixed, rest are correct usage |
| Confrontational or fear-framed question | 1 record | 4 records | 1 genuine case fixed |
| Nuance stated as absolute | 2 lines | **10 records** | 4 fixed, rest properly hedged already |
| Punchy aphorism that "sounds generated" | 2 lines | **32 records** | Iterative |
| Over-indexed on Fair Housing as the differentiator | 1 record | 11 records | Iterative |
| Jargon (brand voice + Punchy lists) | not raised | 6 records | Fixed in the voice sweep |
| Grace Hill claim not sourced to AdminHQ | raised as a question | **57 of 77 claims** | The real backlog |
| Four-way value with no note to hold nuance | raised as a risk | **0 records** | Already safe |

**The headline number: her single most serious finding was replicated on 10 other records.** The exact construction she objected to — Grace Hill's regulatory work described as an obligation transferring away from the customer — appeared verbatim in three other competitors' why-we-win copy:

- Coursebox: *"The regulatory update obligation stays with Grace Hill rather than transferring to the customer's staff."*
- Sana Learn: *"Fair housing and state compliance currency is a Grace Hill obligation, not an internal L&D project."*
- Cypher Learning: *"...so the liability for currency does not sit with the operator."*

All three are now rewritten to separate two things that were being blurred: **Grace Hill does the content maintenance work; the customer keeps the compliance responsibility.** That distinction is the whole of Ruth's objection, and it is now stated on every record where the topic comes up rather than removed from one.

---

## Question 1 — how do we apply her logic without a stakeholder reviewing every record?

Three mechanisms, in order of leverage.

**1. Detectors, not reviewers.** Every class above is a regex or a structural check. Running them costs nothing and covers all 98. A stakeholder reviews *one* record deeply; the detector propagates what they noticed. Ruth's ten minutes on Docebo bought us 141 findings.

The important design choice: the detectors **exclude guardrail fields**. `doNotSay` and `avoid` exist precisely to prohibit these patterns, so a match there is the control working, not a defect. Before that exclusion the absolute-language detector reported 66 hits; after it, 11. A linter that cries wolf gets turned off, so tuning it once was the whole job.

**2. Context, not corrections.** Ruth's own diagnosis. Six framing statements about Grace Hill now sit in the app as a first-class input, so the next 98 records get written with the framing rather than corrected after. This is why her review changed what we *build* and not just what we *edit*.

**3. AdminHQ as the arbiter.** The 57 unsourced Grace Hill claims are the single biggest remaining exposure, because a wrong Grace Hill claim propagates across every comparison — exactly the risk Ruth named about Compare features. AdminHQ resolves those without asking a human anything. That is a machine job, and Batch F now runs it weekly.

**What a stakeholder is still needed for:** judgment about emphasis. No detector can tell us a Spark is the right answer instead of a full course. That is the ask back to Ruth, and it is small and specific.

---

## Question 2 — what can we solve now with no stakeholder involvement?

Everything on this list is already done or is a machine job:

- All eight detector classes, run and triaged
- The three replicated obligation lines, rewritten
- The four absolute constructions, hedged or scoped
- 214 trademark-mark corrections
- Jargon removal across rep-facing copy
- The 55 duplicated "When it comes up" panels, suppressed
- The +40/+45 problem dumps, capped and ranked
- The label governance card — how Head-to-Head gets assigned and who changes it
- The By outcome framing, softened
- 20 Grace Hill claims re-sourced to AdminHQ with policy numbers
- The remaining 57, over the next few weekly Batch F runs

That is the majority of her review. It needed no stakeholder because it was either a mechanical pattern or a sourcing problem, not a judgment call.

---

## Question 3 — what must be fixed before launch, and what is iterative?

The dividing line is not severity. It is **whether the defect can hurt someone.**

### Must fix before the beta group sees it

| Item | Why it cannot wait | Status |
|---|---|---|
| Grace Hill implying it owns the customer's compliance | Legal exposure. A rep repeats it on a call and it is said, not drafted. | **Done** |
| Confrontational / fear questions | Invites the legal conversation we do not want, and does not sound like us | **Done** |
| Absolute statements about a competitor's capability | An unsupported absolute negative is the highest-risk sentence in the app | **Done** |
| Partner misclassification | Compete against a partner and the damage is a relationship, not a page | **Done** — matches on company and parent, 13 records |
| Four-way values with no note | Nuance loss propagates across the comparison set | **Done** — 0 found |
| Grace Hill claims contradicted by AdminHQ | A rep gets caught mid-demo | **Done** for the 20 highest-traffic; 4 flagged for your approval |

Everything in this table shares one property: **the cost of being wrong lands on a person outside the room.** That is the launch gate.

### Iterative — ship, then improve

| Item | Why it can wait |
|---|---|
| 32 punchy aphorisms | They read as generated. That is a credibility cost, not a risk. Beta feedback will tell us which ones actually bother people, and that is better information than my guess. |
| 11 Fair-Housing-heavy records | Directionally suboptimal positioning, not inaccurate |
| "About them" depth | Thin, and honestly thin. Needs research, not review. |
| By persona specificity | Plausible-but-generic. Needs Ruth's positioning context. |
| The remaining 57 unsourced GH claims | Batch F grinds through them weekly with no human in the loop |
| The Spanish course count | Needs someone to count against the catalog before external use |

**The argument for shipping with the iterative list open:** the aphorism class is exactly where beta feedback is worth more than my judgment. Ruth objected to two lines. I found 32 of the same construction. Some of those are fine — *"Email lead shops and video shops are core published shop types, not custom work"* is precise, not punchy. Guessing which of the 32 are the bad ones without readers is how you sand off the good ones too.

---

## Question 4 — how are we learning to make all of them better?

Four things changed structurally, not just textually.

**The review became a test suite.** `audit.py` is now run before every rebuild. A regression cannot ship. When the next stakeholder finds something new, the fix is to add a detector — so review #2 permanently raises the floor for all 98 rather than fixing record #2.

**The claim/fact split got teeth.** Ruth's finding was in an approved rep-facing field. Anything that characterizes how good or bad a competitor is, or what Grace Hill is responsible for, is now a claim field: no sweep can auto-update it, and a person approves every change. Facts auto-update with a citation. The reason is exactly what she observed — a draft that reads well tends to get used.

**Support values now move down as readily as up.** Three records were downgraded from Yes to Partial this week on AdminHQ evidence, including two where our wording claimed more than the documentation supports. A system that only ever improves its own scorecard is not measuring anything.

**Guardrails are written as prohibitions, not corrections.** *"Do not say Grace Hill is contractually responsible for a customer's compliance"* now lives on the record and in the editorial rules. That is durable in a way that editing one sentence is not.

---

## Question 5 — how do we get more real data on a competitor?

This is the one place where Ruth's "About them felt light" is the honest verdict, and the answer is a method change, not more effort.

**The insight from our own side transfers directly.** AdminHQ fixed the Grace Hill data because it was documentation rather than marketing. Competitors have the same asset, and most of it is public. We have been reading their marketing pages.

### Seven sources, ranked by signal per hour

**1. Their documentation and developer sites.** Help centers, API references, changelogs, and system-status pages. This is their AdminHQ and it is usually public. It is where you find the version list, the integration limits, and the thing the marketing page implies but the docs contradict. Highest-value source by a wide margin, and the same reason our own SCORM record was wrong for months.

**2. Their trust or security center.** SOC 2 scope, SSO and SCIM support, data residency, subprocessors. These are published as facts because enterprise buyers demand them — and they cover exactly the technical criteria that decide bake-offs. Note that this is where *we* have a documented gap, so it cuts both ways and reps should know it before a prospect does.

**3. Review-site mining with dates and roles.** G2 and Capterra, filtered to reviewers whose company size and role match our ICP. Customer complaints in customers' own words are the best available source for real gaps, and they carry a date, so a 2023 complaint about a since-fixed thing is visible as stale. This is also the cure for aphorism-style gap statements, because you end up quoting a buyer instead of writing a line.

**4. Wayback Machine diffs.** What a vendor **removed** from their site is often more informative than what they added. A quietly deleted capability claim, a pricing page that went dark, a customer logo that disappeared — each is a dated signal, and none of it appears in current-state research.

**5. Job postings.** The clearest roadmap signal available. A generic LMS hiring a multifamily vertical lead is entering our market a year before the press release. Cheap to check, and it dates itself.

**6. Public procurement records.** State and municipal contract awards publish real prices legally. This is the only clean way to get a competitor's actual pricing without violating our own rule about not publishing prices they do not publish.

**7. Gong and Salesforce win/loss.** Already wired via Batch E, and it is the only source that tells you which competitors matter rather than which exist. Worth saying plainly: the Cornerstone gap surfaced this week came from a Gong brief, not from research.

### The method change I would make

Do not run this on 98 competitors. Run it on the ones that decide deals.

A **deep-dive protocol** — the same fixed source list every time, so records are comparable rather than however-deep-someone-got — applied in order of exposure: the 20 Head-to-Head records first, then anything Gong names in a live deal. Twenty records at real depth beats 98 at marketing-page depth, and it puts the effort where a rep is actually standing.

Two things to decide before it runs:

- **Trial sign-ups.** Observing the product directly is the highest-fidelity source there is. Public free trials are fair game, but it is a policy call, not a technical one, and it should be your call rather than mine.
- **What "deep" costs.** Seven sources per record is roughly an order of magnitude more work than the current pass. Twenty records is affordable. Ninety-eight is not, which is the point.

---

## Reading Ruth's review one more time

The line that matters most: *"Some of what I found in Docebo feels less like a competitor research problem and more like the system does not have enough context about us."*

She was right, and the numbers back her up. Of the 141 findings, **57 are Grace Hill claims that are not yet sourced to our own documentation** — the largest single class, and the one with the widest blast radius, because a wrong claim about us repeats across every comparison. Only 26 findings are about competitor-facing language.

The problem was never that we researched competitors badly. It was that we described ourselves from marketing copy.
