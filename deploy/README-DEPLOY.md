# Hosting the Competitive Intelligence app

One folder, three files. `index.html` is the whole app — no build step, no dependencies,
no external requests. Drag the folder onto a static host and it works.

---

## Recommended: Cloudflare Pages + Cloudflare Access

Free at your scale, and Access authenticates against Google Workspace, so reps sign in with
their Grace Hill account and nobody manages a second password.

### One-time setup (~20 minutes, needs someone with a Cloudflare account)

**1. Create the account**
Go to dash.cloudflare.com and sign up with a Grace Hill email. No domain or credit card needed —
you get a free `*.pages.dev` subdomain.

**2. Create the project**
Workers & Pages → Create → Pages → **Upload assets**. Name it `gracehill-ci`.
Drag this `deploy` folder in. It publishes to `https://gracehill-ci.pages.dev`.

**3. Lock it down — this is the important step**
Zero Trust → Access → Applications → Add an application → Self-hosted.
- Application name: Competitive Intelligence
- Session duration: 24 hours
- Domain: `gracehill-ci.pages.dev`

Then add a policy:
- Policy name: Grace Hill staff
- Action: **Allow**
- Include → **Emails ending in** → `@gracehill.com`

Save. The site is now unreachable to anyone without a Grace Hill email.

**4. Add Google as the login method** (optional but better)
Zero Trust → Settings → Authentication → Add new → Google Workspace. Follow the prompts.
Without this, Access emails a one-time PIN instead — which works, but is clunkier.

### For automated weekly updates

Create an API token so the Monday job can publish without anyone uploading a file:

Cloudflare dashboard → My Profile → API Tokens → Create Token → **Custom token**
- Permissions: `Account` → `Cloudflare Pages` → `Edit`
- Account Resources: your account

Copy the token somewhere safe and send it to me. The deploy command is then:

```bash
npx wrangler pages deploy ./deploy --project-name=gracehill-ci
```

Give reps a friendlier link with a custom domain later — Pages → Custom domains — for example
`compete.gracehill.com`. That needs a DNS record, so it's an IT ask rather than a self-serve one.

---

## Alternatives, if Cloudflare is a non-starter

**Netlify** — Same shape. Drag the folder to app.netlify.com/drop. Password protection requires
a paid plan; without it the URL is public-but-unguessable, which is not the same as private.

**Vercel** — Deployment protection with SSO is on paid plans.

**Google Sites** — No new vendor, automatically restricted to Grace Hill, but it can't host a
raw HTML file. You'd host the app somewhere and embed it, so it doesn't remove the hosting step.

**SharePoint** — Most Microsoft 365 tenants block rendering an uploaded HTML file in the browser;
it downloads instead. Worth a check with IT before relying on it.

---

## What's in this folder

| File | Purpose |
|---|---|
| `index.html` | The app. Self-contained: data, styles, logo, all inlined |
| `_headers` | Cloudflare Pages security headers and a 5-minute cache |
| `robots.txt` | Keeps it out of search engines |

Nothing here calls out to the internet, so the app works on a plane and there is no analytics,
tracking or third-party request to review with security.
