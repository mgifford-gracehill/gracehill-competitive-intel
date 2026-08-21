# Recommended path forward

Grace Hill Competitive Intelligence · prepared for Mandy Gifford · 18 August 2026

---

## 1. Read this first: the partnership problem is bigger than EliseAI

You were right to ask, and it is worse than a missing tag.

The partnerships page lists roughly 40 named partners across six programs — Training, Integration, Survey, Referral/Reseller, Thought Leadership, and Content Creation. Our database has exactly one record marked `Partner`: EliseAI.

Nine records in the database collide with that list:

| Record | Currently says | Grace Hill's actual relationship |
|---|---|---|
| Yardi Aspire | Head-to-head, Tier 1 | Yardi is a listed **integration partner** |
| Yardi Matrix | Head-to-head, Tier 1 | same |
| Entrata Academy | Sometimes in the room | Entrata is a listed **integration partner** |
| Entrata ReputationAdvisor | Sometimes in the room | same |
| ResMan Learning / ResidentIQ | Sometimes in the room | ResMan and Anyone Home (Inhabit) are **integration partners** |
| Knock | Sometimes in the room | listed **integration partner** |
| Funnel | Sometimes in the room | listed **integration partner** |
| Chatmeter | Not our fight | listed **integration partner** |
| EliseAI | Partner | Training **and** Survey partner |

**The fix is not to reclassify them as partners.** Yardi Aspire genuinely is a head-to-head competitor. Both facts are true at once, and that is exactly the landmine: a rep who has read our card and confidently runs down Yardi in a room where the customer runs Yardi PMS — and can see the Grace Hill integration in Yardi's marketplace — has just damaged two relationships in one sentence.

**Recommendation.** Add a `relationship` field, separate from `play`, with the program name and a one-line "what you can and cannot say." It renders as a banner at the top of the competitor page, above everything else:

> ⚠️ **Yardi is an integration partner.** Aspire competes with Vision. The company does not. Compete on Aspire; never characterize Yardi. If the customer runs Yardi PMS, lead with the integration.

Also worth flagging: about 30 partners on that page have no database record at all. Several — Interplay Learning, SkillCat, Rustici, ShopMetrics — sit close enough to our categories that reps will meet them and need to know they are on our side. I would add lightweight partner records for those, marked so they never appear in competitor search results.

**This is the one item I would fix before anything else.** It is the only item on the list where the current state can actively cost a deal.

---

## 2. The organising principle: three depths, not three tabs

Your closing line is the design brief: *give them exactly what they need in a moment, and have the rest if they need more context.*

The research supports it hard. An August 2026 analysis found only about a third of sales teams consistently use the competitive content marketing produces — one director's line was "they mostly freestyle." The same analysis found 47% of battlecards go stale within three months and 82% within six. Klue shipped "Ask Klue" in 2025 specifically because reps were not opening battlecards.

So every screen gets built to a depth, and the depth is declared:

| Depth | Length | When | Where it lives |
|---|---|---|---|
| **The line** | one sentence | mid-call, competitor just named | top of every competitor page, in search results, first thing in every card |
| **The move** | 3 bullets + a question to ask | prepping in the 10 minutes before a call | the "How we win" panel |
| **The record** | everything we know | building a proposal, arming a champion, writing a response | collapsed by default, one click away |

Nothing new gets added to the app that does not declare which depth it is. This is the rule that stops the site drifting back into a list of factoids.

---

## 3. Tabs: six down to four

| Now | Proposed | What happens |
|---|---|---|
| Start here | **Start here** | absorbs Playbook and Competitive Framework entirely |
| All competitors | **Competitors** | Compare becomes a multi-select mode inside this tab, not its own tab |
| Playbook | — | folded into Start here (the pitch, message shift, plays) and into competitor pages (SPICED, who you sell to) |
| Compare | — | becomes a mode |
| By product | **Explore** | by outcome · by problem (jobs to be done) · by product · by play |
| News | **What's new** | weekly watch + competitor news in one feed |

Battlecards stop being a tab and become a button, because that is how they are actually used — you are already on a competitor's page when you want one.

---

## 4. Start here

One page, five blocks, in this order. Everything above the fold is usable without scrolling.

1. **This week's watch** — 3 to 5 lines, auto-populated by the weekend sweep and the Gong pass. "Two deals this month raised Aspire pricing." "RealPage shipped X." Each line links to the record. This is the reason someone opens the tool on a Monday.
2. **The one-paragraph pitch** — what Grace Hill does, in the language the storytelling session settled on: customer is the hero, we are the guide.
3. **The message shift** — Sales vs Account Management, the Corporate Visions frame. Detail in §7 below.
4. **Which battlecard, when** — definitions and best use cases, three rows. Detail in §5.
5. **How to use this tool** — four lines. "Competitor named on a call → search their name, read the top line. Prepping → open the card. Arming a champion → download the PDF."

