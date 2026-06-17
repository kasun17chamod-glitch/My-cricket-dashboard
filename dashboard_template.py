"""
Cricket dashboard HTML template — broadcast scoreboard edition.

Same function signature and data contract as the original. The data layer,
chart configurations, filtering logic, and the core stat computations
(``computeBatting`` / ``computeBowling``) are preserved unchanged. The
presentation has been rebuilt around a live-TV cricket-broadcast visual
language, and four data features were added on top of the existing maths.

Visual identity (broadcast scoreboard)
  • Saira Condensed display/numerals → stadium-scoreboard typography.
  • Header "scorebug" with live dot, in the style of a TV score graphic.
  • Lower-third section headings (accent rail + kicker + condensed title).
  • Scoreboard "score-cell" readouts for hero KPIs and head-to-head stats.
  • Auto-scrolling "LIVE FORM" achievements ticker (replaces the ribbon).
  • Panel treatment with left accent rails and LED scanline texture.

New features (all derived from the existing columns)
  • Player rating card — FIFA-style BAT / BOWL / FIELD / overall index.
  • Head-to-head — pick an opponent, see batting & bowling record vs them.
  • Season-by-season comparison table — runs/avg/SR/HS/wkts/econ/best per year.
  • Expandable match scorecards — click any match row for a full breakdown.

Preserved from the previous edition
  • Theme switcher (Midnight / Stadium / Floodlight), restyled per identity.
  • Floating particles, 3-D card tilt, magnetic buttons, scroll progress,
    scroll-to-top, toasts, reveal animations, print-to-PDF, keyboard shortcuts.

Fonts: Manrope (body) + Saira Condensed / Saira Semi Condensed (display),
all loaded from Google Fonts.
"""

import json


def build_dashboard_html(cricket_data: list, profile_img_src: str) -> str:
    """Return the full self-contained dashboard HTML.

    Parameters
    ----------
    cricket_data : list[dict]
        The same shape as ``window.CRICKET_DATA`` in the original ``data.js``.
    profile_img_src : str
        URL or ``data:`` URI for the player photo.
    """

    data_json = json.dumps(cricket_data)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="midnight">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<meta name="theme-color" content="#0a0e1a" />
<title>Kasun Chamod · Cricket Stats</title>

<!-- Manrope (body) + Saira Condensed (scoreboard display/numerals) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Saira+Condensed:wght@500;600;700;800;900&family=Saira+Semi+Condensed:wght@600;700;800&display=swap" rel="stylesheet">

<!-- Tailwind via play CDN -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {{
    theme: {{
      extend: {{
        colors: {{
          ink:  {{ 0:'#000000', 900:'#0a0e1a' }},
          bat:  {{ 200:'#a5f3fc', 400:'#22d3ee', 500:'#06b6d4' }},
          bowl: {{ 200:'#fde68a', 400:'#fbbf24', 500:'#f59e0b' }},
          mint: {{ 400:'#34d399' }},
        }},
        boxShadow: {{
          glow: '0 0 24px -4px rgba(34,211,238,.45)',
          card: '0 30px 60px -30px rgba(0,0,0,.6)',
        }}
      }}
    }}
  }}
</script>

<!-- Chart.js & Lucide icons -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>

