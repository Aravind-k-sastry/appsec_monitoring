"""
Marketing page content for the Barracuda AppShield Agent pitch site.

Everything here is present-tense, productized copy for a smoke-test ("fake door")
landing experience. The product does not ship yet — the site is designed to
measure real buyer intent via the "Book a demo" CTA and page/CTA analytics.

PRODUCT is the single source of truth for the brand name; change it in one place.
"""

import html

PRODUCT = "Barracuda AppShield Agent"
SHORT = "AppShield Agent"
TAGLINE = "One agent. Total application visibility. Protection you switch on."

# NAV: (path, label)
NAV = [
    ("/", "Overview"),
    ("/how-it-works", "How it works"),
    ("/experience", "Experience"),
    ("/use-cases", "Use cases"),
    ("/pricing", "Pricing"),
    ("/survey", "Survey"),
    ("/demo", "Book a demo"),
]


def home():
    return f"""
<section class="hero">
  <div class="wrap">
    <span class="pill"><span class="live"></span> Now in early access · Barracuda Application Security</span>
    <h1>You can't defend what you can't see.<br>
      <span class="accent">Find out what's really happening on your servers.</span></h1>
    <p class="lede">
      Your cloud WAF guards the front door. Meanwhile, services talk to each other, forgotten apps sit
      exposed, and AI agents call out to the internet — all unseen. {SHORT} installs in minutes and shows you
      every bit of it, so you find the risk before an attacker — or an auditor — does.
    </p>
    <div class="cta-row">
      <a class="btn btn-cta" href="/demo" data-cta="hero_demo">Book a demo &rarr;</a>
      <a class="btn btn-ghost" href="/how-it-works" data-cta="hero_how">See how it works</a>
      <span class="cta-note">No DNS changes · No re-routing to start · Deploys in &lt;10 min</span>
    </div>
    <div class="hero-metrics">
      <div class="m"><div class="n">3</div><div class="l">blind spots closed on day one</div></div>
      <div class="m"><div class="n">&lt;10 min</div><div class="l">to first signal</div></div>
      <div class="m"><div class="n">1</div><div class="l">agent across visibility, protection &amp; AI governance</div></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center">
      <div class="eyebrow">The problem</div>
      <h2>Your cloud WAF only sees traffic routed through it</h2>
      <p class="sub">Three things stay invisible — and attackers know it.</p>
    </div>
    <div class="grid g3">
      <div class="card"><span class="ic">&#x2194;&#xFE0F;</span>
        <h3>East-West traffic</h3>
        <p>Service-to-service calls never leave your data center, so a cloud proxy never sees them. Lateral movement hides here.</p></div>
      <div class="card"><span class="ic">&#x1F441;&#xFE0F;</span>
        <h3>Shadow exposure</h3>
        <p>Apps that are publicly reachable but were never put behind the WAF. You can't protect what you don't know is exposed.</p></div>
      <div class="card"><span class="ic">&#x1F916;</span>
        <h3>AI activity</h3>
        <p>Which apps exchange LLM prompts, with which models, and whether agents on your hosts are reaching external MCP servers and APIs.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center">
      <div class="eyebrow">What you'd see</div>
      <h2 class="center mt0">Day one, the blind spots become a list you can act on</h2>
      <p class="sub">The same three gaps above — now surfaced, named, and ranked. This is the view minutes after the agent is running.</p>
    </div>
    <div class="screen">
      <div class="screen-bar">
        <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
        <span class="screen-title">{SHORT} · Findings — <span class="muted">app-prod-01</span></span>
        <span class="screen-live"><span class="live"></span> live · 00:08 since deploy</span>
      </div>
      <div class="screen-body">
        <div class="finding sev-high">
          <div class="f-tag">EXPOSURE</div>
          <div class="f-main">
            <strong>3 shadow-exposed apps found</strong>
            <span><code>reports-api</code> is reachable from the internet and was never put behind the WAF. 2 others listed.</span>
          </div>
          <div class="f-act">Onboard &rarr;</div>
        </div>
        <div class="finding sev-high">
          <div class="f-tag">EAST-WEST</div>
          <div class="f-main">
            <strong>Unusual service-to-service call</strong>
            <span><code>payments-svc</code> reached an external host it has never contacted before — possible lateral movement.</span>
          </div>
          <div class="f-act">Investigate &rarr;</div>
        </div>
        <div class="finding sev-med">
          <div class="f-tag">AI</div>
          <div class="f-main">
            <strong>AI footprint mapped · 1 prompt-injection attempt</strong>
            <span><code>checkout-app &rarr; OpenAI</code>, <code>support-bot &rarr; Anthropic</code>. One injection attempt blocked on <code>support-bot</code>.</span>
          </div>
          <div class="f-act">View map &rarr;</div>
        </div>
        <div class="finding sev-info">
          <div class="f-tag">ATTACKS</div>
          <div class="f-main">
            <strong>1,204 attacks on your login endpoint this week</strong>
            <span>Credential-stuffing pattern against <code>/api/login</code> — visible now, one click to put it behind inline protection.</span>
          </div>
          <div class="f-act">Protect &rarr;</div>
        </div>
      </div>
    </div>
    <p class="center muted" style="margin-top:14px;font-size:12.5px">Illustrative findings view. Your demo runs on a host like yours — the findings are real.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center">
      <div class="eyebrow">What it means for you</div>
      <h2 class="center mt0">One agent, read differently by every seat at the table</h2>
      <p class="sub">The value lands differently depending on who's asking — it's the same agent underneath.</p>
    </div>
    <div class="grid g3">
      <div class="card"><span class="ic">&#x1F575;&#xFE0F;</span><h3 class="cyan">SOC analyst</h3>
        <p>"I finally see what my services say to each other." Catch lateral movement the perimeter never showed — with host context that makes an alert actionable, not noise.</p></div>
      <div class="card"><span class="ic">&#x1F6E0;&#xFE0F;</span><h3 class="green">App owner</h3>
        <p>"I know every app I'm exposing — and I can protect the ones that matter without a re-architecture." Start by seeing, switch on inline protection per app when you're ready.</p></div>
      <div class="card"><span class="ic">&#x1F9D1;&#x200D;&#x2696;&#xFE0F;</span><h3 class="amber">CISO</h3>
        <p>"I can finally answer what our AI is doing." Map which apps call which models, govern agent egress to an allowed boundary, and show the board a picture instead of a shrug.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center">
      <div class="eyebrow">How it works</div>
      <h2 class="center mt0">See first. Protect when you're ready.</h2>
      <p class="sub">You start with visibility — nothing is re-routed, nothing inline can break your app. You turn on protection only where you decide it's worth it.</p>
    </div>
    <div class="grid g3">
      <div class="card"><h3 class="cyan">1 · See</h3>
        <p>Mount the agent. It sends telemetry only — attacks, East-West traffic, and AI prompt activity on the apps you choose. Zero risk to the running app.</p></div>
      <div class="card"><h3 class="green">2 · Protect</h3>
        <p>Route the public apps worth protecting through the Barracuda cloud: full inline WAF, L3–L7 DDoS, bot and volumetric absorption — scale handled off your host.</p></div>
      <div class="card"><h3 class="amber">3 · Govern</h3>
        <p>Identify agents calling external MCPs and APIs, and fence them to an allowed boundary. Enforcement is pushed down to the agent at the source.</p></div>
    </div>
    <div class="center" style="margin-top:34px">
      <a class="btn btn-ghost" href="/how-it-works" data-cta="home_how">See the architecture &rarr;</a>
      <a class="btn btn-primary" href="/use-cases" data-cta="home_usecases" style="margin-left:10px">Explore use cases &rarr;</a>
    </div>
  </div>
</section>

<section style="border-bottom:0">
  <div class="wrap">
    <div class="band">
      <h2>See this list for your own servers</h2>
      <p class="sub">A 20-minute walkthrough on a host like yours: deploy the agent, surface your blind spots, switch protection on live.</p>
      <a class="btn btn-cta" href="/demo" data-cta="band_demo">Book your demo &rarr;</a>
    </div>
  </div>
</section>
"""


