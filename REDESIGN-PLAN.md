# Competitive Intelligence app — redesign plan

Everything below serves one rule: **a rep gets one screen, and it answers "what do I say."**
Detail moves behind tabs. Nothing is deleted from the database — it just stops being the first thing you see.

---

## 1. The taxonomy problem — three labels doing one job

Right now every competitor carries three overlapping labels:

| Today | Values |
|---|---|
| Competitive category | Direct · Indirect · Status Quo · Partner · Do not compete |
| Tier | Tier 1 · 2 · 3 · Watchlist |
| Stance | Compete · Partial overlap · Do not compete · Partner |

A rep has to read all three and synthesise. That is the single biggest source of the "list of
factoids" feeling.

### Proposal: one label, four values, named as instructions

| Label | What it means | Count today |
|---|---|---|
| **Head-to-head** | Real overlap, and you will meet them in a live deal. Know the whole card. | ~21 |
| **Sometimes in the room** | A real competitor, but rarely the reason a deal is won or lost. Know the one-liner. | ~55 |
| **Not our fight** | Different job. Never compare — the card tells you how to position around it. | ~21 |
| **Partner** | EliseAI. Confirm posture with your manager. | 1 |

**Stance disappears.** It was saying the same thing as category.
**Competitive category disappears from the interface** but stays in the database, because the
weekly sweep uses it to decide what gets reported.
**Tier stays as a sort order**, not a badge. The list is already ranked by it; a rep does not need
to see "T2" to understand "sometimes in the room."

One label, phrased as what to do, is the whole point.

---

## 2. Start Here — the new landing page

Replaces the current home. Four things, nothing else:

1. **The four buckets above**, as four clickable cards. This is the framework, and it is now the first thing anyone sees.
2. **Search**, prominent.
3. **Browse by outcome** — the five RML pathways (below).
4. **One line on how to use this**, and a link to submit a question.

The competitor table moves to its own tab for people who want to scan the whole list.

**Removed:** the "before you push harder" section, and every reference to where a competitor sits
in the tech stack.

---

## 3. Browse by outcome — what the Sales VP asked for

The second way to search, aligned to the RML outcome model rather than to product names:

| Pathway | Goal | Grace Hill products |
|---|---|---|
| **Risk & Compliance** | Minimize risk | Policies, Fair Housing training |
| **Workforce Optimization** | NOI | Onboarding, role-based training, Pathways, Gracie AI, Mystery Shopping, Employee Surveys |
| **Streamlined Leasing** | NOI | Realync |
| **Resident & Prospect Sentiment** | NOI | Surveys, Kingsley benchmarking, Reputation Management |
| **Market Position** | NOI | HelloData |

Click a pathway → the competitors who play there, the discovery questions that surface it, and the
jobs it maps to. This is the "Operational Excellence" or "Policies" entry point the VP described.

---

## 4. Personas — from nine to four

Drop the nine named personas. Use the four roles from the RML work:

**Marketing · L&D · Operations · Owner/Operator**

Each gets four lines, no more: what they own, what they are measured on, what they will push back
on, and which pathway they buy. Anything longer belongs in the personas deck, not here.

---

## 5. ICP — use the real definitions

Replace the invented ICP text with what the business actually runs on.

**Sales segmentation**
- Enterprise — 8,000+ units
- Mid-Market New Logo — 0–7,999 units, Account Status *Prospect*
- Mid-Market Cross-Sell — 0–7,999 units, Account Status *Active*
- Commercial — Account Industry *Commercial*

**Customer Success segmentation** (units, except Strategic)
- GH Success — under 1,999
- Mid-Market — 2,000–7,999
- Enterprise — 8,000+
- Strategic — top 100 by ARR

**Plus the six outcome segments** from the RML baseline, which are more useful for positioning than
either of the above because they describe what the customer is trying to do:

