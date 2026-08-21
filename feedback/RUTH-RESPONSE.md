# Response to Ruth's CI stakeholder review

**Reviewed:** August 20, 2026 · **Responded:** August 21, 2026
**Scope:** every point raised, with what changed, what is queued, and what is still open.

---

## The headline: you diagnosed it correctly

Your central point — that this reads less like a competitor-research problem and more like the system not having enough context about *us* — was right, and it changed what we built next rather than just what we edited.

Two things came out of it.

First, we wrote your context down as a first-class input. There is now a `Grace Hill context` layer in the app holding the six framing statements from your review, each with an owner and a confidence level rather than a source URL, because they came from SME judgment rather than from research. They are not facts to cite. They are the framing that decides what gets emphasized and what gets over-claimed, which is exactly the gap you identified.

Second, and this is the bigger change: **we connected AdminHQ.** Grace Hill ships an MCP connector over the AdminHQ policy and training corpus — the same source Ask Gracie™ draws on. That means the Grace Hill side of every comparison can now cite a policy number and a URL instead of a marketing page. Twenty capability records have been rewritten against it so far. Several of them were wrong, and two of them were wrong in ways a rep would have been caught on.

You said you did not want to load everything without knowing what the system needs. That instinct saved us from a worse version of this. What the system needed was not more documents — it was an authoritative source it could check itself against, plus your framing to know what mattered. Both now exist.

---

## Docebo page — the specific corrections

### "Docebo wins enterprise platform bake-offs"

**Removed.** You were right that nobody here talks like that. It has been cut from the verdict line, and also from a derived panel that had its own copy of the phrase — which is worth noting, because that second copy is why my first fix did not fully take. Anything that reads as a claim about how a competitor performs is now a claim field, which means it cannot be auto-updated by a sweep and requires a person to approve it.

### "Regulatory currency is Grace Hill's obligation, contractually and operationally"

**Removed, and made a standing rule.** This was the most serious thing in your review — it was sitting in approved rep-facing why-we-win copy. It is gone, and there is now an explicit do-not-say entry on the record: *"Do not say Grace Hill is contractually responsible for a customer's compliance."* That phrasing is now blocked at the editorial-rules level, not just fixed on one page.

### "Who is accountable if a fair housing course in your LMS is out of date when a claim lands?"

**Removed.** Agreed it was more confrontational than we want sellers to be, and it invited a legal conversation we do not want to be having. The replacement question is about how they currently learn a course has gone stale, which gets to the same gap without the implied threat.

### "Every fair housing and state compliance course from somewhere else"

**Rewritten, and the framing behind it changed.** You said this oversimplified both our value proposition and our state-specific content, and that the positioning should have centered on broader property-management-specific and role-specific content. That is now one of the six context statements — *Fair Housing is a major strength, but our value is broader* — and it is applied to the Docebo positioning rather than just patched there. Leasing and maintenance role-specific content is named.

### SCORM and xAPI

**Corrected — and it turned out we were wrong in both directions.** You said the "we do not license our courses as SCORM" line was not completely accurate because exceptions and legacy situations exist. Correct, and that caveat is now on the record.

But the inbound side was also understated. Our record said *"xAPI is not confirmed."* AdminHQ Policy 3000 confirms SCORM 1.2, SCORM 2004 3rd and 4th Edition, xAPI, cmi5, and AICC in HACP 2.2, 3.5, and 4.0. It also documents that SCORM 2004 **2nd** Edition is not supported and that Articulate defaults to it, so an Articulate export needs a specific variable set before it will load. The record moved from Partial to Yes, with the version list and the authoring-tool caveats attached. A rep can now answer a technical SCORM question completely.

Source: Create a Course | 3000, and Add and Edit Content Vault Items | 3113.

### Bilingual and Spanish

**Rewritten with the distinction you asked for, plus two limits we did not have.** The record now separates fully translated Spanish courses from the Language Support Tool explicitly, and says which one to ask about. AdminHQ added two things we were missing: Interplay courses are English only, and closed captions are not translatable in the player — Spanish courses carry Spanish captions, nothing else does. Both are things a competitor could use, so reps should know them before a prospect does.

