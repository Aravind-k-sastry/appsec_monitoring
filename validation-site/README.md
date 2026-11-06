# Barracuda AppShield Agent — Pitch / Validation Site

A multi-page **smoke-test ("fake door")** site that pitches the WaaS on-host agent
as if it were a shipping product — **Barracuda AppShield Agent** — to measure real
buyer intent from customers, partners, and field teams.

The product does not exist yet. The site's job is to answer one question:
**do people want it enough to raise their hand?** The signal is measured two ways:

1. **Demo requests** — the primary intent signal (name, email, company, plan interest…), stored in SQLite.
2. **A funnel** — pageviews → CTA clicks → demo requests, so you can see *conversion*, not just raw interest.

**Zero dependencies.** Pure Python standard library (`http.server` + `sqlite3`).
No Flask, no `pip install`, no build step. Runs on any box with Python 3.8+.

## Why a fake-door landing page?

Asking "would you use this?" gets polite yes's. Watching whether someone clicks
**Book a demo** and hands over a work email is a far stronger signal of real
demand. This site presents the product confidently in the present tense, then
measures intent-to-act. A 2–4% visitor→demo conversion from a cold audience is a
meaningful green light; near-zero despite traffic is a cheap, early *no*.

## Files

| File | Purpose |
|------|---------|
| `app.py` | Web server: renders pages, captures demo requests, logs the funnel, serves the dashboard. Run this. |
| `pages.py` | All marketing copy + the product name. **Change the brand in one place:** `PRODUCT` at the top. |
| `static/style.css` | Barracuda dark theme, shared by every page. |
| `appshield.db` | SQLite database — created automatically on first run (`demo_requests` + `events` tables). |

## Pages

| Path | What it is |
|------|-----------|
| `/` | Overview — hero, the 3 blind spots, the land→expand story, CTA bands |
| `/how-it-works` | Architecture: thin agent → cloud brain → policy push-down |
| `/use-cases` | Six concrete jobs-to-be-done + illustrative field quotes |
| `/pricing` | Full four-tier pricing (Starter → Advance → Premium → Premium+) + comparison table |
| `/survey` | **Need-validation survey** — a separate instrument from the demo CTA (see below) |
| `/demo` | **Book a demo** form — the primary conversion |
| `/admin` | Validation dashboard — demo funnel + survey analytics, CSV exports (token-gated) |

## Two instruments, kept separate

The site measures demand two different ways — don't conflate them:

1. **The demo CTA (`/demo`)** measures *intent-to-act* — did someone hand over a work email to see the product. Strongest signal; the core smoke-test number.
2. **The survey (`/survey`)** measures *stated need* — how people see shadow apps, app-layer attacks, and AI/LLM activity on their servers today. No pitch; mostly one-click behavioural questions.

The survey has a **mode toggle at the top**: a prospect fills it in self-serve, or a Barracuda SA fills it in *for an account* (captures the account name + SA name). Multi-select answers are stored `"; "`-joined. Responses land in the `survey_responses` table and surface on `/admin` with: response count, customer-vs-non-customer cohort split, inventory-confidence histogram, the **Q8×Q9 kill-signal cross-tab** (of respondents already running CrowdStrike/Defender, did they add a new tool or extend the one they had — the "we'd just use the agent we have" displacement risk), next-step and interest distributions, plus a raw table + `/export/survey.csv`.

## Run locally (testing)

```bash
cd validation-site
python3 app.py
```

Open <http://localhost:8000/>. Dashboard at <http://localhost:8000/admin>.
Change the port with `PORT=9000 python3 app.py`.

## What's captured

- **`demo_requests`** — timestamp, IP, user-agent, referrer, name, email, company,
  title, role, company size, plan interest, timeframe, free-text problem.
- **`events`** — every pageview and every CTA click (`data-cta` id + the page it
  happened on). CTA clicks are sent by a tiny `navigator.sendBeacon` script in the
  page footer; no third-party analytics, no cookies.

The dashboard turns these into KPIs (unique visitors, page views, CTA clicks,
demo requests), the **visitor→demo conversion rate**, a funnel, views-by-page,
and top CTAs.

## Change the pitch

- **Product name / tagline:** edit `PRODUCT`, `SHORT`, `TAGLINE` at the top of `pages.py`.
- **Copy:** each page is a function in `pages.py` returning HTML — edit the strings.
- **Prices / tiers:** the `pricing()` function in `pages.py`.
- **A new demo field:** add it to the form in `pages.demo_form()` **and** to
  `DEMO_FIELDS` + the `demo_requests` table in `app.py` (delete `appshield.db` to
  recreate the schema).

## Host it 24×7

1. **Copy `validation-site/` to your server.**
2. **Protect the dashboard** so the public can't read your leads:
   ```bash
   ADMIN_TOKEN=pick-a-long-secret PORT=8000 python3 app.py
   ```
   `/admin` and `/export/*` then require `?token=pick-a-long-secret`.
3. **Keep it running** with systemd (survives reboots/crashes):

   `/etc/systemd/system/appshield-pitch.service`
   ```ini
   [Unit]
   Description=AppShield Agent Pitch Site
   After=network.target

   [Service]
   WorkingDirectory=/opt/appshield-pitch
   ExecStart=/usr/bin/python3 /opt/appshield-pitch/app.py
   Environment=PORT=8000
   Environment=ADMIN_TOKEN=pick-a-long-secret
   Restart=always
   User=www-data

   [Install]
   WantedBy=multi-user.target
   ```
   ```bash
   sudo systemctl enable --now appshield-pitch
   ```
4. **Put HTTPS in front of it** with Caddy (auto-TLS) or nginx:
   ```
   appshield.example.com {
       reverse_proxy 127.0.0.1:8000
   }
   ```

### Quick field test without a server

```bash
python3 app.py        # terminal 1
ngrok http 8000       # terminal 2 -> public https URL to share
```

## Getting the data out

- Live dashboard: `/admin`
- Leads CSV: `/export/demos.csv` · Events CSV: `/export/events.csv` · Survey CSV: `/export/survey.csv`
- Or open `appshield.db` with any SQLite tool:
  `sqlite3 appshield.db "SELECT name,email,company,plan_interest FROM demo_requests;"`

## Honest-framing notes

- The footer labels the page an **early-access evaluation** with indicative
  features/pricing — keep that for external use so it's not a hard promise.
- Pricing figures in `pages.py` are **placeholders** ($99 / $249 / $449 per app/mo).
  Set them to whatever you want to pressure-test, or run `price-estimator` first.
- `ThreadingHTTPServer` handles concurrent visitors fine at this scale; each
  request opens and closes its own SQLite connection, which is safe.
- Back up `appshield.db` periodically — it is the only state.