| Segment | What they want | Customers | Avg products |
|---|---|---|---|
| Compliance Seeker | Reduce legal and operational risk | 1,175 | 1.1 |
| Workforce Maximizer | Manage employee capability and consistency | 397 | 1.8 |
| Market Intelligence Seeker | Better pricing and portfolio decisions | 706 | 1.0 |
| Leasing Streamliner | Occupancy and conversion | 55 | 1.0 |
| Sentiment Seeker | Resident and prospect sentiment | 41 | 1.0 |
| Power User | Two or more of the above | 328 | 2.8 |

The migration paths matter for cross-sell: **five of six pathways end at Power User**, and the
single biggest move is Training-only customers adding Mystery Shopping — 52 of them.

---

## 6. Battlecards — three types, one design system

Klue's guidance is four types by audience. Three fit Grace Hill:

| Card | Length | For | Contains |
|---|---|---|---|
| **Quick card** | 1 page | Live on a call | Verdict, three things to say, three not to say, one question to ask |
| **Deal card** | 2 pages | Prep before a demo or proposal | Quick card + us-vs-them on the contested capabilities only, top objections, what we're hearing |
| **Discovery card** | 1 page | BDRs and early calls | What to listen for, the questions that surface this competitor, when to escalate |

All three use Klue's **Fact → Impact → Act** structure: what is true, why it matters, what to do
about it. Every section answers "act" or it does not appear.

Every card looks identical across competitors — same blocks, same order, same place on the page.
A rep should be able to find the objection handling without reading.

**I will mock two design directions before building all 98.**

---

## 7. Jobs to be done → discovery

The piece that turns factoids into selling. From the JTBD session, ten categories and about thirty
job statements. The useful ones for competitive work:

> When performance issues arise, I want to identify whether the issue is skill, process, or effort
> When managing multiple properties, I need consistency so performance isn't dependent on individual teams
> When regulations or risks arise, I need to prove the organization is compliant
> When leasing performance drops, I need to understand why, fast
> When feedback highlights recurring issues, I want to translate those into training

Rendered as a **"hear this → say that"** table. A rep hears the phrase, the app gives the pathway,
the competitor likely in play, and the response. Not all thirty — the eight or ten that actually
come up.

---

## 8. Search — ranked, not sectioned

Today search returns sections, and Grace Hill content outranks competitors. Changing to:

- **One ranked list**, best match first.
- **Competitors outrank Grace Hill content** at equal score, since finding a competitor is the job.
- Outcome pathways and jobs become searchable, so "operational excellence" and "policies" both work.

---

## 9. Submit a question or a correction

A link from every page. Options, in order of how quickly they work:

1. **A Google Form** — nothing to build, lands in a sheet, feeds the existing Requests tab. Recommended.
2. **A mailto link** to you — simplest, but nothing tracks it.
3. **A Slack workflow** posting into #industry-competitive_intel — good if you want it public.

---

## 10. Natural-language questions — the real option

You already have the piece that makes this possible: **the app runs on a Cloudflare Worker.**

A static file cannot answer questions. But a Worker can hold an API key server-side, take a
question from the page, and answer it against the competitor database — with Cloudflare Access
already in front of it, so only Grace Hill staff can ask.

| Option | Effort | Notes |
|---|---|---|
| **Worker + Claude API** | Half a day, plus an API key and a small monthly cost | Ask "how do I handle Yardi on content freshness" and get an answer grounded in the database. The right answer. |
| **Slack bot in the channel** | Similar effort | Reps ask where they already are. No new tool to learn. |
| **Neither** | — | Search plus good structure covers most of it. Worth trying first. |

Honest view: fix the structure first. A question box on top of content nobody can navigate hides
the problem rather than solving it. But the Worker path is real, and it is unusually cheap for you
because the hosting is already there.

---

## Sequence

1. Taxonomy collapse and Start Here page — biggest readability win
2. Trim: remove stack layer, "before you push harder", stance; shorten personas and ICP
3. Outcome pathways and the hear-this-say-that table
4. Search ranking
5. Battlecard design — two mocks, then build
6. Submit-a-question link
7. Natural-language layer, if you still want it after 1–6