One thing still open: our *"110+ Spanish-language courses versus GROW's 75"* line rests on an internal battlecard. AdminHQ names catalog.gracehill.com as the authoritative list, filterable by Spanish and by Language Support Available. **That number should be verified against the catalog before it goes into anything external.** Flagged, not fixed, because it needs someone to count.

Sources: FAQs: Training Content Availability | 125, FAQs: Course Structure & Functionality | 115, Additional FAQs - Training | 300.

### State-specific compliance

**This is now the strongest-sourced part of the record.** Your context statement — *primarily federal, with select state, local, or agency-specific exceptions* — is written into the app. And AdminHQ Policy 110 turns it from a caveat into a citable answer set:

- Washington, DC Human Rights Act course — **no**, our Fair Housing content is federal
- Bloodborne Pathogens — **Federal OSHA only**, not Cal/OSHA
- Safety Series — **Federal OSHA and CDC**, not tailored to individual states
- Florida Human Trafficking in Rental Housing — **yes**, in English and Spanish
- North and South Carolina human trafficking mandates — industry-scoped, so the customer has to evaluate fit
- State fair housing approvals — TDHCA in Texas, DPOR in Virginia

The record now says all of that, with the policy URL. And there is a standing instruction never to present the federal baseline as state coverage.

---

## "What is the source of truth for the Grace Hill side?"

This was the right question and the answer at the time was unsatisfying. Here is the current answer, in priority order:

1. **AdminHQ, via the MCP connector.** Authoritative for product capability, technical configuration, compliance coverage, and release history. Cites a policy number and URL. This is new since your review.
2. **Public release-note PDFs** on info.gracehill.com — the most citable form of what shipped when.
3. **The Confluence PerformanceHQ space** — how things actually work internally.
4. **#product_help** — the human correction layer on top of Ask Gracie™.
5. **Jira**, for roadmap direction only, with a tight filter and a redaction pass. Not synced, deliberately: the discovery project names customers with assignment counts throughout, and carries internal metrics that must never surface.

**The Sources tab now shows the Grace Hill side, not just competitor sources.** That was a real gap and you were the one who found it.

There is also now a weekly job pointed at us rather than at competitors. Every Sunday it combs AdminHQ release notes and spot-checks the eleven Grace Hill claims most likely to drift — SCORM versions, API availability, the Ask Gracie™ limitations, the Intelligence+ category count, survey channels, shop windows, policy versioning. It reports only what changes what a rep can say, and it stays silent otherwise.

### On offering more Content source material

Yes, and here is what would help most, in order:

1. **The nuances and exceptions list.** You mentioned *different content types and programs are designed for different learning needs rather than being interchangeable.* That one is in as a context statement but thin. What we need is the actual distinction — when a Spark is the right answer versus a full course versus a Booster versus a pathway — because right now the app can name the products but cannot tell a rep which one to position.
2. **The state, local, and agency-specific exception list.** AdminHQ answers this case by case, which is good for a specific question and bad for a comparison table. A canonical list would let us stop answering it one policy at a time.
3. **Anything where you would push back on how we currently describe Content.** Two of the six context statements are yours in your words; the other four are my paraphrase of your review and should be checked.

What we do **not** need is bulk documents. AdminHQ covers the documentary layer well. What it cannot give us is judgment about emphasis, which is the thing only you have.

---

## The other Docebo page comments

**"When it comes up" felt repetitive.** Confirmed mechanically, and worse than you thought. Two of its fields were byte-identical to content already on the page, and **55 of 98** panels were auto-derived rather than written. The section is now suppressed entirely on any record where it is derived, so it only appears where someone actually wrote something specific. That removed it from the Docebo page.

**"About them" felt light.** Agreed, and this is the one item where the honest answer is that it is still light. It is on the list, and AdminHQ does not help here — this needs competitor research depth, not Grace Hill context. Not fixed.

**SPICED Pain too narrowly centered on Fair Housing.** Agreed, and it followed directly from the over-indexed positioning. With the broader-than-Fair-Housing framing applied, the Pain entry now leads with role-specific content depth and reaches Fair Housing as one instance rather than the whole argument.

