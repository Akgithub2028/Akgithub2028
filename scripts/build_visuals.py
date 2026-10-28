"""Build original profile artwork: python3 scripts/build_visuals.py.

Requires Pillow and system DejaVu fonts. All generated files are committed, so
GitHub needs no font downloads, scripts, external renderers or image services.
"""

from html import escape
from math import cos, sin, pi
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
BG, PANEL, WHITE = "#080c16", "#0d1422", "#edf4ff"
MUTED, LINE = "#a0b2ca", "#27364d"
CYAN, PINK, LIME = "#67e8f9", "#df79ff", "#cdff87"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def svg(w, h, content, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>'
            f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>{content}</svg>\n')


def text(x, y, value, size=16, color=WHITE, weight=400, mono=False, extra=""):
    family = "DejaVu Sans Mono,monospace" if mono else "DejaVu Sans,Arial,sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>')


def line(x1, y1, x2, y2, color=LINE, width=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def rect(x, y, w, h, fill=PANEL, stroke=LINE, rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'


def write(name, w, h, content, title):
    (OUT / f"{name}.svg").write_text(svg(w, h, content, title))


def icon(kind, x, y, c):
    """Illustrative geometry, never simulated benchmark plots."""
    s = ""
    if kind == "sfp":
        for a in range(3):
            for b in range(3):
                px, py = x + 34 * a + 17 * b, y - 14 * a + 24 * b
                s += rect(px, py, 16, 16, BG, c, 1)
        s += line(x - 8, y + 94, x + 150, y + 26, PINK, 2)
        s += text(x + 2, y + 119, "SUBSPACE / r=32", 11, MUTED, mono=True)
    elif kind == "translator":
        for i in range(27):
            h = 8 + abs(sin(i * .77) * cos(i * .21)) * 72
            s += line(x + i * 6, y + 45 - h/2, x + i * 6, y + 45 + h/2, c, 3)
        s += text(x, y + 106, "AUDIO → TEXT → AUDIO", 11, MUTED, mono=True)
    elif kind == "qlora":
        for i in range(7):
            for j in range(5):
                active = i in (2, 3)
                s += rect(x + i * 21, y + j * 17, 14, 10,
                          c if active else PANEL, c if active else LINE, 1)
        s += text(x, y + 107, "W + ΔW / NF4", 11, MUTED, mono=True)
    else:
        pts = [(x+10,y+45),(x+75,y),(x+75,y+45),(x+75,y+90),(x+145,y+45)]
        for a,b in [(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)]:
            s += line(*pts[a],*pts[b],LINE,2)
        for i,(px,py) in enumerate(pts):
            s += rect(px-9,py-9,18,18,BG,c if i in (0,4) else PINK,4)
        label = "RESEARCH LOOP" if kind == "coscientist" else "RETRIEVE → VERIFY"
        s += text(x-5,y+122,label,11,MUTED,mono=True)
    return s


PROJECTS = [
    dict(slug="sfp", num="01", label="INDEPENDENT RESEARCH", color=CYAN,
         title="Subspace Feature Preservation", mobile=["Subspace Feature", "Preservation"],
         desc="Preserve critical features. Reduce catastrophic forgetting.",
         stack="PYTORCH / PCA / CONTINUAL LEARNING / LEAN 4",
         metrics=[("0.933", "PCA drift R²"), ("0.699", "harmonic score")],
         note="Qwen2.5-1.5B · rank 32 · conditional bound · scale-dependent findings"),
    dict(slug="translator", num="02", label="SPEECH AI / REAL-TIME SYSTEMS", color=PINK,
         title="Real-Time Voice Translator", mobile=["Real-Time Voice", "Translator"],
         desc="Speak. Translate. Hear. A bidirectional speech pipeline.",
         stack="WHISPER / GPT-OSS 20B / ELEVENLABS / NEXT.JS / FASTAPI",
         metrics=[("7", "languages"), ("20 ms", "audio frames")],
         note="WebSockets · AudioWorklet · p50/p95 telemetry · 27 backend tests"),
    dict(slug="qlora", num="03", label="POST-TRAINING / CONTROLLED EVALUATION", color=LIME,
         title="Qwen2.5 · QLoRA Fine-Tuning", mobile=["Qwen2.5 · QLoRA", "Fine-Tuning"],
         desc="Small-model adaptation, measured beyond the average.",
         stack="QWEN2.5-1.5B / 4-BIT NF4 / RANK-16 / PEFT / TRL",
         metrics=[("+30.42%", "relative ROUGE-L"), ("161", "held-out tasks")],
         note="1,286 training examples · 48 topics · 14.2% of held-out tasks regressed"),
    dict(slug="nexus", num="04", label="AGENTIC AI / ENTERPRISE SYSTEMS", color=CYAN,
         title="NexusAgent", mobile=["NexusAgent"],
         desc="Evidence-grounded decisions. Guarded tools. Hybrid retrieval.",
         stack="LANGGRAPH / MILVUS / BM25 / BGE / MCP / SQLGLOT",
         metrics=[("96.25%", "retrieval Hit@1"), ("28/28", "security cases")],
         note="160 answerable synthetic queries · 1,941 unit + 323 offline integration tests"),
    dict(slug="coscientist", num="05", label="AI FOR SCIENCE / PROJECT NOVA", color=PINK,
         title="Autonomous AI Co-Scientist", mobile=["Autonomous AI", "Co-Scientist"],
         desc="From literature to hypotheses, critique and iterative refinement.",
         stack="LANGGRAPH / CORRECTIVE RAG / VECTOR MEMORY / DOCKER",
         metrics=[("Elo", "hypothesis ranking"), ("CRAG", "evidence retrieval")],
         note="Literature → generate → reflect → rank → evolve → research report"),
]


def projects():
    for p in PROJECTS:
        c = p["color"]
        s = line(1, 18, 1, 252, c, 3)
        s += text(32, 37, f'{p["num"]} / {p["label"]}', 14, c, mono=True)
        s += text(1165, 39, "↗", 25, c, extra='text-anchor="end"')
        s += text(32, 88, p["title"], 31, WHITE, 700)
        s += text(32, 124, p["desc"], 18, MUTED)
        s += text(32, 165, p["stack"], 15, c, mono=True)
        s += line(32, 194, 1168, 194)
        s += text(32, 233, p["note"], 15, MUTED)
        s += line(718, 60, 718, 169)
        for i,(value,label) in enumerate(p["metrics"]):
            px = 753+i*225
            s += text(px, 104, value, 34, c, 700)
            s += text(px, 139, label, 16, MUTED)
        write(p["slug"],1200,260,s,p["title"])
        s = line(1, 20, 1, 445, c, 3)
        s += text(27, 38, f'{p["num"]} / {p["label"]}', 12, c, mono=True)
        for i,t in enumerate(p["mobile"]):
            s += text(27,91+i*39,t,30,WHITE,700)
        s += icon(p["slug"],393,54,c)
        for i,(value,label) in enumerate(p["metrics"]):
            px = 27+i*290
            s += text(px,222,value,39,c,700)
            s += text(px,253,label,17,MUTED)
        s += line(27,280,573,280)
        for i,t in enumerate(textwrap.wrap(p["stack"],53)):
            s += text(27,313+i*22,t,13,c,mono=True)
        for i,t in enumerate(textwrap.wrap(p["note"],59)):
            s += text(27,379+i*24,t,16,MUTED)
        s += text(572,441,"EXPLORE ↗",12,c,mono=True,extra='text-anchor="end"')
        write(p["slug"]+"-mobile",600,464,s,p["title"])


def focus():
    groups=[("01 / MODEL RESEARCH", ["Continual learning · QLoRA", "PyTorch · Transformers · Lean 4"],CYAN),
            ("02 / AI ENGINEERING", ["Speech AI · RAG · LangGraph", "FastAPI · Next.js · WebSockets"],PINK),
            ("03 / SOFTWARE & CLOUD", ["AWS · GCP · Docker · Kubernetes", "Terraform · CI/CD · Observability"],CYAN),
            ("04 / DEEPENING", ["CUDA · Triton · C++", "GPU kernels · LLM serving"],LIME)]
    for mobile in (False,True):
        w,h = (600,335) if mobile else (1200,142)
        s = ""
        for i,(label,items,c) in enumerate(groups):
            x = 27+(i%2)*290 if mobile else 28+i*297
            y = 38+(i//2)*156 if mobile else 37
            s += line(x,y-14,x+20,y-14,c,2)
            s += text(x,y+10,label,13,c,mono=True)
            for j,v in enumerate(items):
                s += text(x,y+43+j*25,v,16,MUTED)
        write("focus-mobile" if mobile else "focus",w,h,s,"Research, AI engineering, software and cloud; deepening GPU systems")


def competition():
    for mobile in (False,True):
        w,h = (600,325) if mobile else (1200,202)
        s = line(1,18,1,h-18,LIME,3)
        s += text(28,37,"WUNDER FUND / FORECASTING CHALLENGE / 2025",12,LIME,mono=True)
        s += text(28,85,"HFT Market State Forecasting",26 if mobile else 30,WHITE,700)
        s += text(28,135,"9th",44,LIME,700)
        s += text(135,133,"/ 5,000+ competitors",19,MUTED)
        if mobile:
            s += line(28,163,572,163)
            s += text(28,204,"0.3920",29,WHITE,700)
            s += text(204,203,"final R²",15,MUTED)
            s += text(28,247,"4-layer / 8-head Transformer",17,MUTED)
            s += text(28,280,"torch.compile · Numba · CPU inference",14,LIME)
        else:
            s += line(750,67,750,142)
            s += text(787,101,"0.3920",34,LIME,700)
            s += text(787,132,"final R²",14,MUTED)
            s += text(28,177,"4-layer / 8-head Transformer · torch.compile · Numba · optimized CPU inference",14,MUTED)
        write("competition-mobile" if mobile else "competition",w,h,s,"Wunder Fund forecasting challenge — 9th of 5,000+")
    s = line(28,19,1172,19)
    s += text(28,59,"RESEARCH THE MODEL. ENGINEER THE SYSTEM.",20,WHITE,700)
    s += text(1172,59,"AK / 28",13,CYAN,mono=True,extra='text-anchor="end"')
    write("footer",1200,85,s,"Research the model. Engineer the system.")
    s = line(28,14,572,14)
    s += text(28,50,"RESEARCH THE MODEL.",24,WHITE,700)
    s += text(28,85,"ENGINEER THE SYSTEM.",24,WHITE,700)
    s += text(572,85,"AK/28",12,CYAN,mono=True,extra='text-anchor="end"')
    write("footer-mobile",600,111,s,"Research the model. Engineer the system.")


def font(size, bold=False, mono=False):
    name = "DejaVuSansMono" if mono else "DejaVuSans"
    return ImageFont.truetype(str(FONT_DIR / (name+("-Bold" if bold else "")+".ttf")),size)


def mesh(d,cx,cy,r,t):
    def project(lat,lon):
        a = lon+t*2*pi
        x,y,z = cos(lat)*cos(a),sin(lat),cos(lat)*sin(a)
        yy,zz = y*cos(.32)-z*sin(.32),y*sin(.32)+z*cos(.32)
        scale = 1+.12*zz
        return cx+r*x*scale,cy+r*yy*scale,zz
    for j in range(1,12):
        lat = -pi/2+j*pi/12
        pts = [project(lat,k*2*pi/64) for k in range(65)]
        for a,b in zip(pts,pts[1:]):
            c = (30,77,96) if (a[2]+b[2])/2<0 else (58,144,163)
            d.line([a[:2],b[:2]],fill=c,width=1)
    for k in range(18):
        pts = [project(-pi/2+j*pi/48,k*2*pi/18) for j in range(49)]
        for a,b in zip(pts,pts[1:]):
            c = (28,65,88) if (a[2]+b[2])/2<0 else (83,181,198)
            d.line([a[:2],b[:2]],fill=c,width=1)
        for j in range(3,12,3):
            x,y,z = project(-pi/2+j*pi/12,k*2*pi/18)
            if z>0:
                d.ellipse((x-2,y-2,x+2,y+2),fill=CYAN)
    d.ellipse((cx-r-18,cy-r-18,cx+r+18,cy+r+18),outline=(34,47,73),width=1)
    angle = t*360
    d.arc((cx-r-18,cy-r-18,cx+r+18,cy+r+18),angle,angle+64,fill=PINK,width=3)
    d.arc((cx-r-27,cy-r-27,cx+r+27,cy+r+27),-angle+180,-angle+210,fill=LIME,width=2)


def hero(mobile=False):
    w,h = (600,650) if mobile else (1200,410)
    base = Image.new("RGB",(w,h),BG)
    d = ImageDraw.Draw(base)
    for x in range(24,w,24):
        for y in range(18,h,24):
            d.point((x,y),fill=(29,40,58))
    floor = 535 if mobile else 288
    for x in range(-w,w*2,100):
        d.line((w*.78,floor,x,h),fill=(17,36,51))
    for i in range(6):
        y = floor+(h-floor)*(i/5)**2
        d.line((0,y,w,y),fill=(17,36,51))
    d.line((28,65,w-28,65),fill=LINE)
    d.rectangle((28,27,89,48),fill=CYAN)
    d.text((34,29),"AK/28",font=font(14,True,True),fill=BG)
    d.text((106,30),"RESEARCH TERMINAL",font=font(12,mono=True),fill=MUTED)
    d.text((w-43,29),"+",font=font(18),fill=PINK)
    left = 28 if mobile else 43
    d.text((left,88),"AI RESEARCH / ENGINEERING",font=font(15,mono=True),fill=CYAN)
    d.text((left,118),"AAYAANN",font=font(64 if mobile else 72,True),fill=WHITE)
    d.text((left,188 if mobile else 196),"KAUSAR",font=font(64 if mobile else 72,True),fill=WHITE)
    d.text((left,276 if mobile else 294),"MODELS. SYSTEMS. METAL.",font=font(18,True,True),fill=LIME)
    foot = h-49
    d.line((28,foot-15,w-28,foot-15),fill=LINE)
    d.text((left,foot),"IIT KHARAGPUR / INDIA",font=font(12,mono=True),fill=MUTED)
    if not mobile:
        d.text((w-307,foot),"CUDA / TRITON / CLOUD",font=font(12,mono=True),fill=CYAN)
    frames = []
    for n in range(60):
        im = base.copy()
        d = ImageDraw.Draw(im)
        t = n/60
        cx,cy,r = (410,453,99) if mobile else (961,203,110)
        mesh(d,cx,cy,r,t)
        for i in range(3):
            yy = cy-73+i*75
            d.line((cx-r-47,yy,cx-r-24,yy,cx-r-24,yy+20),fill=(58,76,102),width=1)
        scan = int(t*r*2)
        d.line((cx-r-9,cy-r+scan,cx+r+9,cy-r+scan),fill=(43,80,98),width=1)
        if mobile:
            for i,(label,c) in enumerate(zip(["RESEARCH","TRAIN","SHIP","OPTIMIZE"],[CYAN,PINK,CYAN,LIME])):
                d.text((28,399+i*29),label,font=font(13,mono=True),fill=c)
        else:
            d.text((780,44),"NEURAL FIELD / GENERATIVE GEOMETRY",font=font(11,mono=True),fill=MUTED)
        frames.append(im)
    stem = "hero-mobile" if mobile else "hero"
    frames[0].save(OUT/f"{stem}.png",optimize=True)
    palette = frames[0].quantize(colors=96,method=Image.Quantize.MEDIANCUT)
    indexed = [f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT/f"{stem}.gif",save_all=True,append_images=indexed[1:],duration=100,loop=0,optimize=True,disposal=1)
    print(f"Built {stem}.gif ({(OUT/f'{stem}.gif').stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    projects()
    focus()
    competition()
    hero()
    hero(mobile=True)