The old Competitive Framework content — direct vs indirect, tiers, stance — does not survive as a section. It becomes the single `play` label already on each record, and a short "how we categorize" note at the bottom of Start here for people who want it.

---

## 5. Three battlecards

BDR retired. Executive merged into Sales. Approach-to-Market merged into Product.

| Card | Who | The moment | What it is |
|---|---|---|---|
| **Sales** | AE, on a live deal | competitor is in the deal and you have a call tomorrow | Two pages. Their claim vs where it stops short, three traps, the discovery question that exposes the gap, proof, and one exec-level line on why this matters at the portfolio level. The exec merge means the second page carries the NOI/risk framing rather than a separate card nobody downloads. |
| **Product** | AE or SE, in a demo or an RFP | you need to be precise about what they actually do | Feature-by-feature where it is genuinely different, their go-to-market motion, pricing posture, who they sell to and how they land. The Approach-to-Market content sits here because it answers the same question: how do they win, and where does that break. |
| **Account Management** | CSM, on a renewal or an expansion | an existing customer is being courted, or you are cross-selling into a gap | Churn signals, what the competitor offers that we do not, the retention counter, and the cross-sell that closes the gap. Written for someone protecting revenue, not winning it. |

**Download control.** One button on every competitor page — `Download battlecard ▾` — with Sales / Product / Account Management / **All three**. Same control on Start here with a competitor picker, so someone who lands cold can get a card in two clicks.

Each card carries a "reviewed on" date on the footer and a stale flag if it is over 90 days old. Given the 47%-in-three-months number, that flag is not decoration.

---

## 6. Explore by problem

Alongside Explore by outcome, an Explore by problem view built on the twelve jobs to be done already in the data. It reads as the buyer's sentence, not ours:

> *"When performance issues arise, I need to work out whether it is skill, process, or effort."*
> Where it hurts today · What good looks like · Who says this · Which competitors claim this · What we say

The discovery training makes this the highest-value navigation we can build. Ashlee's whole method is: hear the pain, quantify it, then position. Right now a rep who hears a pain has no way into the tool — they can only enter through a competitor's name, which means the tool only works after they have already lost control of the conversation.

**Add to the search box:** searching a phrase a buyer actually said should return the job, the pathway, and the say-this — before it returns any competitor.

---

## 7. The Sales ↔ Account Management shift

You are right that this is the important nuance, and I would give it real space on Start here, as a three-column strip:

| | **Why change** | **Why stay** | **Why evolve** |
|---|---|---|---|
| Who runs it | Sales, new logo | Account Management, renewal | Account Management, expansion |
| The move | unseat the status quo — make the cost of doing nothing concrete | reinforce the decision they already made — do not re-sell, re-affirm | show what is now possible that was not at signature |
| The mistake | using it on a renewal, which tells your customer they chose wrong | using it on a new logo, where there is nothing to reinforce | leading with product instead of the outcome they have not reached yet |

This maps cleanly onto the segmentation already in the data — New Logo gets Why Change, Cross-Sell and CS get Why Stay and Why Evolve — so it can be driven off the existing fields rather than maintained by hand.

---

## 8. Cross-product and the full platform

Two changes, both of which come straight out of the discovery session.

**The five-step chain.** Ashlee's framing was the sharpest competitive argument in either transcript: read → diagnose → prescribe → assign and prove → connect. "One and two are pretty common in a lot of the other areas. Where Grace Hill differentiates is because we do three and four and five."

That belongs on every competitor page as a five-dot strip showing where the competitor stops. A point solution lights up two dots. A PMS lights up two. We light up five. It is one glance, it is honest, and it makes the platform argument without a feature table.

**Best paired with.** On each competitor page, the products that close the gap the competitor leaves — already scoped, still to build. "They can tell you the score. They cannot assign the training that moves it. Elevate + Vision closes that loop."

---

## 9. What the two training sessions change

These were more useful than I expected. Four concrete additions:

**A story field.** Both sessions converge on it, and Ashlee asked for it out loud: *"we should actually build a spreadsheet collectively... little pocket stories that you all can reference for different pain points."* Jay's structure is Situation / Pain / Impact, two sentences each, ending in an open question, roughly two minutes told. Add a `stories` array to the schema, structured to those beats, tagged by pathway and product, surfaced on the competitor page under "when it comes up" and on the job-to-be-done pages. Seed it from the success stories already on gracehill.com — that is where Jay got the Fogelman story.

Gina flagged the gap that matters: stories are easy for Realync and SurveyWorks, hard for policy and training. Worth knowing which shelves are empty before we ask reps to shop from them.