def how_it_works():
    return f"""
<section class="hero" style="padding-bottom:30px">
  <div class="wrap">
    <span class="pill"><span class="live"></span> Architecture</span>
    <h1>How <span class="accent">{SHORT}</span> works</h1>
    <p class="lede">A thin agent on the host does the seeing. The Barracuda cloud does the thinking.
      Policy is pushed back down when you're ready to enforce.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="flow">
      <div class="node"><div class="step">STEP 1</div><strong>Agent on your server</strong>
        <span>Captures request metadata, app-to-app interactions, and AI prompt activity. Lightweight and inspection-focused.</span></div>
      <div class="arrow">&rarr;</div>
      <div class="node"><div class="step">STEP 2</div><strong>Barracuda cloud brain</strong>
        <span>Analyzes the telemetry, flags likely attacks, and builds a live map of what's running and talking to what.</span></div>
      <div class="arrow">&rarr;</div>
      <div class="node"><div class="step">STEP 3</div><strong>Policy push-down</strong>
        <span>When you choose to enforce, rules go back to the agent — block the next matching request, or fence an agent's egress.</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center"><div class="eyebrow">The architecture</div>
      <h2 class="center mt0">Thin agent on the host, intelligence in the cloud</h2>
      <p class="sub">One agent captures and enforces locally; the Barracuda cloud analyzes, inspects AI prompts, and pushes policy back down. Selected public apps route to the cloud proxy for scale the host never carries.</p></div>
    <div style="overflow-x:auto">
      <svg viewBox="0 0 980 600" width="100%" style="max-width:980px;display:block;margin:0 auto" role="img" aria-label="AppShield Agent architecture: a thin agent on the customer host captures inbound (N-S), internal (E-W) and AI activity and sends compact telemetry to the Barracuda cloud brain, which analyzes it, runs prompt inspection, and pushes policy back down to the agent; selected public apps route to the cloud proxy for inline scale, and alerts surface to the SOC/XDR.">
        <defs>
          <marker id="arB" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#26a1ff"/></marker>
          <marker id="arC" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#00edff"/></marker>
          <marker id="arG" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#0cf2a5"/></marker>
        </defs>

        <rect x="20" y="70" width="430" height="380" rx="14" fill="#11161d" stroke="#30363d"/>
        <rect x="560" y="70" width="400" height="380" rx="14" fill="#11161d" stroke="#30363d"/>
        <text x="40" y="102" fill="#00edff" font-family="Arial" font-size="13" font-weight="700" letter-spacing="2">YOUR SERVER</text>
        <text x="580" y="102" fill="#00edff" font-family="Arial" font-size="13" font-weight="700" letter-spacing="2">BARRACUDA CLOUD</text>

        <rect x="40" y="124" width="118" height="56" rx="9" fill="#0b0f14" stroke="#26a1ff"/>
        <text x="99" y="149" text-anchor="middle" fill="#e6edf3" font-family="Arial" font-size="13">Public app</text>
        <text x="99" y="167" text-anchor="middle" fill="#8b949e" font-family="Arial" font-size="10.5">inbound · N-S</text>
        <rect x="170" y="124" width="140" height="56" rx="9" fill="#0b0f14" stroke="#8b949e"/>
        <text x="240" y="149" text-anchor="middle" fill="#e6edf3" font-family="Arial" font-size="13">Service &#8596; service</text>
        <text x="240" y="167" text-anchor="middle" fill="#8b949e" font-family="Arial" font-size="10.5">internal · E-W</text>
        <rect x="322" y="124" width="96" height="56" rx="9" fill="#0b0f14" stroke="#f5b300"/>
        <text x="370" y="149" text-anchor="middle" fill="#e6edf3" font-family="Arial" font-size="12">AI app / agent</text>
        <text x="370" y="167" text-anchor="middle" fill="#8b949e" font-family="Arial" font-size="10">LLM · MCP</text>

        <line x1="14" y1="152" x2="38" y2="152" stroke="#26a1ff" stroke-width="1.5" marker-end="url(#arB)"/>
        <line x1="99" y1="180" x2="99" y2="230" stroke="#00edff" stroke-width="1.5" marker-end="url(#arC)"/>
        <line x1="240" y1="180" x2="240" y2="230" stroke="#00edff" stroke-width="1.5" marker-end="url(#arC)"/>
        <line x1="370" y1="180" x2="370" y2="230" stroke="#00edff" stroke-width="1.5" marker-end="url(#arC)"/>

        <rect x="40" y="232" width="390" height="150" rx="12" fill="#0e2a30" stroke="#00edff" stroke-width="1.6"/>
        <text x="58" y="266" fill="#00edff" font-family="Arial" font-size="16" font-weight="700">Barracuda AppShield Agent</text>
        <text x="58" y="294" fill="#c9d2dc" font-family="Arial" font-size="12.5">Captures request metadata, app-to-app (E-W) calls,</text>
        <text x="58" y="312" fill="#c9d2dc" font-family="Arial" font-size="12.5">and AI prompt activity</text>
        <text x="58" y="336" fill="#c9d2dc" font-family="Arial" font-size="12.5">Extracts parameters · inspects locally · enforces policy</text>
        <text x="58" y="360" fill="#8b949e" font-family="Arial" font-size="11">Lightweight &#8212; data stays on the host unless sampled</text>
        <text x="40" y="410" fill="#8b949e" font-family="Arial" font-size="11.5">Deploys in minutes · no DNS change · no re-routing to start</text>

        <line x1="430" y1="280" x2="556" y2="150" stroke="#00edff" stroke-width="1.6" marker-end="url(#arC)"/>
        <text x="494" y="198" text-anchor="middle" fill="#00edff" font-family="Arial" font-size="11">compact telemetry &#9650;</text>
        <line x1="558" y1="300" x2="434" y2="344" stroke="#26a1ff" stroke-width="1.6" marker-end="url(#arB)"/>
        <text x="496" y="336" text-anchor="middle" fill="#26a1ff" font-family="Arial" font-size="11">policy push-down &#9660;</text>

        <rect x="580" y="124" width="360" height="62" rx="9" fill="#0b0f14" stroke="#26a1ff"/>
        <text x="598" y="149" fill="#e6edf3" font-family="Arial" font-size="14" font-weight="700">Cloud brain</text>
        <text x="598" y="170" fill="#8b949e" font-family="Arial" font-size="11.5">telemetry analysis · attack detection · live app map</text>
        <rect x="580" y="200" width="360" height="56" rx="9" fill="#0b0f14" stroke="#f5b300"/>
        <text x="598" y="223" fill="#e6edf3" font-family="Arial" font-size="14" font-weight="700">Prompt Inspector</text>
        <text x="598" y="243" fill="#8b949e" font-family="Arial" font-size="11.5">prompt injection · jailbreak · data-leak checks</text>
        <rect x="580" y="270" width="360" height="56" rx="9" fill="#0b0f14" stroke="#26a1ff"/>
        <text x="598" y="293" fill="#e6edf3" font-family="Arial" font-size="14" font-weight="700">Policy engine</text>
        <text x="598" y="313" fill="#8b949e" font-family="Arial" font-size="11.5">builds rules &#8212; pushes them down to the agent</text>

        <line x1="760" y1="186" x2="760" y2="200" stroke="#26a1ff" stroke-width="1.4" marker-end="url(#arB)"/>
        <line x1="760" y1="256" x2="760" y2="270" stroke="#26a1ff" stroke-width="1.4" marker-end="url(#arB)"/>

        <line x1="580" y1="345" x2="940" y2="345" stroke="#30363d" stroke-width="1" stroke-dasharray="4 4"/>
        <text x="760" y="358" text-anchor="middle" fill="#8b949e" font-family="Arial" font-size="10">data plane · scale</text>
        <rect x="580" y="364" width="360" height="74" rx="9" fill="#0b0f14" stroke="#0cf2a5"/>
        <text x="598" y="387" fill="#e6edf3" font-family="Arial" font-size="14" font-weight="700">Cloud proxy &#8212; inline scale</text>
        <text x="598" y="407" fill="#8b949e" font-family="Arial" font-size="11.5">WAF · L3&#8211;L7 DDoS · bot &amp; volumetric absorption</text>
        <text x="598" y="426" fill="#0cf2a5" font-family="Arial" font-size="11">public apps you choose route here &#8212; load off your host</text>

        <line x1="700" y1="450" x2="700" y2="506" stroke="#00edff" stroke-width="1.5" marker-end="url(#arC)"/>
        <text x="712" y="484" fill="#00edff" font-family="Arial" font-size="11">alerts &amp; findings &#8594; XDR</text>
        <rect x="560" y="510" width="400" height="70" rx="12" fill="#0b0f14" stroke="#00edff"/>
        <text x="760" y="539" text-anchor="middle" fill="#e6edf3" font-family="Arial" font-size="14" font-weight="700">Your security team · SOC / XDR</text>
        <text x="760" y="561" text-anchor="middle" fill="#8b949e" font-family="Arial" font-size="11.5">malicious-intent alerts and findings surface here</text>
      </svg>
    </div>
    <div class="center" style="margin-top:14px;font-size:12.5px;color:#8b949e">
      <span style="color:#00edff">&#9679;</span> visibility &amp; telemetry &nbsp;·&nbsp;
      <span style="color:#0cf2a5">&#9679;</span> inline protection (scale) &nbsp;·&nbsp;
      <span style="color:#f5b300">&#9679;</span> AI inspection &nbsp;·&nbsp;
      <span style="color:#26a1ff">&#9679;</span> control &amp; policy
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">Design principles</div>
      <h2 class="mt0">Honest about what runs where</h2></div>
    <div class="grid g2">
      <div class="card"><h3 class="cyan">The agent handles reach</h3>
        <p>It sees East-West traffic, un-onboarded exposed apps, and AI/agent activity — things that never pass through a cloud proxy. It extracts and inspects locally, so your data stays on the host unless sampled.</p></div>
      <div class="card"><h3 class="green">The cloud handles scale</h3>
        <p>Heavy, elastic load — DDoS, bots, volumetric attacks, line-rate ML — is absorbed by the Barracuda cloud, never your host. The agent stays light by design.</p></div>
      <div class="card"><h3 class="amber">Prompt inspection, built in</h3>
        <p>AI prompt analysis runs through Barracuda's Prompt Inspector service — prompt injection, jailbreak, and data-leak checks — with malicious-intent alerts surfaced to your security team.</p></div>
      <div class="card"><h3>Straight talk on overhead</h3>
        <p>The agent uses some host CPU to inspect — we'd rather say so than oversell it. The heavy scale load is exactly what moves off the host. You choose how deep inspection goes per app.</p></div>
    </div>
  </div>
</section>

<section style="border-bottom:0">
  <div class="wrap"><div class="band">
    <h2>Want the architecture deep-dive?</h2>
    <p class="sub">We'll walk your team through deployment, data handling, and the enforcement model.</p>
    <a class="btn btn-cta" href="/demo" data-cta="how_demo">Book a technical demo &rarr;</a>
  </div></div>
</section>
"""


