# Response to the Yardi Aspire review

**August 25, 2026**

Ruth — every item in this review was right, including your guess at the mechanism. One item
turned out to be right for a different reason than either of us assumed, and that turned out to be
the most useful finding in the document. Point by point, then the structural answer to your
Broader Concern, which is the part that actually mattered.

---

## 1. Fair Housing approvals

You were right that the pairing was wrong, and right that it was combining separate facts. But the
conflation was not on the Grace Hill side.

**Our Fair Housing record was correct the whole time.** It says Virginia DPOR renewed annually and
TDHCA-approved versions with navigation locked, sourced to AdminHQ Policies 100 and 110. Florida
never appeared on our side.

The Texas/Florida pairing was on the **Yardi Aspire** record, as a claim about Yardi. And it was
fabricated. Yardi's catalog page lists these on adjacent lines:

> Federal Fair Housing Compliance **(Approved in the State of Texas.)**
> Human Trafficking Awareness **(Approved in the State of Florida)**

The record had turned that into *"fair housing courses approved by TDHCA and the Florida DBPR that
qualify for continuing education credit."* One true fact carrying three inventions: Florida
migrated across from the human-trafficking line, both agency acronyms appear nowhere on the page,
and the continuing-education claim came from nothing. It had propagated into eight rep-facing
fields including a question a rep asks a prospect out loud.

**The part worth pausing on is why you read it as ours.** Because on the comparison view, our
capability note and theirs sit adjacent with small inline labels, and Florida-plus-fair-housing is
exactly the shape of a Grace Hill fact — we do have Florida content, and we do have fair housing
approvals, just not together. A careful subject expert misattributed it. A rep would not stand a
chance.

That is a design defect, not a data defect, and it is fixed: each side of the comparison detail is
now labelled by name — **GRACE HILL —** and **YARDI ASPIRE —** — on its own indented rule.

Corrected, the fact is *more* useful than the invention: TDHCA lists them in the approved fair
housing trainers directory, announced **June 2017**, under the name **Yardi eLearning** — the
predecessor product. Nothing published confirms it carries to Aspire. Summarizing had thrown away
both the date and the product name.

## 2. State-specific content still overemphasized

Fixed, and the fix is a rep-protection rather than a wording change. The line asking how a
prospect covers jurisdictions beyond Texas now carries our own answer alongside it:

> Know our own answer before you ask it: Grace Hill compliance content is built around federal law
> with a limited set of state, local or agency-specific exceptions, so the honest framing is a
> federal baseline you localize, not fifty state variants.

A question we cannot answer ourselves is a trap we set for our own rep. That is the pattern behind
your point, and it now travels with the question.

## 3. "Grace Hill measures competency, not just completion"

Agreed, too broad. Rewritten to name the actual signals:

> Grace Hill carries signals beyond completion — mystery shop results, resident and employee survey
> results, and in-course knowledge checks. Tie the conversation to those specific signals rather
> than to "competency" as a general claim.

## 4. Seller language beyond what the source supports

All three instances fixed — the auditor line, "jurisdiction-current", and the implied turnaround.
GHU 3816 is explicit that monitoring is ongoing review with action when appropriate and not a
guarantee of immediate change, so the app should not imply a clock.

**Then I made it a detector, and it found four more instances across three other records** —
isolved, Learnie, and PowerDMS all said "kept current" about compliance content. You found one; the
detector found the rest. It is now a must-fix, so a build cannot ship with one.

The isolved one also carried your point 2 without either of us looking for it: *"a fair housing
course written for your states"* — implying per-state courses we do not have.

## 5. Subjective positioning presented as sourced fact

This is the one I would have argued with a month ago and you are right.

Positioning is not the problem — we should keep making competitive judgments. The problem is that
*"the most credible head-to-head LMS in the category"* wore the same clothes as a sourced
capability fact. There are now three visible claim types, and no unlabelled state:

| Marker | Means |
|---|---|
| **SOURCED** | A named source says it. Click it, the page opens. |
| **OUR READ** | Our synthesis from the record. Useful for shaping a conversation, not for repeating as published fact. |
| **OUR POSITIONING** | A competitive judgment we made — a ranking, a characterization. |

