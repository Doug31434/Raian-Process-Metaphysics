import math, random
random.seed(7)
W,H=800,940; NAVY='#18233F'; GOLD='#F0CF72'; ORANGE='#F28C28'
OX,OY=560,109
roots_c='#D9443B'; leaf_c='#4FB874'
d=['<defs>',
 '<linearGradient id="trunkG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5A3B1E"/><stop offset="0.45" stop-color="#8A6233"/><stop offset="1" stop-color="#3E2812"/></linearGradient>',
 '<radialGradient id="canopyG" cx="0.45" cy="0.4" r="0.6"><stop offset="0" stop-color="#3E8E5A" stop-opacity="0.5"/><stop offset="1" stop-color="#1F4A33" stop-opacity="0.22"/></radialGradient>',
 '<radialGradient id="creatorG" cx="0.5" cy="0.45" r="0.55"><stop offset="0" stop-color="#F0CF72" stop-opacity="0.16"/><stop offset="1" stop-color="#F0CF72" stop-opacity="0"/></radialGradient>',
 '<radialGradient id="growG"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/><stop offset="0.3" stop-color="#F6DA86" stop-opacity="0.85"/><stop offset="1" stop-color="#F0CF72" stop-opacity="0"/></radialGradient>']
for i,c in enumerate([roots_c,leaf_c]):
    d.append(f'<radialGradient id="o{i}"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/><stop offset="0.25" stop-color="{c}" stop-opacity="0.85"/><stop offset="0.6" stop-color="{c}" stop-opacity="0.3"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
for mid,mc in (('arr','#F28C28'),('arrB','#4A8CF0'),('arrG','#4FB874')):
    d.append(f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{mc}"/></marker>')
for oid,oc in (('oB','#F28C28'),('oF','#4A8CF0')):
    d.append(f'<radialGradient id="{oid}"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/><stop offset="0.3" stop-color="{oc}" stop-opacity="0.9"/><stop offset="0.65" stop-color="{oc}" stop-opacity="0.35"/><stop offset="1" stop-color="{oc}" stop-opacity="0"/></radialGradient>')
d.append('</defs>')
d.append('<ellipse cx="400" cy="430" rx="390" ry="420" fill="url(#creatorG)"/>')
d.append('<path d="M60 640 Q400 625 740 640" fill="none" stroke="#A97F22" stroke-width="2" stroke-opacity="0.5"/>')
roots=[]
for ang,ln in [(-160,300),(-140,250),(-115,200),(-90,150),(-65,200),(-40,250),(-20,300)]:
    a=math.radians(-ang)
    ex,ey=400+ln*math.cos(a)*1.1, 640+abs(ln*math.sin(a))*0.75+20
    mx,my=400+(ex-400)*0.45, 650+(ey-640)*0.2
    roots.append((mx,my,ex,ey))
    d.append(f'<path d="M400 640 Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}" fill="none" stroke="#6B4724" stroke-width="10" stroke-linecap="round" stroke-opacity="0.85"/>')
d.append('<ellipse cx="400" cy="230" rx="330" ry="210" fill="url(#canopyG)"/>')
br=[((400,360),(250,120)),((400,360),(560,200)),((400,330),(400,70)),((400,380),(170,250)),((400,380),(640,290)),((400,345),(310,170)),((400,345),(500,120))]
brc=[]
for (x0,y0),(x1,y1) in br:
    mx,my=(x0+x1)/2+(x1-x0)*0.1,(y0+y1)/2+30
    brc.append((x0,y0,mx,my,x1,y1))
    d.append(f'<path d="M{x0} {y0} Q{mx:.0f} {my:.0f} {x1} {y1}" fill="none" stroke="#5A3B1E" stroke-width="12" stroke-linecap="round" stroke-opacity="0.85"/>')
d.append('<path d="M355 645 C375 560 382 450 388 350 L412 350 C418 450 425 560 445 645 Z" fill="url(#trunkG)" fill-opacity="0.8"/>')
leafcols=['#5FC184','#3E9C62','#8FD6A4','#2F7A4B']
for k in range(85):
    t=random.random()*2*math.pi; rr=math.sqrt(random.random())
    x=400+330*rr*math.cos(t); y=230+200*rr*math.sin(t)
    rot=random.randint(0,180)
    d.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="13" ry="6" transform="rotate({rot} {x:.0f} {y:.0f})" fill="{random.choice(leafcols)}" fill-opacity="0.6"/>')
d.append('<path d="M250 120 Q240 95 252 72" fill="none" stroke="#9BD27A" stroke-width="4" stroke-linecap="round"/><ellipse cx="256" cy="70" rx="9" ry="5" transform="rotate(-40 256 70)" fill="#B9E89A"/>')
# --- Flow: x-ray blue lines through roots, trunk, branches, canopy veins ---
flow=[]
for mx,my,ex,ey in roots: flow.append(f'M{ex:.0f} {ey:.0f} Q{mx:.0f} {my:.0f} 400 640')
for dx in (-14,-5,5,14):
    flow.append(f'M{400+dx*1.6:.0f} 640 C{400+dx*1.2:.0f} 560 {400+dx*0.9:.0f} 450 {400+dx*0.6:.0f} 350')
for x0,y0,mx,my,x1,y1 in brc:
    flow.append(f'M{x0} {y0} Q{mx:.0f} {my:.0f} {x1} {y1}')
    for k in range(3):
        a=random.uniform(0,2*math.pi); L=random.uniform(30,60)
        flow.append(f'M{x1} {y1} Q{x1+L*0.5*math.cos(a+0.6):.0f} {y1+L*0.5*math.sin(a+0.6):.0f} {x1+L*math.cos(a):.0f} {y1+L*math.sin(a):.0f}')
for p in flow:
    d.append(f'<path d="{p}" fill="none" stroke="#3F7FD9" stroke-width="9" stroke-opacity="0.28" stroke-linecap="round"/>')
for p in flow:
    d.append(f'<path d="{p}" fill="none" stroke="#4A8CF0" stroke-width="3.2" stroke-opacity="1" stroke-dasharray="10 7" stroke-linecap="round"/>')
# --- Bark: golden highlight on the outer bark ---
for e in ('M355 645 C375 560 382 450 388 350','M445 645 C425 560 418 450 412 350'):
    d.append(f'<path d="{e}" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-opacity="0.3" stroke-linecap="round"/>')
    d.append(f'<path d="{e}" fill="none" stroke="{ORANGE}" stroke-width="3.5" stroke-linecap="round"/>')
d.append(f'<path d="M150 562 Q250 540 340 570" fill="none" stroke="{ORANGE}" stroke-width="3" marker-end="url(#arr)"/><circle cx="371" cy="575" r="26" fill="url(#oB)"/>')
# --- Growth: golden epicenter with concentric rings ---
gx,gy=400,405
N=13
for k in range(N):
    rx=30+(390-30)*k/(N-1); ry=rx*450/390
    op=0.9-0.7*k/(N-1)
    d.append(f'<ellipse cx="{gx}" cy="{gy}" rx="{rx:.0f}" ry="{ry:.0f}" fill="none" stroke="{GOLD}" stroke-width="{3.2-1.8*k/(N-1):.1f}" stroke-opacity="{op:.2f}"/>')
d.append(f'<circle cx="{gx}" cy="{gy}" r="40" fill="url(#growG)"/>')
d.append('<circle cx="400" cy="495" r="28" fill="url(#oF)"/>')
d.append('<path d="M650 485 Q550 463 432 493" fill="none" stroke="#4A8CF0" stroke-width="3" marker-end="url(#arrG_placeholder)"/>'.replace('arrG_placeholder','arrB'))
d.append('<path d="M742 150 Q680 160 612 196" fill="none" stroke="#4FB874" stroke-width="3" marker-end="url(#arrG)"/>')
# --- Roots and Leaf sources with angelic spirals ---
for i,(x,y,c) in enumerate([(400,745,roots_c),(575,210,leaf_c)]):
    d.append(f'<circle cx="{x}" cy="{y}" r="46" fill="url(#o{i})"/>')
    for s in range(5):
        base=2*math.pi*s/5+i*2
        ox,oy=x+42*math.cos(base),y+42*math.sin(base)
        pts=[f'{ox+(1+13*k/25)*math.cos(base+2.4*math.pi*k/25):.1f} {oy+(1+13*k/25)*math.sin(base+2.4*math.pi*k/25):.1f}' for k in range(26)]
        d.append(f'<path d="M{" L".join(pts)}" fill="none" stroke="{c}" stroke-width="2" stroke-opacity="0.85" stroke-linecap="round"/>')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" aria-label="A tree standing for the Creator, seen as if by x-ray: blue flow lines run through roots, trunk and branches; the outer bark is lit gold; a golden epicenter sends concentric rings outward for Growth; glowing sources with angelic spirals sit at the roots and in the leaves." width="{W}" height="{H}" viewBox="0 -45 {W} {H}">'+''.join(d)+'</svg>'
F="font-family:'Cormorant Garamond', Georgia, serif;font-size:40px;font-weight:600"
def lab(x,y,w,txt,c,align='left'):
    return f'<p style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{align};{F};color:{c}">{txt}</p>'
labels=(lab(1030,830,260,'Roots',roots_c)
 +lab(OX+750,OY+150-34,200,'Leaf',leaf_c)
 +lab(OX+gx+48,OY+gy-30,200,'Growth',GOLD)
 +lab(OX+10,OY+562-30,130,'Bark',ORANGE,'right')
 +lab(OX+660,OY+485-30,200,'Flow','#4A8CF0'))
note=("Here's the Tree again, drawn the way the sphere was drawn. The whole tree is the Creator, and each archangel is one of its functions. "
 "Look at it as if by x-ray. The blue lines are Flow, its source glowing at the heart of the trunk, moving through the roots, up the trunk, and out through every branch into the leaves. "
 "The outer bark, lit in orange, is Bark, holding and protecting, with its source on the bark itself. At the center, Growth sends golden rings outward, the tree widening year by year. "
 "Roots and Leaf glow as sources, and the small spirals around them are their angelics, carrying that function into a particular root or leaf. "
 "None of them ever left the tree. What one leaf knows, the tree knows.")
sec=(f'<section id="treeimg" data-transition="fade" style="background:{NAVY};color:#F5EFE2;font-family:\'Source Sans 3\', Arial, sans-serif;padding:0">'
 f'<div style="position:absolute;left:{OX}px;top:64px;width:{W}px;height:{H}px">{svg}</div>'
 f'<p style="position:absolute;left:128px;top:64px;width:700px;font-family:\'Cormorant Garamond\', Georgia, serif;font-size:72px;font-weight:600;line-height:1.1;color:#F5EFE2">The Creator as a Tree</p>'
 f'<p style="position:absolute;left:128px;top:160px;width:400px;font-size:30px;line-height:1.35;color:#C9CFDB">Each archangel is a function of the Tree.</p>'
 f'<p style="position:absolute;left:128px;top:860px;width:400px;font-size:28px;font-style:italic;color:#F0CF72">Spirals = Angelics</p>'
 f'{labels}<aside>{note}</aside></section>')
open('slides/treeimg.html','w',encoding='utf-8').write(sec)
print(len(svg.encode()))
