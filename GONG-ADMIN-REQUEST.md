# Gong configuration request — competitive intelligence

**From:** Mandy Gifford
**Why:** Grace Hill's competitive intelligence app tracks ~98 competitors. Today the "what
are we actually hearing in deals" part comes from whatever someone remembers to post in
Slack. Gong can replace that with real counts and recurring objections, pulled from deals
already in flight — but it needs one configuration change to do it well.

---

## Ask 1 — publish a "Competitive Mentions" brief · *the important one*

The Claude connector can call `generate_brief` against any brief published in our Gong
workspace. Today there are eight: Account health–CSM, Account overview, Contact overview,
Customer overview, Deal health, Implementation Brief, Quick deal review, and Survey Program
Brief. None of them is competitive.

Without one, we have to ask each deal a free-text question and parse prose back out, which is
slower, costs more, and answers inconsistently week to week. A published brief returns the same
structure every time.

**What to create:** a brief type named exactly `Competitive Mentions`, available for **DEAL**
entities, published to the workspace so the API can reach it.

**Suggested prompt for the brief:**

> Identify every competing vendor, alternative solution, incumbent system, or in-house/manual
> approach the buyer mentioned on calls in this period. For each one, report:
>
> 1. The vendor or approach by name, exactly as the buyer said it.
> 2. Whether they are the incumbent, an active evaluation, or a passing reference.
> 3. What the buyer said about it — capabilities, price, satisfaction, frustration.
> 4. Any specific claim they made about that vendor's product, whether or not it is accurate.
> 5. Any objection to Grace Hill raised in comparison to it.
> 6. Whether the buyer indicated a leaning, and toward what.
>
> If no competitor or alternative was mentioned, say so plainly rather than inferring one.
> Do not speculate about vendors that were not named.

**Suggested sections:** Vendors named · Buyer's view of each · Objections to us · Direction of travel

The exactness matters: the connector looks up briefs by name, so `Competitive Mentions` has to
match character for character.

---

## Ask 2 — confirm the connector's scope

Please confirm which Gong workspaces the Claude connector can see, and that it covers the
workspace where the sales team's calls live. If Grace Hill has more than one workspace, we need
the workspace ID or its exact name to pass on every call — otherwise the lookups fail.

Read-only is correct and sufficient. Nothing in this work writes back to Gong.

---

## Ask 3 — only if we want transcript-level search later

The official Gong connector deliberately does not expose call search, transcripts, or keyword
trackers. It answers questions about one CRM account or deal at a time and returns synthesis,
not verbatim text. That is fine for counts and themes.

If we later want *"show me every call where a competitor name was said, across the whole
workspace"*, that needs the Gong REST API directly — which does support call listing,
transcripts, and Trackers — via a small custom MCP server. That is a developer task, not an
admin one, and it would need a Gong API key with call and transcript read scope. Worth knowing
the option exists; not needed to start.

If we go that route, configuring **Gong Trackers** for our competitor names would be the first
step, so we only pull transcripts for calls that actually tripped one.

---

## How the data will be handled

Worth stating plainly, since this reads customer conversations.

- **Nothing customer-identifying reaches the app.** Gong returns named accounts and named
  contacts. Everything is aggregated to patterns and counts before it goes anywhere a rep can
  see it: *"Yardi Aspire came up in 7 deals this month; the recurring objection was content
  freshness."* Never the account, never the person, never the quote.
- **Read-only, weekly, and narrow.** The sweep asks about opportunities in Demo/Solution
  Evaluation with activity in the last seven days — roughly 53 deals a week, not the full
  4,000-deal pipeline.
- **Grace Hill's own companies are excluded** — Edge2Learn, Ellis Partners, EPMS, HelloData,
  Realync, SkillCat, Visto, Kingsley. A first test already surfaced Ellis as a "competitor"
  when it was actually an internal migration to PerformanceHQ, so this filter is not theoretical.
- **No verbatim quotes anywhere.** The connector paraphrases by design, and we keep it that way.

---

## Reference

Gong's own documentation on creating and managing brief types:
https://help.gong.io/docs/create-and-use-account-and-deal-briefs