def use_cases():
    return f"""
<section class="hero" style="padding-bottom:30px">
  <div class="wrap">
    <span class="pill"><span class="live"></span> Use cases</span>
    <h1>What <span class="accent">{SHORT}</span> is used for</h1>
    <p class="lede">From the SOC analyst chasing lateral movement to the CISO governing AI — one agent, many jobs.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid g2">
      <div class="card"><span class="ic">&#x2194;&#xFE0F;</span><h3>Catch lateral movement (East-West)</h3>
        <p>Surface service-to-service calls a cloud WAF never sees. Spot an app reaching something it never should — the first sign of an attacker moving inside.</p></div>
      <div class="card"><span class="ic">&#x1F575;&#xFE0F;</span><h3>Find shadow-exposed apps</h3>
        <p>Discover applications that are publicly reachable but were never put behind the WAF — before an attacker does. Then onboard them with one click.</p></div>
      <div class="card"><span class="ic">&#x1F916;</span><h3>See your AI footprint</h3>
        <p>Map which apps exchange LLM prompts, with which models, and flag prompt injection, jailbreaks, and data leakage against your own AI apps.</p></div>
      <div class="card"><span class="ic">&#x1F6A7;</span><h3>Govern agent egress</h3>
        <p>For the CISO: identify AI agents on your hosts calling external MCP servers and APIs, and fence them to an allowed boundary — enforced at the source.</p></div>
      <div class="card"><span class="ic">&#x1F6E1;&#xFE0F;</span><h3>Protect public apps at scale</h3>
        <p>Route your internet-facing apps through the Barracuda cloud for full inline WAF, DDoS, and bot defense — without the heavy load ever touching your host.</p></div>
      <div class="card"><span class="ic">&#x1F4CA;</span><h3>Prove exposure to leadership</h3>
        <p>"Here are the attacks hitting your login endpoint this week, and the three exposed apps we found." Turn invisible risk into a board-ready picture.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center"><div class="eyebrow">In the field</div><h2 class="center mt0">Why it resonates</h2></div>
    <div class="grid g2">
      <div class="quote"><p>"We route our front door through a WAF, but we've never had eyes on what our services say to each other. That's the gap that keeps me up."</p><div class="who">— Head of Security, mid-market SaaS <span class="muted">(illustrative)</span></div></div>
      <div class="quote"><p>"Every team is shipping AI features and nobody can tell me what they're calling out to. I need that map yesterday."</p><div class="who">— CISO, regional financial services <span class="muted">(illustrative)</span></div></div>
    </div>
  </div>
</section>

<section style="border-bottom:0">
  <div class="wrap"><div class="band">
    <h2>Which of these is your problem?</h2>
    <p class="sub">Tell us on the call — we'll tailor the walkthrough to it.</p>
    <a class="btn btn-cta" href="/demo" data-cta="usecases_demo">Book a demo &rarr;</a>
  </div></div>
</section>
"""


