# Setting up the request form

Five minutes of setup, then send me two things and the Ask button starts writing to your sheet.

---

## Why it works this way

The app is a single self-contained HTML file with no backend — that is deliberate, and it is why
it loads instantly and makes zero external requests. A form inside it has nowhere to send data.
Separately, the Google Drive connector can *read* an existing sheet but cannot *edit* one, which
is the same limitation that made us DM you paste-ready tables instead of appending to the admin
sheet.

So the row has to be written by something that owns the sheet. Google Forms does that for free,
and — the part that solves your notification worry — **I can read the resulting sheet**, so the
alerting comes from machinery we already have rather than a new inbox.

---

## Step 1 — create the form

New Google Form, in either CI folder. Name it **CI requests**.

In **Settings → Responses**, turn on **Collect email addresses → Verified**. That gives you a
"who asked" column without anyone typing their name.

Then add these five questions, in this order. The wording matches the in-app form exactly, so
answers arrive already shaped like the Requests tab.

**1. What kind of request is this?** · *Dropdown* · Required

- Something here is wrong or out of date
- A competitor is missing
- I have a question I could not answer on a call
- I need more on a competitor we already track
- I heard something in a deal worth recording

**2. Which competitor or page?** · *Short answer* · Required

Description: `The competitor name, or the page you were looking at.`

**3. What do you need, or what is wrong?** · *Paragraph* · Required

Description: `One or two plain sentences is plenty. Please do not name a customer or prospect — describe the situation instead. This goes into a shared record.`

**4. Source or link, if you have one** · *Short answer* · Optional

**5. How urgent is it?** · *Dropdown* · Required

- Whenever — good to fix eventually
- This week — I have a deal open
- Today — I am on a call about it

---

## Step 2 — send responses to a sheet

**Responses → Link to Sheets → Create new spreadsheet.** Name it **CI requests (responses)** and
move it into the same folder.

Then add one column by hand to the right of the last response column, headed **Status**. Forms
will not touch it, so it survives every new submission. That is where you mark things Open,
Done, or Rejected — and it is what the daily DM reads to know what to stop reminding you about.

---

## Step 3 — send me two things

**A. The form's live link** — the `/viewform` URL from the Send button, or Preview.

**B. A pre-filled link.** In the form's ⋮ menu, choose **Get pre-filled link**, type a recognisable
dummy value into each of the five questions — literally `AAA`, `BBB`, `CCC`, `DDD`, `EEE` in order
— then press **Get link** and **Copy link**. Paste me the whole URL.

That URL contains the field IDs. Without it the button still opens the form, people just fill it
in themselves. With it, the form arrives already filled in from whatever they typed in the app —
including the competitor name when they clicked from a competitor page. It is one click for them
instead of two rounds of typing, which is the difference between a form people use and one they
do not.

**C. The response sheet's file ID** — the long string in its URL between `/d/` and `/edit`.

---

## What happens then

I set three constants in the app, rebuild, and you redeploy. The Ask button and the "Something
wrong here?" button on every competitor page both route to the form.

I also create a scheduled task that, each weekday morning:

- reads the response sheet
- finds rows added since it last ran whose **Status** is not Done or Rejected
- DMs you one message with each new request — who, what, which competitor, how urgent
- says nothing at all on days with no new requests
- flags anything marked **Today — I am on a call about it** at the top

Open requests also get folded into the Sunday-night owner-only DM you already read before
approving the digests, so nothing sits unseen for a week.

Until you send those, nothing breaks — the button falls back to opening an email to you, exactly
as it does today.