<style>
  /* ============= THEME TOKENS ============= */
  :root {{
    --grain-opacity: .035;
    --bg-0: #060912;
    --bg-1: #0a0e1a;
    --bg-2: #0e1422;
    --surface-1: rgba(255,255,255,.04);
    --surface-2: rgba(255,255,255,.015);
    --border-1: rgba(255,255,255,.08);
    --border-2: rgba(255,255,255,.14);
    --text-1: #e5e7eb;
    --text-2: #cbd5e1;
    --text-3: #94a3b8;
    --text-4: #64748b;
    --bat: #22d3ee;
    --bat-glow: rgba(34,211,238,.45);
    --bowl: #fbbf24;
    --bowl-glow: rgba(245,158,11,.4);
    --mint: #34d399;
    --rose: #fb7185;
  }}
  [data-theme="stadium"] {{
    --bg-0: #03110a;
    --bg-1: #061b10;
    --bg-2: #082818;
    --bat: #4ade80;
    --bat-glow: rgba(74,222,128,.45);
    --bowl: #fbbf24;
  }}
  [data-theme="floodlight"] {{
    --bg-0: #0d0820;
    --bg-1: #14102e;
    --bg-2: #1a1640;
    --bat: #a78bfa;
    --bat-glow: rgba(167,139,250,.5);
    --bowl: #f472b6;
    --bowl-glow: rgba(244,114,182,.45);
  }}

  html, body {{ background: var(--bg-1); }}
  body {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif;
    color: var(--text-1);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
    margin: 0;
  }}

  body, button, input, select, option, textarea, label, table, th, td,
  thead, tbody, tr, nav, header, footer, p, span, div, small, strong,
  em, a, li, ul, ol, code, h1, h2, h3, h4, h5, h6 {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif !important;
  }}
  .font-mono {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif !important;
  }}
  /* Scoreboard display face — condensed, broadcast-grade */
  .font-serif, .num-display, .num, .scorenum, h1, h2, h3,
  .ticker, .lt-title, .panel-kicker {{
    font-family: 'Saira Condensed', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif !important;
  }}
  .italic, i:not([data-lucide]) {{ font-style: normal !important; }}
  .font-serif {{ font-weight: 800; letter-spacing: 0; text-transform: uppercase; }}
  h1.font-serif, h2.font-serif {{ letter-spacing: .01em; }}
  .num-display {{ font-weight: 800; letter-spacing: 0; font-variant-numeric: tabular-nums; }}
  .font-mono, .num {{ font-variant-numeric: tabular-nums; }}
  .num {{ font-weight: 700; }}

  /* ============= BACKGROUND ============= */
  .app-bg {{
    position: fixed; inset: 0; z-index: -3;
    background:
      radial-gradient(70% 50% at 8% -5%,  var(--bat-glow) 0%, transparent 60%),
      radial-gradient(50% 40% at 95% 12%, var(--bowl-glow) 0%, transparent 60%),
      radial-gradient(50% 60% at 60% 110%, rgba(59,130,246,.18) 0%, transparent 60%),
      linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 60%, var(--bg-1) 100%);
    transition: background 0.6s ease;
  }}
  .app-bg::before {{
    content: ""; position: absolute; inset: 0;
    background-image:
      radial-gradient(circle at 50% 50%, transparent 0%, rgba(0,0,0,.3) 100%);
    pointer-events: none;
  }}
  .app-grain {{
    position: fixed; inset: 0; z-index: -2; pointer-events: none;
    opacity: var(--grain-opacity);
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  }}
  /* Floating cricket-ball particles */
  .particles {{
    position: fixed; inset: 0; z-index: -1; pointer-events: none; overflow: hidden;
  }}
  .particles span {{
    position: absolute; width: 6px; height: 6px; border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #d62828, #6b0f0f);
    opacity: 0; animation: floatUp 18s linear infinite;
    box-shadow: 0 0 8px rgba(214,40,40,.4);
  }}
  @keyframes floatUp {{
    0%   {{ transform: translateY(110vh) translateX(0); opacity: 0; }}
    10%  {{ opacity: .25; }}
    90%  {{ opacity: .25; }}
    100% {{ transform: translateY(-10vh) translateX(40px); opacity: 0; }}
  }}

  /* ============= GLASS / CARDS ============= */
  .glass {{
    position: relative;
    background: linear-gradient(180deg, var(--surface-1) 0%, var(--surface-2) 100%);
    border: 1px solid var(--border-1);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 22px;
  }}
  .glass::before {{
    content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
    background: linear-gradient(180deg, rgba(255,255,255,.06), transparent 30%);
    opacity: .8;
  }}
  .glass-strong {{
    position: relative;
    background: linear-gradient(180deg, rgba(20,28,48,.7) 0%, rgba(10,14,26,.7) 100%);
    border: 1px solid var(--border-1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
  }}
  .glass-strong::before {{
    content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
    background: linear-gradient(180deg, rgba(255,255,255,.07), transparent 25%);
  }}

  /* Stat card hover with subtle 3D tilt */
  .stat-card {{
    transition: transform .35s cubic-bezier(.2,.7,.2,1), border-color .35s, box-shadow .35s;
    transform-style: preserve-3d;
    will-change: transform;
  }}
  .stat-card:hover {{
    transform: translateY(-3px);
    border-color: rgba(34,211,238,.35);
    box-shadow: 0 20px 40px -20px rgba(34,211,238,.25);
  }}
  .stat-card--bowl:hover {{
    border-color: rgba(251,191,36,.45);
    box-shadow: 0 20px 40px -20px rgba(251,191,36,.25);
  }}
  .stat-card.tilt-active {{ transition: transform .12s ease; }}

  /* Reveal animation */
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(18px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .reveal {{ animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }}
  .io-hidden {{ opacity: 0; transform: translateY(14px); }}
  .io-show   {{ animation: rise .8s cubic-bezier(.2,.7,.2,1) both; }}

  /* Profile ring pulse */
  @keyframes ringPulse {{
    0%,100% {{ box-shadow: 0 0 0 0 rgba(34,211,238,.35), inset 0 0 0 1px rgba(34,211,238,.4); }}
    50%     {{ box-shadow: 0 0 0 12px rgba(34,211,238,0), inset 0 0 0 1px rgba(34,211,238,.4); }}
  }}
  .profile-ring {{ animation: ringPulse 3s ease-in-out infinite; }}
  @keyframes spinSlow {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
  .ring-rotate {{ animation: spinSlow 16s linear infinite; }}

  /* ============= TOP SCROLL PROGRESS ============= */
  .scroll-progress {{
    position: fixed; top: 0; left: 0; right: 0; height: 2px; z-index: 60;
    background: linear-gradient(90deg, var(--bat) 0%, var(--bowl) 100%);
    transform-origin: 0 50%;
    transform: scaleX(0);
    transition: transform .12s linear;
    box-shadow: 0 0 12px var(--bat-glow);
  }}

  /* ============= TABS ============= */
  .tab-btn {{ position: relative; transition: color .25s; background: transparent; border: 0; cursor: pointer; color: inherit; }}
  .tab-btn[data-active="true"] {{ color: #fff; }}
  .tab-btn[data-active="true"]::after {{
    content: ""; position: absolute; left: 12px; right: 12px; bottom: -1px; height: 2px;
    background: linear-gradient(90deg, var(--bat), var(--bowl));
    border-radius: 2px;
    box-shadow: 0 0 12px var(--bat-glow);
  }}

  /* ============= CHIP ============= */
  .chip {{
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 12px; border-radius: 999px;
    border: 1px solid rgba(255,255,255,.1);
    background: rgba(255,255,255,.04);
    font-size: 13px; color: #cbd5e1;
    transition: all .2s;
    cursor: pointer; user-select: none;
    white-space: nowrap;
  }}
  .chip:hover {{ border-color: rgba(255,255,255,.25); color: #fff; transform: translateY(-1px); }}
  .chip[data-active="true"] {{
    background: linear-gradient(180deg, rgba(34,211,238,.18), rgba(34,211,238,.06));
    border-color: rgba(34,211,238,.45);
    color: #ecfeff;
  }}
  .chip[data-active="true"][data-color="bowl"] {{
    background: linear-gradient(180deg, rgba(245,158,11,.18), rgba(245,158,11,.06));
    border-color: rgba(245,158,11,.45);
    color: #fffbeb;
  }}
  .chip[data-active="true"][data-color="mint"] {{
    background: linear-gradient(180deg, rgba(52,211,153,.18), rgba(52,211,153,.06));
    border-color: rgba(52,211,153,.45);
    color: #ecfdf5;
  }}

  /* ============= FORM PILL ============= */
  .form-pill {{
    width: 30px; height: 30px; border-radius: 9px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 800; color: #fff;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
  }}

  /* ============= SCROLLBAR ============= */
  ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
  ::-webkit-scrollbar-track {{ background: transparent; }}
  ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,.08); border-radius: 10px; }}
  ::-webkit-scrollbar-thumb:hover {{ background: rgba(255,255,255,.18); }}

  .scroll-x {{ -ms-overflow-style: none; scrollbar-width: none; }}
  .scroll-x::-webkit-scrollbar {{ display: none; }}

  .mobile-tabbar {{ padding-bottom: max(0.5rem, env(safe-area-inset-bottom)); }}
  section[id] {{ scroll-margin-top: 80px; }}

  .accent-line {{
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--bat), var(--bowl), transparent);
    opacity: .65;
  }}
  /* Cricket-ball seam divider */
  .seam-divider {{
    height: 28px; display: flex; align-items: center; justify-content: center; margin: 28px 0;
    color: rgba(255,255,255,.18);
  }}
  .seam-divider svg {{ width: 100%; max-width: 360px; }}

  /* ============= TABLE ============= */
  .ctable {{ width: 100%; border-collapse: separate; border-spacing: 0; }}
  .ctable th {{
    font-size: 11px; text-transform: uppercase; letter-spacing: .08em;
    color: var(--text-3); font-weight: 700; padding: 12px 14px; text-align: left;
    background: rgba(255,255,255,.025); border-bottom: 1px solid rgba(255,255,255,.06);
    position: sticky; top: 0; backdrop-filter: blur(8px);
  }}
  .ctable td {{ padding: 12px 14px; border-bottom: 1px solid rgba(255,255,255,.05); font-size: 14px; }}
  .ctable tr:last-child td {{ border-bottom: none; }}
  .ctable tr {{ transition: background .2s; }}
  .ctable tr:hover td {{ background: rgba(34,211,238,.04); }}
  .ctable th.sortable {{ cursor: pointer; user-select: none; }}
  .ctable th.sortable:hover {{ color: #fff; }}
  .ctable th.sortable::after {{
    content: " ↕"; opacity: .35; font-size: 10px;
  }}

  /* ============= BADGES ============= */
  .badge {{
    display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 700;
    border: 1px solid rgba(255,255,255,.1); background: rgba(255,255,255,.04); color: #cbd5e1;
  }}
  .badge-bat  {{ color: #a5f3fc; border-color: rgba(34,211,238,.3); background: rgba(34,211,238,.08); }}
  .badge-bowl {{ color: #fde68a; border-color: rgba(245,158,11,.3); background: rgba(245,158,11,.08); }}
  .badge-100  {{ color: #fff;    background: linear-gradient(135deg,#06b6d4,#0891b2); border-color: transparent; box-shadow: 0 4px 12px -4px rgba(8,145,178,.6); }}
  .badge-50   {{ color: #082f49; background: linear-gradient(135deg,#a5f3fc,#67e8f9); border-color: transparent; }}
  .badge-5w   {{ color: #fff;    background: linear-gradient(135deg,#d97706,#92400e); border-color: transparent; box-shadow: 0 4px 12px -4px rgba(217,119,6,.6); }}
  .badge-3w   {{ color: #422006; background: linear-gradient(135deg,#fde68a,#fbbf24); border-color: transparent; }}

  .hr-soft {{ height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,.12), transparent); }}

  button:focus-visible, [role="tab"]:focus-visible, .chip:focus-visible {{
    outline: 2px solid var(--bat); outline-offset: 2px; border-radius: 12px;
  }}

  canvas {{ max-width: 100%; }}
  .glass canvas {{ width: 100% !important; height: 100% !important; display: block; }}

  .donut-wrap {{ position: relative; }}
  .donut-wrap canvas {{ width: 100% !important; height: 100% !important; display: block; }}
  .donut-center {{
    position: absolute; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; pointer-events: none; text-align: center;
  }}

  .empty {{
    color: #64748b; font-size: 13px; padding: 20px; text-align: center;
    border: 1px dashed rgba(255,255,255,.1); border-radius: 14px;
  }}

  .search-input {{
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.1);
    color: var(--text-1);
    padding: 10px 14px 10px 38px;
    border-radius: 12px;
    width: 100%;
    font-size: 14px;
    transition: all .2s;
  }}
  .search-input:focus {{ outline: none; border-color: var(--bat); background: rgba(255,255,255,.06); box-shadow: 0 0 0 4px var(--bat-glow); }}
  .search-input::placeholder {{ color: #64748b; }}

  @media (max-width: 640px) {{
    .num-display {{ letter-spacing: -0.03em; }}
    section[id] {{ scroll-margin-top: 64px; }}
  }}

  .tab-mob {{ color: #64748b; transition: color .2s; background: transparent; border: 0; cursor: pointer; }}
  .tab-mob[data-active="true"] {{ color: var(--bat); }}
  .tab-mob[data-active="true"] i {{ filter: drop-shadow(0 0 8px var(--bat-glow)); }}

  /* ============= MAGNETIC BUTTON ============= */
  .magnetic {{ transition: transform .25s cubic-bezier(.2,.7,.2,1); }}

  /* ============= SCROLL TO TOP ============= */
  .scroll-top {{
    position: fixed; right: 18px; bottom: 86px; z-index: 45;
    width: 44px; height: 44px; border-radius: 50%;
    background: linear-gradient(135deg, var(--bat), var(--bowl));
    color: #0a0e1a; border: 0; cursor: pointer;
    display: grid; place-items: center;
    box-shadow: 0 12px 30px -8px var(--bat-glow);
    opacity: 0; pointer-events: none;
    transition: opacity .3s, transform .3s;
    transform: translateY(8px);
  }}
  .scroll-top.show {{ opacity: 1; pointer-events: auto; transform: translateY(0); }}
  @media (min-width: 768px) {{
    .scroll-top {{ bottom: 24px; right: 24px; }}
  }}

  /* ============= TOAST ============= */
  .toast-wrap {{
    position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%);
    z-index: 70; pointer-events: none;
  }}
  .toast {{
    background: rgba(10,14,26,.95);
    color: #fff; padding: 10px 16px; border-radius: 12px;
    border: 1px solid var(--border-1);
    box-shadow: 0 12px 30px -10px rgba(0,0,0,.6);
    font-size: 13px; font-weight: 600;
    display: inline-flex; align-items: center; gap: 8px;
    animation: toastIn .35s cubic-bezier(.2,.7,.2,1);
    backdrop-filter: blur(12px);
  }}
  @keyframes toastIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @media (min-width: 768px) {{ .toast-wrap {{ bottom: 30px; }} }}

  /* ============= PITCH SVG ============= */
  .pitch-svg {{ position: absolute; inset: 0; width: 100%; height: 100%; opacity: .06; pointer-events: none; }}

  /* ============= CAREER TIMELINE ============= */
  .timeline-track {{
    position: relative; height: 56px;
    background: linear-gradient(90deg, rgba(34,211,238,.05), rgba(245,158,11,.05));
    border-radius: 12px;
    border: 1px solid var(--border-1);
    overflow: hidden;
  }}
  .timeline-track::before {{
    content: ""; position: absolute; left: 16px; right: 16px; top: 50%;
    height: 2px;
    background: linear-gradient(90deg, var(--bat), var(--bowl));
    transform: translateY(-50%);
    border-radius: 2px;
    opacity: .8;
  }}
  .timeline-node {{
    position: absolute; top: 50%; transform: translate(-50%,-50%);
    width: 14px; height: 14px; border-radius: 50%;
    background: var(--bat); border: 3px solid var(--bg-1);
    box-shadow: 0 0 0 1px var(--bat), 0 0 12px var(--bat-glow);
    cursor: pointer;
    transition: transform .2s;
  }}
  .timeline-node:hover {{ transform: translate(-50%,-50%) scale(1.4); }}
  .timeline-label {{
    position: absolute; transform: translateX(-50%);
    font-size: 10px; color: var(--text-3);
    font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
    bottom: 4px;
  }}

  /* ============= ACHIEVEMENT RIBBON ============= */
  .achv {{
    flex: 0 0 auto;
    display: inline-flex; align-items: center; gap: 8px;
    padding: 10px 14px; border-radius: 999px;
    background: rgba(255,255,255,.03);
    border: 1px solid var(--border-1);
    font-size: 12px; color: var(--text-2);
    transition: all .25s;
  }}
  .achv:hover {{ background: rgba(255,255,255,.06); border-color: var(--border-2); transform: translateY(-1px); }}
  .achv .ico {{
    width: 20px; height: 20px; border-radius: 50%;
    display: grid; place-items: center;
    background: linear-gradient(135deg, var(--bat), var(--bowl));
    color: #0a0e1a;
  }}

  /* ============= THEME PICKER DOT ============= */
  .theme-dot {{
    width: 18px; height: 18px; border-radius: 50%;
    border: 2px solid transparent; cursor: pointer;
    transition: transform .2s, border-color .2s;
  }}
  .theme-dot:hover {{ transform: scale(1.15); }}
  .theme-dot[data-active="true"] {{ border-color: #fff; }}

  /* ============================================================
     BROADCAST SCOREBOARD LAYER
     ============================================================ */

  /* Scorebug — the TV brand bug in the header */
  .scorebug {{
    position: relative;
    display: inline-flex; align-items: center; gap: 0;
    border-radius: 8px; overflow: hidden;
    box-shadow: 0 6px 18px -8px rgba(0,0,0,.7), inset 0 0 0 1px rgba(255,255,255,.06);
  }}
  .scorebug .sb-tag {{
    background: linear-gradient(180deg, var(--bat), color-mix(in srgb, var(--bat) 70%, #000));
    color: #04121a; font-weight: 900; letter-spacing: .06em;
    padding: 6px 9px; font-size: 12px; text-transform: uppercase;
    display: inline-flex; align-items: center; gap: 5px;
  }}
  .scorebug .sb-name {{
    background: rgba(0,0,0,.35); padding: 6px 12px 6px 11px;
    display: flex; flex-direction: column; line-height: 1;
  }}

  /* Live dot */
  @keyframes blink {{ 0%,60%{{opacity:1}} 80%,100%{{opacity:.25}} }}
  .live-dot {{ width:7px; height:7px; border-radius:50%; background:var(--rose); box-shadow:0 0 10px var(--rose); animation: blink 1.4s infinite; }}

  /* Lower-third section heading — the signature broadcast graphic */
  .lt {{ display:flex; align-items:stretch; gap:12px; }}
  .lt-bar {{
    flex:0 0 auto; width:7px; border-radius:3px;
    background: linear-gradient(180deg, var(--bat), var(--bowl));
    box-shadow: 0 0 16px var(--bat-glow);
  }}
  .lt-kicker {{
    font-size:11px; letter-spacing:.3em; text-transform:uppercase;
    color: var(--bat); font-weight:800;
    display:inline-flex; align-items:center; gap:7px;
  }}
  .lt-title {{ font-weight:800; text-transform:uppercase; line-height:.95; letter-spacing:.01em; color:#fff; }}
  .lt-sub {{ font-size:13px; color: var(--text-3); margin-top:3px; }}

  /* Scoreboard panel treatment — left accent rail + LED scanline */
  .panel {{ border-radius: 14px; overflow:hidden; }}
  .panel::after {{
    content:""; position:absolute; left:0; top:0; bottom:0; width:3px;
    background: linear-gradient(180deg, var(--bat), var(--bowl)); opacity:.95;
  }}
  .panel--bowl::after {{ background: linear-gradient(180deg, var(--bowl), var(--bowl)); }}
  .panel--mint::after {{ background: linear-gradient(180deg, var(--mint), var(--bat)); }}

  /* Scoreboard cell — for the hero KPI readout */
  .score-cell {{
    position: relative;
    background:
      repeating-linear-gradient(0deg, rgba(255,255,255,.025) 0 1px, transparent 1px 3px),
      linear-gradient(180deg, rgba(0,0,0,.35), rgba(0,0,0,.15));
    border: 1px solid var(--border-1);
    border-radius: 12px; padding: 12px 14px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
  }}
  .score-cell .sc-label {{
    font-size:10px; letter-spacing:.16em; text-transform:uppercase;
    color: var(--text-3); font-weight:700;
    display:inline-flex; align-items:center; gap:6px;
  }}
  .score-cell .sc-val {{
    font-family:'Saira Condensed','Manrope',sans-serif; font-weight:800;
    font-variant-numeric: tabular-nums; line-height:1; margin-top:6px;
    text-shadow: 0 0 18px currentColor;
  }}

  /* ============= TICKER (broadcast bottom-ticker) ============= */
  .ticker-rail {{
    position: relative; overflow: hidden;
    border: 1px solid var(--border-1); border-radius: 12px;
    background: linear-gradient(90deg, rgba(0,0,0,.35), rgba(0,0,0,.15));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
  }}
  .ticker-rail::before {{
    content: "LIVE FORM"; position:absolute; left:0; top:0; bottom:0; z-index:2;
    display:flex; align-items:center; gap:6px; padding:0 14px;
    background: linear-gradient(180deg, var(--bowl), color-mix(in srgb, var(--bowl) 65%, #000));
    color:#1a1205; font-weight:900; font-size:11px; letter-spacing:.14em;
    font-family:'Saira Condensed','Manrope',sans-serif;
  }}
  .ticker {{
    display:inline-flex; align-items:center; gap:34px; white-space:nowrap;
    padding: 11px 0 11px 120px;
    animation: tickerScroll 38s linear infinite;
    font-weight:700; letter-spacing:.04em;
  }}
  .ticker:hover {{ animation-play-state: paused; }}
  .ticker .tk {{ display:inline-flex; align-items:center; gap:8px; color: var(--text-2); font-size:13px; text-transform:uppercase; }}
  .ticker .tk i {{ color: var(--bat); }}
  .ticker .tk .dot {{ width:5px; height:5px; border-radius:50%; background: var(--bowl); }}
  @keyframes tickerScroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}

  /* ============= PLAYER RATING CARD ============= */
  .rating-card {{
    position: relative; overflow: hidden; border-radius: 18px;
    background:
      radial-gradient(120% 80% at 80% -10%, var(--bat-glow), transparent 60%),
      linear-gradient(160deg, rgba(20,28,48,.85), rgba(8,11,20,.92));
    border: 1px solid var(--border-2);
    box-shadow: 0 30px 60px -30px rgba(0,0,0,.7);
  }}
  .rating-card::before {{
    content:""; position:absolute; inset:0; pointer-events:none;
    background: repeating-linear-gradient(115deg, rgba(255,255,255,.04) 0 2px, transparent 2px 9px);
    opacity:.5;
  }}
  .ovr-badge {{
    font-family:'Saira Condensed',sans-serif; font-weight:900; line-height:.82;
    color:#fff; text-shadow:0 0 30px var(--bat-glow);
  }}
  .rating-bar {{ height:7px; border-radius:5px; background: rgba(255,255,255,.08); overflow:hidden; }}
  .rating-bar > span {{ display:block; height:100%; border-radius:5px; background: linear-gradient(90deg, var(--bat), var(--bowl)); transition: width 1s cubic-bezier(.2,.7,.2,1); box-shadow:0 0 12px var(--bat-glow); }}

  /* ============= HEAD-TO-HEAD ============= */
  .h2h-select {{
    appearance:none; -webkit-appearance:none;
    background: rgba(255,255,255,.04) url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2.5'><path d='M6 9l6 6 6-6'/></svg>") no-repeat right 12px center;
    border:1px solid var(--border-2); color: var(--text-1);
    padding:10px 38px 10px 14px; border-radius:12px; font-weight:700; font-size:14px;
    cursor:pointer; min-width: 200px;
  }}
  .h2h-select:focus {{ outline:none; border-color: var(--bat); box-shadow:0 0 0 4px var(--bat-glow); }}
  .vs-stat {{ text-align:center; }}
  .vs-stat .v {{ font-family:'Saira Condensed',sans-serif; font-weight:800; line-height:1; }}
  .vs-stat .k {{ font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--text-3); margin-top:4px; }}

  /* ============= EXPANDABLE SCORECARD ============= */
  .ctable tr.match-row {{ cursor:pointer; }}
  .ctable tr.match-row td:first-child {{ position:relative; }}
  .ctable tr.match-row td:first-child::before {{
    content:"▸"; color: var(--text-4); margin-right:6px; display:inline-block;
    transition: transform .2s; font-size:10px;
  }}
  .ctable tr.match-row.open td:first-child::before {{ transform: rotate(90deg); color: var(--bat); }}
  .scorecard-row > td {{ padding:0 !important; border-bottom:1px solid var(--border-1) !important; }}
  .scorecard {{
    padding: 16px 18px;
    background:
      repeating-linear-gradient(0deg, rgba(255,255,255,.02) 0 1px, transparent 1px 4px),
      rgba(0,0,0,.28);
    border-left: 3px solid var(--bat);
  }}
  .scorecard .sc-grid {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(120px,1fr)); gap:14px; }}
  .sc-box {{ background: rgba(255,255,255,.03); border:1px solid var(--border-1); border-radius:10px; padding:10px 12px; }}
  .sc-box .l {{ font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--text-3); font-weight:700; }}
  .sc-box .v {{ font-family:'Saira Condensed',sans-serif; font-weight:800; font-size:22px; margin-top:3px; }}
  .card-expand {{ overflow:hidden; }}
  .card-expand .scorecard {{ margin-top:12px; border-radius:10px; border-left:3px solid var(--bat); }}

  /* ============= SEASON COMPARISON TABLE ============= */
  .season-table {{ width:100%; border-collapse:separate; border-spacing:0; }}
  .season-table th {{
    font-size:10px; text-transform:uppercase; letter-spacing:.1em; color:var(--text-3);
    font-weight:800; padding:10px 12px; text-align:right; white-space:nowrap;
    border-bottom:1px solid var(--border-2);
  }}
  .season-table th:first-child {{ text-align:left; }}
  .season-table td {{ padding:11px 12px; text-align:right; font-variant-numeric:tabular-nums; border-bottom:1px solid var(--border-1); }}
  .season-table td:first-child {{ text-align:left; font-weight:800; font-family:'Saira Condensed',sans-serif; }}
  .season-table tr:last-child td {{ border-bottom:none; }}
  .season-table tr:hover td {{ background: rgba(34,211,238,.04); }}
  .season-table .yr-bar {{
    display:inline-block; height:4px; border-radius:3px; vertical-align:middle; margin-left:6px;
    background: linear-gradient(90deg, var(--bat), var(--bowl));
  }}

  /* ============= PRINT ============= */
  @media print {{
    .app-bg, .app-grain, .particles, .scroll-progress, .scroll-top, .toast-wrap,
    #openFilters, #activeFiltersBar, .mobile-tabbar, #filterDrawer,
    nav#topTabs button[data-active="false"] {{ display: none !important; }}
    body, html {{ background: #fff !important; color: #000 !important; }}
    .glass, .glass-strong {{ background: #fff !important; border: 1px solid #ddd !important; box-shadow: none !important; }}
    [data-tab-pane] {{ display: block !important; page-break-before: auto; }}
    [data-tab-pane].hidden {{ display: block !important; }}
    canvas {{ max-height: 240px !important; }}
    .num-display, .text-bat-400, .text-bowl-400 {{ color: #000 !important; }}
  }}
</style>
</head>

<body>
<!-- Background layers -->
<div class="app-bg"></div>
<div class="app-grain"></div>
<div class="particles" id="particles" aria-hidden="true"></div>

<!-- Scroll progress bar -->
<div class="scroll-progress" id="scrollProgress"></div>

<!-- ============= TOP NAV ============= -->
<header class="sticky top-0 z-40 backdrop-blur-xl border-b border-white/5" style="background: color-mix(in srgb, var(--bg-1) 80%, transparent);">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 h-14 sm:h-16 flex items-center justify-between gap-4">
    <div class="scorebug min-w-0">
      <span class="sb-tag"><i data-lucide="trophy" class="w-3.5 h-3.5"></i>STATS</span>
      <span class="sb-name min-w-0">
        <span class="text-[10px] uppercase tracking-[0.22em] text-slate-400 flex items-center gap-1.5"><span class="live-dot"></span>Player Centre</span>
        <span class="text-sm font-bold truncate text-white" style="font-family:'Saira Semi Condensed',sans-serif;letter-spacing:.02em;">KASUN CHAMOD</span>
      </span>
    </div>

    <nav id="topTabs" class="hidden md:flex items-center gap-1 text-sm text-slate-400 font-semibold" role="tablist">
      <button class="tab-btn px-3 py-2"   data-tab="overview" data-active="true"  role="tab">Overview</button>
      <button class="tab-btn px-3 py-2"   data-tab="batting"  data-active="false" role="tab">Batting</button>
      <button class="tab-btn px-3 py-2"   data-tab="bowling"  data-active="false" role="tab">Bowling</button>
      <button class="tab-btn px-3 py-2"   data-tab="matches"  data-active="false" role="tab">Matches</button>
    </nav>

    <div class="flex items-center gap-2 shrink-0">
      <!-- Theme picker -->
      <div class="hidden sm:flex items-center gap-1.5 px-2 py-1.5 rounded-lg border border-white/10 bg-white/5">
        <button class="theme-dot" data-theme-set="midnight" data-active="true" style="background:linear-gradient(135deg,#22d3ee,#0a0e1a);" title="Midnight"></button>
        <button class="theme-dot" data-theme-set="stadium"  data-active="false" style="background:linear-gradient(135deg,#4ade80,#03110a);" title="Stadium"></button>
        <button class="theme-dot" data-theme-set="floodlight" data-active="false" style="background:linear-gradient(135deg,#a78bfa,#14102e);" title="Floodlight"></button>
      </div>
      <!-- Print -->
      <button id="printBtn" class="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-2 rounded-lg border border-white/10 hover:border-white/25 hover:bg-white/5 transition" style="color:#cbd5e1;background:transparent;" title="Print / Save as PDF (P)">
        <i data-lucide="printer" class="w-3.5 h-3.5"></i>
      </button>
      <!-- Share -->
      <button id="shareBtn" class="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-2 rounded-lg border border-white/10 hover:border-white/25 hover:bg-white/5 transition" style="color:#cbd5e1;background:transparent;" title="Copy summary">
        <i data-lucide="share-2" class="w-3.5 h-3.5"></i>
      </button>
      <!-- Filters -->
      <button id="openFilters" class="flex items-center gap-2 text-sm font-semibold px-3 py-2 rounded-lg border border-white/10 hover:border-white/25 hover:bg-white/5 transition magnetic" style="color:#e5e7eb;background:transparent;" title="Filters (F)">
        <i data-lucide="sliders-horizontal" class="w-4 h-4"></i>
        <span class="hidden sm:inline">Filters</span>
        <span id="activeFilterCount" class="hidden text-[11px] px-1.5 py-0.5 rounded-md bg-bat-400 text-ink-900 font-bold"></span>
      </button>
    </div>
  </div>
</header>

<!-- ============= MAIN ============= -->
<main class="max-w-7xl mx-auto px-4 sm:px-6 pb-32 md:pb-12">

  <!-- HERO -->
  <section class="pt-6 sm:pt-10 reveal">
    <div class="glass-strong shadow-card overflow-hidden relative">
      <!-- Cricket pitch backdrop -->
      <svg class="pitch-svg" viewBox="0 0 800 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" stroke-width="0.5"/>
          </pattern>
          <linearGradient id="pitchG" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%"   stop-color="#fffbeb" stop-opacity="0.5"/>
            <stop offset="100%" stop-color="#fffbeb" stop-opacity="0.1"/>
          </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)"/>
        <!-- Pitch strip -->
        <rect x="370" y="40" width="60" height="320" fill="url(#pitchG)" opacity="0.9"/>
        <!-- Crease lines -->
        <line x1="350" y1="80"  x2="450" y2="80"  stroke="#fff" stroke-width="1" opacity="0.5"/>
        <line x1="350" y1="320" x2="450" y2="320" stroke="#fff" stroke-width="1" opacity="0.5"/>
        <!-- Stumps top -->
        <g opacity="0.6" stroke="#fff" stroke-width="1.5" stroke-linecap="round">
          <line x1="392" y1="68" x2="392" y2="80"/>
          <line x1="400" y1="68" x2="400" y2="80"/>
          <line x1="408" y1="68" x2="408" y2="80"/>
        </g>
        <g opacity="0.6" stroke="#fff" stroke-width="1.5" stroke-linecap="round">
          <line x1="392" y1="320" x2="392" y2="332"/>
          <line x1="400" y1="320" x2="400" y2="332"/>
          <line x1="408" y1="320" x2="408" y2="332"/>
        </g>
        <!-- Boundary arc -->
        <ellipse cx="400" cy="200" rx="380" ry="180" fill="none" stroke="#fff" stroke-width="0.7" stroke-dasharray="3 5" opacity="0.4"/>
      </svg>

      <div class="relative grid grid-cols-1 md:grid-cols-[auto,1fr] gap-6 md:gap-10 p-6 sm:p-8 md:p-10 items-center">
        <div class="flex md:block items-center gap-5">
          <div class="relative w-24 h-24 sm:w-32 sm:h-32 md:w-44 md:h-44 shrink-0">
            <div class="absolute inset-0 rounded-full bg-gradient-to-br from-bat-400 via-blue-500 to-bowl-500 blur-2xl opacity-50"></div>
            <!-- Rotating gradient halo -->
            <div class="absolute -inset-1 rounded-full ring-rotate" style="background: conic-gradient(from 0deg, transparent 0%, var(--bat) 25%, transparent 50%, var(--bowl) 75%, transparent 100%); filter: blur(6px); opacity: .55;"></div>
            <div class="relative w-full h-full rounded-full p-[3px] bg-gradient-to-br from-bat-400 via-blue-500 to-bowl-500 profile-ring">
              <img src="{profile_img_src}" alt="Kasun Chamod" class="w-full h-full rounded-full object-cover" loading="eager"/>
            </div>
          </div>

          <div class="md:hidden">
            <div class="text-[11px] uppercase tracking-[0.2em] text-bat-400 font-bold">All-Rounder</div>
            <h1 class="font-serif text-3xl leading-tight mt-1">Kasun Chamod</h1>
          </div>
        </div>

        <div>
          <div class="hidden md:flex items-center gap-3">
            <span class="inline-flex items-center gap-1.5 text-[11px] uppercase tracking-[0.25em] text-bat-400 font-bold px-2.5 py-1 rounded-full border border-bat-400/30 bg-bat-400/5">
              <span class="w-1.5 h-1.5 rounded-full bg-bat-400 animate-pulse"></span>All-Rounder
            </span>
            <div class="h-3 w-px bg-white/15"></div>
            <span class="text-[11px] uppercase tracking-[0.25em] text-slate-400">Career 2024 — 2026</span>
          </div>

          <h1 class="hidden md:block font-serif text-5xl lg:text-6xl leading-[1.05] mt-3 text-white">
            Kasun Chamod
          </h1>

          <p class="mt-2 sm:mt-3 text-slate-300 text-sm sm:text-base flex flex-wrap items-center gap-x-3 gap-y-1">
            <span class="inline-flex items-center gap-1.5"><i data-lucide="circle-dot" class="w-3.5 h-3.5 text-bat-400"></i>Right-hand Bat</span>
            <span class="text-slate-600">·</span>
            <span class="inline-flex items-center gap-1.5"><i data-lucide="rotate-ccw" class="w-3.5 h-3.5 text-bowl-400"></i>Left-arm Orthodox</span>
          </p>

          <div class="accent-line mt-5"></div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5">
            <div class="score-cell">
              <div class="sc-label"><i data-lucide="layers" class="w-3 h-3"></i>Matches</div>
              <div class="sc-val num text-4xl sm:text-5xl text-white" id="kpi-matches">—</div>
            </div>
            <div class="score-cell">
              <div class="sc-label"><i data-lucide="circle-dot" class="w-3 h-3"></i>Runs</div>
              <div class="sc-val num text-4xl sm:text-5xl text-bat-400" id="kpi-runs">—</div>
            </div>
            <div class="score-cell">
              <div class="sc-label"><i data-lucide="rotate-ccw" class="w-3 h-3"></i>Wickets</div>
              <div class="sc-val num text-4xl sm:text-5xl text-bowl-400" id="kpi-wickets">—</div>
            </div>
            <div class="score-cell">
              <div class="sc-label"><i data-lucide="hand" class="w-3 h-3"></i>Catches</div>
              <div class="sc-val num text-4xl sm:text-5xl text-mint-400" id="kpi-catches">—</div>
            </div>
          </div>

          <div class="mt-6 flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-6">
            <div class="flex items-center gap-3">
              <span class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Recent Form</span>
              <div id="recentFormPills" class="flex items-center gap-1.5"></div>
            </div>
            <div id="recentFormSummary" class="text-sm text-slate-300"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ACHIEVEMENTS TICKER -->
  <section class="mt-4 reveal">
    <div class="ticker-rail">
      <div id="achievementsRibbon" class="ticker"></div>
    </div>
  </section>

  <!-- ACTIVE FILTERS -->
  <section id="activeFiltersBar" class="mt-4 hidden">
    <div class="flex items-center gap-2 flex-wrap">
      <span class="text-[11px] uppercase tracking-[0.15em] text-slate-400 mr-1">Active filters</span>
      <div id="activeFiltersChips" class="flex flex-wrap gap-2"></div>
      <button id="clearAllFilters" class="text-xs text-bat-400 hover:text-bat-200 underline underline-offset-4 ml-2" style="background:transparent;border:0;cursor:pointer;">Clear all</button>
    </div>
  </section>

  <!-- OVERVIEW -->
  <div data-tab-pane="overview">

    <!-- PLAYER RATING CARD -->
    <section class="mt-8 io-hidden">
      <div class="lt mb-4">
        <div class="lt-bar"></div>
        <div>
          <div class="lt-kicker"><i data-lucide="gauge" class="w-3.5 h-3.5"></i>Player Index</div>
          <h2 class="lt-title text-3xl sm:text-4xl">Overall Rating</h2>
          <div class="lt-sub">Auto-derived from career batting, bowling &amp; fielding</div>
        </div>
      </div>
      <div class="rating-card p-5 sm:p-7">
        <div class="grid grid-cols-1 md:grid-cols-[auto,1fr] gap-6 md:gap-9 items-center relative z-10">
          <!-- OVR block -->
          <div class="flex items-center gap-5 md:flex-col md:items-start md:gap-2">
            <div class="flex flex-col items-center md:items-start">
              <div class="ovr-badge text-7xl sm:text-8xl" id="ovrValue">—</div>
              <div class="text-[11px] uppercase tracking-[0.3em] text-slate-400 font-bold mt-1">Overall</div>
            </div>
            <div class="md:mt-3">
              <span id="ovrTier" class="inline-flex items-center gap-1.5 text-[11px] uppercase tracking-[0.18em] font-bold px-3 py-1.5 rounded-full border border-bat-400/40 bg-bat-400/10 text-bat-200">All-Rounder</span>
            </div>
          </div>
          <!-- attribute bars -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-x-7 gap-y-4" id="ratingBars"></div>
        </div>
      </div>
    </section>

    <section class="mt-10 io-hidden">
      <div class="lt mb-4">
        <div class="lt-bar"></div>
        <div>
          <div class="lt-kicker"><i data-lucide="trophy" class="w-3.5 h-3.5"></i>Formats</div>
          <h2 class="lt-title text-3xl sm:text-4xl">Career at a glance</h2>
          <div class="lt-sub">A quick read of every format</div>
        </div>
      </div>
      <div id="formatGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
    </section>

    <!-- CAREER TIMELINE -->
    <section class="mt-10 io-hidden">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Career timeline</h3>
            <p class="text-xs text-slate-400">Matches across the years</p>
          </div>
          <i data-lucide="calendar-clock" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div id="timelineTrack" class="timeline-track"></div>
        <div id="timelineLabels" class="relative h-5 mt-1"></div>
      </div>
    </section>

    <!-- SEASON BY SEASON -->
    <section class="mt-10 io-hidden">
      <div class="lt mb-4">
        <div class="lt-bar"></div>
        <div>
          <div class="lt-kicker"><i data-lucide="calendar-range" class="w-3.5 h-3.5"></i>Year on Year</div>
          <h2 class="lt-title text-3xl sm:text-4xl">Season by season</h2>
          <div class="lt-sub">Every campaign, side by side</div>
        </div>
      </div>
      <div class="glass panel p-2 sm:p-3 overflow-x-auto">
        <table class="season-table">
          <thead>
            <tr>
              <th>Season</th>
              <th>M</th>
              <th>Runs</th>
              <th>Avg</th>
              <th>SR</th>
              <th>HS</th>
              <th>Wkts</th>
              <th>Econ</th>
              <th>Best</th>
            </tr>
          </thead>
          <tbody id="seasonTableBody"></tbody>
        </table>
      </div>
    </section>

    <div class="seam-divider" aria-hidden="true">
      <svg viewBox="0 0 360 12" fill="none">
        <line x1="0" y1="6" x2="360" y2="6" stroke="currentColor" stroke-width="0.6" stroke-dasharray="0.5 5"/>
        <circle cx="180" cy="6" r="3.5" fill="none" stroke="currentColor" stroke-width="0.8"/>
        <line x1="176" y1="6" x2="184" y2="6" stroke="currentColor" stroke-width="0.6"/>
      </svg>
    </div>

    <section class="mt-2 grid grid-cols-1 lg:grid-cols-2 gap-4 io-hidden">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-bat-400/15 grid place-items-center"><i data-lucide="circle-dot" class="w-4 h-4 text-bat-400"></i></div>
            <h3 class="text-lg font-bold">Batting</h3>
          </div>
          <button class="text-xs text-bat-400 hover:text-bat-200 inline-flex items-center gap-1 magnetic" data-jump="batting" style="background:transparent;border:0;cursor:pointer;">Details <i data-lucide="arrow-right" class="w-3 h-3"></i></button>
        </div>
        <div class="grid grid-cols-3 gap-3 text-center" id="overviewBattingMini"></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-bowl-500/15 grid place-items-center"><i data-lucide="rotate-ccw" class="w-4 h-4 text-bowl-400"></i></div>
            <h3 class="text-lg font-bold">Bowling</h3>
          </div>
          <button class="text-xs text-bowl-400 hover:text-bowl-200 inline-flex items-center gap-1 magnetic" data-jump="bowling" style="background:transparent;border:0;cursor:pointer;">Details <i data-lucide="arrow-right" class="w-3 h-3"></i></button>
        </div>
        <div class="grid grid-cols-3 gap-3 text-center" id="overviewBowlingMini"></div>
      </div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-[1.4fr,1fr] gap-4 io-hidden">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Runs &amp; Wickets by year</h3>
            <p class="text-xs text-slate-400">Yearly batting &amp; bowling output combined</p>
          </div>
          <div class="flex items-center gap-3 text-[11px] text-slate-400">
            <span class="inline-flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-sm bg-bat-400"></span>Runs</span>
            <span class="inline-flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-sm bg-bowl-400"></span>Wickets</span>
          </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="h-56 sm:h-64"><canvas id="chart-runs-year"></canvas></div>
          <div class="h-56 sm:h-64"><canvas id="chart-wickets-year"></canvas></div>
        </div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Performance radar</h3>
            <p class="text-xs text-slate-400">Skills profile (normalized)</p>
          </div>
          <i data-lucide="radar" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-56 sm:h-64"><canvas id="chart-radar"></canvas></div>
      </div>
    </section>

    <!-- HEAD TO HEAD -->
    <section class="mt-10 io-hidden">
      <div class="lt mb-4">
        <div class="lt-bar"></div>
        <div>
          <div class="lt-kicker"><i data-lucide="swords" class="w-3.5 h-3.5"></i>Match-up</div>
          <h2 class="lt-title text-3xl sm:text-4xl">Head to head</h2>
          <div class="lt-sub">Your record against any opponent</div>
        </div>
      </div>
      <div class="glass panel--mint panel p-5 sm:p-6">
        <div class="flex flex-col sm:flex-row sm:items-center gap-3 mb-5">
          <span class="text-[11px] uppercase tracking-[0.18em] text-slate-400 font-bold">Opponent</span>
          <select id="h2hSelect" class="h2h-select"></select>
          <span id="h2hMeta" class="text-sm text-slate-400 sm:ml-auto"></span>
        </div>
        <div id="h2hBody" class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3"></div>
      </div>
    </section>

    <section class="mt-10 io-hidden">
      <div class="lt mb-1">
        <div class="lt-bar"></div>
        <div>
          <div class="lt-kicker"><i data-lucide="medal" class="w-3.5 h-3.5"></i>Honours</div>
          <h2 class="lt-title text-3xl sm:text-4xl">Milestones</h2>
          <div class="lt-sub">Notable performances</div>
        </div>
      </div>
      <div id="milestonesGrid" class="mt-5 grid grid-cols-2 md:grid-cols-4 gap-3"></div>
    </section>
  </div>

  <!-- BATTING -->
  <div data-tab-pane="batting" class="hidden">
    <section class="mt-8 io-hidden">
      <div class="lt mb-4">
        <div class="lt-bar"></div>
        <div>
          <div class="lt-kicker"><i data-lucide="circle-dot" class="w-3.5 h-3.5"></i>With the bat</div>
          <h2 class="lt-title text-3xl sm:text-4xl">Batting</h2>
          <div class="lt-sub">Every metric, every milestone</div>
        </div>
      </div>
      <div id="battingStatGrid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4"></div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4 io-hidden">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Average progression</h3>
            <p class="text-xs text-slate-400">Cumulative average per innings</p>
          </div>
          <i data-lucide="trending-up" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bat-avg"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Strike rate progression</h3>
            <p class="text-xs text-slate-400">Cumulative strike rate per innings</p>
          </div>
          <i data-lucide="zap" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bat-sr"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6 lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Runs per innings</h3>
            <p class="text-xs text-slate-400">Each bar is one innings · highest score highlighted</p>
          </div>
          <i data-lucide="bar-chart-3" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bat-perInnings"></canvas></div>
      </div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-[1fr,1.4fr] gap-4 io-hidden">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">How got out</h3>
            <p class="text-xs text-slate-400">Dismissal breakdown</p>
          </div>
          <i data-lucide="pie-chart" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="donut-wrap h-56 sm:h-64">
          <canvas id="chart-dismissals"></canvas>
          <div class="donut-center">
            <div class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Total outs</div>
            <div id="dismissTotal" class="num-display num text-4xl mt-0.5">0</div>
          </div>
        </div>
        <div id="dismissLegend" class="mt-4 grid grid-cols-2 gap-2"></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Best knocks</h3>
            <p class="text-xs text-slate-400">All scores 30 and above</p>
          </div>
          <i data-lucide="award" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div id="bestKnocksList" class="space-y-2"></div>
      </div>
    </section>
  </div>

  <!-- BOWLING -->
  <div data-tab-pane="bowling" class="hidden">
    <section class="mt-8 io-hidden">
      <div class="lt mb-4">
        <div class="lt-bar"></div>
        <div>
          <div class="lt-kicker" style="color:var(--bowl)"><i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>With the ball</div>
          <h2 class="lt-title text-3xl sm:text-4xl">Bowling</h2>
          <div class="lt-sub">Wickets, control and consistency</div>
        </div>
      </div>
      <div id="bowlingStatGrid" class="mt-4 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4"></div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4 io-hidden">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Bowling average</h3>
            <p class="text-xs text-slate-400">Cumulative · lower is better</p>
          </div>
          <i data-lucide="trending-down" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bowl-avg"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Economy</h3>
            <p class="text-xs text-slate-400">Cumulative runs per over</p>
          </div>
          <i data-lucide="gauge" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bowl-econ"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6 lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Wickets per match</h3>
            <p class="text-xs text-slate-400">Each bar is one bowling innings</p>
          </div>
          <i data-lucide="bar-chart-3" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bowl-perInnings"></canvas></div>
      </div>
    </section>

    <section class="mt-10 io-hidden">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold">Best bowling spells</h3>
            <p class="text-xs text-slate-400">3-wicket hauls and better</p>
          </div>
          <i data-lucide="flame" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div id="bestSpellsList" class="space-y-2"></div>
      </div>
    </section>
  </div>

  <!-- MATCHES -->
  <div data-tab-pane="matches" class="hidden">
    <section class="mt-8 io-hidden">
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3 mb-4">
        <div class="lt">
          <div class="lt-bar"></div>
          <div>
            <div class="lt-kicker"><i data-lucide="list" class="w-3.5 h-3.5"></i>Full record</div>
            <h2 class="lt-title text-3xl sm:text-4xl">Match log</h2>
            <div class="lt-sub">Every game, every contribution · tap a row to expand</div>
          </div>
        </div>
        <div class="relative w-full sm:max-w-xs">
          <i data-lucide="search" class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
          <input id="matchSearch" type="text" placeholder="Search opponent…" class="search-input"/>
        </div>
      </div>

      <div class="glass overflow-hidden">
        <div class="hidden md:block overflow-x-auto">
          <table class="ctable">
            <thead>
              <tr>
                <th class="sortable" data-sort="matchId">#</th>
                <th class="sortable" data-sort="Year">Year</th>
                <th class="sortable" data-sort="Match_Type">Format</th>
                <th class="sortable" data-sort="Opponent">Opponent</th>
                <th class="sortable text-right" data-sort="Runs">Bat</th>
                <th class="sortable" data-sort="Dismissal">Dismissal</th>
                <th class="sortable text-right" data-sort="Wickets">Bowl</th>
                <th class="text-right">Notes</th>
              </tr>
            </thead>
            <tbody id="matchTableBody"></tbody>
          </table>
        </div>
        <div id="matchCardList" class="md:hidden divide-y divide-white/5"></div>
      </div>

      <div id="matchEmpty" class="empty mt-3 hidden">No matches match the current filters.</div>
    </section>
  </div>

  <footer class="mt-16 pt-8 border-t border-white/5 text-center text-xs text-slate-500">
    <p>Career stats · Updated <span id="lastUpdated"></span></p>
    <p class="mt-1">Built with care · Hosted on Streamlit · Edit <code class="text-slate-400">data.py</code> to add new matches.</p>
    <p class="mt-2 text-[10px] text-slate-600">
      Shortcuts:
      <span class="text-slate-500">1–4</span> tabs ·
      <span class="text-slate-500">F</span> filters ·
      <span class="text-slate-500">R</span> reset ·
      <span class="text-slate-500">T</span> theme ·
      <span class="text-slate-500">P</span> print
    </p>
  </footer>
</main>

<!-- Scroll-to-top -->
<button id="scrollTopBtn" class="scroll-top" aria-label="Back to top">
  <i data-lucide="arrow-up" class="w-5 h-5"></i>
</button>

<!-- Toast -->
<div class="toast-wrap" id="toastWrap"></div>

<!-- MOBILE BOTTOM TAB BAR -->
<nav class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-ink-900/90 backdrop-blur-xl border-t border-white/10 mobile-tabbar">
  <div class="grid grid-cols-4 max-w-md mx-auto" id="mobileTabs" role="tablist">
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-semibold" data-tab="overview" data-active="true">
      <i data-lucide="layout-dashboard" class="w-5 h-5"></i><span>Overview</span>
    </button>
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-semibold" data-tab="batting" data-active="false">
      <i data-lucide="circle-dot" class="w-5 h-5"></i><span>Batting</span>
    </button>
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-semibold" data-tab="bowling" data-active="false">
      <i data-lucide="rotate-ccw" class="w-5 h-5"></i><span>Bowling</span>
    </button>
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-semibold" data-tab="matches" data-active="false">
      <i data-lucide="list" class="w-5 h-5"></i><span>Matches</span>
    </button>
  </div>
</nav>

<!-- FILTER DRAWER -->
<div id="filterDrawer" class="fixed inset-0 z-50 hidden">
  <div id="filterBackdrop" class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

  <aside class="absolute right-0 top-0 bottom-0 w-full sm:max-w-md border-l border-white/10 overflow-y-auto p-5 sm:p-6" style="background: var(--bg-1);">
    <div class="flex items-center justify-between mb-6">
      <div>
        <div class="text-[11px] uppercase tracking-[0.2em] text-slate-400">Filters</div>
        <h3 class="text-2xl font-serif mt-0.5">Refine stats</h3>
      </div>
      <button id="closeFilters" class="w-9 h-9 grid place-items-center rounded-lg border border-white/10 hover:border-white/30 transition" style="background:transparent;color:inherit;cursor:pointer;">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>

    <div class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-bold text-bat-400 flex items-center gap-2">
          <i data-lucide="calendar" class="w-4 h-4"></i> Year
        </h4>
        <button class="text-xs text-slate-400 hover:text-white" data-toggle-all="years" style="background:transparent;border:0;cursor:pointer;">Toggle all</button>
      </div>
      <div id="yearFilters" class="flex flex-wrap gap-2"></div>
    </div>

    <div class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-bold text-bowl-400 flex items-center gap-2">
          <i data-lucide="trophy" class="w-4 h-4"></i> Format
        </h4>
        <button class="text-xs text-slate-400 hover:text-white" data-toggle-all="types" style="background:transparent;border:0;cursor:pointer;">Toggle all</button>
      </div>
      <div id="typeFilters" class="flex flex-wrap gap-2"></div>
    </div>

    <div class="mb-6">
      <h4 class="text-sm font-bold text-mint-400 flex items-center gap-2 mb-3">
        <i data-lucide="users" class="w-4 h-4"></i> Opponent
      </h4>
      <div class="relative mb-2">
        <i data-lucide="search" class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
        <input id="opponentSearch" type="text" placeholder="Search teams…" class="search-input"/>
      </div>
      <div id="opponentFilters" class="flex flex-wrap gap-2 max-h-56 overflow-y-auto pr-1"></div>
      <p class="text-[11px] text-slate-500 mt-2">Leave none selected to include all opponents.</p>
    </div>

    <div class="hr-soft my-4"></div>

    <div class="flex items-center gap-3">
      <button id="resetFilters" class="flex-1 px-4 py-3 rounded-xl border border-white/10 text-sm font-bold hover:border-white/30 transition" style="background:transparent;color:#e5e7eb;cursor:pointer;">Reset</button>
      <button id="applyFilters" class="flex-1 px-4 py-3 rounded-xl bg-gradient-to-r from-bat-500 to-bat-400 text-ink-900 text-sm font-extrabold hover:from-bat-400 hover:to-bat-200 transition" style="border:0;cursor:pointer;">Apply</button>
    </div>
  </aside>
</div>

<!-- ============= DATA & APP LOGIC ============= -->
<script>
window.CRICKET_DATA = {data_json};
</script>

<script>
(() => {{
  'use strict';

  const $  = (sel, ctx=document) => ctx.querySelector(sel);
  const $$ = (sel, ctx=document) => Array.from(ctx.querySelectorAll(sel));
  const fmt = (n, d=0) => (n == null || isNaN(n)) ? '—' : Number(n).toLocaleString('en-US', {{ minimumFractionDigits:d, maximumFractionDigits:d }});

  if (window.Chart) {{
    Chart.defaults.font.family = "'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif";
    Chart.defaults.font.size = 12;
  }}

  const oversToBalls = ov => {{
    if (ov == null) return 0;
    const s = String(ov);
    const [o, b='0'] = s.split('.');
    return (parseInt(o,10)||0)*6 + (parseInt(b,10)||0);
  }};
  const ballsToOvers = balls => `${{Math.floor(balls/6)}}.${{balls%6}}`;

  const normalizeDismissal = d => {{
    if (!d) return null;
    const k = String(d).trim().toLowerCase();
    const map = {{
      'lbw':'LBW','runout':'Run Out','run out':'Run Out',
      'stump':'Stumped','stumped':'Stumped','bowled':'Bowled',
      'caught':'Caught','hit wkt':'Hit Wicket','hit wicket':'Hit Wicket',
      'caught b':'Caught Behind','caught and bowled':'Caught Behind',
      'caught & bowled':'Caught Behind','c&b':'Caught Behind',
      'caught behind':'Caught Behind'
    }};
    return map[k] || (k.charAt(0).toUpperCase()+k.slice(1));
  }};

  const normalizeMatchType = t => {{
    if (!t) return t;
    const clean = String(t).trim();
    const lower = clean.toLowerCase();
    const map = {{
      'inter uni': 'Inter University',
      'inter university': 'Inter University',
    }};
    return map[lower] || clean;
  }};

  const RAW = (window.CRICKET_DATA || []).map((r,i) => ({{
    ...r,
    matchId: r.matchId ?? (i+1),
    Dismissal: normalizeDismissal(r.Dismissal),
    Match_Type: normalizeMatchType(r.Match_Type),
  }}));

  const allYears  = [...new Set(RAW.map(r => r.Year).filter(Boolean))].sort();
  const allTypes  = [...new Set(RAW.map(r => r.Match_Type).filter(Boolean))].sort();
  const allOpps   = [...new Set(RAW.map(r => r.Opponent).filter(Boolean))].sort();

  const state = {{
    years:  new Set(allYears),
    types:  new Set(allTypes),
    opps:   new Set(),
    tab:    'overview',
    matchSort: {{ key:'matchId', dir:'asc' }},
    matchSearch: '',
    h2hOpp: null,
    openRows: new Set(),
  }};

  function getFiltered() {{
    return RAW.filter(r =>
      state.years.has(r.Year) &&
      state.types.has(r.Match_Type) &&
      (state.opps.size === 0 || state.opps.has(r.Opponent))
    );
  }}

  function computeBatting(df) {{
    const bat = df.filter(r => r.Runs != null);
    const matches = df.length;
    const innings = bat.length;
    const runs = bat.reduce((s,r) => s + (r.Runs||0), 0);
    const balls = bat.reduce((s,r) => s + (r.Balls||0), 0);
    const outs = bat.filter(r => String(r.Out||'').toLowerCase() === 'yes').length;
    const fours = df.reduce((s,r) => s + (r['4s']||0), 0);
    const sixes = df.reduce((s,r) => s + (r['6s']||0), 0);
    const catches = df.reduce((s,r) => s + (r.Catch||0), 0);
    const average = outs > 0 ? runs/outs : 0;
    const sr = balls > 0 ? (runs/balls)*100 : 0;

    let highest = 0, highestNotOut = false;
    if (innings > 0) {{
      const max = Math.max(...bat.map(r => r.Runs||0));
      highest = max;
      highestNotOut = bat.some(r => r.Runs === max && String(r.Out||'').toLowerCase() !== 'yes');
    }}

    const thirties = bat.filter(r => r.Runs >= 30 && r.Runs < 50).length;
    const fifties  = bat.filter(r => r.Runs >= 50 && r.Runs < 100).length;
    const hundreds = bat.filter(r => r.Runs >= 100).length;

    const dismMap = {{}};
    bat.forEach(r => {{
      if (r.Dismissal && String(r.Out||'').toLowerCase() === 'yes') {{
        dismMap[r.Dismissal] = (dismMap[r.Dismissal]||0) + 1;
      }}
    }});

    return {{
      matches, innings, runs, balls, outs, fours, sixes, catches,
      average, sr, highest, highestNotOut,
      thirties, fifties, hundreds, dismissals: dismMap,
      highestDisplay: innings ? `${{highest}}${{highestNotOut?'*':''}}` : '—',
    }};
  }}

  function computeBowling(df) {{
    const bowl = df.filter(r => r.Overs != null);
    const innings = bowl.length;
    const balls = bowl.reduce((s,r) => s + oversToBalls(r.Overs), 0);
    const overs = ballsToOvers(balls);
    const runs = bowl.reduce((s,r) => s + (r.Runs_Conceded||0), 0);
    const wickets = bowl.reduce((s,r) => s + (r.Wickets||0), 0);
    const maidens = bowl.reduce((s,r) => s + (r.Maidens||0), 0);
    const economy = balls > 0 ? runs / (balls/6) : 0;
    const average = wickets > 0 ? runs / wickets : 0;
    const sr = wickets > 0 ? balls / wickets : 0;

    let bestW = 0, bestR = Infinity;
    bowl.forEach(r => {{
      const w = r.Wickets||0, c = r.Runs_Conceded||0;
      if (w > bestW || (w === bestW && c < bestR)) {{ bestW = w; bestR = c; }}
    }});
    const best = innings ? `${{bestW}}/${{bestR === Infinity ? 0 : bestR}}` : '—';

    const threeW = bowl.filter(r => (r.Wickets||0) >= 3).length;
    const fiveW  = bowl.filter(r => (r.Wickets||0) >= 5).length;

    return {{ innings, balls, overs, runs, wickets, maidens, economy, average, sr, best, threeW, fiveW }};
  }}

  function animateCount(el, to, decimals=0, duration=900) {{
    if (!el) return;
    const from = 0;
    const start = performance.now();
    const ease = t => 1 - Math.pow(1-t, 3);
    function tick(now) {{
      const t = Math.min(1, (now-start)/duration);
      const v = from + (to-from)*ease(t);
      el.textContent = decimals === 0 ? Math.round(v).toLocaleString() : v.toFixed(decimals);
      if (t < 1) requestAnimationFrame(tick);
      else el.textContent = decimals === 0 ? Math.round(to).toLocaleString() : to.toFixed(decimals);
    }}
    requestAnimationFrame(tick);
  }}

  function renderHero(df, bat, bowl) {{
    animateCount($('#kpi-matches'), df.length);
    animateCount($('#kpi-runs'),    bat.runs);
    animateCount($('#kpi-wickets'), bowl.wickets);
    animateCount($('#kpi-catches'), bat.catches);

    const recent = [...df].slice(-5);
    const pillsEl = $('#recentFormPills');
    pillsEl.innerHTML = '';
    if (!recent.length) {{
      pillsEl.innerHTML = '<span class="text-xs text-slate-500">No matches</span>';
    }} else {{
      recent.forEach(r => {{
        let label = '–', bg = 'rgba(255,255,255,.06)', color = '#94a3b8';
        if (r.Runs != null && r.Runs >= 30) {{ label = r.Runs; bg = 'rgba(34,211,238,.18)'; color = '#a5f3fc'; }}
        else if (r.Wickets != null && r.Wickets >= 3) {{ label = `${{r.Wickets}}W`; bg = 'rgba(245,158,11,.18)'; color = '#fde68a'; }}
        else if (r.Runs != null && r.Runs > 0) {{ label = r.Runs; bg = 'rgba(255,255,255,.05)'; color = '#cbd5e1'; }}
        else if (r.Wickets != null && r.Wickets >= 1) {{ label = `${{r.Wickets}}w`; bg = 'rgba(255,255,255,.05)'; color = '#cbd5e1'; }}
        else if (r.Runs === 0) {{ label = '0'; bg = 'rgba(244,63,94,.15)'; color = '#fb7185'; }}

        const pill = document.createElement('div');
        pill.className = 'form-pill';
        pill.style.background = bg;
        pill.style.color = color;
        pill.textContent = label;
        pill.title = `vs ${{r.Opponent}} (${{r.Year}})`;
        pillsEl.appendChild(pill);
      }});
    }}

    const last5 = recent;
    const r5 = last5.reduce((s,r) => s + (r.Runs||0), 0);
    const w5 = last5.reduce((s,r) => s + (r.Wickets||0), 0);
    $('#recentFormSummary').textContent = last5.length
      ? `${{r5}} runs · ${{w5}} wickets in last ${{last5.length}}`
      : '';
  }}

  function renderAchievements(bat, bowl, df) {{
    const ribbon = $('#achievementsRibbon');
    if (!ribbon) return;
    const items = [];
    if (bat.hundreds > 0)  items.push({{ icon:'crown',  text:`${{bat.hundreds}} century${{bat.hundreds>1?'s':''}}` }});
    if (bat.fifties > 0)   items.push({{ icon:'star',   text:`${{bat.fifties}} half-century${{bat.fifties>1?'s':''}}` }});
    if (bat.highest > 0)   items.push({{ icon:'flame',  text:`Top score: ${{bat.highestDisplay}}` }});
    if (bowl.fiveW > 0)    items.push({{ icon:'flame',  text:`${{bowl.fiveW}} five-wicket haul${{bowl.fiveW>1?'s':''}}` }});
    if (bowl.threeW > 0)   items.push({{ icon:'zap',    text:`${{bowl.threeW}} three-wicket haul${{bowl.threeW>1?'s':''}}` }});
    if (bowl.wickets >= 50) items.push({{ icon:'target', text:`${{bowl.wickets}} career wickets` }});
    if (bat.runs >= 1000)  items.push({{ icon:'trophy', text:`${{bat.runs.toLocaleString()}} career runs` }});
    if (bat.catches >= 10) items.push({{ icon:'hand',   text:`${{bat.catches}} catches taken` }});
    if (bowl.maidens > 0)  items.push({{ icon:'shield', text:`${{bowl.maidens}} maiden over${{bowl.maidens>1?'s':''}}` }});
    if (df.length > 0)     items.push({{ icon:'calendar-check', text:`${{df.length}} match${{df.length>1?'es':''}} played` }});

    ribbon.innerHTML = '';
    if (!items.length) {{
      ribbon.style.animation = 'none';
      ribbon.innerHTML = '<span class="tk" style="padding-left:8px">No achievements yet — keep playing.</span>';
      return;
    }}
    // Duplicate the set so the -50% translate loop is seamless.
    const tkHTML = it => `<span class="tk"><i data-lucide="${{it.icon}}" class="w-3.5 h-3.5"></i>${{it.text}}<span class="dot"></span></span>`;
    const seq = items.map(tkHTML).join('');
    ribbon.style.animation = '';
    ribbon.innerHTML = seq + seq;
    if (window.lucide) lucide.createIcons();
  }}

  /* ============= PLAYER RATING (FIFA-style index) ============= */
  function computeRating(bat, bowl, df) {{
    // Normalise each facet to a 0–99 band off realistic club ceilings,
    // then clamp. These are presentational, derived purely from existing stats.
    const clamp = v => Math.max(35, Math.min(99, Math.round(v)));
    const has = (n) => n != null && !isNaN(n);

    // Batting index: average (·40 cap), strike rate, output volume.
    const batScore = bat.innings
      ? 0.50 * Math.min(100, (bat.average / 35) * 100)
      + 0.30 * Math.min(100, (bat.sr / 130) * 100)
      + 0.20 * Math.min(100, (bat.runs / 400) * 100)
      : 0;

    // Bowling index: economy (lower better), average (lower better), wickets.
    const econScore = bowl.balls ? Math.max(0, 100 - ((bowl.economy - 3) / 6) * 100) : 0;
    const avgScore  = bowl.wickets ? Math.max(0, 100 - ((bowl.average - 10) / 30) * 100) : 0;
    const bowlScore = bowl.innings
      ? 0.40 * Math.min(100, Math.max(0, econScore))
      + 0.30 * Math.min(100, Math.max(0, avgScore))
      + 0.30 * Math.min(100, (bowl.wickets / 40) * 100)
      : 0;

    // Fielding index: catches.
    const fieldScore = Math.min(100, (bat.catches / 15) * 100);

    const BAT = clamp(batScore * 0.65 + 30);
    const BWL = clamp(bowlScore * 0.65 + 30);
    const FLD = clamp(fieldScore * 0.6 + 38);

    // Overall weights the two strong suits (rewards all-round balance).
    const facets = [BAT, BWL, FLD].sort((a,b) => b-a);
    const OVR = clamp(facets[0] * 0.5 + facets[1] * 0.35 + facets[2] * 0.15);

    let tier = 'Prospect';
    if (OVR >= 85) tier = 'Elite All-Rounder';
    else if (OVR >= 75) tier = 'Star All-Rounder';
    else if (OVR >= 65) tier = 'All-Rounder';
    else if (BAT - BWL >= 12) tier = 'Specialist Batter';
    else if (BWL - BAT >= 12) tier = 'Specialist Bowler';

    return {{ OVR, BAT, BWL, FLD, tier }};
  }}

  function renderRatingCard(bat, bowl, df) {{
    const r = computeRating(bat, bowl, df);
    const ovrEl = $('#ovrValue');
    if (ovrEl) animateCount(ovrEl, r.OVR, 0, 1100);
    const tierEl = $('#ovrTier');
    if (tierEl) tierEl.textContent = r.tier;

    const bars = $('#ratingBars');
    if (!bars) return;
    const rows = [
      {{ key:'BAT', label:'Batting',  val:r.BAT, icon:'circle-dot',
         detail:`${{fmt(bat.runs)}} runs · avg ${{bat.average?fmt(bat.average,1):'—'}}` }},
      {{ key:'BWL', label:'Bowling',  val:r.BWL, icon:'rotate-ccw',
         detail:`${{fmt(bowl.wickets)}} wkts · econ ${{bowl.economy?fmt(bowl.economy,2):'—'}}` }},
      {{ key:'FLD', label:'Fielding', val:r.FLD, icon:'hand',
         detail:`${{fmt(bat.catches)}} catches` }},
    ];
    bars.innerHTML = rows.map(row => `
      <div>
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-xs uppercase tracking-[0.12em] text-slate-300 font-bold inline-flex items-center gap-1.5">
            <i data-lucide="${{row.icon}}" class="w-3.5 h-3.5"></i>${{row.label}}
          </span>
          <span class="num-display num text-2xl text-white">${{row.val}}</span>
        </div>
        <div class="rating-bar"><span style="width:0%" data-w="${{row.val}}"></span></div>
        <div class="text-[11px] text-slate-500 mt-1.5">${{row.detail}}</div>
      </div>
    `).join('');
    // Animate the bar fills after layout.
    requestAnimationFrame(() => $$('#ratingBars .rating-bar > span').forEach(s => {{
      s.style.width = (s.dataset.w || 0) + '%';
    }}));
    if (window.lucide) lucide.createIcons();
  }}

  /* ============= SEASON BY SEASON ============= */
  function renderSeasonComparison(df) {{
    const tbody = $('#seasonTableBody');
    if (!tbody) return;
    const yrs = [...new Set(df.map(r => r.Year).filter(v => v != null))].sort();
    if (!yrs.length) {{
      tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;color:#64748b;padding:18px">No seasons match the current filters.</td></tr>';
      return;
    }}
    const maxRuns = Math.max(1, ...yrs.map(y => computeBatting(df.filter(r => r.Year === y)).runs));
    tbody.innerHTML = '';
    yrs.forEach(y => {{
      const sub = df.filter(r => r.Year === y);
      const b = computeBatting(sub);
      const bo = computeBowling(sub);
      const barW = Math.round((b.runs / maxRuns) * 46);
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="text-white">${{y}}</span><span class="yr-bar" style="width:${{barW}}px"></span></td>
        <td class="num text-slate-300">${{sub.length}}</td>
        <td class="num text-bat-400">${{fmt(b.runs)}}</td>
        <td class="num text-slate-200">${{b.average ? fmt(b.average,1) : '—'}}</td>
        <td class="num text-slate-200">${{b.sr ? fmt(b.sr,1) : '—'}}</td>
        <td class="num text-slate-200">${{b.highestDisplay}}</td>
        <td class="num text-bowl-400">${{fmt(bo.wickets)}}</td>
        <td class="num text-slate-200">${{bo.economy ? fmt(bo.economy,2) : '—'}}</td>
        <td class="num text-slate-200">${{bo.best}}</td>
      `;
      tbody.appendChild(tr);
    }});
  }}

  /* ============= HEAD TO HEAD ============= */
  function renderHeadToHead(df) {{
    const sel = $('#h2hSelect');
    const body = $('#h2hBody');
    if (!sel || !body) return;

    // Opponents present in the current filtered set, by matches played.
    const oppCounts = {{}};
    df.forEach(r => {{ if (r.Opponent) oppCounts[r.Opponent] = (oppCounts[r.Opponent]||0) + 1; }});
    const opps = Object.keys(oppCounts).sort((a,b) => oppCounts[b]-oppCounts[a] || a.localeCompare(b));

    if (!opps.length) {{
      sel.innerHTML = '<option>No opponents</option>';
      body.innerHTML = '<div class="empty col-span-full">No opponents match the current filters.</div>';
      $('#h2hMeta').textContent = '';
      return;
    }}

    // Preserve current selection if still valid, else default to most-played.
    if (!state.h2hOpp || !oppCounts[state.h2hOpp]) state.h2hOpp = opps[0];
    sel.innerHTML = opps.map(o =>
      `<option value="${{o.replace(/"/g,'&quot;')}}"${{o===state.h2hOpp?' selected':''}}>${{o}} (${{oppCounts[o]}})</option>`
    ).join('');

    const sub = df.filter(r => r.Opponent === state.h2hOpp);
    const b = computeBatting(sub);
    const bo = computeBowling(sub);
    $('#h2hMeta').textContent = `${{sub.length}} meeting${{sub.length===1?'':'s'}}`;

    const cells = [
      {{ k:'Matches', v: sub.length, c:'text-white', sz:'text-3xl' }},
      {{ k:'Runs',    v: fmt(b.runs), c:'text-bat-400', sz:'text-3xl' }},
      {{ k:'Avg',     v: b.average ? fmt(b.average,1) : '—', c:'text-slate-100', sz:'text-3xl' }},
      {{ k:'HS',      v: b.highestDisplay, c:'text-slate-100', sz:'text-3xl' }},
      {{ k:'Wkts',    v: fmt(bo.wickets), c:'text-bowl-400', sz:'text-3xl' }},
      {{ k:'Econ',    v: bo.economy ? fmt(bo.economy,2) : '—', c:'text-slate-100', sz:'text-3xl' }},
      {{ k:'Best',    v: bo.best, c:'text-slate-100', sz:'text-3xl' }},
    ];
    body.innerHTML = cells.map(c => `
      <div class="vs-stat score-cell">
        <div class="v ${{c.c}} ${{c.sz}}">${{c.v}}</div>
        <div class="k">${{c.k}}</div>
      </div>
    `).join('');
  }}

  function renderTimeline(df) {{
    const track = $('#timelineTrack');
    const labels = $('#timelineLabels');
    if (!track || !labels) return;
    track.innerHTML = '';
    labels.innerHTML = '';

    if (!df.length) {{
      track.innerHTML = '<div class="empty" style="margin:6px;">No matches yet.</div>';
      return;
    }}
    const yearCounts = {{}};
    df.forEach(r => {{
      if (r.Year != null) yearCounts[r.Year] = (yearCounts[r.Year]||0) + 1;
    }});
    const yrs = Object.keys(yearCounts).map(Number).sort();
    if (yrs.length < 2) yrs.unshift(yrs[0] - 1);
    const min = yrs[0], max = yrs[yrs.length-1];
    const span = Math.max(1, max - min);

    yrs.forEach(y => {{
      const pct = ((y - min) / span) * 96 + 2;
      const node = document.createElement('div');
      node.className = 'timeline-node';
      node.style.left = `${{pct}}%`;
      const count = yearCounts[y] || 0;
      node.title = count > 0 ? `${{y}} · ${{count}} match${{count>1?'es':''}}` : `${{y}}`;
      const sz = Math.min(22, 10 + count * 0.6);
      node.style.width = `${{sz}}px`;
      node.style.height = `${{sz}}px`;
      track.appendChild(node);

      const lab = document.createElement('div');
      lab.className = 'timeline-label';
      lab.style.left = `${{pct}}%`;
      lab.textContent = y;
      labels.appendChild(lab);
    }});
  }}

  function renderFormatGrid(df) {{
    const grid = $('#formatGrid');
    grid.innerHTML = '';
    const types = [...new Set(df.map(r => r.Match_Type).filter(Boolean))].sort();
    if (!types.length) {{
      grid.innerHTML = '<div class="empty col-span-full">No formats match the current filters.</div>';
      return;
    }}
    types.forEach((t, i) => {{
      const sub = df.filter(r => r.Match_Type === t);
      const b = computeBatting(sub);
      const bo = computeBowling(sub);
      const card = document.createElement('div');
      card.className = 'glass stat-card p-5 sm:p-6 reveal';
      card.style.animationDelay = `${{i*70}}ms`;
      card.innerHTML = `
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-base font-bold flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-bat-400"></span>
            ${{t}}
          </h3>
          <span class="text-[11px] uppercase tracking-[0.15em] text-slate-400">${{sub.length}} match${{sub.length===1?'':'es'}}</span>
        </div>
        <div class="grid grid-cols-3 gap-3">
          <div>
            <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">Runs</div>
            <div class="num-display num text-2xl text-bat-400 mt-0.5">${{fmt(b.runs)}}</div>
          </div>
          <div>
            <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">Wkts</div>
            <div class="num-display num text-2xl text-bowl-400 mt-0.5">${{fmt(bo.wickets)}}</div>
          </div>
          <div>
            <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">HS / Best</div>
            <div class="num-display num text-2xl text-white mt-0.5 truncate" title="HS ${{b.highestDisplay}} · Best ${{bo.best}}">${{b.highestDisplay}}</div>
          </div>
        </div>
        <div class="hr-soft my-4"></div>
        <div class="grid grid-cols-3 gap-3 text-xs text-slate-300">
          <div><span class="text-slate-500">Avg</span><br><span class="num">${{b.average ? fmt(b.average,1) : '—'}}</span></div>
          <div><span class="text-slate-500">SR</span><br><span class="num">${{b.sr ? fmt(b.sr,1) : '—'}}</span></div>
          <div><span class="text-slate-500">Econ</span><br><span class="num">${{bo.economy ? fmt(bo.economy,2) : '—'}}</span></div>
        </div>
      `;
      grid.appendChild(card);
    }});
  }}

  function miniStat(label, value, color='text-white') {{
    return `
      <div class="glass stat-card p-3">
        <div class="text-[10px] uppercase tracking-[0.1em] text-slate-400">${{label}}</div>
        <div class="num-display num text-2xl mt-1 ${{color}}">${{value}}</div>
      </div>`;
  }}

  function renderOverviewMini(bat, bowl) {{
    $('#overviewBattingMini').innerHTML =
      miniStat('Innings', fmt(bat.innings), 'text-white') +
      miniStat('Average', bat.average ? fmt(bat.average,2) : '—', 'text-bat-400') +
      miniStat('Strike rate', bat.sr ? fmt(bat.sr,1) : '—', 'text-bat-400');

    $('#overviewBowlingMini').innerHTML =
      miniStat('Innings', fmt(bowl.innings), 'text-white') +
      miniStat('Average', bowl.average ? fmt(bowl.average,2) : '—', 'text-bowl-400') +
      miniStat('Economy', bowl.economy ? fmt(bowl.economy,2) : '—', 'text-bowl-400');
  }}

  function renderMilestones(df, bat, bowl) {{
    const grid = $('#milestonesGrid');
    grid.innerHTML = '';
    const items = [
      {{ label:'Hundreds', value: bat.hundreds, sub:'100+ scores', icon:'crown', color:'bat' }},
      {{ label:'Fifties',  value: bat.fifties,  sub:'50–99 scores', icon:'star', color:'bat' }},
      {{ label:'Thirties', value: bat.thirties, sub:'30–49 scores', icon:'award', color:'bat' }},
      {{ label:'Highest',  value: bat.highestDisplay, sub:'Top knock', icon:'flame', color:'bat' }},
      {{ label:'5W hauls', value: bowl.fiveW, sub:'5+ wickets', icon:'flame', color:'bowl' }},
      {{ label:'3W hauls', value: bowl.threeW, sub:'3+ wickets', icon:'zap', color:'bowl' }},
      {{ label:'Best fig.', value: bowl.best, sub:'Best bowling', icon:'crown', color:'bowl' }},
      {{ label:'Maidens',  value: bowl.maidens, sub:'Total maidens', icon:'target', color:'bowl' }},
    ];
    items.forEach((it,i) => {{
      const colorMap = {{
        bat:  {{ ring:'rgba(34,211,238,.25)',  num:'text-bat-400' }},
        bowl: {{ ring:'rgba(245,158,11,.25)',  num:'text-bowl-400' }},
      }};
      const c = colorMap[it.color];
      const el = document.createElement('div');
      el.className = `glass stat-card ${{it.color === 'bowl' ? 'stat-card--bowl' : ''}} p-4 sm:p-5 reveal`;
      el.style.animationDelay = `${{i*40}}ms`;
      el.innerHTML = `
        <div class="flex items-center gap-2 text-slate-400 text-[11px] uppercase tracking-[0.1em] font-semibold">
          <i data-lucide="${{it.icon}}" class="w-3.5 h-3.5"></i>${{it.label}}
        </div>
        <div class="num-display num text-3xl sm:text-4xl mt-1 ${{c.num}}">${{it.value}}</div>
        <div class="text-xs text-slate-500 mt-1">${{it.sub}}</div>
      `;
      grid.appendChild(el);
    }});
    if (window.lucide) lucide.createIcons();
  }}

  function renderBattingTab(df, bat) {{
    const grid = $('#battingStatGrid');
    grid.innerHTML = '';
    const cells = [
      ['Matches',     fmt(bat.matches)],
      ['Innings',     fmt(bat.innings)],
      ['Runs',        fmt(bat.runs),      'text-bat-400'],
      ['Balls',       fmt(bat.balls)],
      ['Average',     bat.average ? fmt(bat.average,2) : '—', 'text-bat-400'],
      ['Strike rate', bat.sr ? fmt(bat.sr,1) : '—',           'text-bat-400'],
      ['Highest',     bat.highestDisplay,'text-white'],
      ['100s',        fmt(bat.hundreds)],
      ['50s',         fmt(bat.fifties)],
      ['30+',         fmt(bat.thirties)],
      ['4s',          fmt(bat.fours)],
      ['6s',          fmt(bat.sixes)],
    ];
    cells.forEach(([label, val, color], i) => {{
      const card = document.createElement('div');
      card.className = 'glass stat-card p-4 sm:p-5 reveal';
      card.style.animationDelay = `${{i*30}}ms`;
      card.innerHTML = `
        <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400 font-semibold">${{label}}</div>
        <div class="num-display num text-3xl sm:text-4xl mt-1.5 ${{color||'text-white'}}">${{val}}</div>
      `;
      grid.appendChild(card);
    }});

    const knocks = df
      .filter(r => r.Runs != null && r.Runs >= 30)
      .sort((a,b) => (b.Runs||0) - (a.Runs||0));
    const list = $('#bestKnocksList');
    list.innerHTML = '';
    if (!knocks.length) {{
      list.innerHTML = '<div class="empty">No 30+ scores yet — chip away.</div>';
    }} else {{
      knocks.slice(0,12).forEach(r => {{
        const sr = r.Balls ? ((r.Runs/r.Balls)*100).toFixed(1) : '—';
        const isHundred = r.Runs >= 100;
        const isFifty   = r.Runs >= 50 && r.Runs < 100;
        const badge = isHundred ? '<span class="badge badge-100">100</span>'
                    : isFifty   ? '<span class="badge badge-50">50</span>'
                    : '<span class="badge">30+</span>';
        const out = String(r.Out||'').toLowerCase() === 'yes' ? r.Dismissal||'Out' : 'Not out';
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between gap-3 p-3 rounded-xl border border-white/5 hover:border-white/10 hover:bg-white/[.02] transition';
        item.innerHTML = `
          <div class="min-w-0 flex items-center gap-3">
            <div class="num-display num text-2xl sm:text-3xl text-bat-400 min-w-[60px]">${{r.Runs}}${{out==='Not out'?'<span class=\\"text-bat-200\\">*</span>':''}}</div>
            <div class="min-w-0">
              <div class="text-sm font-semibold truncate">vs ${{r.Opponent || 'Unknown'}}</div>
              <div class="text-xs text-slate-400 truncate">${{r.Match_Type||'—'}} · ${{r.Year||''}} · ${{r.Balls||0}} balls · SR ${{sr}} · ${{out}}</div>
            </div>
          </div>
          ${{badge}}
        `;
        list.appendChild(item);
      }});
    }}
  }}

  function renderBowlingTab(df, bowl) {{
    const grid = $('#bowlingStatGrid');
    grid.innerHTML = '';
    const cells = [
      ['Innings',     fmt(bowl.innings)],
      ['Overs',       bowl.overs || '—'],
      ['Wickets',     fmt(bowl.wickets), 'text-bowl-400'],
      ['Maidens',     fmt(bowl.maidens)],
      ['Average',     bowl.average ? fmt(bowl.average,2) : '—', 'text-bowl-400'],
      ['Economy',     bowl.economy ? fmt(bowl.economy,2) : '—', 'text-bowl-400'],
      ['Strike rate', bowl.sr ? fmt(bowl.sr,1) : '—'],
      ['Best',        bowl.best, 'text-white'],
      ['5W',          fmt(bowl.fiveW)],
      ['3W',          fmt(bowl.threeW)],
      ['Runs given',  fmt(bowl.runs)],
      ['Balls',       fmt(bowl.balls)],
    ];
    cells.forEach(([label, val, color], i) => {{
      const card = document.createElement('div');
      card.className = 'glass stat-card stat-card--bowl p-4 sm:p-5 reveal';
      card.style.animationDelay = `${{i*30}}ms`;
      card.innerHTML = `
        <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400 font-semibold">${{label}}</div>
        <div class="num-display num text-3xl sm:text-4xl mt-1.5 ${{color||'text-white'}}">${{val}}</div>
      `;
      grid.appendChild(card);
    }});

    const spells = df
      .filter(r => r.Overs != null && (r.Wickets||0) >= 3)
      .sort((a,b) => (b.Wickets-a.Wickets) || ((a.Runs_Conceded||0)-(b.Runs_Conceded||0)));
    const list = $('#bestSpellsList');
    list.innerHTML = '';
    if (!spells.length) {{
      list.innerHTML = '<div class="empty">No 3+ wicket spells yet.</div>';
    }} else {{
      spells.slice(0,15).forEach(r => {{
        const isFive = (r.Wickets||0) >= 5;
        const badge = isFive ? '<span class="badge badge-5w">5W</span>' : '<span class="badge badge-3w">3W</span>';
        const econ = r.Overs ? ((r.Runs_Conceded||0) / (oversToBalls(r.Overs)/6)).toFixed(2) : '—';
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between gap-3 p-3 rounded-xl border border-white/5 hover:border-white/10 hover:bg-white/[.02] transition';
        item.innerHTML = `
          <div class="min-w-0 flex items-center gap-3">
            <div class="num-display num text-2xl sm:text-3xl text-bowl-400 min-w-[80px] whitespace-nowrap">${{r.Wickets||0}}/${{r.Runs_Conceded||0}}</div>
            <div class="min-w-0">
              <div class="text-sm font-semibold truncate">vs ${{r.Opponent||'Unknown'}}</div>
              <div class="text-xs text-slate-400 truncate">${{r.Match_Type||'—'}} · ${{r.Year||''}} · ${{r.Overs||0}} overs · econ ${{econ}}</div>
            </div>
          </div>
          ${{badge}}
        `;
        list.appendChild(item);
      }});
    }}
  }}

  const chartColors = {{
    bat:    '#22d3ee',
    bowl:   '#f59e0b',
    bat2:   '#0891b2',
    bowl2:  '#d97706',
    grid:   'rgba(255,255,255,.06)',
    tick:   'rgba(226,232,240,.7)',
    label:  'rgba(226,232,240,.85)',
  }};

  function gradientFill(ctx, area, hex) {{
    if (!area) return hex+'40';
    const g = ctx.createLinearGradient(0, area.top, 0, area.bottom);
    g.addColorStop(0, hex+'66');
    g.addColorStop(1, hex+'00');
    return g;
  }}

  const baseLineOpts = (color, label) => ({{
    type: 'line',
    options: {{
      responsive: true, maintainAspectRatio: false,
      animation: {{ duration: 700, easing: 'easeOutCubic' }},
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: 'rgba(10,14,26,.95)', borderColor: 'rgba(255,255,255,.1)', borderWidth: 1,
          titleColor: '#fff', bodyColor: '#cbd5e1', padding: 12, cornerRadius: 10,
          displayColors: false,
          callbacks: {{ title: items => `Match ${{items[0].label}}` }}
        }}
      }},
      scales: {{
        x: {{ grid: {{ color: chartColors.grid, drawBorder:false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }} }},
        y: {{ grid: {{ color: chartColors.grid, drawBorder:false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }}, beginAtZero: true }}
      }}
    }},
    data: {{
      labels: [],
      datasets: [{{
        label, data: [], borderColor: color, borderWidth: 2.5,
        pointRadius: 3, pointHoverRadius: 6, pointBackgroundColor: color, pointBorderColor: '#0a0e1a',
        tension: 0.35, fill: true,
        backgroundColor: function(context) {{
          const {{ ctx, chartArea }} = context.chart;
          return gradientFill(ctx, chartArea, color);
        }}
      }}]
    }}
  }});

  const baseBarOpts = (color) => ({{
    type: 'bar',
    options: {{
      responsive: true, maintainAspectRatio: false,
      animation: {{ duration: 700 }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: 'rgba(10,14,26,.95)', borderColor: 'rgba(255,255,255,.1)', borderWidth: 1,
          titleColor: '#fff', bodyColor: '#cbd5e1', padding: 12, cornerRadius: 10, displayColors: false,
        }}
      }},
      scales: {{
        x: {{ grid: {{ display: false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }} }},
        y: {{ grid: {{ color: chartColors.grid, drawBorder:false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }}, beginAtZero: true }}
      }}
    }},
    data: {{ labels: [], datasets: [{{ data: [], backgroundColor: color, borderRadius: 6, borderSkipped: false, maxBarThickness: 28 }}] }}
  }});

  const charts = {{}};

  function destroyCharts() {{
    Object.values(charts).forEach(c => c && c.destroy());
    Object.keys(charts).forEach(k => delete charts[k]);
  }}

  function renderCharts(df) {{
    destroyCharts();
    state._lastDf = df;
    renderOverviewCharts(df);
    if (state.tab === 'batting') renderBattingChartsOnly(df);
    if (state.tab === 'bowling') renderBowlingChartsOnly(df);
  }}

  function renderOverviewCharts(df) {{
    const ordered = [...df].sort((a,b) => (a.Year-b.Year) || (a.matchId-b.matchId));
    const yrs = [...new Set(ordered.map(r => r.Year))].sort();
    const yearMap = {{}}, wktYearMap = {{}};
    ordered.forEach(r => {{
      if (r.Runs != null) yearMap[r.Year] = (yearMap[r.Year]||0) + (r.Runs||0);
      if (r.Overs != null) wktYearMap[r.Year] = (wktYearMap[r.Year]||0) + (r.Wickets||0);
    }});

    if (charts.runsYear) charts.runsYear.destroy();
    const runsYearCfg = baseBarOpts(chartColors.bat);
    runsYearCfg.data.labels = yrs;
    runsYearCfg.data.datasets[0].data = yrs.map(y => yearMap[y]||0);
    charts.runsYear = new Chart($('#chart-runs-year'), runsYearCfg);

    if (charts.wktsYear) charts.wktsYear.destroy();
    const wktsYearCfg = baseBarOpts(chartColors.bowl);
    wktsYearCfg.data.labels = yrs;
    wktsYearCfg.data.datasets[0].data = yrs.map(y => wktYearMap[y]||0);
    charts.wktsYear = new Chart($('#chart-wickets-year'), wktsYearCfg);

    // Performance Radar — derived from existing computations only.
    if (charts.radar) charts.radar.destroy();
    const bat = computeBatting(df);
    const bowl = computeBowling(df);
    const norm = {{
      Runs:    Math.min(100, (bat.runs / 1500) * 100),
      Average: Math.min(100, (bat.average / 50) * 100),
      'Strike Rate': Math.min(100, (bat.sr / 150) * 100),
      Wickets: Math.min(100, (bowl.wickets / 60) * 100),
      Economy: Math.min(100, Math.max(0, 100 - (bowl.economy / 8) * 100)),
      Catches: Math.min(100, (bat.catches / 30) * 100),
    }};
    const radarLabels = Object.keys(norm);
    const radarData   = radarLabels.map(k => Math.round(norm[k]));
    const radarCanvas = $('#chart-radar');
    if (radarCanvas) {{
      charts.radar = new Chart(radarCanvas, {{
        type: 'radar',
        data: {{
          labels: radarLabels,
          datasets: [{{
            label: 'Skill profile',
            data: radarData,
            backgroundColor: 'rgba(34,211,238,.18)',
            borderColor: chartColors.bat,
            borderWidth: 2,
            pointBackgroundColor: chartColors.bat,
            pointBorderColor: '#0a0e1a',
            pointRadius: 3, pointHoverRadius: 5,
          }}]
        }},
        options: {{
          responsive: true, maintainAspectRatio: false,
          animation: {{ duration: 700, easing: 'easeOutCubic' }},
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              backgroundColor: 'rgba(10,14,26,.95)',
              borderColor: 'rgba(255,255,255,.1)', borderWidth: 1,
              titleColor: '#fff', bodyColor: '#cbd5e1',
              padding: 10, cornerRadius: 10, displayColors: false,
              callbacks: {{ label: c => `${{c.label}}: ${{c.parsed.r}}/100` }}
            }}
          }},
          scales: {{
            r: {{
              beginAtZero: true, max: 100,
              angleLines: {{ color: 'rgba(255,255,255,.08)' }},
              grid: {{ color: 'rgba(255,255,255,.07)' }},
              pointLabels: {{ color: chartColors.label, font: {{ size: 10, weight: '600' }} }},
              ticks: {{ display: false, stepSize: 25 }}
            }}
          }}
        }}
      }});
    }}
  }}

  function renderBattingChartsOnly(df) {{
    const ordered = [...df].sort((a,b) => (a.Year-b.Year) || (a.matchId-b.matchId));
    const bat = ordered.filter(r => r.Runs != null);
    let cumRuns = 0, cumOuts = 0, cumBalls = 0;
    const labels = [], avg = [], sr = [], runsArr = [];
    bat.forEach((r, i) => {{
      cumRuns += (r.Runs||0);
      cumBalls += (r.Balls||0);
      if (String(r.Out||'').toLowerCase() === 'yes') cumOuts++;
      labels.push(String(i+1));
      avg.push(cumOuts ? +(cumRuns/cumOuts).toFixed(2) : cumRuns);
      sr.push(cumBalls ? +((cumRuns/cumBalls)*100).toFixed(2) : 0);
      runsArr.push(r.Runs||0);
    }});

    if (charts.batAvg) charts.batAvg.destroy();
    const avgCfg = baseLineOpts(chartColors.bat, 'Average');
    avgCfg.data.labels = labels; avgCfg.data.datasets[0].data = avg;
    avgCfg.options.plugins.tooltip.callbacks.label = c => `Avg: ${{c.parsed.y.toFixed(2)}}`;
    charts.batAvg = new Chart($('#chart-bat-avg'), avgCfg);

    if (charts.batSR) charts.batSR.destroy();
    const srCfg = baseLineOpts(chartColors.bat2, 'Strike rate');
    srCfg.data.labels = labels; srCfg.data.datasets[0].data = sr;
    srCfg.options.plugins.tooltip.callbacks.label = c => `SR: ${{c.parsed.y.toFixed(1)}}`;
    charts.batSR = new Chart($('#chart-bat-sr'), srCfg);

    if (charts.batPI) charts.batPI.destroy();
    const max = Math.max(...runsArr, 0);
    const perInnCfg = baseBarOpts(chartColors.bat);
    perInnCfg.data.labels = labels;
    perInnCfg.data.datasets[0].data = runsArr;
    perInnCfg.data.datasets[0].backgroundColor = runsArr.map(v => v === max && max > 0 ? '#22d3ee' : 'rgba(34,211,238,.45)');
    perInnCfg.options.plugins.tooltip.callbacks = {{
      title: items => `Innings ${{items[0].label}}`,
      label: c => {{
        const r = bat[c.dataIndex];
        return [`${{c.parsed.y}} runs vs ${{r.Opponent||'?'}}`, `${{r.Year||''}} · ${{r.Match_Type||''}}`];
      }}
    }};
    charts.batPI = new Chart($('#chart-bat-perInnings'), perInnCfg);

    const batStats = computeBatting(df);
    renderDismissalsDonut(batStats);
  }}

  function renderBowlingChartsOnly(df) {{
    const ordered = [...df].sort((a,b) => (a.Year-b.Year) || (a.matchId-b.matchId));
    const bowl = ordered.filter(r => r.Overs != null);
    let cR = 0, cW = 0, cB = 0;
    const blabels = [], bavg = [], econ = [], wkts = [];
    bowl.forEach((r, i) => {{
      cR += (r.Runs_Conceded||0);
      cW += (r.Wickets||0);
      cB += oversToBalls(r.Overs);
      blabels.push(String(i+1));
      bavg.push(cW ? +(cR/cW).toFixed(2) : 0);
      econ.push(cB ? +(cR / (cB/6)).toFixed(2) : 0);
      wkts.push(r.Wickets||0);
    }});

    if (charts.bowlAvg) charts.bowlAvg.destroy();
    const bAvgCfg = baseLineOpts(chartColors.bowl, 'Bowling avg');
    bAvgCfg.data.labels = blabels; bAvgCfg.data.datasets[0].data = bavg;
    bAvgCfg.options.plugins.tooltip.callbacks.label = c => `Avg: ${{c.parsed.y.toFixed(2)}}`;
    charts.bowlAvg = new Chart($('#chart-bowl-avg'), bAvgCfg);

    if (charts.bowlEcon) charts.bowlEcon.destroy();
    const econCfg = baseLineOpts(chartColors.bowl2, 'Economy');
    econCfg.data.labels = blabels; econCfg.data.datasets[0].data = econ;
    econCfg.options.plugins.tooltip.callbacks.label = c => `Econ: ${{c.parsed.y.toFixed(2)}}`;
    charts.bowlEcon = new Chart($('#chart-bowl-econ'), econCfg);

    if (charts.bowlPI) charts.bowlPI.destroy();
    const wpiCfg = baseBarOpts(chartColors.bowl);
    wpiCfg.data.labels = blabels;
    wpiCfg.data.datasets[0].data = wkts;
    wpiCfg.data.datasets[0].backgroundColor = wkts.map(v => v >= 5 ? '#fb923c' : v >= 3 ? '#f59e0b' : 'rgba(245,158,11,.45)');
    wpiCfg.options.plugins.tooltip.callbacks = {{
      title: items => `Innings ${{items[0].label}}`,
      label: c => {{
        const r = bowl[c.dataIndex];
        return [`${{c.parsed.y}} wkts · ${{r.Runs_Conceded||0}} runs in ${{r.Overs||0}} ov`, `vs ${{r.Opponent||'?'}} · ${{r.Year||''}}`];
      }}
    }};
    charts.bowlPI = new Chart($('#chart-bowl-perInnings'), wpiCfg);
  }}

  function renderDismissalsDonut(bat) {{
    if (charts.donut) charts.donut.destroy();
    const data = bat.dismissals;
    const labels = Object.keys(data);
    const values = labels.map(k => data[k]);
    const total = values.reduce((a,b) => a+b, 0);
    $('#dismissTotal').textContent = total;

    const palette = ['#22d3ee', '#f59e0b', '#34d399', '#a78bfa', '#fb7185', '#60a5fa', '#fde68a', '#fb923c'];
    const colors = labels.map((_,i) => palette[i % palette.length]);

    if (!labels.length) {{
      $('#dismissLegend').innerHTML = '<div class="empty col-span-2">No dismissals to chart.</div>';
      charts.donut = new Chart($('#chart-dismissals'), {{
        type: 'doughnut',
        data: {{ labels: ['No data'], datasets: [{{ data: [1], backgroundColor: ['rgba(255,255,255,.06)'], borderWidth: 0 }}] }},
        options: {{ responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }} }}
      }});
      return;
    }}

    charts.donut = new Chart($('#chart-dismissals'), {{
      type: 'doughnut',
      data: {{ labels, datasets: [{{ data: values, backgroundColor: colors, borderWidth: 0, hoverOffset: 8 }}] }},
      options: {{
        responsive: true, maintainAspectRatio: false,
        cutout: '72%',
        animation: {{ animateRotate: true, duration: 800 }},
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            backgroundColor: 'rgba(10,14,26,.95)', borderColor: 'rgba(255,255,255,.1)', borderWidth: 1,
            titleColor: '#fff', bodyColor: '#cbd5e1', padding: 12, cornerRadius: 10,
            callbacks: {{
              label: c => `${{c.label}}: ${{c.parsed}} (${{((c.parsed/total)*100).toFixed(0)}}%)`
            }}
          }}
        }}
      }}
    }});

    const legend = $('#dismissLegend');
    legend.innerHTML = '';
    labels.forEach((lab, i) => {{
      const pct = ((values[i]/total)*100).toFixed(0);
      const el = document.createElement('div');
      el.className = 'flex items-center justify-between gap-2 text-xs p-2 rounded-lg bg-white/[.02] border border-white/5';
      el.innerHTML = `
        <div class="flex items-center gap-2 min-w-0">
          <span class="w-2.5 h-2.5 rounded-full shrink-0" style="background:${{colors[i]}}"></span>
          <span class="truncate">${{lab}}</span>
        </div>
        <div class="text-slate-400 shrink-0"><span class="num text-white">${{values[i]}}</span> · ${{pct}}%</div>
      `;
      legend.appendChild(el);
    }});
  }}

  function renderMatchesTab(df) {{
    const tbody = $('#matchTableBody');
    const cardList = $('#matchCardList');
    const empty = $('#matchEmpty');
    tbody.innerHTML = '';
    cardList.innerHTML = '';

    let rows = [...df];
    if (state.matchSearch) {{
      const q = state.matchSearch.toLowerCase();
      rows = rows.filter(r => (r.Opponent||'').toLowerCase().includes(q));
    }}

    const {{ key, dir }} = state.matchSort;
    rows.sort((a,b) => {{
      let av = a[key], bv = b[key];
      if (av == null && bv == null) return 0;
      if (av == null) return 1;
      if (bv == null) return -1;
      if (typeof av === 'number' && typeof bv === 'number') return dir === 'asc' ? av-bv : bv-av;
      return dir === 'asc' ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
    }});

    if (!rows.length) empty.classList.remove('hidden'); else empty.classList.add('hidden');

    rows.forEach(r => {{
      const out = String(r.Out||'').toLowerCase() === 'yes';
      const batCell = r.Runs != null
        ? `<span class="num text-bat-400 font-bold">${{r.Runs}}${{out ? '' : '<span class=\\"text-bat-200\\">*</span>'}}</span><span class="text-slate-500"> (${{r.Balls||0}})</span>`
        : '<span class="text-slate-600">—</span>';
      const dismissCell = r.Runs != null ? (out ? (r.Dismissal||'Out') : 'Not out') : '<span class="text-slate-600">—</span>';
      const bowlCell = r.Overs != null
        ? `<span class="num text-bowl-400 font-bold">${{r.Wickets||0}}/${{r.Runs_Conceded||0}}</span><span class="text-slate-500"> (${{r.Overs}})</span>`
        : '<span class="text-slate-600">—</span>';

      const notes = [];
      if ((r.Runs||0) >= 100) notes.push('<span class="badge badge-100">100</span>');
      else if ((r.Runs||0) >= 50) notes.push('<span class="badge badge-50">50</span>');
      else if ((r.Runs||0) >= 30) notes.push('<span class="badge">30+</span>');
      if ((r.Wickets||0) >= 5) notes.push('<span class="badge badge-5w">5W</span>');
      else if ((r.Wickets||0) >= 3) notes.push('<span class="badge badge-3w">3W</span>');
      if ((r.Catch||0) > 0) notes.push(`<span class="badge">+${{r.Catch}} ct</span>`);

      const isOpen = state.openRows.has(r.matchId);

      const tr = document.createElement('tr');
      tr.className = 'match-row' + (isOpen ? ' open' : '');
      tr.dataset.mid = r.matchId;
      tr.innerHTML = `
        <td class="text-slate-500 num">${{r.matchId}}</td>
        <td class="num">${{r.Year||''}}</td>
        <td><span class="badge">${{r.Match_Type||'—'}}</span></td>
        <td class="text-slate-200">${{r.Opponent||''}}</td>
        <td class="text-right">${{batCell}}</td>
        <td class="text-slate-300 text-xs">${{dismissCell}}</td>
        <td class="text-right">${{bowlCell}}</td>
        <td class="text-right space-x-1">${{notes.join(' ')||''}}</td>
      `;
      tr.addEventListener('click', () => toggleRow(r.matchId));
      tbody.appendChild(tr);

      if (isOpen) {{
        const sc = document.createElement('tr');
        sc.className = 'scorecard-row';
        sc.innerHTML = `<td colspan="8">${{scorecardHTML(r)}}</td>`;
        tbody.appendChild(sc);
      }}

      const card = document.createElement('div');
      card.className = 'p-4 hover:bg-white/[.02] transition cursor-pointer';
      card.innerHTML = `
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="text-sm font-semibold truncate">vs ${{r.Opponent||'Unknown'}}</div>
            <div class="text-xs text-slate-400 mt-0.5">#${{r.matchId}} · ${{r.Year||''}} · ${{r.Match_Type||'—'}}</div>
          </div>
          <div class="flex items-center gap-2">
            <div class="flex flex-col items-end gap-1">${{notes.join(' ')||''}}</div>
            <i data-lucide="chevron-down" class="w-4 h-4 text-slate-500 transition-transform" style="${{isOpen?'transform:rotate(180deg)':''}}"></i>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3 mt-3 text-sm">
          <div class="rounded-lg border border-white/5 p-2.5">
            <div class="text-[10px] uppercase tracking-[0.1em] text-slate-500">Bat</div>
            <div class="mt-0.5">${{batCell}}</div>
            <div class="text-[11px] text-slate-500 mt-0.5 truncate">${{dismissCell}}</div>
          </div>
          <div class="rounded-lg border border-white/5 p-2.5">
            <div class="text-[10px] uppercase tracking-[0.1em] text-slate-500">Bowl</div>
            <div class="mt-0.5">${{bowlCell}}</div>
            <div class="text-[11px] text-slate-500 mt-0.5">${{r.Maidens||0}} maidens</div>
          </div>
        </div>
        <div class="card-expand" style="display:${{isOpen?'block':'none'}}">${{scorecardHTML(r)}}</div>
      `;
      card.addEventListener('click', () => toggleRow(r.matchId));
      cardList.appendChild(card);
    }});

    if (window.lucide) lucide.createIcons();
  }}

  // Per-match scorecard markup (used by the expandable match log).
  function scorecardHTML(r) {{
    const out = String(r.Out||'').toLowerCase() === 'yes';
    const sr = (r.Runs != null && r.Balls) ? ((r.Runs/r.Balls)*100).toFixed(1) : '—';
    const econ = r.Overs ? ((r.Runs_Conceded||0)/(oversToBalls(r.Overs)/6)).toFixed(2) : '—';
    const boxes = [];
    if (r.Runs != null) {{
      boxes.push(`<div class="sc-box"><div class="l">Runs (Balls)</div><div class="v text-bat-400">${{r.Runs}}${{out?'':'<span class="text-bat-200">*</span>'}} <span class="text-slate-500" style="font-size:13px">(${{r.Balls||0}})</span></div></div>`);
      boxes.push(`<div class="sc-box"><div class="l">Strike rate</div><div class="v text-slate-100">${{sr}}</div></div>`);
      boxes.push(`<div class="sc-box"><div class="l">Boundaries</div><div class="v text-slate-100">${{r['4s']||0}}<span style="font-size:12px;color:#64748b">×4</span> ${{r['6s']||0}}<span style="font-size:12px;color:#64748b">×6</span></div></div>`);
      boxes.push(`<div class="sc-box"><div class="l">Dismissal</div><div class="v text-slate-100" style="font-size:15px;line-height:1.2">${{out ? (r.Dismissal||'Out') : 'Not out'}}</div></div>`);
    }}
    if (r.Overs != null) {{
      boxes.push(`<div class="sc-box"><div class="l">Figures</div><div class="v text-bowl-400">${{r.Wickets||0}}/${{r.Runs_Conceded||0}}</div></div>`);
      boxes.push(`<div class="sc-box"><div class="l">Overs</div><div class="v text-slate-100">${{r.Overs}}</div></div>`);
      boxes.push(`<div class="sc-box"><div class="l">Economy</div><div class="v text-slate-100">${{econ}}</div></div>`);
      boxes.push(`<div class="sc-box"><div class="l">Maidens</div><div class="v text-slate-100">${{r.Maidens||0}}</div></div>`);
    }}
    boxes.push(`<div class="sc-box"><div class="l">Catches</div><div class="v text-mint-400">${{r.Catch||0}}</div></div>`);
    return `<div class="scorecard">
      <div class="text-[11px] uppercase tracking-[0.18em] text-slate-400 font-bold mb-3">Match #${{r.matchId}} · vs ${{r.Opponent||'Unknown'}} · ${{r.Match_Type||'—'}} · ${{r.Year||''}}</div>
      <div class="sc-grid">${{boxes.join('')}}</div>
    </div>`;
  }}

  function toggleRow(mid) {{
    if (state.openRows.has(mid)) state.openRows.delete(mid);
    else state.openRows.add(mid);
    renderMatchesTab(getFiltered());
  }}

  function renderFilterDrawerUI() {{
    const yEl = $('#yearFilters');
    yEl.innerHTML = '';
    allYears.forEach(y => {{
      const el = document.createElement('button');
      el.className = 'chip';
      el.dataset.active = state.years.has(y);
      el.dataset.color = 'bat';
      el.innerHTML = `<i data-lucide="${{state.years.has(y)?'check':'plus'}}" class="w-3 h-3"></i>${{y}}`;
      el.onclick = () => {{
        if (state.years.has(y)) state.years.delete(y); else state.years.add(y);
        renderFilterDrawerUI(); rerender();
      }};
      yEl.appendChild(el);
    }});

    const tEl = $('#typeFilters');
    tEl.innerHTML = '';
    allTypes.forEach(t => {{
      const el = document.createElement('button');
      el.className = 'chip';
      el.dataset.active = state.types.has(t);
      el.dataset.color = 'bowl';
      el.innerHTML = `<i data-lucide="${{state.types.has(t)?'check':'plus'}}" class="w-3 h-3"></i>${{t}}`;
      el.onclick = () => {{
        if (state.types.has(t)) state.types.delete(t); else state.types.add(t);
        renderFilterDrawerUI(); rerender();
      }};
      tEl.appendChild(el);
    }});

    const oEl = $('#opponentFilters');
    oEl.innerHTML = '';
    const q = ($('#opponentSearch').value || '').toLowerCase();
    const list = allOpps.filter(o => !q || o.toLowerCase().includes(q));
    if (!list.length) {{
      oEl.innerHTML = '<span class="text-xs text-slate-500">No teams match.</span>';
    }}
    list.forEach(o => {{
      const el = document.createElement('button');
      el.className = 'chip';
      el.dataset.active = state.opps.has(o);
      el.dataset.color = 'mint';
      el.innerHTML = `<i data-lucide="${{state.opps.has(o)?'check':'plus'}}" class="w-3 h-3"></i>${{o}}`;
      el.onclick = () => {{
        if (state.opps.has(o)) state.opps.delete(o); else state.opps.add(o);
        renderFilterDrawerUI(); rerender();
      }};
      oEl.appendChild(el);
    }});

    if (window.lucide) lucide.createIcons();
  }}

  function renderActiveFilters() {{
    const bar = $('#activeFiltersBar');
    const chips = $('#activeFiltersChips');
    chips.innerHTML = '';

    const yearMissing = allYears.filter(y => !state.years.has(y));
    const typeMissing = allTypes.filter(t => !state.types.has(t));
    const opps = [...state.opps];

    if (yearMissing.length) {{
      const yearsSelected = allYears.filter(y => state.years.has(y));
      yearsSelected.forEach(y => addActiveChip(`Year: ${{y}}`, () => {{ state.years.delete(y); renderFilterDrawerUI(); rerender(); }}, 'bat'));
    }}
    if (typeMissing.length) {{
      const typesSelected = allTypes.filter(t => state.types.has(t));
      typesSelected.forEach(t => addActiveChip(`Format: ${{t}}`, () => {{ state.types.delete(t); renderFilterDrawerUI(); rerender(); }}, 'bowl'));
    }}
    opps.forEach(o => addActiveChip(`vs ${{o}}`, () => {{ state.opps.delete(o); renderFilterDrawerUI(); rerender(); }}, 'mint'));

    function addActiveChip(label, onClose, color) {{
      const c = document.createElement('span');
      c.className = 'chip';
      c.dataset.active = 'true';
      c.dataset.color = color;
      c.innerHTML = `${{label}}<i data-lucide="x" class="w-3 h-3 ml-1"></i>`;
      c.onclick = onClose;
      chips.appendChild(c);
    }}

    if (chips.children.length === 0) {{
      bar.classList.add('hidden');
      $('#activeFilterCount').classList.add('hidden');
    }} else {{
      bar.classList.remove('hidden');
      $('#activeFilterCount').classList.remove('hidden');
      $('#activeFilterCount').textContent = chips.children.length;
    }}

    if (window.lucide) lucide.createIcons();
  }}

  function switchTab(name) {{
    state.tab = name;
    $$('[data-tab-pane]').forEach(p => p.classList.toggle('hidden', p.dataset.tabPane !== name));
    $$('[data-tab]').forEach(b => b.dataset.active = String(b.dataset.tab === name));
    requestAnimationFrame(() => {{
      const df = state._lastDf || getFiltered();
      if (name === 'batting') renderBattingChartsOnly(df);
      if (name === 'bowling') renderBowlingChartsOnly(df);
      Object.values(charts).forEach(c => {{ if (c) {{ c.resize(); }} }});
    }});
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }}

  function rerender() {{
    const df  = getFiltered();
    const bat = computeBatting(df);
    const bowl = computeBowling(df);

    renderHero(df, bat, bowl);
    renderAchievements(bat, bowl, df);
    renderRatingCard(bat, bowl, df);
    renderTimeline(df);
    renderSeasonComparison(df);
    renderHeadToHead(df);
    renderFormatGrid(df);
    renderOverviewMini(bat, bowl);
    renderMilestones(df, bat, bowl);
    renderBattingTab(df, bat);
    renderBowlingTab(df, bowl);
    renderMatchesTab(df);
    renderCharts(df);
    renderActiveFilters();

    if (window.lucide) lucide.createIcons();
  }}

  /* ============= UI ENHANCEMENTS ============= */

  // Toast notification
  function toast(msg, icon='check') {{
    const wrap = $('#toastWrap');
    if (!wrap) return;
    const t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = `<i data-lucide="${{icon}}" class="w-4 h-4 text-bat-400"></i><span>${{msg}}</span>`;
    wrap.appendChild(t);
    if (window.lucide) lucide.createIcons();
    setTimeout(() => {{
      t.style.transition = 'opacity .3s, transform .3s';
      t.style.opacity = '0';
      t.style.transform = 'translateY(8px)';
      setTimeout(() => t.remove(), 320);
    }}, 2200);
  }}

  // Scroll progress + scroll-to-top toggle
  function setupScroll() {{
    const bar = $('#scrollProgress');
    const top = $('#scrollTopBtn');
    const onScroll = () => {{
      const h = document.documentElement;
      const max = (h.scrollHeight - h.clientHeight) || 1;
      const pct = Math.min(1, h.scrollTop / max);
      if (bar) bar.style.transform = `scaleX(${{pct}})`;
      if (top) top.classList.toggle('show', h.scrollTop > 400);
    }};
    window.addEventListener('scroll', onScroll, {{ passive: true }});
    if (top) top.addEventListener('click', () => window.scrollTo({{ top:0, behavior:'smooth' }}));
    onScroll();
  }}

  // IntersectionObserver-driven reveal (subtle staggered entry as user scrolls)
  function setupReveal() {{
    if (!('IntersectionObserver' in window)) {{
      $$('.io-hidden').forEach(el => el.classList.add('io-show'));
      return;
    }}
    const io = new IntersectionObserver(entries => {{
      entries.forEach(e => {{
        if (e.isIntersecting) {{
          e.target.classList.add('io-show');
          e.target.classList.remove('io-hidden');
          io.unobserve(e.target);
        }}
      }});
    }}, {{ threshold: 0.08, rootMargin: '0px 0px -40px 0px' }});
    $$('.io-hidden').forEach(el => io.observe(el));
  }}

  // Magnetic button hover (desktop only)
  function setupMagnetic() {{
    if (window.matchMedia && window.matchMedia('(hover: none)').matches) return;
    $$('.magnetic').forEach(el => {{
      el.addEventListener('mousemove', (e) => {{
        const r = el.getBoundingClientRect();
        const x = e.clientX - r.left - r.width/2;
        const y = e.clientY - r.top - r.height/2;
        el.style.transform = `translate(${{x*0.15}}px, ${{y*0.2}}px)`;
      }});
      el.addEventListener('mouseleave', () => {{
        el.style.transform = '';
      }});
    }});
  }}

  // 3D tilt on stat cards (desktop only, lightweight)
  function setupTilt() {{
    if (window.matchMedia && window.matchMedia('(hover: none)').matches) return;
    document.addEventListener('mousemove', (e) => {{
      const card = e.target.closest && e.target.closest('.stat-card');
      $$('.stat-card.tilt-active').forEach(c => {{
        if (c !== card) {{
          c.style.transform = '';
          c.classList.remove('tilt-active');
        }}
      }});
      if (!card) return;
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5;
      const py = (e.clientY - r.top) / r.height - 0.5;
      card.classList.add('tilt-active');
      card.style.transform = `translateY(-3px) perspective(700px) rotateX(${{(-py*4).toFixed(2)}}deg) rotateY(${{(px*4).toFixed(2)}}deg)`;
    }});
    document.addEventListener('mouseleave', () => {{
      $$('.stat-card.tilt-active').forEach(c => {{ c.style.transform = ''; c.classList.remove('tilt-active'); }});
    }});
  }}

  // Theme switcher
  function setupTheme() {{
    const apply = (theme) => {{
      document.documentElement.setAttribute('data-theme', theme);
      $$('.theme-dot').forEach(b => b.dataset.active = String(b.dataset.themeSet === theme));
      try {{ localStorage.setItem('cricket-theme', theme); }} catch (e) {{}}
    }};
    $$('.theme-dot').forEach(b => b.addEventListener('click', () => {{
      apply(b.dataset.themeSet);
      toast(`Theme: ${{b.dataset.themeSet.charAt(0).toUpperCase() + b.dataset.themeSet.slice(1)}}`, 'palette');
    }}));
    let saved = null;
    try {{ saved = localStorage.getItem('cricket-theme'); }} catch (e) {{}}
    if (saved) apply(saved);
  }}

  // Spawn floating particles (cricket-ball dust)
  function setupParticles() {{
    const wrap = $('#particles');
    if (!wrap) return;
    const N = 14;
    for (let i = 0; i < N; i++) {{
      const s = document.createElement('span');
      s.style.left = (Math.random()*100) + 'vw';
      s.style.animationDelay = (Math.random() * 18) + 's';
      s.style.animationDuration = (14 + Math.random()*10) + 's';
      s.style.opacity = (0.15 + Math.random()*0.2);
      wrap.appendChild(s);
    }}
  }}

  // Print + Share + Keyboard shortcuts
  function setupActions() {{
    const printBtn = $('#printBtn');
    if (printBtn) printBtn.addEventListener('click', () => {{
      toast('Opening print preview…', 'printer');
      setTimeout(() => window.print(), 250);
    }});

    const shareBtn = $('#shareBtn');
    if (shareBtn) shareBtn.addEventListener('click', async () => {{
      const df = getFiltered();
      const bat = computeBatting(df);
      const bowl = computeBowling(df);
      const summary =
`Kasun Chamod · Cricket Stats
Matches: ${{df.length}}
Runs: ${{bat.runs}} (Avg ${{bat.average ? bat.average.toFixed(2) : '—'}}, SR ${{bat.sr ? bat.sr.toFixed(1) : '—'}})
Highest: ${{bat.highestDisplay}} · 100s ${{bat.hundreds}} · 50s ${{bat.fifties}}
Wickets: ${{bowl.wickets}} (Avg ${{bowl.average ? bowl.average.toFixed(2) : '—'}}, Econ ${{bowl.economy ? bowl.economy.toFixed(2) : '—'}})
Best bowling: ${{bowl.best}} · 5W ${{bowl.fiveW}} · 3W ${{bowl.threeW}}`;
      try {{
        if (navigator.share) {{
          await navigator.share({{ title: 'Kasun Chamod · Cricket Stats', text: summary }});
        }} else {{
          await navigator.clipboard.writeText(summary);
          toast('Summary copied to clipboard', 'clipboard-check');
        }}
      }} catch (e) {{
        toast('Could not share', 'x');
      }}
    }});

    document.addEventListener('keydown', e => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === '1') switchTab('overview');
      else if (e.key === '2') switchTab('batting');
      else if (e.key === '3') switchTab('bowling');
      else if (e.key === '4') switchTab('matches');
      else if (e.key.toLowerCase() === 'f') {{ $('#openFilters')?.click(); }}
      else if (e.key.toLowerCase() === 'r') {{ $('#resetFilters')?.click(); toast('Filters reset', 'refresh-cw'); }}
      else if (e.key.toLowerCase() === 't') {{
        const order = ['midnight','stadium','floodlight'];
        const cur = document.documentElement.getAttribute('data-theme') || 'midnight';
        const next = order[(order.indexOf(cur)+1) % order.length];
        $(`.theme-dot[data-theme-set="${{next}}"]`)?.click();
      }}
      else if (e.key.toLowerCase() === 'p') {{ $('#printBtn')?.click(); }}
    }});
  }}

  function bindEvents() {{
    $$('[data-tab]').forEach(btn => btn.addEventListener('click', () => switchTab(btn.dataset.tab)));
    $$('[data-jump]').forEach(btn => btn.addEventListener('click', () => switchTab(btn.dataset.jump)));

    $('#openFilters').onclick = () => {{ $('#filterDrawer').classList.remove('hidden'); renderFilterDrawerUI(); }};
    $('#closeFilters').onclick = closeDrawer;
    $('#filterBackdrop').onclick = closeDrawer;
    $('#applyFilters').onclick = () => {{ closeDrawer(); toast('Filters applied', 'filter'); }};
    function closeDrawer() {{ $('#filterDrawer').classList.add('hidden'); }}

    $('#resetFilters').onclick = () => {{
      state.years = new Set(allYears);
      state.types = new Set(allTypes);
      state.opps  = new Set();
      $('#opponentSearch').value = '';
      renderFilterDrawerUI(); rerender();
    }};
    $('#clearAllFilters').onclick = () => $('#resetFilters').click();

    $$('[data-toggle-all]').forEach(btn => btn.onclick = () => {{
      const target = btn.dataset.toggleAll;
      if (target === 'years') {{
        state.years = state.years.size === allYears.length ? new Set() : new Set(allYears);
      }}
      if (target === 'types') {{
        state.types = state.types.size === allTypes.length ? new Set() : new Set(allTypes);
      }}
      renderFilterDrawerUI(); rerender();
    }});

    $('#opponentSearch').addEventListener('input', renderFilterDrawerUI);

    $('#matchSearch').addEventListener('input', e => {{
      state.matchSearch = e.target.value;
      renderMatchesTab(getFiltered());
    }});

    $('#h2hSelect').addEventListener('change', e => {{
      state.h2hOpp = e.target.value;
      renderHeadToHead(getFiltered());
    }});

    $$('th.sortable').forEach(th => th.addEventListener('click', () => {{
      const k = th.dataset.sort;
      if (state.matchSort.key === k) {{
        state.matchSort.dir = state.matchSort.dir === 'asc' ? 'desc' : 'asc';
      }} else {{
        state.matchSort = {{ key: k, dir: 'asc' }};
      }}
      renderMatchesTab(getFiltered());
    }}));

    document.addEventListener('keydown', e => {{
      if (e.key === 'Escape') $('#filterDrawer').classList.add('hidden');
    }});

    let rt;
    window.addEventListener('resize', () => {{
      clearTimeout(rt);
      rt = setTimeout(() => Object.values(charts).forEach(c => c && c.resize()), 120);
    }});
  }}

  function init() {{
    if (!RAW.length) {{
      document.body.innerHTML = `<div style="padding:40px;color:#cbd5e1;text-align:center">
        <h1 style="font-size:24px;margin-bottom:12px">No data found</h1>
        <p>Make sure <code>data.py</code> contains <code>CRICKET_DATA</code>.</p>
      </div>`;
      return;
    }}
    $('#lastUpdated').textContent = new Date().toLocaleDateString('en-US', {{ year:'numeric', month:'short', day:'numeric' }});
    bindEvents();
    setupScroll();
    setupReveal();
    setupMagnetic();
    setupTilt();
    setupTheme();
    setupParticles();
    setupActions();
    rerender();
    switchTab('overview');
  }}

  function whenLibsReady(cb) {{
    if (window.Chart && window.lucide && window.tailwind) cb();
    else setTimeout(() => whenLibsReady(cb), 30);
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', () => whenLibsReady(init));
  }} else {{
    whenLibsReady(init);
  }}
}})();
</script>
</body>
</html>
"""
