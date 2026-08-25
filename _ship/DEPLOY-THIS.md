# Deploy this folder

**Everything in this zip is current as of August 26, 2026.** It replaces every earlier
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

- **Start here is short.** Three ways in, this week's watch, then a list of collapsed
  questions. If you see long sections explaining how the tool is sourced and maintained,
  you are on the old build.
- **Explore → all five tabs look the same.** Same row shape everywhere: name, one chip,
  one line, a `+` or `›` to open. By product shows four per line with a **Show N more**.
- **What's new** leads with why it matters; the background is behind a **Background** toggle.
- **Quick / Full detail** now changes a lot. On Explore it is the difference between a
  page you can scan and everything expanded.
- **A competitor page → Us vs them** says **The catch:** in red where a limit applies.

## What changed in this one

- Start here rebuilt as a FAQ — 17,400 characters down to 6,400. Anything about how the
  tool is maintained came out; it is not what a rep needs on a call.
- All five Explore tabs share one row component, so learning to read one teaches you all five.
- By product capped at four per line before a Show-more.
- What's new collapses its background paragraphs.
- The confusing "Say before they find it" heading is now "The catch".
- The Ask button lives only in the top navigation now.

## If something looks wrong

The app is one file, so a bad deploy is always fixable by re-uploading the previous one.
Cloudflare keeps every deployment — Deployments tab → find the last good one → **Rollback**.