def experience():
    return f"""
<section class="hero" style="padding-bottom:26px">
  <div class="wrap">
    <span class="pill"><span class="live"></span> The experience</span>
    <h1>What you actually get,<br><span class="accent">from minute one</span></h1>
    <p class="lede">
      Not a feature list — the real journey. Here's what you do, what you see on screen, and what it
      feels like, from the first install command to the report you hand your board.
    </p>
    <div class="jstepper" style="margin-top:30px">
      <span class="st"><b>1</b> Deploy</span><span class="sep">&rsaquo;</span>
      <span class="st"><b>2</b> See</span><span class="sep">&rsaquo;</span>
      <span class="st"><b>3</b> Investigate</span><span class="sep">&rsaquo;</span>
      <span class="st"><b>4</b> Protect</span><span class="sep">&rsaquo;</span>
      <span class="st"><b>5</b> Govern</span><span class="sep">&rsaquo;</span>
      <span class="st"><b>6</b> Prove</span>
    </div>
  </div>
</section>

<!-- STEP 1 — DEPLOY -->
<section style="padding-top:40px">
  <div class="wrap">
    <div class="jstep">
      <div class="jcopy">
        <span class="num">1</span><span class="when">Minute 0&ndash;10 · you</span>
        <h3>You paste one command. That's the install.</h3>
        <p>Create an account, copy a single install line, and run it on a server. No DNS changes,
          no re-routing, no app restart, no agent to hand-build. It connects to the Barracuda cloud and
          starts watching the apps you point it at.</p>
        <div class="feel"><b>Feel:</b><span>&ldquo;That was it?&rdquo; &mdash; you went from nothing to live
          telemetry before your coffee cooled.</span></div>
      </div>
      <div class="screen">
        <div class="screen-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="screen-title">root@app-prod-01 &mdash; install</span>
          <span class="screen-live"><span class="live"></span> connecting</span></div>
        <div class="screen-body"><div class="term">
<span class="p">$</span> curl -sSL https://get.barracuda.app/agent | sh -s -- --key=<span class="hl">AKP-7Q2F</span><br>
<span class="dim">Downloading AppShield Agent (12 MB)… done</span><br>
<span class="ok">&#10003;</span> Agent installed &nbsp;<span class="dim">v1.4.0</span><br>
<span class="ok">&#10003;</span> Connected to Barracuda cloud &nbsp;<span class="dim">region: us-east</span><br>
<span class="ok">&#10003;</span> Discovering apps on this host…<br>
<span class="ok">&#10003;</span> Now watching <span class="hl">6 apps</span> · telemetry only · <span class="dim">no traffic re-routed</span><br>
<span class="dim">→ Open console: https://console.barracuda.app/app-prod-01</span>
        </div></div>
      </div>
    </div>
  </div>
</section>

<!-- STEP 2 — SEE -->
<section style="padding-top:0;border-bottom:0">
  <div class="wrap">
    <div class="jstep rev">
      <div class="jcopy">
        <span class="num">2</span><span class="when">Minute 10 · the console</span>
        <h3>The console lights up with the surface you've never had in one place.</h3>
        <p>Every app on the host, side by side: which are internet-exposed, which talk service-to-service,
          which call AI models. Three blind spots are already flagged &mdash; before you&rsquo;ve configured a thing.</p>
        <div class="feel"><b>Feel:</b><span>&ldquo;I didn&rsquo;t know that was running.&rdquo; &mdash; your real
          attack surface, not the one on the architecture diagram.</span></div>
      </div>
      <div class="screen">
        <div class="screen-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="screen-title">{SHORT} · Dashboard &mdash; <span class="muted">app-prod-01</span></span>
          <span class="screen-live"><span class="live"></span> live</span></div>
        <div class="screen-body"><div class="ui-grid">
          <div class="ui-side">
            <a class="on">&#9632;&nbsp; Dashboard</a><a>&#9888;&nbsp; Findings</a><a>&#129302;&nbsp; AI map</a>
            <a>&#128737;&nbsp; Protection</a><a>&#128272;&nbsp; Egress</a><a>&#128202;&nbsp; Reports</a>
          </div>
          <div class="ui-main">
            <div class="tiles">
              <div class="tile"><div class="n">6</div><div class="l">apps discovered</div></div>
              <div class="tile bad"><div class="n">3</div><div class="l">blind spots</div></div>
              <div class="tile warn"><div class="n">1,204</div><div class="l">attacks / wk</div></div>
              <div class="tile"><div class="n">2</div><div class="l">apps calling AI</div></div>
            </div>
            <div class="rowline"><span class="app">reports-api <small>internet-exposed · never onboarded</small></span><span class="chip risk">SHADOW</span></div>
            <div class="rowline"><span class="app">payments-svc <small>east-west · new external peer</small></span><span class="chip risk">ANOMALY</span></div>
            <div class="rowline"><span class="app">checkout-app <small>N-S · behind WAF</small></span><span class="chip see">MONITORED</span></div>
            <div class="rowline"><span class="app">support-bot <small>calls Anthropic · LLM</small></span><span class="chip see">MONITORED</span></div>
          </div>
        </div></div>
      </div>
    </div>
  </div>
</section>

<!-- STEP 3 — INVESTIGATE -->
<section style="padding-top:0;border-bottom:0">
  <div class="wrap">
    <div class="jstep">
      <div class="jcopy">
        <span class="num">3</span><span class="when">Day 1 · the analyst</span>
        <h3>Click a finding and it opens with host context you can act on.</h3>
        <p>Which process, which identity, what it talked to, and why it&rsquo;s suspicious &mdash; ranked by
          severity. A credential-stuffing run on your login endpoint. A payments service reaching a host it
          has never contacted before.</p>
        <div class="feel"><b>Feel:</b><span>&ldquo;Now I can chase this.&rdquo; &mdash; an alert with a thread
          to pull, not a number on a dashboard.</span></div>
      </div>
      <div class="screen">
        <div class="screen-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="screen-title">{SHORT} · Findings</span>
          <span class="screen-live"><span class="live"></span> 4 open</span></div>
        <div class="screen-body">
          <div class="finding sev-high"><div class="f-tag">EXPOSURE</div>
            <div class="f-main"><strong>3 shadow-exposed apps found</strong>
              <span><code>reports-api</code> is reachable from the internet and was never put behind the WAF.</span></div>
            <div class="f-act">Onboard &rarr;</div></div>
          <div class="finding sev-high"><div class="f-tag">EAST-WEST</div>
            <div class="f-main"><strong>Unusual service-to-service call</strong>
              <span><code>payments-svc</code> reached an external host it has never contacted &mdash; possible lateral movement.</span></div>
            <div class="f-act">Investigate &rarr;</div></div>
          <div class="finding sev-info"><div class="f-tag">ATTACKS</div>
            <div class="f-main"><strong>1,204 attacks on your login endpoint this week</strong>
              <span>Credential-stuffing against <code>/api/login</code> &mdash; one click to put it behind inline protection.</span></div>
            <div class="f-act">Protect &rarr;</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STEP 4 — PROTECT -->
<section style="padding-top:0;border-bottom:0">
  <div class="wrap">
    <div class="jstep rev">
      <div class="jcopy">
        <span class="num">4</span><span class="when">When you&rsquo;re ready · the app owner</span>
        <h3>Decide an app is worth protecting. Flip one toggle.</h3>
        <p>It routes through the Barracuda cloud &mdash; full inline WAF, L3&ndash;L7 DDoS and bot absorption
          handled off your host. Seeing never risked the app; switching on protection is a decision, not a
          re-architecture.</p>
        <div class="feel"><b>Feel:</b><span>&ldquo;One switch, not a quarter of work.&rdquo; &mdash; protection
          becomes something you turn on per app, when it earns it.</span></div>
      </div>
      <div class="screen">
        <div class="screen-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="screen-title">{SHORT} · Protection</span>
          <span class="screen-live"><span class="live"></span> saving…</span></div>
        <div class="screen-body" style="padding:14px">
          <div class="rowline"><span class="app">reports-api <small>just routed through cloud · inline WAF + DDoS</small></span>
            <span class="chip prot">PROTECTED</span><span class="toggle on"><span></span></span></div>
          <div class="rowline"><span class="app">checkout-app <small>routed through cloud</small></span>
            <span class="chip prot">PROTECTED</span><span class="toggle on"><span></span></span></div>
          <div class="rowline"><span class="app">payments-svc <small>internal · visibility only</small></span>
            <span class="chip see">MONITORING</span><span class="toggle"><span></span></span></div>
          <div class="rowline"><span class="app">support-bot <small>internal · visibility only</small></span>
            <span class="chip see">MONITORING</span><span class="toggle"><span></span></span></div>
          <p class="muted" style="font-size:12px;margin:10px 2px 0">Toggle on &rarr; traffic routes to the Barracuda cloud. The heavy load never touches your host.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STEP 5 — GOVERN -->
<section style="padding-top:0;border-bottom:0">
  <div class="wrap">
    <div class="jstep">
      <div class="jcopy">
        <span class="num">5</span><span class="when">Ongoing · the CISO</span>
        <h3>See every AI agent&rsquo;s egress &mdash; and fence it.</h3>
        <p>Which apps call which models, which agents reach external MCP servers and APIs. Set an allowed
          boundary; anything outside it is blocked at the source and surfaced to your SOC. One flagged
          prompt-injection attempt, already stopped.</p>
        <div class="feel"><b>Feel:</b><span>&ldquo;I can finally answer what our AI is doing.&rdquo; &mdash;
          the map the board keeps asking for.</span></div>
      </div>
      <div class="screen">
        <div class="screen-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="screen-title">{SHORT} · AI egress</span>
          <span class="screen-live"><span class="live"></span> policy active</span></div>
        <div class="screen-body" style="padding:12px">
          <div class="map">
            <div class="col">
              <div class="mnode">checkout-app<small>your app</small></div>
              <div class="mnode">support-bot<small>your app</small></div>
              <div class="mnode flag">invoice-agent<small>MCP · unknown dest</small></div>
            </div>
            <div class="mid"><div class="ar">&rarr;</div>egress</div>
            <div class="col">
              <div class="mnode">OpenAI<small>allowed</small></div>
              <div class="mnode">Anthropic<small>allowed</small></div>
              <div class="mnode flag">x-mcp.ru<small>blocked</small></div>
            </div>
          </div>
          <div class="rowline" style="margin-top:10px"><span class="app">checkout-app &rarr; OpenAI</span><span class="chip allow">ALLOWED</span></div>
          <div class="rowline"><span class="app">invoice-agent &rarr; x-mcp.ru <small>prompt-injection attempt · stopped at source</small></span><span class="chip block">BLOCKED</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STEP 6 — PROVE -->
<section style="padding-top:0;border-bottom:0">
  <div class="wrap">
    <div class="jstep rev">
      <div class="jcopy">
        <span class="num">6</span><span class="when">Monthly · leadership</span>
        <h3>Hand leadership a picture, not a shrug.</h3>
        <p>A posture view that rolls up what changed: blind spots closed, attacks stopped, AI calls governed
          &mdash; with a one-click board report. The invisible risk you started with, now a trend line going
          the right way.</p>
        <div class="feel"><b>Feel:</b><span>&ldquo;A number I can stand behind.&rdquo; &mdash; the before/after
          you couldn&rsquo;t produce a month ago.</span></div>
      </div>
      <div class="screen">
        <div class="screen-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="screen-title">{SHORT} · Security posture</span>
          <span class="screen-live"><span class="live"></span> this month</span></div>
        <div class="screen-body" style="padding:14px">
          <div class="gauge">
            <div class="score">82<small>/100</small></div>
            <div class="meta">Posture score <b>&uarr; from 54</b> at install<br>
              <span class="muted" style="font-size:12px">3 blind spots closed · 2 apps now protected · AI egress governed</span></div>
          </div>
          <div class="sumbar"><div class="lab"><span>Blind spots closed</span><span>3 / 3</span></div><div class="track"><span style="width:100%"></span></div></div>
          <div class="sumbar"><div class="lab"><span>Attacks absorbed off-host</span><span>18,400</span></div><div class="track"><span style="width:88%"></span></div></div>
          <div class="sumbar"><div class="lab"><span>AI calls under policy</span><span>100%</span></div><div class="track"><span style="width:100%"></span></div></div>
          <p class="muted" style="font-size:12px;margin:10px 2px 0">&#8595; Export board report (PDF)</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section style="border-top:1px solid var(--line)">
  <div class="wrap"><div class="band">
    <h2>Walk this journey on a host like yours</h2>
    <p class="sub">A 20-minute guided demo &mdash; deploy the agent, surface your blind spots, switch protection on live.</p>
    <a class="btn btn-cta" href="/demo" data-cta="experience_demo">Book your demo &rarr;</a>
  </div></div>
</section>
"""