**Us vs Them, and reducing capabilities to Yes/Partial/No/Unknown losing nuance.** This is the concern I take most seriously, because you are right that an error here propagates across the comparison set rather than sitting on one page. Two changes. Every capability now carries a note field that is as long as it needs to be, so the four-way value is a filter rather than the answer — and the notes are where the nuance lives. And support values now move *down* as readily as up: three records were downgraded from Yes to Partial this week on AdminHQ evidence, including two where our previous wording claimed more than the documentation supports. Anything moving in the direction that flatters us is queued for approval rather than applied.

---

## Explore

**By persona — content feels generic.** Fair. Partially addressed: the four audience pain sets from the discovery deck are now in, using role titles rather than invented persona names, each with five pains and the live question to ask. Still needs your positioning context to get specific rather than plausible, which is a real remaining gap.

**By product — how are the four classifications determined and maintained?** This was a governance gap, not a data gap, and it is now answered on the page. There is a card explaining the test in order (partner status outranks overlap; overlap plus live-deal naming is head-to-head; overlap without deal evidence is sometimes-in-the-room; different job is not-our-fight), what moves a label (only deal evidence or a relationship change), and the fact that **the label is a claim field** — nothing changes it automatically, a person approves every move. Partner status now matches on company *and* parent, so a new Yardi or Entrata product inherits the warning rather than waiting for someone to remember. That caught 13 records, not the 9 that had been hand-listed.

**Compare features may be the most valuable part.** Agreed, and see the Us vs Them answer above — that is where the AdminHQ work went first, for exactly the propagation reason you named.

**By outcome — "one minimizes risk, four serve NOI" is too clean.** Fixed. The frame now says these are entry points rather than boundaries, that risk and compliance is the one that gets funded on its own terms while the other four tend to be argued in NOI terms, and that in practice they run together — a maintenance issue sitting too long is a resident experience problem, a reputation problem, and a renewal problem at once. It also now says explicitly that this is our internal organizing language, not a customer-facing framework, and to use the customer's words when they differ.

**By problem was least useful — "+40 or +45 competitors" does not narrow anything.** Fixed, and this was a good catch about the tool being actively unhelpful rather than merely verbose. It now shows at most six, ranked head-to-head first and then by who buyers are actually naming in live deals, with a note saying so. The rest are reachable by product line, which is the right way to browse a long tail. The dump is gone.

**Language that sounds like generated sales copy and makes nuanced things absolute.** Both lines you quoted are rewritten:

- *"Storage is not the problem — evidence is"* → "Most operators can already store a policy. The harder part is showing who read which version, and when."
- *"A score without a comparison set means nothing, and a finding without an assignment changes nothing"* → "A score is easier to act on with a comparison set behind it, and a finding tends to stall without an owner."

The pattern behind both was a rhetorical construction that trades accuracy for memorability. A separate voice pass went further: 214 corrections for missing trademark marks on Ask Gracie™, HelloData®, and Kingsley Index™, and "best-in-class," "seamlessly," "robust," and "leverage" as a verb removed from rep-facing copy. Competitor quotes were left as written, since quoting their marketing is the point.

---

## Still open

Named honestly, because a list of everything-fixed would not be credible.

| Item | Status |
|---|---|
| "About them" depth | Not fixed. Needs competitor research, not Grace Hill context. |
| By persona specificity | Partly fixed. Needs your positioning context to stop being plausible-but-generic. |
| The "110+ Spanish courses" figure | Needs verifying against catalog.gracehill.com before external use. |
| Content-type distinctions (Spark vs course vs Booster vs pathway) | Context statement exists but is thin. This is the highest-value thing you could give us. |
| Four of the six context statements | My paraphrase of your review. Should be checked in your words. |
| 30+ years of benchmarks vs 35+ years of experience | Two different claims sitting one slide apart in the deck. Needs a decision on wording. |

---

## What would help most from you

Three things, smallest first:

1. **Check the six context statements** — roughly ten minutes. Two are yours; four are my reading of your review and may have drifted.
2. **The content-type distinction.** When is a Spark right, when is a full course right, when is a Booster right, when is a pathway right? The app can name them and cannot position them.
3. **Where you would still push back on how we describe Content.** You found things nobody else did, including a legal exposure sitting in approved copy. That is worth another pass once these changes are in front of you.

Thank you for the depth of this. Most reviews of a tool this size come back with a list of typos. Yours came back with the actual problem.
