#!/usr/bin/env python3
"""
Barracuda AppShield Agent — smoke-test ("fake door") pitch site.

A multi-page marketing site for a product that does NOT ship yet. Its job is to
measure real buyer intent: how many visitors land, how many click a CTA, and how
many actually book a demo. Demo requests and a pageview/CTA funnel are stored in
SQLite.

Zero third-party dependencies — Python standard library only (http.server +
sqlite3). Runs anywhere Python 3.8+ is installed.

Routes
  GET  /, /how-it-works, /use-cases, /pricing, /survey, /demo  -> marketing pages
  POST /demo-request                                   -> store demo request, show thank-you
  POST /survey-response                                -> store survey response, show thank-you
  POST /track                                          -> log a CTA click (beacon, returns 204)
  GET  /admin                                          -> funnel dashboard + leads + survey (token-gated)
  GET  /export/demos.csv, /export/events.csv, /export/survey.csv -> CSV exports (token-gated)
  GET  /static/<file>                                  -> css/assets
  GET  /health                                         -> liveness check

Env
  PORT (default 8000), HOST (default 0.0.0.0)
  ADMIN_TOKEN  -> if set, /admin and /export/* require ?token=<ADMIN_TOKEN>
"""

import csv
import html
import io
import os
import sqlite3
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "appshield.db")
STATIC_DIR = os.path.join(BASE_DIR, "static")

PORT = int(os.environ.get("PORT", "8000"))
HOST = os.environ.get("HOST", "0.0.0.0")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

DEMO_FIELDS = [
    "name", "email", "company", "title", "role",
    "company_size", "plan_interest", "timeframe", "problem",
]

# Need-validation survey fields (multi-select answers are stored "; "-joined).
SURVEY_FIELDS = [
    "mode", "account", "sa_name",
    "role", "company_size", "app_count", "is_customer",
    "inventory_confidence", "shadow_freq", "visibility_today",
    "installed_agents", "last_visibility_action", "install_difficulty",
    "paid_last_year", "owner",
    "next_step", "pay_trigger",
    "interest", "contact_name", "email", "company",
]

STATIC_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

# which GET paths are "real" marketing pages we count as pageviews
PAGE_PATHS = {"/", "/how-it-works", "/experience", "/use-cases", "/pricing", "/survey", "/demo"}


# ---------------------------------------------------------------------------
# DB
# ---------------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS demo_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_at TEXT NOT NULL,
            remote_addr TEXT, user_agent TEXT, referrer TEXT,
            name TEXT, email TEXT, company TEXT, title TEXT, role TEXT,
            company_size TEXT, plan_interest TEXT, timeframe TEXT, problem TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            kind TEXT NOT NULL,        -- 'pageview' | 'cta'
            name TEXT,                 -- path for pageview, data-cta id for cta
            path TEXT,                 -- page the event happened on
            remote_addr TEXT, user_agent TEXT
        )
        """
    )
    survey_cols = ",\n            ".join(f"{f} TEXT" for f in SURVEY_FIELDS)
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_at TEXT NOT NULL,
            remote_addr TEXT, user_agent TEXT, referrer TEXT,
            {survey_cols}
        )
        """
    )
    conn.commit()
    conn.close()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def log_event(kind, name, path, addr, ua):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO events (ts, kind, name, path, remote_addr, user_agent) VALUES (?,?,?,?,?,?)",
            (now_iso(), kind, name, path, addr, ua),
        )
        conn.commit()
        conn.close()
    except Exception as exc:  # noqa: BLE001
        print("WARN event log failed:", exc)


def insert_demo(data, addr, ua, referrer):
    conn = sqlite3.connect(DB_PATH)
    cols = ["submitted_at", "remote_addr", "user_agent", "referrer"] + DEMO_FIELDS
    vals = [now_iso(), addr, ua, referrer] + [data.get(f, "") for f in DEMO_FIELDS]
    conn.execute(
        f"INSERT INTO demo_requests ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",
        vals,
    )
    conn.commit()
    conn.close()