def pricing():
    return f"""
<section class="hero" style="padding-bottom:26px">
  <div class="wrap">
    <span class="pill"><span class="live"></span> Pricing</span>
    <h1>Start with visibility.<br><span class="accent">Pay to turn protection on.</span></h1>
    <p class="lede">Four plans, one agent. Land with low-cost visibility, expand into inline protection,
      and add AI governance when you need it. Prices shown are introductory early-access rates.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="tiers">
      <div class="tier">
        <div class="name">Starter</div>
        <div class="who">App owner · the land</div>
        <div class="price">$<span>10</span><span class="period">/server/mo</span></div>
        <ul>
          <li>One agent per physical server — deploy in minutes</li>
          <li>Log ingestion &amp; inspection</li>
          <li>Attack detection &amp; analysis (visibility)</li>
          <li>East-West traffic visibility</li>
          <li>AI prompt activity visibility</li>
          <li class="off">Inline protection</li>
          <li class="off">DDoS / bot absorption</li>
        </ul>
        <a class="btn btn-ghost" href="/demo" data-cta="price_starter">Start now</a>
      </div>

      <div class="tier">
        <div class="name">Advance</div>
        <div class="who">App owner · protect</div>
        <div class="price">$<span>99</span><span class="period">/app/mo</span></div>
        <ul>
          <li>Everything in Starter</li>
          <li>Inline WAF (OWASP, 0-day, intel)</li>
          <li>Full-spectrum L3–L7 DDoS, unmetered</li>
          <li>Bot defense</li>
          <li>API security + ZTNA + CDN</li>
          <li class="off">On-host visibility add-on</li>
        </ul>
        <a class="btn btn-primary" href="/demo" data-cta="price_advance">Book a demo</a>
      </div>

      <div class="tier feature">
        <div class="ribbon">MOST POPULAR</div>
        <div class="name">Premium</div>
        <div class="who">App owner · protect+</div>
        <div class="price">$<span>249</span><span class="period">/app/mo</span></div>
        <ul>
          <li>Everything in Advance</li>
          <li>ML-based bot detection</li>
          <li>Automated API discovery</li>
          <li>Per-app dedicated IP + container</li>
          <li>60-day logs, multi-SIEM export</li>
          <li class="off">AI security suite</li>
        </ul>
        <a class="btn btn-cta" href="/demo" data-cta="price_premium">Book a demo</a>
      </div>

      <div class="tier">
        <div class="name">Premium+ <span class="badge new">AI</span></div>
        <div class="who">CISO · govern</div>
        <div class="price">$<span>449</span><span class="period">/app/mo</span></div>
        <ul>
          <li>Everything in Premium</li>
          <li>On-host visibility (E-W + AI)</li>
          <li>LLM / prompt inspection</li>
          <li>AI-crawler protection</li>
          <li>Agent egress governance (MCP/API)</li>
          <li>URL-sequencing defense</li>
        </ul>
        <a class="btn btn-primary" href="/demo" data-cta="price_premiumplus">Talk to sales</a>
      </div>
    </div>
    <p class="center muted" style="margin-top:16px;font-size:13px">
      Introductory early-access pricing. Starter is billed per physical server running the agent; protection tiers are billed per protected application. Volume and MSP pricing available on the call.
    </p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center"><div class="eyebrow">Compare</div><h2 class="center mt0">Capabilities by plan</h2></div>
    <table class="cmp">
      <tr><th>Capability</th><th>Starter</th><th>Advance</th><th>Premium</th><th>Premium+</th></tr>
      <tr><td>Core WAF detection</td><td class="see">See</td><td class="yes">Protect</td><td class="yes">Protect</td><td class="yes">Protect</td></tr>
      <tr><td>Full-spectrum DDoS (L3–L7)</td><td class="no">—</td><td class="yes">Protect</td><td class="yes">Protect</td><td class="yes">Protect</td></tr>
      <tr><td>Bot defense</td><td class="see">See</td><td class="yes">Protect</td><td class="yes">+ ML</td><td class="yes">+ ML</td></tr>
      <tr><td>API discovery &amp; security</td><td class="see">See</td><td class="yes">Protect</td><td class="yes">+ Auto</td><td class="yes">+ Auto</td></tr>
      <tr><td>On-host visibility (E-W + AI)</td><td class="see">See</td><td class="no">—</td><td class="no">—</td><td class="see">See</td></tr>
      <tr><td>LLM / prompt inspection</td><td class="no">—</td><td class="no">—</td><td class="no">—</td><td class="yes">Protect</td></tr>
      <tr><td>AI-crawler protection</td><td class="no">—</td><td class="no">—</td><td class="no">—</td><td class="yes">Protect</td></tr>
      <tr><td>Agent egress governance</td><td class="see">See</td><td class="no">—</td><td class="no">—</td><td class="yes">Govern</td></tr>
    </table>
    <p class="center muted" style="margin-top:10px;font-size:12.5px">
      <span class="see">See</span> = visibility &nbsp;·&nbsp; <span class="yes">Protect / Govern</span> = enforced &nbsp;·&nbsp; — = not included.
    </p>
  </div>
</section>

<section style="border-bottom:0">
  <div class="wrap"><div class="band">
    <h2>Not sure which plan fits?</h2>
    <p class="sub">Book a demo and we'll map your environment to the right starting point.</p>
    <a class="btn btn-cta" href="/demo" data-cta="pricing_demo">Book a demo &rarr;</a>
  </div></div>
</section>
"""


