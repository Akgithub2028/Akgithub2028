"""Build the profile's original gradient artwork and self-contained animations.

Requires Pillow and DejaVu fonts. Run: python3 scripts/build_visuals.py
All text layout uses measured font widths. No browser scripts or remote fonts.
"""

from html import escape
from math import sin, cos, pi
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
FONTS = Path('/usr/share/fonts/truetype/dejavu')
WHITE = '#f5f7ff'
MUTED = '#d0d8ec'


def font(size, bold=False, mono=False):
    name = 'DejaVuSansMono' if mono else 'DejaVuSans'
    return ImageFont.truetype(str(FONTS / (name + ('-Bold' if bold else '') + '.ttf')), size)


def rgb(color):
    return tuple(bytes.fromhex(color.lstrip('#')))


def blend(a, b, t):
    return tuple(round(x+(y-x)*t) for x,y in zip(a,b))


def backdrop(w, h, left, right, accent):
    im = Image.new('RGB', (w,h))
    d = ImageDraw.Draw(im)
    a,b = rgb(left),rgb(right)
    for x in range(w):
        d.line((x,0,x,h),fill=blend(a,b,x/w))
    glow = Image.new('RGBA',(w,h))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((w*.55,-h*.8,w*1.25,h*.8),fill=(*rgb(accent),35))
    glow = glow.filter(ImageFilter.GaussianBlur(h*.25))
    return Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB')


def gradient_text(im, xy, value, typeface, colors, phase=0):
    bbox = typeface.getbbox(value)
    width,height = int(typeface.getlength(value))+3,bbox[3]+3
    mask = Image.new('L',(width,height))
    ImageDraw.Draw(mask).text((0,0),value,font=typeface,fill=255)
    ink = Image.new('RGB',(width,height))
    d = ImageDraw.Draw(ink)
    a,b = map(rgb,colors)
    for x in range(width):
        t = .5+.5*sin(x/max(width,1)*pi+phase*2*pi)
        d.line((x,0,x,height),fill=blend(a,b,t))
    im.paste(ink,xy,mask)


def wrap(value, typeface, width):
    lines = []
    line = ''
    for word in value.split():
        candidate = f'{line} {word}'.strip()
        if typeface.getlength(candidate)>width and line:
            lines.append(line)
            line=word
        else:
            line=candidate
    if line:
        lines.append(line)
    return lines