The Yardi verdict now reads *"The strongest head-to-head LMS in the category **on our read**"* and
carries a positioning marker saying: *the capability details inside it are sourced; the ranking is
ours.* Same for "one of the deepest content areas" on the Fair Housing record — now *"a deep
content area — that judgment is ours, not a sourced metric."*

Current state across strengths and gaps: **761 of 798 lines sourced, 37 not.** Those 37 are now a
visible work queue rather than an invisible liability.

---

## Your Broader Concern — the five determinations

You listed five things the tool needed a clearer way to determine. That list was better than the
architecture I had, so it is now the architecture. All five are in `policy.json`, which every
automated task reads before it writes anything.

**Which sources are authoritative when they conflict.** Rank decides: GHU, AdminHQ, catalog,
release notes, RFP responses (context only), marketing pages. When two sources of *equal* rank
disagree, rank cannot help — so there is now a conflict register where the disagreement is recorded
and resolved in writing, with the winner named. Three entries are in it, including your recording-
consent state list. **Never average two conflicting sources into a confident middle** — that
produces a number no source supports.

**Current-state versus roadmap versus discovery.** Three states, never interchangeable. Current
state is the only thing a rep may present as capability. Roadmap means "not today" with no date
attached unless the company published one. Discovery — the Jira Product Discovery boards in your
appendix — is somebody thinking, and it is never rep-facing in any form. Worth flagging plainly
since you offered those as sources: they are genuinely useful for *my* context and genuinely
dangerous as rep-facing material, and the rule now says so.

**When a source supports a narrow fact but not a broader conclusion.** The rule is written as a
verb test: when you catch yourself widening a noun — one state to "states", one signal to a
category, a process to a guarantee — stop and write the narrow version. Every example in your
review is an instance of that one move. The narrow version is usually the better sentence anyway,
because it survives the follow-up question.

**When positioning is inference rather than approved claim.** The three markers above.

**How much confidence to show when information is ambiguous.** Ambiguity is shown, not smoothed.
Unresolved conflicts display a caution to the rep with a safe line to use in the meantime — the
HelloData unit count is the live example, where four different first-party figures are on our own
site. It shows on the seven records where it is relevant, not all 98, because a caution on every
page is wallpaper.

Your closing line is the one I would put at the top of this document:

> *"The presentation is polished enough that users may reasonably assume the language has been
> validated, even when part of it is AI-generated synthesis."*

That is exactly what happened. The fabricated version of the Fair Housing claim read as *more*
rigorous than the truth — "approved in Texas" sounds like marketing copy, "approved by TDHCA and
the Florida DBPR for CE credit" sounds like someone did the work. Fluency was functioning as a
credibility signal when it is not one. Every control added this week is a way of making the seams
visible again.

---

## Three things from your appendix

**The Instructional Design Principles policy number.** Your appendix says 3813; it resolves in GHU
as **8313**. Probably a transposition, but worth a five-second check since it is now a cited source.

**The two Jira links are identical.** "Content Opportunities" and "Content Roadmap" point to the
same view. If they are meant to be two different boards, I have only one.

**The RFP folder names a customer.** Both the link and the surrounding note name the account. We
have a hard rule against a customer or prospect name appearing anywhere in this system — prose or
URL slug — so I have not pulled that folder in. If the vendor scorecard and vendor questions are
useful, send them with the account name stripped and I will use them as rank-5 context.

---

## On reporting

Use **"Something wrong here?"** for specific line errors. It captures which record and which field
you were on, which is precisely what took the forensic work here — your note said "repeatedly" and
finding all eight instances meant tracing them by hand.

But please keep using Slack and the doc for the pattern observations. The button is good at "this
line is wrong." It is not good at *"the system needs a clearer way to determine how much inference
it can make"* — and that observation has now changed the architecture twice. Neither of your
reviews would have fitted in a form field, and both were worth more than the individual
corrections inside them.