def demo_form():
    return f"""
<section class="hero" style="padding-bottom:24px">
  <div class="wrap">
    <span class="pill"><span class="live"></span> Book a demo</span>
    <h1>See <span class="accent">{SHORT}</span> on a host like yours</h1>
    <p class="lede">A 20-minute walkthrough tailored to your environment. Tell us a bit about you and we'll reach out to schedule.</p>
  </div>
</section>

<section style="border-bottom:0">
  <div class="wrap" style="max-width:820px">
    <form class="formwrap" method="POST" action="/demo-request">
      <div class="form-grid">
        <div class="field"><label>Full name <span class="req">*</span></label><input type="text" name="name" required></div>
        <div class="field"><label>Work email <span class="req">*</span></label><input type="email" name="email" required></div>
        <div class="field"><label>Company <span class="req">*</span></label><input type="text" name="company" required></div>
        <div class="field"><label>Job title</label><input type="text" name="title"></div>
        <div class="field"><label>Your role</label>
          <select name="role">
            <option value="">— select —</option>
            <option>Security / CISO</option>
            <option>App owner / DevOps</option>
            <option>IT / infrastructure</option>
            <option>Partner / MSP</option>
            <option>Barracuda field / SE</option>
            <option>Other</option>
          </select></div>
        <div class="field"><label>Company size</label>
          <select name="company_size">
            <option value="">— select —</option>
            <option>1–50</option><option>51–250</option><option>251–1,000</option>
            <option>1,001–5,000</option><option>5,000+</option>
          </select></div>
        <div class="field"><label>Plan of interest</label>
          <select name="plan_interest">
            <option value="">— select —</option>
            <option>Starter ($10/server — visibility)</option>
            <option>Advance</option>
            <option>Premium</option>
            <option>Premium+ (AI security)</option>
            <option>Not sure yet</option>
          </select></div>
        <div class="field"><label>Timeframe</label>
          <select name="timeframe">
            <option value="">— select —</option>
            <option>Actively evaluating now</option>
            <option>Next quarter</option>
            <option>This year</option>
            <option>Just exploring</option>
          </select></div>
        <div class="field full"><label>What problem are you hoping this solves? <span class="hint">(optional, but it helps us tailor the demo)</span></label>
          <textarea name="problem" placeholder="E.g. we have no visibility into East-West traffic, or we're trying to govern AI agent egress…"></textarea></div>
      </div>
      <button class="btn btn-cta" type="submit" data-cta="demo_submit">Request my demo</button>
      <p class="muted" style="font-size:12.5px;margin-top:14px">
        We'll use your details only to schedule and follow up on this demo.
      </p>
    </form>
  </div>
</section>
"""


