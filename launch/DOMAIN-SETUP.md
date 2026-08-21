# Pointing ci-gracehill.com at the app

**Do this before you post the Slack message.** Two steps, and the second one matters more than
the first.

---

## Step 1 — attach the domain to the Worker

Prerequisite: `ci-gracehill.com` has to be an **active zone in your Cloudflare account**. If you
bought it through Cloudflare Registrar it already is. If you bought it elsewhere, add the site in
Cloudflare first and change the nameservers at your registrar — that propagates in minutes to a
few hours, and nothing below works until it shows **Active**.

Then:

1. **Workers & Pages** → select the **ci** Worker
2. **Settings** → **Domains & Routes** → **Add** → **Custom Domain**
3. Enter `ci-gracehill.com`
4. **Add Custom Domain**

Cloudflare creates the DNS record and issues the certificate for you. It cannot be a hostname
that already has a CNAME record on it.

Consider adding `www.ci-gracehill.com` the same way, since people will type it.

---

## Step 2 — extend Cloudflare Access to the new hostname

**This is the one that bites.** Access applications are scoped **by hostname**. Your existing
policy protects `ci.gracehill.workers.dev`. It does **not** automatically protect
`ci-gracehill.com` just because both point at the same Worker.

If you skip this, the moment the custom domain goes live the site is reachable by anyone on the
internet with no login — an internal competitive database, indexed and public. Do this in the same
sitting as step 1, not afterward.

1. **Zero Trust** → **Access** → **Applications**
2. Open the existing application for the CI site
3. Add `ci-gracehill.com` as an additional domain on that application — or, if it won't take a
   second domain, create a second self-hosted application for `ci-gracehill.com` with the same
   one-time-PIN policy and the same allowed email list
4. Add `www.ci-gracehill.com` too if you created it

**Then test it in a private window before you post anything.** Go to `https://ci-gracehill.com`
and confirm you are stopped by the login screen. If the app loads without asking for a code, stop
and fix Access before sharing the link.

---

## Step 3 — tidy up

Once the custom domain works and is gated:

- Consider disabling the `workers.dev` route (**Settings** → **Domains & Routes**) so there's one
  door, not two. Every extra hostname is another thing to remember to protect.
- Tell me once it's live and I'll update the link the weekly digest posts to Slack — it currently
  points at `ci.gracehill.workers.dev`.