def save_animation(stem, frames, duration=100, static_index=0):
    outside=Image.new('L',frames[0].size,255)
    ImageDraw.Draw(outside).rounded_rectangle((0,0,frames[0].width-1,frames[0].height-1),radius=18,fill=0)
    still=frames[static_index].convert('RGBA')
    still.putalpha(outside.point(lambda x:255-x))
    still.save(OUT/f'{stem}.png',optimize=True)
    # A shared palette avoids flicker. Include multiple phases in the palette.
    sample=Image.new('RGB',(frames[0].width,frames[0].height*3))
    for i,n in enumerate([0,len(frames)//3,2*len(frames)//3]):
        sample.paste(frames[n],(0,frames[0].height*i))
    palette=sample.quantize(colors=192,method=Image.Quantize.MEDIANCUT)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    for im in indexed:
        im.paste(255,(0,0),outside)
    indexed[0].save(OUT/f'{stem}.gif',save_all=True,append_images=indexed[1:],
                    duration=duration,loop=0,optimize=True,disposal=1,transparency=255,background=255)
    print(f'{stem}: {(OUT/f"{stem}.gif").stat().st_size//1024} KiB')


def hero(mobile=False):
    w,h=(600,450) if mobile else (1100,340)
    base=backdrop(w,h,'#17223e','#302146','#8f8cff')
    # Rich blue, violet and teal shading replaces the previous terminal/grid motif.
    glow=Image.new('RGBA',(w,h))
    gd=ImageDraw.Draw(glow)
    gd.ellipse((-w*.3,h*.6,w*.6,h*1.7),fill=(35,197,198,45))
    gd.ellipse((w*.6,-h,w*1.5,h*.4),fill=(227,136,213,40))
    base=Image.alpha_composite(base.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(90))).convert('RGB')
    d=ImageDraw.Draw(base)
    x=32 if mobile else 42
    d.rounded_rectangle((x,26,x+184,61),radius=17,fill='#41416d')
    d.text((x+16,33),'IIT KHARAGPUR',font=font(17,True),fill='#ece9ff')
    if not mobile:
        d.text((w-349,35),'RESEARCH  /  BUILD  /  OPTIMIZE',font=font(16),fill=MUTED)
    y_role=236 if mobile else 169
    y_type=286 if mobile else 220
    d.text((x,y_role),'AI Research & Engineering',font=font(28 if mobile else 30,True),fill=WHITE)
    tagline='Understanding models. Building useful systems.'
    for i,t in enumerate(wrap(tagline,font(22 if mobile else 21),w-x*2)):
        d.text((x,(357 if mobile else 283)+i*30),t,font=font(22 if mobile else 21),fill=MUTED)
    roles=[('Continual learning & model adaptation','#b6b0ff'),
           ('Speech AI & evidence-grounded agents','#ffbdac'),
           ('Software systems & cloud infrastructure','#94d4ff'),
           ('GPU programming: CUDA & Triton','#85e6ce')]
    frames=[]
    for n in range(100):
        im=base.copy()
        phase=n/100
        if mobile:
            gradient_text(im,(x,80),'Aayaann',font(60,True),('#ffffff','#b8ceff'),phase)
            gradient_text(im,(x,148),'Kausar',font(60,True),('#d8c5ff','#a4e4ef'),phase)
        else:
            gradient_text(im,(x,80),'Aayaann Kausar',font(68,True),('#ffffff','#bad0ff'),phase)
        d=ImageDraw.Draw(im)
        index=(n+18)//25%4
        step=(n+18)%25
        phrase,color=roles[index]
        count=min(len(phrase),max(1,round((step+1)/17*len(phrase))))
        typed=phrase[:count]
        face=font(22 if mobile else 25)
        d.text((x,y_type),typed,font=face,fill=color)
        if n%8<5:
            cursor=x+face.getlength(typed)+4
            d.line((cursor,y_type+5,cursor,y_type+face.size+5),fill=color,width=2)
        # A restrained animated colour rail, away from the readable content.
        for px in range(w):
            color=blend(rgb('#7899ff'),rgb('#e49bcf'),.5+.5*sin(px/w*pi*2-phase*pi*2))
            d.line((px,h-4,px,h),fill=color)
        frames.append(im)
    save_animation('hero-mobile' if mobile else 'hero',frames,150)


PROJECTS=[
 dict(slug='sfp',label='01  /  INDEPENDENT RESEARCH',title='Subspace Feature Preservation',
      mobile=['Subspace Feature','Preservation'],strap='Reducing forgetting through feature preservation',
      stack='PyTorch · PCA · Continual learning · Lean 4',
      primary=('0.933','drift prediction R²'),secondary=('0.699','harmonic score'),
      accent='#b8b0ff',second='#8bcaff',left='#211e3b',right='#182e43'),
 dict(slug='translator',label='02  /  SPEECH AI & REAL-TIME SYSTEMS',title='Real-Time Voice Translator',
      mobile=['Real-Time Voice','Translator'],strap='A streaming, bidirectional speech-to-speech pipeline',
      stack='Whisper · GPT-OSS 20B · ElevenLabs · FastAPI',
      primary=('7','languages, both directions'),secondary=('20 ms','audio frames'),
      accent='#ffc399',second='#f6a1c4',left='#382333',right='#30253f'),
 dict(slug='qlora',label='03  /  MODEL ADAPTATION & EVALUATION',title='Qwen2.5 · QLoRA Fine-Tuning',
      mobile=['Qwen2.5 · QLoRA','Fine-Tuning'],strap='Efficient fine-tuning with controlled evaluation',
      stack='4-bit NF4 · Rank-16 adapters · PEFT · TRL',
      primary=('+30.42%','relative ROUGE-L gain'),secondary=('161','held-out tasks'),
      accent='#8be8cb',second='#91cfff',left='#123735',right='#203347'),
 dict(slug='nexus',label='04  /  AGENTIC AI & ENTERPRISE SYSTEMS',title='NexusAgent',
      mobile=['NexusAgent'],strap='Hybrid retrieval and guarded tools for decision support',
      stack='LangGraph · Milvus · BGE · MCP · SQLGlot',
      primary=('96.25%','retrieval Hit@1'),secondary=('28/28','security cases'),
      accent='#a1cfff',second='#c5b0ff',left='#1b2e4c',right='#2e2948'),
 dict(slug='coscientist',label='05  /  AI FOR SCIENCE · PROJECT NOVA',title='Autonomous AI Co-Scientist',
      mobile=['Autonomous AI','Co-Scientist'],strap='A multi-agent workflow for scientific exploration',
      stack='LangGraph · Corrective RAG · Vector memory',
      primary=('Elo','hypothesis tournaments'),secondary=('CRAG','evidence retrieval'),
      accent='#f2b3df',second='#bdb3ff',left='#352541',right='#242d49'),
]


def project_card(p,mobile=False):
    w,h=(600,370) if mobile else (1100,236)
    x=28 if mobile else 32
    base=backdrop(w,h,p['left'],p['right'],p['accent'])
    d=ImageDraw.Draw(base)
    d.text((x,22),p['label'],font=font(16,True),fill=p['accent'])
    title_face=font(34,True)
    title_lines=p['mobile'] if mobile else [p['title']]
    for i,value in enumerate(title_lines):
        if title_face.getlength(value)> (544 if mobile else 708):
            raise ValueError(f'Title too wide: {value}')
    if mobile:
        metrics_y=188
        d.line((x,metrics_y-14,w-x,metrics_y-14),fill='#656781',width=1)
        d.text((x,metrics_y),p['primary'][0],font=font(43,True),fill=p['accent'])
        d.text((x,metrics_y+57),p['primary'][1],font=font(20),fill=MUTED)
        d.text((340,metrics_y+8),p['secondary'][0],font=font(31,True),fill=p['second'])
        # Secondary labels wrap instead of shrinking.
        for i,t in enumerate(wrap(p['secondary'][1],font(20),225)):
            d.text((340,metrics_y+57+i*25),t,font=font(20),fill=MUTED)
        for i,t in enumerate(wrap(p['stack'],font(21),w-2*x)):
            d.text((x,307+i*27),t,font=font(21),fill=WHITE)
    else:
        d.text((x,122),p['strap'],font=font(21),fill=MUTED)
        d.text((x,177),p['stack'],font=font(20),fill=WHITE)
        d.rounded_rectangle((761,56,1072,207),radius=15,fill='#111a2b')
        d.text((785,69),p['primary'][0],font=font(44,True),fill=p['accent'])
        d.text((785,126),p['primary'][1],font=font(19),fill=MUTED)
        detail=p['secondary'][0]+' · '+p['secondary'][1]
        d.text((785,174),detail,font=font(18),fill=p['second'])
    frames=[]
    for n in range(40):
        im=base.copy()
        phase=n/40
        for i,value in enumerate(title_lines):
            gradient_text(im,(x,60+i*43),value,title_face,('#ffffff',p['accent']),phase)
        d=ImageDraw.Draw(im)
        d.line((x,h-15,w-x,h-15),fill=p['left'],width=2)
        # A soft glint travels under the card, with all numerical results fixed.
        pos=x+phase*(w-2*x)
        for offset in range(-38,39):
            px=round(pos+offset)
            if x<=px<=w-x:
                c=blend(rgb(p['left']),rgb(p['accent']),(1-abs(offset)/39)*.8)
                d.line((px,h-15,px,h-14),fill=c)
        frames.append(im)
    stem=p['slug']+('-mobile' if mobile else '')
    save_animation(stem,frames,120)


def svg_text(x,y,value,size=22,color=WHITE,bold=False):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>'


def write_svg(name,w,h,content,title):
    (OUT/f'{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{content}</svg>\n')


def focus():
    groups=[('AI research',['Continual learning · QLoRA','PyTorch · Transformers · Lean 4'],'#b8b0ff','#26223d'),
            ('AI engineering',['Speech AI · RAG · LangGraph','FastAPI · Next.js · WebSockets'],'#ffc399','#332536'),
            ('Software & cloud',['AWS · GCP · Docker · Kubernetes','Terraform · CI/CD · Observability'],'#a1cfff','#1c3047'),
            ('GPU & AI infrastructure',['Exploring CUDA · Triton · C++','GPU kernels · LLM serving'],'#8be8cb','#193731')]
    for mobile in (False,True):
        w,h=(600,568) if mobile else (1100,288)
        s=''
        for i,(label,items,color,bg) in enumerate(groups):
            x=0 if mobile else (i%2)*560
            y=i*142 if mobile else (i//2)*144
            cw=600 if mobile else 540
            s+=f'<rect x="{x}" y="{y}" width="{cw}" height="130" rx="14" fill="{bg}"/>'
            s+=f'<rect x="{x+22}" y="{y+25}" width="4" height="77" rx="2" fill="{color}"/>'
            s+=svg_text(x+43,y+43,label,24,color,True)
            for j,t in enumerate(items):
                s+=svg_text(x+43,y+76+j*27,t,22,MUTED)
        write_svg('focus-mobile' if mobile else 'focus',w,h,s,'Research, AI engineering, software and cloud, GPU infrastructure')


def competition():
    for mobile in (False,True):
        w,h=(600,350) if mobile else (1100,218)
        s=f'<defs><linearGradient id="bg"><stop stop-color="#30324b"/><stop offset="1" stop-color="#3e2c3e"/></linearGradient></defs><rect width="{w}" height="{h}" rx="16" fill="url(#bg)"/>'
        s+=svg_text(28,36,'WUNDER FUND · FORECASTING CHALLENGE',16,'#ffd2a5',True)
        if mobile:
            s+=svg_text(28,87,'HFT Market State',30,WHITE,True)
            s+=svg_text(28,126,'Forecasting',30,WHITE,True)
            s+=svg_text(28,204,'9th',49,'#ffd2a5',True)
            s+=svg_text(146,201,'of 5,000+ competitors',22,MUTED)
            s+=svg_text(28,257,'0.3920',32,WHITE,True)
            s+=svg_text(205,254,'final R²',22,MUTED)
            s+=svg_text(28,310,'Transformer · torch.compile · Numba',21,MUTED)
        else:
            s+=svg_text(28,87,'HFT Market State Forecasting',34,WHITE,True)
            s+=svg_text(28,151,'9th',48,'#ffd2a5',True)
            s+=svg_text(139,147,'of 5,000+ competitors',24,MUTED)
            s+=svg_text(823,101,'0.3920',43,'#ffd2a5',True)
            s+=svg_text(823,138,'final R²',22,MUTED)
            s+=svg_text(28,192,'4-layer, 8-head Transformer · torch.compile · Numba · CPU inference',21,MUTED)
        write_svg('competition-mobile' if mobile else 'competition',w,h,s,'Wunder Fund — 9th of 5,000+ competitors')
    for mobile in (False,True):
        w,h=(600,124) if mobile else (1100,95)
        s=f'<defs><linearGradient id="f"><stop stop-color="#a4b9ff"/><stop offset=".5" stop-color="#ebbcdf"/><stop offset="1" stop-color="#8fe4d0"/></linearGradient></defs><rect width="{w}" height="{h}" rx="15" fill="#20263d"/>'
        if mobile:
            s+=svg_text(28,48,'Curious about models.',27,'url(#f)',True)
            s+=svg_text(28,89,'Serious about systems.',27,'url(#f)',True)
        else:
            s+=svg_text(32,58,'Curious about models. Serious about systems.',30,'url(#f)',True)
        write_svg('footer-mobile' if mobile else 'footer',w,h,s,'Curious about models. Serious about systems.')


if __name__=='__main__':
    hero()
    hero(mobile=True)
    for p in PROJECTS:
        project_card(p)
        project_card(p,mobile=True)
    focus()
    competition()
