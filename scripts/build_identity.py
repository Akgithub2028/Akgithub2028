"""Build the profile's responsive, self-contained SVG masthead (stdlib only)."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'identity'
OUT.mkdir(parents=True, exist_ok=True)


def render(mobile: bool, light: bool) -> str:
    w, h = (480, 166) if mobile else (960, 178)
    bg, ink, muted, line = ('#ffffff', '#172235', '#576778', '#e0e7ef') if light else ('#0d1117', '#edf3fc', '#9baec5', '#263447')
    blue, purple, teal = ('#315bd9', '#7545c7', '#087c83') if light else ('#83b5ff', '#c1a1ff', '#6eddd1')
    size = 39 if mobile else 67
    title_y = 88 if mobile else 99
    meta_y = 120 if mobile else 135
    right = w - 24
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">Aayaann Kausar — AI research and engineering</title>
<desc id="desc">IIT Kharagpur. Model research, AI applications, and systems engineering.</desc>
<style>
 .flow {{ stroke-dasharray: 36 344; animation: flow 9s linear infinite; }}
 @keyframes flow {{ to {{ stroke-dashoffset: -380; }} }}
 @media (prefers-reduced-motion: reduce) {{ .flow {{ animation: none; }} }}
</style>
<defs>
  <linearGradient id="name" x1="0" x2="1"><stop stop-color="{ink}"/><stop offset=".55" stop-color="{blue}"/><stop offset="1" stop-color="{purple}"/></linearGradient>
  <linearGradient id="spectrum"><stop stop-color="{blue}"/><stop offset=".48" stop-color="{purple}"/><stop offset="1" stop-color="{teal}"/></linearGradient>
</defs>
<rect width="{w}" height="{h}" fill="{bg}"/>
<g fill="none" stroke="{line}" stroke-width="1">
 <path d="M24 46V24H104 M{w-104} 24H{right}V46 M24 {h-36}V{h-18}H104 M{w-104} {h-18}H{right}V{h-36}"/>
 <path d="M24 35H{w*.27} M{w*.73} 35H{right}" stroke-dasharray="2 6"/>
</g>
<g font-family="'DejaVu Sans',Arial,sans-serif" text-anchor="middle">
 <text x="{w/2}" y="30" font-size="10" letter-spacing="2.8" fill="{muted}">IIT KHARAGPUR · INDIA</text>
 <text x="{w/2}" y="{title_y}" font-weight="700" font-size="{size}" letter-spacing="-1.7" fill="url(#name)">Aayaann Kausar</text>
 <text x="{w/2}" y="{meta_y}" font-size="{11 if mobile else 13}" letter-spacing="{1.5 if mobile else 2.8}" fill="{muted}">AI RESEARCH &amp; ENGINEERING</text>
</g>
<rect x="{w*.3}" y="{h-19}" width="{w*.4}" height="2" rx="1" fill="url(#spectrum)" opacity=".4"/>
<path class="flow" d="M{w*.3} {h-18}H{w*.7}" pathLength="380" stroke="url(#spectrum)" stroke-width="2" fill="none"/>
</svg>'''


for mobile in (False, True):
    for light in (False, True):
        name = f"masthead{'-mobile' if mobile else ''}{'-light' if light else ''}.svg"
        (OUT / name).write_text(render(mobile, light))
print('Built four responsive masthead variants.')
