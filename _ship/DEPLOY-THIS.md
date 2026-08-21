# Deploy this folder

**Everything in this zip is current as of August 21, 2026 (second build today — this one has the density switch and the Back-button fix).** It replaces every earlier
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

Open the app and check these. All are new in this build:

- **Top right of the header: a `QUICK | FULL DETAIL` switch.** Quick is the default. That
  is the whole point of this build — front-line staff get the important thing at a glance,
  and anyone validating a claim flips to Full detail.
- **A competitor page → "Us vs them".** One line per capability now, with the source link
  and a `DETAIL ▸` toggle. Claims with approved wording open with **Say:** in bold; claims
  with a sentence to avoid show a red **Do not say:** line.
- **A competitor page → "About them".** Three things only: what the research found, what
  changed recently, and what their customers say. Methodology and the rest are behind one
  toggle, and there is a **Download the full report** button at the bottom.
- **Explore → By product.** A ranked list, one line per competitor, head-to-head first —
  not a wall of boxes.
- **The Back button.** Open a competitor, press Back. You should land on the list you came
  from. Previously this dropped you at the sign-in page, because the app never wrote its own
  history entries and the login was the only thing behind it.

## What changed in this one

- Detail collapses instead of being deleted. Nothing that was researched was thrown away —
  it moved behind a toggle, or into the downloadable report.
- Us vs them is roughly a fifth of its former length in Quick view.
- Personas show the pitch, what they're measured on, and who you're up against; goals,
  blockers, and objections are one click away.
- Deep-dive research on screen is the 3–5 findings that change a conversation, plus dated
  movement and customer complaints. The full pass prints to PDF.
- URLs now reflect where you are, so a link to a competitor card can be pasted to a colleague.

## If something looks wrong

The app is one file, so a bad deploy is always fixable by re-uploading the previous one.
Cloudflare keeps every deployment — Deployments tab → find the last good one → **Rollback**.
