![crag_logo_v2](https://github.com/user-attachments/assets/4f1cd16a-7a27-4041-be5f-3ead4204fd6f)# crag — Code RAG

![Uploading crag_<svg width="100%" viewBox="0 0 680 370" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0f0e1a"/>
      <stop offset="100%" stop-color="#0a0910"/>
    </linearGradient>
    <linearGradient id="termGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a1828"/>
      <stop offset="100%" stop-color="#120f24"/>
    </linearGradient>
    <linearGradient id="tealLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5DCAA5" stop-opacity="0"/>
      <stop offset="20%" stop-color="#5DCAA5"/>
      <stop offset="80%" stop-color="#1D9E75"/>
      <stop offset="100%" stop-color="#1D9E75" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="purpleLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7F77DD" stop-opacity="0"/>
      <stop offset="30%" stop-color="#7F77DD"/>
      <stop offset="70%" stop-color="#534AB7"/>
      <stop offset="100%" stop-color="#534AB7" stop-opacity="0"/>
    </linearGradient>
    <!-- Beam from crag peak to terminal -->
    <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5DCAA5" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#5DCAA5" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="680" height="360" fill="url(#bg)" style="stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>

  <!-- ── TERMINAL WINDOW (center piece) ── -->
  <rect x="60" y="160" width="560" height="168" rx="10" fill="url(#termGrad)" stroke="#534AB7" stroke-width="0.8" stroke-opacity="0.6" style="stroke:rgb(83, 74, 183);color:rgb(255, 255, 255);stroke-width:0.8px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>

  <!-- Terminal titlebar -->
  <rect x="60" y="160" width="560" height="28" rx="10" fill="#1a1828" style="fill:rgb(26, 24, 40);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="60" y="174" width="560" height="14" fill="#1a1828" style="fill:rgb(26, 24, 40);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <!-- Traffic lights -->
  <circle cx="84" cy="174" r="5" fill="#FF5F57" opacity="0.8" style="fill:rgb(255, 95, 87);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.8;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="100" cy="174" r="5" fill="#FEBC2E" opacity="0.8" style="fill:rgb(254, 188, 46);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.8;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="116" cy="174" r="5" fill="#28C840" opacity="0.8" style="fill:rgb(40, 200, 64);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.8;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <!-- Title -->
  <text x="340" y="179" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="11" fill="#7F77DD" text-anchor="middle" opacity="0.7" style="fill:rgb(127, 119, 221);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.7;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:middle;dominant-baseline:auto">crag — code retrieval augmented grounding</text>

  <!-- Terminal content -->
  <!-- Line 1: prompt + query -->
  <text x="82" y="214" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="12" fill="#5DCAA5" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:12px;font-weight:400;text-anchor:start;dominant-baseline:auto">❯</text>
  <text x="98" y="214" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="12" fill="#EEEDFE" style="fill:rgb(238, 237, 254);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:12px;font-weight:400;text-anchor:start;dominant-baseline:auto">crag ask <tspan fill="#AFA9EC" style="fill:rgb(175, 169, 236);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:12px;font-weight:400;text-anchor:start;dominant-baseline:auto">"how does the auth middleware work?"</tspan></text>

  <!-- Line 2: indexing status -->
  <text x="82" y="233" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="11" fill="#534AB7" opacity="0.8" style="fill:rgb(83, 74, 183);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.8;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:start;dominant-baseline:auto">  ✦ indexed 148 chunks across 23 files</text>

  <!-- Line 3: answer with highlight -->
  <text x="82" y="252" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="11" fill="#c2c0e8" style="fill:rgb(194, 192, 232);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:start;dominant-baseline:auto">  The middleware in <tspan fill="#5DCAA5" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:start;dominant-baseline:auto">src/auth/index.ts</tspan> validates JWT</text>
  <text x="82" y="268" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="11" fill="#c2c0e8" style="fill:rgb(194, 192, 232);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:start;dominant-baseline:auto">  tokens, attaches <tspan fill="#5DCAA5" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:start;dominant-baseline:auto">req.user</tspan>, and calls <tspan fill="#5DCAA5" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:start;dominant-baseline:auto">next()</tspan> on success.</text>

  <!-- Line 4: source grounding -->
  <text x="82" y="287" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="11" fill="#534AB7" opacity="0.9" style="fill:rgb(83, 74, 183);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.9;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:start;dominant-baseline:auto">  ↳ grounded in auth/index.ts:42  middleware.js:17</text>

  <!-- Cursor blink -->
  <rect x="82" y="303" width="7" height="13" rx="1" fill="#5DCAA5" opacity="0.85" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.85;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>

  <!-- ── LOGO WORDMARK above terminal ── -->
  <!-- Big crag text -->
  <text x="340" y="118" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="72" font-weight="700" letter-spacing="6" text-anchor="middle" fill="#EEEDFE" style="fill:rgb(238, 237, 254);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:72px;font-weight:700;text-anchor:middle;dominant-baseline:auto">crag</text>

  <!-- Teal underline -->
  <rect x="160" y="126" width="360" height="2.5" rx="1.5" fill="url(#tealLine)" style="stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>

  <!-- Tagline -->
  <text x="340" y="148" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="11" letter-spacing="3" text-anchor="middle" fill="#534AB7" opacity="0.85" style="fill:rgb(83, 74, 183);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.85;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:11px;font-weight:400;text-anchor:middle;dominant-baseline:auto">code retrieval augmented grounding</text>

  <!-- ── DECORATIVE: faint grid / scan lines suggesting embeddings ── -->
  <!-- Left column of faint code lines (repo being indexed) -->
  <rect x="20" y="178" width="28" height="2" rx="1" fill="#26215C" opacity="0.6" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.6;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="186" width="18" height="2" rx="1" fill="#26215C" opacity="0.4" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.4;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="194" width="24" height="2" rx="1" fill="#26215C" opacity="0.5" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.5;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="202" width="14" height="2" rx="1" fill="#26215C" opacity="0.3" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.3;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="210" width="22" height="2" rx="1" fill="#26215C" opacity="0.5" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.5;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="218" width="30" height="2" rx="1" fill="#26215C" opacity="0.4" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.4;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="226" width="16" height="2" rx="1" fill="#26215C" opacity="0.3" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.3;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="234" width="26" height="2" rx="1" fill="#26215C" opacity="0.5" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.5;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="242" width="20" height="2" rx="1" fill="#26215C" opacity="0.4" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.4;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <rect x="20" y="250" width="28" height="2" rx="1" fill="#26215C" opacity="0.35" style="fill:rgb(38, 33, 92);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.35;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <text x="34" y="274" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="9" fill="#3C3489" text-anchor="middle" opacity="0.5" style="fill:rgb(60, 52, 137);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.5;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:9px;font-weight:400;text-anchor:middle;dominant-baseline:auto">repo</text>

  <!-- Arrow from left repo to terminal -->
  <line x1="50" y1="230" x2="58" y2="230" stroke="#534AB7" stroke-width="1" stroke-opacity="0.5" marker-end="url(#arr)" style="fill:rgb(0, 0, 0);stroke:rgb(83, 74, 183);color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>

  <!-- Right column: faint vector dots (embeddings) -->
  <circle cx="640" cy="184" r="2" fill="#1D9E75" opacity="0.4" style="fill:rgb(29, 158, 117);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.4;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="650" cy="198" r="1.5" fill="#5DCAA5" opacity="0.3" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.3;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="636" cy="210" r="2.5" fill="#1D9E75" opacity="0.5" style="fill:rgb(29, 158, 117);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.5;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="652" cy="222" r="1.5" fill="#5DCAA5" opacity="0.35" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.35;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="642" cy="236" r="2" fill="#1D9E75" opacity="0.4" style="fill:rgb(29, 158, 117);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.4;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="634" cy="248" r="3" fill="#5DCAA5" opacity="0.5" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.5;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="655" cy="260" r="1.5" fill="#1D9E75" opacity="0.3" style="fill:rgb(29, 158, 117);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.3;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <circle cx="645" cy="272" r="2" fill="#5DCAA5" opacity="0.4" style="fill:rgb(93, 202, 165);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.4;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <!-- faint connecting lines between dots -->
  <polyline points="640,184 650,198 636,210 652,222 642,236 634,248 655,260 645,272" fill="none" stroke="#1D9E75" stroke-width="0.5" opacity="0.25" style="fill:none;stroke:rgb(29, 158, 117);color:rgb(255, 255, 255);stroke-width:0.5px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.25;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>
  <text x="645" y="292" font-family="'SF Mono','Fira Code','Courier New',monospace" font-size="9" fill="#0F6E56" text-anchor="middle" opacity="0.5" style="fill:rgb(15, 110, 86);stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.5;font-family:&quot;SF Mono&quot;, &quot;Fira Code&quot;, &quot;Courier New&quot;, monospace;font-size:9px;font-weight:400;text-anchor:middle;dominant-baseline:auto">index</text>

  <!-- Arrow from terminal to right index -->
  <line x1="622" y1="240" x2="630" y2="240" stroke="#1D9E75" stroke-width="1" stroke-opacity="0.5" style="fill:rgb(0, 0, 0);stroke:rgb(29, 158, 117);color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:1;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>

  <!-- Bottom subtle rule -->
  <rect x="160" y="340" width="360" height="1" rx="0.5" fill="url(#purpleLine)" opacity="0.4" style="stroke:none;color:rgb(255, 255, 255);stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;opacity:0.4;font-family:&quot;Anthropic Sans&quot;, -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, sans-serif;font-size:16px;font-weight:400;text-anchor:start;dominant-baseline:auto"/>

  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#534AB7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
</svg>logo_v2.svg…]()

> A local, AST-aware retrieval-augmented generation CLI for exploring codebases.

Ingest any repository, ask questions in natural language, get answers grounded in your actual code. **No GPU, no model downloads, no ML setup required.**

<!-- ![demo](code_rag/demo.gif) -->

## Why crag?

Most code search tools split files by character count, breaking functions in half and losing context. **crag** uses tree-sitter AST parsing to preserve functions, classes, and methods as intact retrieval units — so you always get complete, meaningful code in results.

**Zero ML required for core functionality.** Ingestion and retrieval use a deterministic hash-based embedding — no model downloads, no GPU, no network calls. LLM-powered answer generation is optional and supports multiple providers.

## Quick Start

```bash
cd code_rag
pip install -e .

# Ingest a repository
crag ingest /path/to/your/project

# Ask questions (works immediately with fallback mode)
crag ask "Where is the CLI entry point?"

# For LLM-powered answers, pick any provider:
pip install -e ".[anthropic]"          # or .[openai], .[gemini], .[ollama], .[all]
export ANTHROPIC_API_KEY="sk-ant-..."  # set your preferred provider's key
crag ask "How does the parser work?"
```

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         crag ingest                              │
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────────────┐  │
│  │ Crawler  │───▶│  tree-sitter │───▶│   Hash Embeddings     │  │
│  │          │    │   Parser     │    │   (SHA1, 256-dim)     │  │
│  │ walks    │    │              │    │                       │  │
│  │ repo,    │    │ extracts     │    │  deterministic,       │  │
│  │ skips    │    │ functions,   │    │  no ML, no GPU,       │  │
│  │ .git/    │    │ classes,     │    │  no downloads         │  │
│  │ venv/    │    │ methods as   │    │                       │  │
│  │ etc.     │    │ intact       │    └──────────┬────────────┘  │
│  └──────────┘    │ CodeChunks   │               │               │
│                  └──────────────┘               ▼               │
│                                        ┌────────────────┐       │
│                                        │   ChromaDB     │       │
│                                        │   (local,      │       │
│                                        │    persistent)  │       │
│                                        └────────┬───────┘       │
└─────────────────────────────────────────────────┼───────────────┘
                                                  │
┌─────────────────────────────────────────────────┼───────────────┐
│                         crag ask                │               │
│                                                 ▼               │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────┐         │
│  │  Answer  │◀───│   LLM        │◀───│ Vector Search  │         │
│  │          │    │   Provider   │    │ (top-k chunks) │         │
│  │ grounded │    │              │    └────────────────┘         │
│  │ response │    │ Anthropic │                                  │
│  │ with     │    │ OpenAI    │                                  │
│  │ source   │    │ Gemini    │                                  │
│  │ refs     │    │ Ollama    │                                  │
│  │          │    │ Fallback  │                                  │
│  └──────────┘    └──────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline Detail

1. **Crawler** walks the repo, skipping `.git`, `node_modules`, `__pycache__`, etc.
2. **Parser** uses tree-sitter to extract functions, classes, methods, and global scope as intact chunks with metadata (file path, line range, docstring).
3. **Indexer** embeds chunks using a deterministic SHA1-based hash function (256-dim vectors) enriched with file name, chunk name, and docstring metadata. Stored in a local ChromaDB database.
4. **Retriever** performs vector similarity search to find the top-k relevant chunks.
5. **Generator** builds a grounded prompt and sends it to the configured LLM, or returns a fallback summary with excerpts.

## LLM Providers

crag tries providers in order and uses the first one that is both installed and configured:

| Provider | Install | Environment Variable |
|---|---|---|
| Google Gemini | `pip install -e ".[gemini]"` | `GOOGLE_API_KEY` |
| OpenAI | `pip install -e ".[openai]"` | `OPENAI_API_KEY` |
| Anthropic | `pip install -e ".[anthropic]"` | `ANTHROPIC_API_KEY` |
| Ollama (local) | `pip install -e ".[ollama]"` | `CODE_RAG_OLLAMA_MODEL` or `OLLAMA_HOST` |
| Fallback | *(built-in)* | *(none needed)* |

The **fallback mode** returns the most relevant code chunks with excerpts — no hallucination, no network calls. Useful on its own for code search even without any LLM.

### Model Configuration

| Variable | Default |
|---|---|
| `CODE_RAG_GEMINI_MODEL` | `gemini-2.5-flash` |
| `CODE_RAG_OPENAI_MODEL` | `gpt-4o-mini` |
| `CODE_RAG_ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` |
| `CODE_RAG_OLLAMA_MODEL` | `qwen2.5-coder` |
| `OLLAMA_HOST` | `http://localhost:11434` |

## CLI Reference

### `crag ingest <directory>`

Crawl and index a repository. Re-running replaces stale data for that repo.

```bash
crag ingest .
crag ingest /path/to/project
```

### `crag ask <question>`

Query indexed code and get a grounded answer.

```bash
crag ask "How does ingestion work?"
crag ask "Where are the Pydantic models defined?" --top-k 10
crag ask "Show me all CLI commands" --directory /path/to/project
crag ask "Compare parser implementations" --all-repos
```

| Flag | Description | Default |
|---|---|---|
| `--top-k` | Number of chunks to retrieve | `5` |
| `--directory` / `-d` | Repository to search | `.` |
| `--all-repos` | Search all ingested repositories | `false` |

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `CODE_RAG_DB_PATH` | ChromaDB storage directory | `~/.code_rag_db` |
| `CODE_RAG_COLLECTION` | Collection name | `code_chunks` |
| `CODE_RAG_TOP_K` | Default retrieval depth | `5` |

## Project Structure

```
code_rag/
├── code_rag/
│   ├── main.py              # CLI commands (ingest, ask)
│   ├── config.py            # Environment-based configuration
│   ├── models.py            # CodeChunk, QueryResult (Pydantic)
│   ├── parser/
│   │   ├── engine.py        # Language detection & routing
│   │   └── py_parser.py     # Python AST parser (tree-sitter)
│   ├── indexer/
│   │   ├── crawler.py       # Repository walker with ignore rules
│   │   └── db.py            # ChromaDB + hash embedding
│   └── retriever/
│       ├── search.py        # Vector similarity search
│       └── generator.py     # Multi-provider answer generation
├── tests/
├── pyproject.toml
└── requirements.txt
```

## Why Deterministic Embeddings?

The hash-based embedding function:
- **Works offline** with zero setup
- **Produces identical results** every time (deterministic)
- **Requires no model downloads** or GPU
- **Keeps the core install under 100MB**

The tradeoff is lower semantic retrieval quality compared to learned embeddings. For most code search tasks on a single repository, keyword-level matching works surprisingly well — especially with the metadata-enriched indexing.

## Supported Languages

- **Python** — full AST-aware chunking via tree-sitter
- More languages planned

## Development

```bash
python -m venv .venv && source .venv/bin/activate
cd code_rag
pip install -r requirements.txt
pip install -e ".[all]"

# Run tests
python -m unittest discover -s tests -v

# Dev workflow
crag ingest .
crag ask "How is ingestion implemented?"
```

## Troubleshooting

**"No indexed code chunks matched the query"** — Run `crag ingest` first, or broaden your question.

**Ollama not answering** — Ensure Ollama is running and you've set `CODE_RAG_OLLAMA_MODEL` or `OLLAMA_HOST`.

**Poor retrieval results** — Try more specific keywords, include function/file names in your query, or increase `--top-k`.

**ChromaDB telemetry warnings** — Harmless version mismatch in ChromaDB's telemetry client. Doesn't affect functionality.

## License

MIT