def insert_survey(data, addr, ua, referrer):
    conn = sqlite3.connect(DB_PATH)
    cols = ["submitted_at", "remote_addr", "user_agent", "referrer"] + SURVEY_FIELDS
    vals = [now_iso(), addr, ua, referrer] + [data.get(f, "") for f in SURVEY_FIELDS]
    conn.execute(
        f"INSERT INTO survey_responses ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",
        vals,
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Layout — wraps page bodies in nav/footer, injects CTA-tracking script
# ---------------------------------------------------------------------------
def render_page(path, body, title):
    nav_links = "".join(
        f'<a class="link{" active" if p == path else ""}" href="{p}">{html.escape(label)}</a>'
        for p, label in pages.NAV
    )
    footer_links = "".join(
        f'<a href="{p}">{html.escape(label)}</a>' for p, label in pages.NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<nav class="nav"><div class="wrap nav-inner">
  <a class="logo" href="/"><span class="dot"></span><span>Barracuda<small>APPSHIELD AGENT</small></span></a>
  <div class="spacer"></div>
  <div class="nav-links">{nav_links}
    <a class="btn btn-cta btn-sm" href="/demo" data-cta="nav_demo">Book a demo</a>
  </div>
</div></nav>

{body}

<footer class="footer"><div class="wrap">
  <div class="cols">
    <div><h4>{html.escape(pages.PRODUCT)}</h4>{footer_links}</div>
    <div><h4>Barracuda</h4>
      <a href="/">Application Security</a>
      <a href="/how-it-works">How it works</a>
      <a href="/pricing">Pricing</a>
    </div>
  </div>
  <div class="disclaimer">
    &copy; Barracuda Networks · {html.escape(pages.PRODUCT)}. This page is part of an early-access
    evaluation. Features and pricing shown are indicative and subject to change.
  </div>
</div></footer>

<script>
// Lightweight CTA tracking: any element with data-cta posts a beacon on click.
document.addEventListener('click', function(e){{
  var el = e.target.closest('[data-cta]');
  if(!el) return;
  try{{
    navigator.sendBeacon('/track',
      new Blob([JSON.stringify({{name: el.getAttribute('data-cta'), path: location.pathname}})],
      {{type:'application/json'}}));
  }}catch(_){{ /* best-effort */ }}
}});
</script>
</body>
</html>"""


PAGE_BUILDERS = {
    "/": (pages.home, f"{pages.PRODUCT} — {pages.TAGLINE}"),
    "/how-it-works": (pages.how_it_works, f"How it works — {pages.PRODUCT}"),
    "/experience": (pages.experience, f"The experience — {pages.PRODUCT}"),
    "/use-cases": (pages.use_cases, f"Use cases — {pages.PRODUCT}"),
    "/pricing": (pages.pricing, f"Pricing — {pages.PRODUCT}"),
    "/survey": (pages.survey, f"Need-check survey — {pages.PRODUCT}"),
    "/demo": (pages.demo_form, f"Book a demo — {pages.PRODUCT}"),
}


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "AppShieldPitch/1.0"

    def _send(self, code, body, ctype="text/html; charset=utf-8", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _addr(self):
        return self.client_address[0]

    def _ua(self):
        return self.headers.get("User-Agent", "")

    def _authorized(self):
        if not ADMIN_TOKEN:
            return True
        q = urllib.parse.urlparse(self.path).query
        return urllib.parse.parse_qs(q).get("token", [""])[0] == ADMIN_TOKEN

    def log_message(self, fmt, *args):
        print(f"{datetime.now().strftime('%H:%M:%S')}  {self._addr()}  {fmt % args}")

    # --- GET ---
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path.startswith("/static/"):
            return self._serve_static(path)
        if path == "/health":
            return self._send(200, "ok", "text/plain; charset=utf-8")
        if path == "/admin":
            return self._serve_admin()
        if path == "/export/demos.csv":
            return self._export("demo_requests", "appshield_demo_requests.csv")
        if path == "/export/events.csv":
            return self._export("events", "appshield_events.csv")
        if path == "/export/survey.csv":
            return self._export("survey_responses", "appshield_survey_responses.csv")
        if path in PAGE_BUILDERS:
            builder, title = PAGE_BUILDERS[path]
            log_event("pageview", path, path, self._addr(), self._ua())
            return self._send(200, render_page(path, builder(), title))
        return self._send(404, render_page("/", "<section class='hero'><div class='wrap'>"
                          "<h1>404</h1><p class='lede'>Page not found. "
                          "<a href='/'>Back to overview</a></p></div></section>",
                          "Not found — " + pages.PRODUCT))

    # --- POST ---
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/demo-request":
            return self._handle_demo()
        if path == "/survey-response":
            return self._handle_survey()
        if path == "/track":
            return self._handle_track()
        return self._send(404, "Not found", "text/plain; charset=utf-8")

    # --- handlers ---
    def _serve_static(self, path):
        rel = path[len("/static/"):]
        safe = os.path.normpath(rel).lstrip("/.")
        full = os.path.join(STATIC_DIR, safe)
        if not full.startswith(STATIC_DIR) or not os.path.isfile(full):
            return self._send(404, "Not found", "text/plain; charset=utf-8")
        ctype = STATIC_TYPES.get(os.path.splitext(full)[1], "application/octet-stream")
        with open(full, "rb") as f:
            self._send(200, f.read(), ctype)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        return self.rfile.read(length).decode("utf-8") if length else ""

    def _handle_demo(self):
        raw = self._read_body()
        data = {k: v[0] for k, v in urllib.parse.parse_qs(raw).items()}
        try:
            insert_demo(data, self._addr(), self._ua(), self.headers.get("Referer", ""))
            log_event("cta", "demo_submitted", "/demo", self._addr(), self._ua())
        except Exception as exc:  # noqa: BLE001
            print("ERROR inserting demo:", exc)
            return self._send(500, "Could not save your request. Please try again.",
                              "text/plain; charset=utf-8")
        body = pages.thank_you(data.get("name", ""))
        return self._send(200, render_page("/demo", body, "Thank you — " + pages.PRODUCT))

    def _handle_survey(self):
        raw = self._read_body()
        # Multi-select answers (checkboxes) arrive as repeated keys -> join them.
        parsed = urllib.parse.parse_qs(raw, keep_blank_values=False)
        data = {k: "; ".join(v) for k, v in parsed.items()}
        try:
            insert_survey(data, self._addr(), self._ua(), self.headers.get("Referer", ""))
            log_event("cta", "survey_submitted", "/survey", self._addr(), self._ua())
        except Exception as exc:  # noqa: BLE001
            print("ERROR inserting survey:", exc)
            return self._send(500, "Could not save your response. Please try again.",
                              "text/plain; charset=utf-8")
        body = pages.survey_thanks(data.get("mode", "self"))
        return self._send(200, render_page("/survey", body, "Thank you — " + pages.PRODUCT))

    def _handle_track(self):
        raw = self._read_body()
        name = path = ""
        # body is JSON from sendBeacon; parse leniently without importing json failures
        try:
            import json
            obj = json.loads(raw) if raw else {}
            name = str(obj.get("name", ""))[:120]
            path = str(obj.get("path", ""))[:200]
        except Exception:  # noqa: BLE001
            pass
        if name:
            log_event("cta", name, path, self._addr(), self._ua())
        return self._send(204, b"", "text/plain")

    def _serve_admin(self):
        if not self._authorized():
            return self._send(403, "Forbidden — append ?token=YOUR_TOKEN",
                              "text/plain; charset=utf-8")
        return self._send(200, render_admin())

    def _export(self, table, filename):
        if not self._authorized():
            return self._send(403, "Forbidden — append ?token=YOUR_TOKEN",
                              "text/plain; charset=utf-8")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(f"SELECT * FROM {table} ORDER BY id DESC").fetchall()
        conn.close()
        buf = io.StringIO()
        writer = csv.writer(buf)
        if rows:
            writer.writerow(rows[0].keys())
            for r in rows:
                writer.writerow([r[k] for k in r.keys()])
        else:
            writer.writerow(["(no data)"])
        self._send(200, buf.getvalue(), "text/csv; charset=utf-8",
                   {"Content-Disposition": f"attachment; filename={filename}"})


# ---------------------------------------------------------------------------
# Admin dashboard
# ---------------------------------------------------------------------------
def _tok():
    return f"?token={urllib.parse.quote(ADMIN_TOKEN)}" if ADMIN_TOKEN else ""


def render_admin():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    def scalar(q, *a):
        return conn.execute(q, a).fetchone()[0]

    total_views = scalar("SELECT COUNT(*) FROM events WHERE kind='pageview'")
    unique_visitors = scalar("SELECT COUNT(DISTINCT remote_addr) FROM events")
    cta_clicks = scalar("SELECT COUNT(*) FROM events WHERE kind='cta' AND name!='demo_submitted'")
    demos = scalar("SELECT COUNT(*) FROM demo_requests")

    # funnel: unique visitors -> visited /demo -> submitted
    demo_pageviews = scalar("SELECT COUNT(*) FROM events WHERE kind='pageview' AND path='/demo'")
    conv = (demos / unique_visitors * 100) if unique_visitors else 0

    # views by page
    page_rows = conn.execute(
        "SELECT path, COUNT(*) c FROM events WHERE kind='pageview' GROUP BY path ORDER BY c DESC"
    ).fetchall()
    # top CTAs
    cta_rows = conn.execute(
        "SELECT name, COUNT(*) c FROM events WHERE kind='cta' GROUP BY name ORDER BY c DESC"
    ).fetchall()
    # leads
    leads = conn.execute("SELECT * FROM demo_requests ORDER BY id DESC").fetchall()

    # --- survey analytics ---
    surv_total = scalar("SELECT COUNT(*) FROM survey_responses")
    cohort_rows = conn.execute(
        "SELECT is_customer v, COUNT(*) c FROM survey_responses WHERE is_customer!='' "
        "GROUP BY is_customer ORDER BY c DESC").fetchall()
    conf_rows = conn.execute(
        "SELECT inventory_confidence v, COUNT(*) c FROM survey_responses "
        "WHERE inventory_confidence!='' GROUP BY inventory_confidence ORDER BY v").fetchall()
    next_rows = conn.execute(
        "SELECT next_step v, COUNT(*) c FROM survey_responses WHERE next_step!='' "
        "GROUP BY next_step ORDER BY c DESC").fetchall()
    interest_rows = conn.execute(
        "SELECT interest v, COUNT(*) c FROM survey_responses WHERE interest!='' "
        "GROUP BY interest ORDER BY c DESC").fetchall()
    # kill-signal cross-tab: among hosts already running CrowdStrike/Defender,
    # did they add a new tool or extend/ask the vendor they already had?
    edr_total = scalar(
        "SELECT COUNT(*) FROM survey_responses "
        "WHERE installed_agents LIKE '%CrowdStrike%' OR installed_agents LIKE '%Defender%'")
    edr_action_rows = conn.execute(
        "SELECT last_visibility_action v, COUNT(*) c FROM survey_responses "
        "WHERE (installed_agents LIKE '%CrowdStrike%' OR installed_agents LIKE '%Defender%') "
        "AND last_visibility_action!='' GROUP BY last_visibility_action ORDER BY c DESC").fetchall()
    surveys = conn.execute("SELECT * FROM survey_responses ORDER BY id DESC").fetchall()
    conn.close()

    def kpi(n, l):
        return f"<div class='kpi'><div class='n'>{n}</div><div class='l'>{html.escape(l)}</div></div>"

    # funnel bars (relative to max = unique_visitors)
    base = max(unique_visitors, 1)
    def bar(label, val):
        pct = val / base * 100
        return (f"<div style='margin:10px 0'><div style='display:flex;justify-content:space-between;"
                f"font-size:13px;color:#c9d2dc'><span>{html.escape(label)}</span><span>{val}</span></div>"
                f"<div class='funnel-bar'><span style='width:{pct:.1f}%'></span></div></div>")

    page_table = "".join(
        f"<tr><td>{html.escape(r['path'])}</td><td>{r['c']}</td></tr>" for r in page_rows
    ) or "<tr><td colspan='2' class='no'>No pageviews yet</td></tr>"
    cta_table = "".join(
        f"<tr><td>{html.escape(r['name'] or '')}</td><td>{r['c']}</td></tr>" for r in cta_rows
    ) or "<tr><td colspan='2' class='no'>No CTA clicks yet</td></tr>"

    lead_cols = ["id", "submitted_at", "name", "email", "company", "role",
                 "company_size", "plan_interest", "timeframe", "problem"]
    lead_head = "".join(f"<th>{c}</th>" for c in lead_cols)
    lead_body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(r[c]) if r[c] is not None else '')}</td>"
                          for c in lead_cols) + "</tr>"
        for r in leads
    ) or f"<tr><td colspan='{len(lead_cols)}' class='no'>No demo requests yet</td></tr>"

    # --- survey section HTML ---
    def sbar(label, val, base):
        pct = (val / base * 100) if base else 0
        return (f"<div style='margin:7px 0'><div style='display:flex;justify-content:space-between;"
                f"font-size:13px;color:#c9d2dc'><span>{html.escape(str(label))}</span>"
                f"<span>{val}</span></div><div class='funnel-bar' style='height:18px'>"
                f"<span style='width:{pct:.1f}%'></span></div></div>")

    def barset(rows, base, empty):
        return "".join(sbar(r["v"], r["c"], base) for r in rows) or f"<p class='muted'>{empty}</p>"

    surv_cols = ["id", "submitted_at", "mode", "account", "role", "is_customer",
                 "inventory_confidence", "installed_agents", "last_visibility_action",
                 "paid_last_year", "next_step", "interest", "email"]
    surv_head = "".join(f"<th>{c}</th>" for c in surv_cols)
    surv_body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(r[c]) if r[c] is not None else '')}</td>"
                          for c in surv_cols) + "</tr>"
        for r in surveys
    ) or f"<tr><td colspan='{len(surv_cols)}' class='no'>No survey responses yet</td></tr>"

    survey_section = f"""
<hr style="border:0;border-top:1px solid var(--line);margin:34px 0 10px">
<h1 style="font-size:26px">Need-validation survey</h1>
<p class="muted">Stated-need signal — separate from the demo/intent funnel above.
  Behavioural answers (Q8&times;Q9, past spend) carry the weight; treat Q13 as a stated intention, not a forecast.</p>

<div class="kpis" style="grid-template-columns:repeat(2,1fr);max-width:520px">
  {kpi(surv_total, "Survey responses")}
  {kpi(edr_total, "Running CrowdStrike / Defender")}
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:20px">
  <div><h2 style="font-size:18px">Customer vs non-customer (cohort split)</h2>
    {barset(cohort_rows, surv_total, "No responses yet")}</div>
  <div><h2 style="font-size:18px">Inventory confidence (1 low &ndash; 5 high)</h2>
    {barset(conf_rows, surv_total, "No responses yet")}</div>
</div>

<div style="margin-top:22px;padding:16px 18px;background:var(--panel);border:1px solid var(--line);border-radius:12px">
  <h2 style="font-size:18px;margin-top:0">Kill-signal cross-tab &mdash; already run an EDR (N={edr_total})</h2>
  <p class="muted" style="margin-top:4px">Of those already running CrowdStrike/Defender, what did they do last time they
    needed new host visibility? Heavy &ldquo;extended / asked the vendor I already use&rdquo; = the
    &ldquo;we&rsquo;d just use the agent we have&rdquo; displacement risk.</p>
  {barset(edr_action_rows, edr_total, "No EDR-running responses yet")}
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:22px">
  <div><h2 style="font-size:18px">If it were free &mdash; next step (Q13)</h2>
    {barset(next_rows, surv_total, "No responses yet")}</div>
  <div><h2 style="font-size:18px">Early-access interest (Q15)</h2>
    {barset(interest_rows, surv_total, "No responses yet")}</div>
</div>

<div style="display:flex;gap:16px;align-items:center;margin-top:26px">
  <h2 style="font-size:18px;margin:0">Responses &mdash; {surv_total}</h2>
  <a href="/export/survey.csv{_tok()}">Download survey CSV &darr;</a>
</div>
<div style="overflow-x:auto"><table class="data"><tr>{surv_head}</tr>{surv_body}</table></div>
"""

    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AppShield Agent — validation dashboard</title>
<link rel="stylesheet" href="/static/style.css">
<style>body{{padding:24px}} .wrap{{max-width:1120px}}</style>
</head><body><div class="wrap">
<h1 style="font-size:30px">Validation dashboard</h1>
<p class="muted">Smoke-test funnel for {html.escape(pages.PRODUCT)}. The number that matters is demo conversion.</p>

<div class="kpis">
  {kpi(unique_visitors, "Unique visitors")}
  {kpi(total_views, "Page views")}
  {kpi(cta_clicks, "CTA clicks")}
  {kpi(f"{demos}", "Demo requests")}
</div>
<div class="kpi" style="margin-bottom:8px"><div class="n green">{conv:.1f}%</div>
  <div class="l">Visitor → demo-request conversion (the core intent signal)</div></div>

<h2 style="font-size:20px;margin-top:26px">Funnel</h2>
{bar("Unique visitors", unique_visitors)}
{bar("Viewed Book-a-demo page", demo_pageviews)}
{bar("Submitted demo request", demos)}

<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:26px">
  <div><h2 style="font-size:20px">Views by page</h2>
    <table class="data"><tr><th>Page</th><th>Views</th></tr>{page_table}</table></div>
  <div><h2 style="font-size:20px">CTA clicks</h2>
    <table class="data"><tr><th>CTA</th><th>Clicks</th></tr>{cta_table}</table></div>
</div>

<div style="display:flex;gap:16px;align-items:center;margin-top:30px">
  <h2 style="font-size:20px;margin:0">Demo requests &mdash; {demos}</h2>
  <a href="/export/demos.csv{_tok()}">Download leads CSV &darr;</a>
  <a href="/export/events.csv{_tok()}">Download events CSV &darr;</a>
</div>
<div style="overflow-x:auto"><table class="data"><tr>{lead_head}</tr>{lead_body}</table></div>
{survey_section}
</div></body></html>"""


def main():
    init_db()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"{pages.PRODUCT} pitch site running at http://{HOST}:{PORT}/")
    print(f"  Site      : http://localhost:{PORT}/")
    print(f"  Dashboard : http://localhost:{PORT}/admin" + (" (token required)" if ADMIN_TOKEN else ""))
    print(f"  Database  : {DB_PATH}")
    if not ADMIN_TOKEN:
        print("  NOTE: ADMIN_TOKEN not set — /admin and exports are open. Set it before public hosting.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        httpd.shutdown()


if __name__ == "__main__":
    main()