def thank_you(name):
    first = (name or "").strip().split(" ")[0] if name else ""
    hi = f"Thanks, {first}." if first else "Thank you."
    return f"""
<section class="hero" style="min-height:60vh">
  <div class="wrap" style="max-width:640px;text-align:center">
    <h1 style="font-size:40px">{hi}</h1>
    <p class="lede" style="margin:0 auto">
      Your demo request for {PRODUCT} is in. Our team will reach out within one business day to find a time.
    </p>
    <div class="cta-row" style="justify-content:center">
      <a class="btn btn-ghost" href="/" data-cta="ty_home">&larr; Back to overview</a>
      <a class="btn btn-primary" href="/pricing" data-cta="ty_pricing">See pricing</a>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Need-validation survey  (separate instrument from the demo/intent funnel)
# ---------------------------------------------------------------------------
def _opts(name, options, kind="radio", required=False, row=False):
    """Render a radio/checkbox option group."""
    r = " required" if required else ""
    inner = "".join(
        f'<label class="opt"><input type="{kind}" name="{name}" '
        f'value="{html.escape(o)}"{r}><span>{html.escape(o)}</span></label>'
        for o in options
    )
    return f'<div class="opts{" row" if row else ""}">{inner}</div>'


def _q(num, label, body, hint=""):
    h = f' <span class="hint">{html.escape(hint)}</span>' if hint else ""
    return f'<div class="q"><div class="qlab"><b>{num}.</b> {html.escape(label)}{h}</div>{body}</div>'


def survey():
    # 1-5 confidence scale (Q5)
    scale = "".join(
        f'<label class="sc"><input type="radio" name="inventory_confidence" value="{i}" required>'
        f'<span>{i}</span></label>'
        for i in range(1, 6)
    )
    q5_body = (
        '<div class="scalewrap"><span class="scale-cap">Not at all</span>'
        f'<div class="scale">{scale}</div>'
        '<span class="scale-cap">Completely</span></div>'
    )

    return f"""
