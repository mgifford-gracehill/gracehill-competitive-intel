# Deploy this folder

**Everything in this zip is current as of August 21, 2026.** It replaces every earlier
zip I sent you — you do not need any of them. If you have several lying around, this is
the one with today's date in the filename.

## The three files

| File | What it is |
|---|---|
| `index.html` | The entire app. All CSS, JavaScript, data, and the logo are inlined. No build step, no dependencies, no external requests. |
| `_headers` | Security headers and a 5-minute cache. Cloudflare reads this automatically. |
| `robots.txt` | `Disallow: /` — keeps the app out of search engines. |

Do not rename `index.html`. Cloudflare serves it as the site root because of that name.

## Deploying an update (2 minutes)

You already have the project and Cloudflare Access set up, so this is just a re-upload.

1. Go to **dash.cloudflare.com** → **Workers & Pages** → your CI project.
2. **Create deployment** (or **Upload assets**).
3. Drag in **all three files** from this folder — not the folder itself, the files.
4. Wait for "Success." The live URL updates in under a minute.
5. Open **ci-gracehill.com** in a private window. You should hit the Access sign-in
   first, then the app. If you land on the app without signing in, Access is not
   covering the domain — tell me and I will walk you through it.

## How to tell the deploy actually worked

Open the app and check any one of these. All three are new in this build:

- **A competitor page → "Us vs them" tab.** Detail cells now open with *"Say it this way"*
  in italics on the claims that have approved wording, and a red *"Do not say"* line
  where there is a sentence to avoid.
- **Explore → Compare features → Policies.** There is a new row, *"Ask an AI assistant a
  question about policy content."* Grace Hill is a Yes on it.
- **Explore → Compare features → Platform & AI.** New row, *"Answers limited to the
  customer's own approved content."* Grace Hill is a Partial — that is correct, not a bug.

If you see all three, you are on the current build.

## What changed in this one

- All 18 Grace Hill capability claims you approved are applied, and the review flags are
  cleared and replaced with an approval record showing who decided and when.
- 104 Grace Hill claims, every one citing first-party documentation.
- The Realync stat now always shows both rates: 47% with video engagement, 15% without.
- Recording-consent state list corrected to 14 states, including Oregon.
- Editorial gate: 0 must-fix findings.

## If something looks wrong

The app is one file, so a bad deploy is always fixable by re-uploading the previous one.
Cloudflare keeps every deployment — Deployments tab → find the last good one → **Rollback**.
