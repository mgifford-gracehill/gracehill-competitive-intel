# Making the app keep itself current

**What I found, and why the obvious plan needs one change.**

A scheduled run gets a fresh, empty cloud container: no app files, no git history, and nothing
it writes survives. All four connectors work and it hits no permission prompts, so it can
*gather* anything — it just cannot *build or publish*.

The fix is to give the app a durable home. But there is a catch I hit while preparing this,
and it decides which route you take:

**A scheduled cloud run has no way to authenticate to GitHub.** No `gh` CLI, no SSH key, no
credential helper, no stored token. So "the task pushes to GitHub and Cloudflare rebuilds"
does not work out of the box. The only way to make a cloud task push is to put a personal
access token in the task's prompt, in plain text, where it sits in your account indefinitely.
**I am not recommending that**, and I have not built it that way.

There are two honest routes. Do Route 1 today regardless — it is fifteen minutes and removes
the staleness. Route 2 is the full automation and needs one decision from you.

---

## Route 1 — GitHub + Cloudflare Pages, you push (15 minutes, do this now)

This gets you: version history, rollback, and **a deploy that is one command instead of a
zip upload**. The weekly research still reaches you through Slack as it does today.

### A. Create the repo

1. github.com → **New repository**
2. Name: `gracehill-competitive-intel`
3. **Private**. This contains competitive positioning and internal claims — it is not public.
4. Do **not** add a README, .gitignore or licence. The repo already has all three.
5. Create, then copy the URL it shows you: `https://github.com/<org>/gracehill-competitive-intel.git`

### B. Push what exists

The repo here has 16 commits of real history. From a session, I run:

```
git remote add origin https://github.com/<org>/gracehill-competitive-intel.git
git push -u origin main
```

I need you to authorise that push when it prompts — `git push` is on the deny list in the
permission file you installed, deliberately, so it will stop and ask. That is working as
intended: pushing code is exactly the kind of thing that should need a human.

### C. Connect Cloudflare Pages

1. dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Authorise GitHub, pick `gracehill-competitive-intel`
3. Build settings — **leave the build command empty**:
   - Framework preset: **None**
   - Build command: *(blank)*
   - Build output directory: **`public`**
4. Save and Deploy

The build command is blank on purpose. `public/index.html` is committed already built, so
Cloudflare only has to serve it. Nothing to install, no Python on their side, nothing to break.

### D. Point the domain and re-check Access

1. In the new Pages project → **Custom domains** → add `ci-gracehill.com`
2. **Zero Trust → Access → Applications** — confirm the policy covers the new project's
   domain. If it only covers the old `*.workers.dev` address, the app is briefly public.
   **Check this before you tell anyone the URL has moved.**

### After this is done

Deploying becomes: I commit and push, Cloudflare rebuilds in about a minute. No zip, no
upload, no attachment for you to find. You approve the push; everything else is automatic.

---

## Route 2 — full automation, including the weekly refresh

Two ways to close the last gap. They differ in where the work runs.

### Option A — a task that runs on your computer *(recommended)*

Cowork tasks can run on your machine instead of in the cloud. A task bound to your computer
sees your actual folders, so the repo persists between runs and **git uses the credentials
you already have** — no token in a prompt, nothing new to store.

What it would do each Sunday: pull, apply the week's findings, run `build.py`, commit, push.
Cloudflare deploys on the push. You approve nothing unless something needs a decision.

What you would need: the repo cloned into a folder on your Mac that Cowork can reach, and
your machine awake when it runs. Say the word and I will set the task up — it is a
`requires_local_device` task, which means you approve the device binding once at creation.

### Option B — a Cloudflare API token in the task

Cloudflare Pages supports direct upload, so a cloud task could deploy without GitHub at all.
It needs a scoped API token stored in the task prompt. It works, it needs no machine of yours
awake — and it puts a live credential in plain text in your account. **I would only do this
if Option A is genuinely impractical**, and if we do, the token should be scoped to Pages
deploy on this one project and nothing else.

---

## What I would actually do

**Route 1 now**, because it is fifteen minutes and it ends the zip-file shuffle.

Then **Route 2 Option A**, because it is the only version where a credential never leaves
your control. The weekly digest already works; this only adds "and update the app too".

Route 2 Option B is the fallback if your machine cannot be relied on to be awake — and it is
a real trade, not a shortcut. Say which you prefer and I will build it.

---

## One thing to fix in the permission file either way

`Bash(git push:*)` is currently in the **deny** list. That is right for now, since every push
should be deliberate. If you later move to Route 2 Option A, the task needs it allowed —
move that one line from `deny` to `allow` at that point, and not before.