**Hear this / say that, expanded.** Already in the data as eight rows. The discovery session gives us the buyer phrases to add — "why can't we do this with our PMS," "I just want pricing," "I'll follow up with my VP," "we already have a survey vendor." Each with the signal and the response. This is the single highest-traffic thing in the tool if we get the phrasing right.

**Project vs problem.** Ashlee's test — *"a problem is tied to growth, cost and risk; a project is a thorn in my side"* — plus the arithmetic she demonstrated (hours per week × loaded salary → an annual number that justifies the spend). Build it as a small calculator on the job-to-be-done pages: enter hours and headcount, get the number. This is the one place a tool can do something a document cannot.

**Arm the champion.** Dot's question was essentially "I have no brief to hand my champion." The Sales battlecard's second page should be explicitly written for that — the three questions their VP will ask, including "why can't our PMS do this" and "is this another vendor to manage," with the answers written for someone who does not work here.

---

## 10. Klue and Crayon: what we match, skip, and beat

**Match** — the parts that actually drive adoption:

- Fact / Impact / Act structure on every card. We are already close; making it explicit will tighten the writing.
- Crayon's role-based card types. Our three-card split is exactly their pattern.
- Contributor vs consumer separation. You curate; everyone else reads. Already how this works.
- Field intel from call recordings. We have this via Gong and it is the loop Klue charges most for.

**Skip deliberately** — these are where the money goes and the value does not:

- Automated web monitoring across thousands of sources. Reviewers' loudest complaint about Crayon and Kompyte is signal-to-noise on niche competitors. Our weekend sweep, aimed at about 40 names in one vertical, is *better* than a horizontal crawler, not a poor substitute for one.
- Per-card view analytics. It needs their instrumentation. Win rate by competitor comes out of Salesforce for free.
- A browser extension. Klue's is curator-only and nobody consumes through it.

**Where we genuinely beat them:**

1. **Freshness by architecture.** Their 47%-stale-in-three-months problem is a document problem. We maintain records, not cards; cards are generated. Nothing goes stale independently.
2. **Vertical depth.** Klue cannot tell you that Yardi is simultaneously an integration partner, that the buying committee in multifamily runs through a regional manager, or what NOI means to the person on the call. We can.
3. **Our own data.** Gong, Salesforce, the Kingsley Index, 7.3M residents surveyed a year. No platform can import that.
4. **Cost.** Klue entry is reported at $15–20K, enterprise past $100K.

The one thing they have that we do not is Ask Klue — natural language in Slack and Salesforce. That is the same thing you asked for. It is the right next build after this round, and Slack is the right surface, because that is where your team already is.

---

## 11. Sequence

**First — this week**
1. Relationship field and the partner banner. Nine records, plus lightweight records for the unlisted partners.
2. Tabs six to four; Start here absorbs Playbook and Framework.
3. Battlecards consolidated to three, download dropdown, Download all.

**Second — next**
4. Explore by problem, and phrase search hitting jobs before competitors.
5. Message shift strip and the five-step chain on competitor pages.
6. This week's watch wired to the weekend sweep.

**Third — once the shape is settled**
7. Story field, seeded from gracehill.com, opened for submissions.
8. Hear-this/say-that expanded with the discovery phrases.
9. Project-vs-problem calculator.
10. Ask-in-Slack.

---

## 12. Three decisions I need from you

1. **The partner banner wording.** I have drafted "compete on the product, never on the company." If Yardi or Entrata is politically more delicate than that, tell me and I will soften it — but reps need *something* there.
2. **Retire or hide the BDR card?** Retiring is cleaner. Hiding means it is there the day you hire.
3. **Stories — seed or wait?** I can seed 15–20 from the public success stories this week, or wait for Product Marketing, who Jay said are already building revised battlecards and customer stories. Duplicating their work would be a waste; not having stories in the tool is the gap Ashlee named twice.

---

**Sources**

- [Grace Hill Partnerships](https://gracehill.com/partnerships/)
- [Klue — Fact, Impact, Act](https://klue.com/blog/fact-impact-act-the-battlecard-framework-you-need-to-be-using)
- [Klue — Ask Klue](https://klue.com/blog/ask-klue) · [Compete Agent](https://klue.com/compete-agent) · [Measure](https://klue.com/product/measure)
- [Crayon — Modern Battlecard Blueprint](https://www.crayon.co/blog/modern-battlecard-blueprint)
- [MarTech — the first martech category replaced by AI](https://martech.org/heres-the-first-martech-category-replaced-by-ai/) (staleness and adoption figures)
- [G2 — Crayon reviews](https://www.g2.com/products/crayon-crayon/reviews) · [Kompyte reviews](https://www.g2.com/products/kompyte/reviews)
- Grace Hill Sales Discovery Training, 17 August 2026 (transcript)
- Grace Hill Sales Storytelling Training, 18 August 2026 (transcript)
