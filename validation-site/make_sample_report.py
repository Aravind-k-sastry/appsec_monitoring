#!/usr/bin/env python3
"""
Generate static/sample-report.pdf — the downloadable sample Security Posture
Report linked from the Experience page.

Pure Python standard library only (no reportlab / weasyprint), so it keeps the
AppShield pitch site's zero-dependency contract. Hand-draws a 3-page PDF using
the base-14 Helvetica fonts (no embedding) with WinAnsi encoding.

Run after editing to regenerate the artifact:
    python3 make_sample_report.py

The report is honest to the product model:
  - Incoming traffic is OBSERVED in detect mode (eBPF + parallel log analysis
    after ingestion). The agent does NOT sit inline on incoming — attacks are
    "detected / identified", never "blocked inline / absorbed".
  - Agent-triggered EGRESS (MCP / API / LLM calls out) IS blocked at the source.
  - Incoming inline protection is available only by onboarding an app to the
    Advance / Premium plan (routes through the Barracuda cloud proxy).
Figures are illustrative sample data.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(BASE_DIR, "static", "sample-report.pdf")

# --- palette (0..1 RGB) ---
NAVY   = (0.043, 0.165, 0.290)   # #0B2A4A header bands
ACCENT = (0.173, 0.651, 0.878)   # #2CA6E0 accent
DARK   = (0.102, 0.137, 0.196)   # body text
MUTED  = (0.42,  0.45,  0.50)    # secondary text
LIGHT  = (0.949, 0.961, 0.973)   # #F2F5F8 zebra / cards
BORDER = (0.847, 0.871, 0.902)   # #D8DEE6 lines
WHITE  = (1, 1, 1)
PALE   = (0.80, 0.86, 0.92)      # text on navy
RED    = (0.753, 0.224, 0.169)
AMBER  = (0.878, 0.541, 0.0)
GREEN  = (0.118, 0.557, 0.353)

W, H = 612, 792  # US Letter
TOTAL_PAGES = 3


def yt(top):
    """Convert a top-origin y (pt from page top) to PDF bottom-origin y."""
    return H - top


def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def T(x, y_top, s, font="F1", size=9, color=DARK):
    r, g, b = color
    return (f"BT /{font} {size} Tf {r:.3f} {g:.3f} {b:.3f} rg "
            f"1 0 0 1 {x:.2f} {yt(y_top):.2f} Tm ({esc(s)}) Tj ET\n")


def rect(x, top, w, h, color):
    r, g, b = color
    return f"{r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {yt(top + h):.2f} {w:.2f} {h:.2f} re f\n"


def line(x1, top1, x2, top2, color, width=0.5):
    r, g, b = color
    return (f"{width:.2f} w {r:.3f} {g:.3f} {b:.3f} RG "
            f"{x1:.2f} {yt(top1):.2f} m {x2:.2f} {yt(top2):.2f} l S\n")


def table(ops, top, col_x, headers, rows, body_size=8.5):
    """Draw a header-banded, zebra-striped table. rows = list of (cells, last_color)."""
    rh = 18
    y = top
    ops.append(rect(40, y, 532, rh, NAVY))
    for i, h in enumerate(headers):
        ops.append(T(col_x[i] + 5, y + 12.5, h, "F2", 8.5, WHITE))
    y += rh
    for ri, (cells, last_color) in enumerate(rows):
        if ri % 2 == 1:
            ops.append(rect(40, y, 532, rh, LIGHT))
        for i, cell in enumerate(cells):
            col = last_color if (i == len(cells) - 1 and last_color) else DARK
            font = "F2" if (i == len(cells) - 1 and last_color) else "F1"
            ops.append(T(col_x[i] + 5, y + 12.5, cell, font, body_size, col))
        ops.append(line(40, y + rh, 572, y + rh, BORDER, 0.5))
        y += rh
    ops.append(line(40, top, 40, y, BORDER, 0.5))
    ops.append(line(572, top, 572, y, BORDER, 0.5))
    return y


def group_label(ops, top, text, note="", note_x=250):
    ops.append(T(40, top, text, "F2", 10, NAVY))
    if note:
        ops.append(T(note_x, top, note, "F1", 8, MUTED))


def header_band(ops, cont=False, page_no=1):
    bh = 50 if cont else 78
    ops.append(rect(0, 0, W, bh, NAVY))
    ops.append(T(40, 22, "BARRACUDA", "F2", 11, WHITE))
    if cont:
        ops.append(T(40, 40, "AppShield Agent  ·  Security Posture Report (continued)",
                     "F2", 12, WHITE))
        ops.append(T(470, 36, f"Page {page_no} of {TOTAL_PAGES}", "F1", 8.5, PALE))
    else:
        ops.append(T(40, 44, "AppShield Agent  ·  Security Posture Report", "F2", 15, WHITE))
        ops.append(T(40, 64, "Host app-prod-01  ·  November 2026  ·  Monthly board report",
                     "F1", 9, PALE))
        ops.append(T(470, 36, "POSTURE SCORE", "F1", 8, PALE))
        ops.append(T(470, 58, "82 / 100", "F2", 18, (0.56, 0.86, 0.98)))
        ops.append(T(470, 72, "+28 since install", "F1", 8, PALE))


def page_footer(ops):
    ops.append(line(40, 760, 572, 760, BORDER, 0.5))
    ops.append(T(40, 774,
                 "Sample report — figures are illustrative. AppShield Agent is in early-access evaluation.",
                 "F1", 8, MUTED))
    ops.append(T(470, 774, "© Barracuda Networks", "F1", 8, MUTED))


# ---------------------------------------------------------------------------
# PAGE 1 — summary + apps discovered
# ---------------------------------------------------------------------------
def page1():
    ops = []
    header_band(ops)

    # KPI strip
    ky = 98
    cell_w, gap, x0 = 82, 6, 40
    kpis = [
        ("9", "apps & agents"),
        ("3", "blind spots closed"),
        ("92,456", "incoming detected"),
        ("94", "AI egress blocked"),
        ("0", "incidents"),
        ("100%", "AI calls governed"),
    ]
    for i, (n, l) in enumerate(kpis):
        cx = x0 + i * (cell_w + gap)
        ops.append(rect(cx, ky, cell_w, 48, LIGHT))
        ops.append(rect(cx, ky, cell_w, 3, ACCENT))
        ops.append(T(cx + 7, ky + 26, n, "F2", 13, NAVY))
        ops.append(T(cx + 7, ky + 41, l, "F1", 7, MUTED))

    sy = 172
    ops.append(T(40, sy, "What the agent discovered", "F2", 13, DARK))
    ops.append(T(40, sy + 14,
                 "Public-facing apps taking incoming traffic (detect mode) and agents making calls to external apps (egress).",
                 "F1", 8.5, MUTED))

    col_x = [40, 185, 300, 362, 470]

    # --- Table 1: public-facing apps (incoming) ---
    group_label(ops, sy + 34, "Public-facing apps — incoming (detect mode)")
    headers1 = ["Application (domain)", "Type", "Host", "Status", "Risk"]
    apps = [
        (["reports.acme.com", "REST API", "app-prod-01", "Advance · cloud-routed", "Resolved"], GREEN),
        (["checkout.acme.com", "Web app", "app-prod-01", "Detect mode", "High · active attacks"], RED),
        (["login.acme.com", "Auth gateway", "app-prod-01", "Detect mode", "High · brute-force"], RED),
        (["admin.acme.com", "Admin portal", "app-prod-01", "Detect mode", "Medium · was shadow"], AMBER),
        (["store-api.acme.com", "REST API", "app-prod-02", "Detect mode", "Medium · was shadow"], AMBER),
    ]
    end1 = table(ops, sy + 48, col_x, headers1, apps)

    # --- Table 2: agents making external calls (egress) ---
    gy = end1 + 22
    group_label(ops, gy, "Agents calling external apps — egress")
    headers2 = ["Agent", "Type", "Host", "Egress destination", "Status"]
    agents = [
        (["invoice-agent", "AI agent (MCP)", "app-prod-03", "MCP · x-mcp.ru", "2 blocked at egress"], RED),
        (["support-bot", "LLM assistant", "app-prod-01", "Anthropic, OpenAI", "1 blocked · controlled"], AMBER),
        (["report-gen", "AI agent", "app-prod-01", "OpenAI", "Allowed · controlled"], GREEN),
        (["data-sync", "Service agent", "app-prod-02", "api.partner.com", "Allowed · controlled"], GREEN),
    ]
    end2 = table(ops, gy + 14, col_x, headers2, agents)

    ny = end2 + 16
    ops.append(T(40, ny,
                 "3 apps were shadow-exposed (internet-reachable, never onboarded) — now surfaced; reports.acme.com is onboarded to Advance.",
                 "F1", 8.5, MUTED))
    ops.append(T(40, ny + 15,
                 "Public apps: incoming is detected in detect mode (eBPF + parallel analysis). Onboard to Advance/Premium for cloud inline protection.",
                 "F1", 8.5, MUTED))
    ops.append(T(40, ny + 30,
                 "Agents: external egress (MCP / API / LLM) is blocked at the source when it violates policy.",
                 "F1", 8.5, MUTED))

    page_footer(ops)
    return ops


# ---------------------------------------------------------------------------
# PAGE 2 — attacks found (incoming detected + agent egress blocked)
# ---------------------------------------------------------------------------
def page2():
    ops = []
    header_band(ops, cont=True, page_no=2)

    sy = 74
    ops.append(T(40, sy, "Attacks found on your apps", "F2", 13, DARK))
    ops.append(T(40, sy + 14,
                 "Incoming attacks are identified in detect mode (eBPF observation + parallel log analysis). "
                 "Agent egress is blocked at the source.",
                 "F1", 8.5, MUTED))

    col_x = [40, 165, 345, 405, 478]
    headers = ["Vector", "Target app / endpoint", "Volume", "Peak", "Outcome"]

    # --- incoming, detected ---
    group_label(ops, sy + 36, "Incoming — detected (detect mode)",
                "observed via eBPF, identified after log ingestion — not blocked inline", note_x=255)
    incoming = [
        (["Credential stuffing", "reports.acme.com · /api/login", "42,118", "2,100/min", "Detected"], GREEN),
        (["Brute-force login", "login.acme.com · /login", "9,330", "480/min", "Detected"], GREEN),
        (["L7 HTTP flood", "reports.acme.com", "18,440", "9,100/s", "Detected"], GREEN),
        (["SQL injection probes", "checkout.acme.com · /search", "3,207", "—", "Detected"], GREEN),
        (["Reflected XSS", "checkout.acme.com · /cart", "1,942", "—", "Detected"], GREEN),
        (["Path traversal / LFI", "admin.acme.com · /../", "1,106", "—", "Detected"], GREEN),
        (["Directory brute-force", "admin.acme.com", "2,540", "—", "Detected"], GREEN),
        (["SSRF attempt", "store-api.acme.com · /fetch", "388", "—", "Detected"], GREEN),
        (["Command injection", "reports.acme.com · /export", "174", "—", "Detected"], GREEN),
        (["Open-redirect abuse", "checkout.acme.com · /out", "512", "—", "Detected"], GREEN),
        (["Sensitive-file scan", "multiple · .env / .git", "4,760", "—", "Detected"], GREEN),
        (["Malicious bot / scraper", "store-api.acme.com", "6,815", "—", "Detected"], GREEN),
        (["API enumeration (BOLA)", "store-api.acme.com · /v2", "903", "—", "Detected"], GREEN),
        (["Session / cookie tampering", "checkout.acme.com", "221", "—", "Detected"], GREEN),
    ]
    end_y = table(ops, sy + 50, col_x, headers, incoming)
    ops.append(T(40, end_y + 15,
                 "92,456 incoming attacks detected — identified from eBPF telemetry in detect mode (not blocked inline).",
                 "F2", 9, NAVY))

    # --- agent egress, blocked ---
    gy = end_y + 34
    group_label(ops, gy, "Agent egress — blocked at source",
                "outbound calls triggered by your agents (MCP / API / LLM)", note_x=255)
    egress = [
        (["Prompt injection (tool-call)", "invoice-agent -> MCP", "47", "—", "Blocked at egress"], RED),
        (["LLM data-exfil attempt", "support-bot -> external", "12", "—", "Blocked at egress"], RED),
        (["Unapproved MCP destination", "invoice-agent -> x-mcp.ru", "29", "—", "Blocked at egress"], RED),
        (["Outbound API-key leak", "support-bot -> api.*", "6", "—", "Blocked at egress"], RED),
    ]
    end_y2 = table(ops, gy + 14, col_x, headers, egress)
    ops.append(T(40, end_y2 + 15,
                 "94 agent-egress calls blocked at the source — enforced locally by the agent.",
                 "F2", 9, GREEN))

    page_footer(ops)
    return ops


# ---------------------------------------------------------------------------
# PAGE 3 — posture + value + AI egress policy + compliance
# ---------------------------------------------------------------------------
def page3():
    ops = []
    header_band(ops, cont=True, page_no=3)

    # Posture trend
    py = 78
    ops.append(T(40, py, "Posture trend — last 4 months", "F2", 12, DARK))
    base_top = 172
    bars = [("Aug", 54), ("Sep", 63), ("Oct", 74), ("Nov", 82)]
    bx = 60
    for label, score in bars:
        h = score * 0.7
        ops.append(rect(bx, base_top - h, 42, h, ACCENT))
        ops.append(T(bx + 9, base_top - h - 5, str(score), "F2", 9, NAVY))
        ops.append(T(bx + 11, base_top + 13, label, "F1", 8, MUTED))
        bx += 78
    ops.append(line(55, base_top, 370, base_top, BORDER, 0.6))

    # Quantified value (honest: detection value + real egress prevention)
    vy = 210
    ops.append(T(40, vy, "Quantified value — this month", "F2", 12, DARK))
    vals = [
        ("62 hrs", "analyst time saved on triage"),
        ("94", "risky AI egress calls blocked"),
        ("3 of 3", "shadow apps surfaced & evidenced"),
    ]
    vx = 40
    for amt, cap in vals:
        ops.append(rect(vx, vy + 12, 170, 46, LIGHT))
        ops.append(rect(vx, vy + 12, 3, 46, ACCENT))
        ops.append(T(vx + 12, vy + 34, amt, "F2", 16, NAVY))
        ops.append(T(vx + 12, vy + 50, cap, "F1", 8, MUTED))
        vx += 182

    # AI egress — under policy
    ey = 300
    ops.append(T(40, ey, "AI egress — every model / MCP call, under policy", "F2", 12, DARK))
    egress = [
        ("checkout-app  ->  OpenAI", "ALLOWED", GREEN),
        ("support-bot  ->  Anthropic", "ALLOWED", GREEN),
        ("invoice-agent  ->  x-mcp.ru", "BLOCKED · prompt-injection, stopped at source", RED),
    ]
    ly = ey + 18
    for left, status, col in egress:
        ops.append(T(48, ly + 12, left, "F1", 9, DARK))
        ops.append(T(300, ly + 12, status, "F2", 9, col))
        ops.append(line(40, ly + 18, 572, ly + 18, BORDER, 0.4))
        ly += 20

    # Compliance
    cy = 410
    ops.append(T(40, cy, "Compliance evidence — auto-mapped to what the agent observed", "F2", 12, DARK))
    badges = ["PCI DSS 6.4 / 11.5", "SOC 2 CC6.1 / CC7.2", "ISO 27001 A.8.16", "NIST CSF DE.CM"]
    bx = 40
    for b in badges:
        bw = 130
        ops.append(rect(bx, cy + 14, bw, 22, LIGHT))
        ops.append(rect(bx + 8, cy + 22, 6, 6, GREEN))
        ops.append(T(bx + 20, cy + 29, b, "F1", 8, DARK))
        bx += bw + 6

    ops.append(T(40, cy + 60,
                 "Detection evidence (DE.CM) comes from the agent's observation path; egress enforcement is logged at the source.",
                 "F1", 8, MUTED))

    page_footer(ops)
    return ops


# ---------------------------------------------------------------------------
# PDF assembly
# ---------------------------------------------------------------------------
def build(pages_ops):
    out = bytearray()
    out += b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    offsets = {}

    def add(num, body):
        offsets[num] = len(out)
        out.extend(f"{num} 0 obj\n".encode("latin-1"))
        out.extend(body)
        out.extend(b"\nendobj\n")

    n = len(pages_ops)
    kids = " ".join(f"{5 + 2 * i} 0 R" for i in range(n))
    add(1, b"<< /Type /Catalog /Pages 2 0 R >>")
    add(2, f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode("latin-1"))
    add(3, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    add(4, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

    for i, ops in enumerate(pages_ops):
        pagenum, contentnum = 5 + 2 * i, 6 + 2 * i
        sb = "".join(ops).encode("cp1252")
        page = (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W} {H}] "
                f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {contentnum} 0 R >>")
        add(pagenum, page.encode("latin-1"))
        add(contentnum, b"<< /Length " + str(len(sb)).encode() + b" >>\nstream\n" + sb + b"\nendstream")

    xref_pos = len(out)
    maxnum = 4 + 2 * n
    out.extend(f"xref\n0 {maxnum + 1}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for num in range(1, maxnum + 1):
        out.extend(f"{offsets[num]:010d} 00000 n \n".encode("latin-1"))
    out.extend(f"trailer\n<< /Size {maxnum + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode("latin-1"))
    return bytes(out)


def main():
    pdf = build([page1(), page2(), page3()])
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "wb") as f:
        f.write(pdf)
    print(f"Wrote {OUT_PATH}  ({len(pdf):,} bytes)")


if __name__ == "__main__":
    main()