<section class="hero" style="padding-bottom:20px">
  <div class="wrap">
    <span class="pill"><span class="live"></span> 3-minute need check</span>
    <h1>Where are your <span class="accent">application blind spots</span>?</h1>
    <p class="lede">A short, no-pitch survey about how you see what runs on your servers today —
      shadow apps, app-layer attacks, and AI/LLM activity. Honest answers help us build the right thing
      (or decide not to). Most questions are one click.</p>
  </div>
</section>

<section style="border-bottom:0">
  <div class="wrap" style="max-width:860px">
    <form class="formwrap" method="POST" action="/survey-response">

      <div class="modebar">
        <span class="modelab">Filling this in as:</span>
        <label class="opt"><input type="radio" name="mode" value="self" checked onclick="saToggle()"><span>A customer / prospect</span></label>
        <label class="opt"><input type="radio" name="mode" value="sa" onclick="saToggle()"><span>A Barracuda SA (for an account)</span></label>
      </div>
      <div id="sa-fields" class="sa-fields" style="display:none">
        <div class="form-grid">
          <div class="field"><label>Account / company</label><input type="text" name="account"></div>
          <div class="field"><label>Your name (SA)</label><input type="text" name="sa_name"></div>
        </div>
      </div>

      <div class="sgroup">About you</div>
      {_q(1, "Your role", _opts("role", ["SecOps / SOC", "CISO / security leadership", "App / DevOps owner", "Platform / Infrastructure", "MSP / MSSP", "Other"], required=True))}
      {_q(2, "Company size (employees)", _opts("company_size", ["Under 100", "100–1,000", "1,000–5,000", "5,000+"], row=True))}
      {_q(3, "Roughly how many internet-facing + internal apps/services do you run?", _opts("app_count", ["1–10", "11–50", "51–200", "200+", "Don't know"], row=True))}
      {_q(4, "Current Barracuda WaaS / WAF customer?", _opts("is_customer", ["Yes", "No", "Not sure"], required=True, row=True))}

      <div class="sgroup">Visibility today</div>
      {_q(5, "How confident are you that you have a complete, current inventory of what runs on your app servers — including shadow services and AI/LLM integrations?", q5_body)}
      {_q(6, "In the last 12 months, how often did you find an app, service, or AI integration running that you didn't know was there?", _opts("shadow_freq", ["Never", "Once", "A few times", "Many times"], row=True))}
      {_q(7, "How do you see app-layer attacks and what your servers talk to today?", _opts("visibility_today", ["Cloud WAF", "EDR / XDR", "API discovery / ASM tool", "Manual / scripts", "Nothing specific"], kind="checkbox"), hint="(select all that apply)")}

      <div class="sgroup">What's on the host</div>
      {_q(8, "What's installed on your production app servers now?", _opts("installed_agents", ["CrowdStrike", "Microsoft Defender", "SentinelOne", "Other EDR", "Cloud WAF agent", "None", "Don't know"], kind="checkbox"), hint="(select all that apply)")}
      {_q(9, "Last time you needed new security visibility on those hosts, what did you actually do?", _opts("last_visibility_action", ["Added a new tool", "Extended a tool already installed", "Asked a vendor I already use", "Did nothing — too hard"]))}
      {_q(10, "How hard is it to get a new privileged agent approved on a production server?", _opts("install_difficulty", ["Easy", "Moderate", "Hard", "Near-impossible"], row=True))}

      <div class="sgroup">Budget &amp; ownership</div>
      {_q(11, "In the last 12 months, did you pay for app/API visibility or on-host security tooling?", _opts("paid_last_year", ["Yes — new purchase", "Yes — expanded existing", "No", "Don't know"]))}
      {_q(12, "Who owns finding shadow apps / shadow AI on servers?", _opts("owner", ["Me", "My team", "Another team", "Nobody clearly"], row=True))}

      <div class="sgroup">If it were free</div>
      {_q(13, "If a free agent showed you apps, attacks, and AI/MCP calls you didn't know about — most likely next step?", _opts("next_step", ["Ignore it", "Investigate manually", "Evaluate paid protection", "Loop in the owning team", "Nothing — not my budget"]))}
      <div class="q"><div class="qlab"><b>14.</b> What would make a finding worth paying to act on? <span class="hint">(optional)</span></div>
        <textarea name="pay_trigger" placeholder="E.g. if it proved an actual attack got through, or found data leaving via an AI agent…"></textarea></div>

      <div class="sgroup">One last thing</div>
      {_q(15, "Want early access / a demo of what we build?", _opts("interest", ["Yes", "Maybe", "No"], row=True))}
      <div class="form-grid" style="margin-top:6px">
        <div class="field"><label>Name <span class="hint">(optional)</span></label><input type="text" name="contact_name"></div>
        <div class="field"><label>Work email <span class="hint">(optional)</span></label><input type="email" name="email"></div>
        <div class="field full"><label>Company <span class="hint">(optional)</span></label><input type="text" name="company"></div>
      </div>

      <button class="btn btn-cta" type="submit" data-cta="survey_submit">Submit survey</button>
      <p class="muted" style="font-size:12.5px;margin-top:14px">
        No wrong answers — we're validating a need, not selling. Responses are used in aggregate to decide what to build.
      </p>
    </form>
  </div>
</section>

<script>
function saToggle(){{
  var el = document.querySelector('input[name=mode]:checked');
  var sa = el && el.value === 'sa';
  document.getElementById('sa-fields').style.display = sa ? 'block' : 'none';
}}
</script>
"""


def survey_thanks(mode):
    again = ('<a class="btn btn-primary" href="/survey" data-cta="sv_again">Log another account</a>'
             if mode == "sa" else
             '<a class="btn btn-primary" href="/demo" data-cta="sv_demo">Book a demo</a>')
    return f"""
<section class="hero" style="min-height:60vh">
  <div class="wrap" style="max-width:640px;text-align:center">
    <h1 style="font-size:40px">Thank you.</h1>
    <p class="lede" style="margin:0 auto">
      Your answers are recorded. This kind of ground-truth is exactly what decides whether — and how — we build {PRODUCT}.
    </p>
    <div class="cta-row" style="justify-content:center">
      <a class="btn btn-ghost" href="/" data-cta="sv_home">&larr; Back to overview</a>
      {again}
    </div>
  </div>
</section>
"""
