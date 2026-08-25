# Why the Fair Housing claim was wrong

**August 24, 2026 — response to the Yardi Aspire review**

Ruth, you were right, and your instinct about the mechanism was right too. It was combining
separate facts in synthesis. Here is the whole trace, because the *how* matters more than the fix.

---

## What the source actually says

The Yardi Aspire course catalog page lists these on adjacent lines:

> Federal Fair Housing Compliance **(Approved in the State of Texas.)**
> Human Trafficking Awareness **(Approved in the State of Florida)**

Two courses. Two different subjects. Two different states. Correctly separated on the page.

## What the app was saying

> "fair housing courses approved by **TDHCA and the Florida DBPR** that **qualify for continuing
> education credit**"

**One true fact, carrying three separate inventions.**

| What was claimed | What the source says | Verdict |
|---|---|---|
| Texas approval for fair housing | "Approved in the State of Texas" | **True** |
| Florida approval for fair housing | Florida is the **human trafficking** course | **Conflated** — migrated across two adjacent list items |
| Approved by "TDHCA" and "the Florida DBPR" | Neither acronym appears anywhere on the page | **Invented** |
| "Qualify for continuing education credit" | No CE claim anywhere on the page | **Invented** |

## Why it happened — the specific mechanism

Three failure modes stacked, and they are worth naming separately because they need different controls.

**1. Adjacency read as shared attribute.** Two list items sat next to each other. Summarizing
collapsed them into one category and Florida came along. You can see both versions in the record
itself: one field kept the separation correctly — *"Texas fair housing; Florida human
trafficking"* — while the field right next to it had merged them. Same record, same run. That is
the fingerprint of a synthesis error rather than a bad source.

**2. Slot-filling a plausible authority.** "Approved in the State of Texas" implies *some* agency
approved it. The agency name was supplied from general knowledge rather than from the page.
TDHCA happens to be roughly right — they do run the Texas approved-trainer directory. "Florida
DBPR" is a real Florida agency attached to an approval that does not exist.

**This is the most dangerous of the three**, and it is the one that gets a rep hurt. An invented
regulator makes a claim read as *more* rigorous than the truth it replaced. "Approved in Texas"
sounds like marketing copy. "Approved by TDHCA and the Florida DBPR for CE credit" sounds like
someone did the work.

**3. Silent propagation.** The conflation happened once, in a feature note. It then flowed into
**eight rep-facing fields** — strengths, gaps, why-we-win, do-not-say, two feature notes, and,
worst of all, a question a rep asks a prospect out loud: *"For the states your portfolio operates
in beyond Texas and Florida…"* A prospect who knows their vendor's approvals hears that and the
rep has lost the room.

---

## What is fixed

**The record.** All eight fields now say what the source says. And the corrected version is a
*better* competitive fact than the invented one:

> Texas lists them as an approved fair housing trainer — TDHCA added **Yardi eLearning** to the
> approved fair housing trainers directory, announced **June 2017**. That is the only fair housing
> state approval they publish.

Two details that summarizing had thrown away: the approval is **nine years old**, and it names the
**predecessor product**. Nothing published confirms it carries to Aspire. That is a real question
for a rep to raise, and it only exists because we went back to the primary source.

**The control.** A new detector — any rep-facing line naming a regulator, agency, statute or
docket must carry a URL, or the build fails. Not because a citation makes a claim true, but
because **an invented agency has no page to link to.** A fabricated authority cannot survive the
requirement to cite it.

I validated this the only way that counts: re-injected the exact original text and confirmed the
detector fires and blocks the build. A control that would not have caught the bug it was written
for is worthless. It also required one fix along the way — the first version tested the whole
sentence for hedging language, so *"approvals are Texas (TDHCA) and Florida (DBPR); no broader
list is published"* passed, because the honest second clause covered for the invented first one.
It now judges clause by clause.

**Five standing rules**, now in the policy file every automated task reads:

1. **Never name an authority the source does not name.** If the page says "approved in the State
   of Texas," write that. Do not supply the agency because one plausibly exists.
2. **One source line, one claim.** Adjacency in a list is not evidence of a shared attribute.
3. **Date and name the artefact.** A 2017 approval under an old product name is a different fact.
4. **If it names a regulator, it carries a URL.** Must-fix, enforced at build.
5. **Absence is the safe form.** "No other state approval is published" is defensible. "Approved
   in 12 states" is not, unless twelve are listed.

---

## Your bigger point, which is the more important one

> *"I'm a little concerned that a rep won't be able to distinguish a sourced Grace Hill fact from
> something the AI inferred when both are presented with the same level of confidence."*

This was the actual defect. The Fair Housing error is a symptom.

Every strengths and gaps line now carries one of two markers, and **there is no unlabelled state**:

- **SOURCED** — click it, and the page it came from opens. 761 of 798 lines.
- **OUR READ** — no source attached. Useful for shaping a conversation, not for repeating to a
  buyer as a published fact. 37 lines, about 5%.

Previously a source link appeared when a source existed and *nothing* appeared when one did not,
so an unsourced line and a sourced line looked identical. Making the absence visible is the whole
fix. Those 37 lines are now the work queue rather than a hidden liability.

---

## On reporting: use "Something wrong here?"

Please switch to the in-tool button, and here is the honest reason it is better than Slack for
this — not that Slack is a burden, but that the button captures **which record and which field**
you were looking at. Your Yardi note took real forensic work to trace back to specific fields;
the button would have handed me the location. It routes to the same place and nothing gets lost.

Keep using Slack and the doc for the *pattern* observations, though. The button is good at "this
line is wrong." It is not good at *"the system does not know which sources are authoritative and
how far it may infer from them"* — which is the observation that actually changed the
architecture, twice now. Both of your reviews have done that, and neither would have fitted in a
form field.
