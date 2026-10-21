# Tegner studentlandsbyen til toppfeltet som isometrisk «arbeidstegning», i samme strek som mikrohus-3d.svg.
# Kjør fra prosjektside/:  python -I verktoy/lag-studentlandsby.py <forslag 1-6> <ut.svg>
#
# Hovedmotivet er GMT Mikrohus (lang hoveddel 7,5 × 3,8 m + høyere tilbygg). Alt skal følge fysikken:
# ingenting svever, laster henger loddrett under løpekatten, kranen har fundament, mast, utligger,
# kontrautligger med motvekt og strekkstag, og en benk har fire bein.
#
# Forslagene:  1 Gaterekke   2 Tun   3 Byggeplass   4 Eksplodert mikrohus   5 Terreng ved Mjøsa   6 Plan og 3D
import math, sys

S, OX, OY, ZOFF = 10.0, 330.0, 60.0, 0.0
C30 = math.cos(math.radians(30))
W, H = 660, 430

STREK = '#9fbcf0'
TRE = '#e9b36f'
KALD, VARM, EL = '#62c8ff', '#ff8a73', '#ffd34d'
ORANSJE = '#f29228'
STAAL = '#d2dcf0'
TOPP, FRONT, SIDE = 'rgba(130,170,240,.62)', 'rgba(42,82,154,.62)', 'rgba(28,55,110,.78)'
BAKTAK = 'rgba(130,170,240,.42)'

def iso(x, y, z=0.0):
    z += ZOFF
    return (OX + (x - y) * C30 * S, OY + (x + y) * 0.5 * S - z * S)

def pts(*p):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in (iso(*q) for q in p))

ut = []
def poly(*p, fill='none', stroke=STREK, sw=1.4, extra=''):
    ut.append(f'<polygon points="{pts(*p)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
def line(a, b, stroke=STREK, sw=1.4, extra=''):
    (x1, y1), (x2, y2) = iso(*a), iso(*b)
    ut.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" {extra}/>')
def path(*p, stroke=STREK, sw=1.4, extra='', lukk=False):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in (iso(*q) for q in p)) + (' Z' if lukk else '')
    ut.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def tekst(x, y, z, t, size=9, fill=STREK, anchor='middle', dy=0, dx=0):
    a, b = iso(x, y, z)
    ut.append(f'<text x="{a + dx:.1f}" y="{b + dy:.1f}" font-family="JetBrains Mono, Consolas, monospace" font-size="{size}" font-weight="600" fill="{fill}" text-anchor="{anchor}">{t}</text>')
def sirkel(x, y, z, r, fill, stroke='none', sw=1):
    a, b = iso(x, y, z)
    ut.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def boks(x, y, z, w, d, h, fill=(TOPP, FRONT, SIDE), stroke=STREK, sw=1.2):
    """Rett boks som står på z. Tegner topp, front (y+d) og høyre side (x+w)."""
    topp, front, side = fill
    poly((x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h), fill=front, stroke=stroke, sw=sw)
    poly((x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h), fill=side, stroke=stroke, sw=sw)
    poly((x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h), fill=topp, stroke=stroke, sw=sw)
def skygge(x, y, w, d, ox=1.1):
    poly((x + ox, y + ox), (x + w + ox, y + ox), (x + w + ox, y + d + ox), (x + ox, y + d + ox), fill='rgba(0,0,0,.28)', stroke='none')

# ---------- Hustypene ----------
# Alle følger TEK17 § 1-2 niende ledd (mikrohus, fra 1.7.2023): inntil 30 m² BRA, én boenhet, én etasje
# uten kjeller, og ikke høyere enn 4,5 m over bakken. Utvendige mål under; BRA er målt innenfor ytterveggene.
#   A  GMT Mikrohus   7,5 × 3,8 m, saltak + høyere tilbygg       BRA ≈ 23 m², møne 4,4 m
#   B  Pulttak        8,0 × 4,2 m, skråtak mot sør                BRA ≈ 28 m², høyeste punkt 3,6 m
#   C  Kvadrat        5,6 × 5,6 m, bratt saltak, hems under mønet  BRA ≈ 26 m², møne 4,4 m
#   D  Flatt tak      7,0 × 4,4 m, takterrasse med rekkverk        BRA ≈ 25 m², rekkverk 3,4 m
HW, HD, HH, HR = 7.5, 3.8, 2.6, 1.2      # A: hoveddel bredde, dybde, vegghøyde, takhøyde (møne langs x)
TW, TH, TR = 3.2, 3.1, 1.3               # A: tilbygg i høyre ende (møne langs y), topp 4,4 m

def saltak_boks(x, y, w, d, h, r, langs_x=True, fill=(TOPP, FRONT, SIDE), sw=1.4, stroke=STREK, baktak=BAKTAK):
    topp, front, side = fill
    if langs_x:
        poly((x, y, h), (x + w, y, h), (x + w, y + d / 2, h + r), (x, y + d / 2, h + r), fill=baktak, sw=sw, stroke=stroke)
        poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, h), (x, y + d, h), fill=front, sw=sw, stroke=stroke)
        poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, h), (x + w, y, h), fill=side, sw=sw, stroke=stroke)
        poly((x + w, y, h), (x + w, y + d, h), (x + w, y + d / 2, h + r), fill=side, sw=sw, stroke=stroke)
        poly((x, y + d / 2, h + r), (x + w, y + d / 2, h + r), (x + w, y + d, h), (x, y + d, h), fill=topp, sw=sw, stroke=stroke)
    else:
        poly((x, y, h), (x + w / 2, y, h + r), (x + w / 2, y + d, h + r), (x, y + d, h), fill=baktak, sw=sw, stroke=stroke)
        poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, h), (x, y + d, h), fill=front, sw=sw, stroke=stroke)
        poly((x, y + d, h), (x + w, y + d, h), (x + w / 2, y + d, h + r), fill=front, sw=sw, stroke=stroke)
        poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, h), (x + w, y, h), fill=side, sw=sw, stroke=stroke)
        poly((x + w / 2, y, h + r), (x + w / 2, y + d, h + r), (x + w, y + d, h), (x + w, y, h), fill=topp, sw=sw, stroke=stroke)

def vindu(x, y, z, b=1.2, hh=1.3):
    poly((x, y, z), (x + b, y, z), (x + b, y, z + hh), (x, y, z + hh), fill='rgba(13,24,48,.65)', sw=1)
    line((x + b / 2, y, z), (x + b / 2, y, z + hh), sw=.7); line((x, y, z + hh / 2), (x + b, y, z + hh / 2), sw=.7)

def mikrohus(x, y, solceller=False, varmepumpe=False, dor=True):
    skygge(x, y, HW, HD)
    saltak_boks(x, y, HW - TW, HD, HH, HR, True)
    tx = x + HW - TW
    saltak_boks(tx, y, TW, HD, TH, TR, False)
    vindu(x + .8, y + HD, .9); vindu(x + 2.6, y + HD, .9)
    if dor:
        dx = x + HW - TW - 1.5
        poly((dx, y + HD, 0), (dx + .95, y + HD, 0), (dx + .95, y + HD, 2.1), (dx, y + HD, 2.1), fill=ORANSJE, stroke='none')
    vindu(tx + 1.0, y + HD, 1.0, b=1.2, hh=1.2); vindu(tx + 1.0, y + HD, 2.6, b=1.2, hh=.9)
    if solceller:
        for i in range(3):
            px = x + .6 + i * 1.35
            z0, z1 = HH + HR * .5 / (HD / 2), HH + HR * 1.6 / (HD / 2)
            poly((px, y + HD - .5, z0), (px + 1.1, y + HD - .5, z0), (px + 1.1, y + HD - 1.6, z1), (px, y + HD - 1.6, z1),
                 fill='rgba(13,24,48,.7)', stroke='#62c8ff', sw=.9)
    if varmepumpe:   # utedel på bakken inntil høyre gavl, på en liten sokkel
        gx = x + HW + .15
        boks(gx, y + 2.0, 0, .55, 1.2, .25, fill=('rgba(120,130,150,.5)',) * 3, sw=.8)
        boks(gx, y + 2.0, .25, .55, 1.2, .85, fill=('rgba(214,222,236,.55)', 'rgba(200,215,240,.5)', 'rgba(160,175,200,.6)'), sw=1)
        sirkel(gx + .56, y + 2.6, .68, 2.6, 'none', STAAL, 1)

def spokelse(x, y):
    """Neste hus: bare stiplet omriss."""
    kw = dict(sw=1.1, extra='stroke-dasharray="4 4" opacity=".75"')
    w = HW - TW
    path((x, y + HD, 0), (x + w, y + HD, 0), (x + w, y + HD, HH), (x, y + HD, HH), lukk=True, **kw)
    path((x, y + HD, HH), (x, y + HD / 2, HH + HR), (x + w, y + HD / 2, HH + HR), (x + w, y + HD, HH), **kw)
    path((x, y, 0), (x, y, HH), (x, y + HD / 2, HH + HR), **kw); line((x, y, 0), (x, y + HD, 0), **kw)
    tx = x + w
    path((tx, y + HD, 0), (tx + TW, y + HD, 0), (tx + TW, y + HD, TH), (tx + TW / 2, y + HD, TH + TR), (tx, y + HD, TH), (tx, y + HD, HH), **kw)
    path((tx + TW, y + HD, 0), (tx + TW, y, 0), (tx + TW, y, TH), (tx + TW / 2, y, TH + TR), (tx + TW / 2, y + HD, TH + TR), **kw)
    line((tx + TW, y, TH), (tx + TW, y + HD, TH), **kw); line((tx + TW, y, 0), (tx, y, 0), **kw)

def hus_b(x, y, solceller=False):
    """B: pulttak. Høy bakvegg (3,6 m) og lav front (2,4 m), vindusbånd mot sør."""
    w, d, hb, hf = 8.0, 4.2, 3.6, 2.4
    skygge(x, y, w, d)
    poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, hf), (x, y + d, hf), fill=FRONT)
    poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, hf), (x + w, y, hb), fill=SIDE)
    poly((x, y, hb), (x + w, y, hb), (x + w, y + d, hf), (x, y + d, hf), fill=TOPP)
    line((x, y, hb), (x + w, y, hb), sw=2.2)   # takutstikk bak
    for i in range(4):
        vindu(x + .5 + i * 1.5, y + d, .8, b=1.1, hh=1.2)
    poly((x + 6.6, y + d, 0), (x + 7.5, y + d, 0), (x + 7.5, y + d, 2.1), (x + 6.6, y + d, 2.1), fill=ORANSJE, stroke='none')
    poly((x + w, y + 1.4, 1.0), (x + w, y + 2.8, 1.0), (x + w, y + 2.8, 2.2), (x + w, y + 1.4, 2.2), fill='rgba(13,24,48,.65)', sw=1)
    if solceller:
        for i in range(4):
            px = x + .5 + i * 1.8
            z0 = hf + (hb - hf) * .55; z1 = hf + (hb - hf) * .85
            poly((px, y + d * .45, z0), (px + 1.5, y + d * .45, z0), (px + 1.5, y + d * .15, z1), (px, y + d * .15, z1), fill='rgba(13,24,48,.7)', stroke='#62c8ff', sw=.9)

def hus_c(x, y):
    """C: kvadratisk hus 5,6 × 5,6 m med bratt saltak og hems under mønet. Rundt vindu i gavlen."""
    w, d, h, r = 5.6, 5.6, 2.5, 1.9
    skygge(x, y, w, d)
    saltak_boks(x, y, w, d, h, r, True)
    vindu(x + .6, y + d, .9, b=1.3, hh=1.3); vindu(x + 3.7, y + d, .9, b=1.3, hh=1.3)
    poly((x + 2.3, y + d, 0), (x + 3.25, y + d, 0), (x + 3.25, y + d, 2.1), (x + 2.3, y + d, 2.1), fill=ORANSJE, stroke='none')
    poly((x + w, y + 1.2, 1.0), (x + w, y + 2.4, 1.0), (x + w, y + 2.4, 2.2), (x + w, y + 1.2, 2.2), fill='rgba(13,24,48,.65)', sw=1)
    sirkel(x + w, y + d / 2, h + r * .55, 4.2, 'rgba(13,24,48,.65)', STREK, 1)   # hemsvindu i gavlen
    for i in range(2):   # takvinduer til hemsen
        z0, z1 = h + r * .9 / (d / 2), h + r * 1.7 / (d / 2)
        poly((x + 1.2 + i * 2.4, y + d - .9, z0), (x + 2.0 + i * 2.4, y + d - .9, z0), (x + 2.0 + i * 2.4, y + d - 1.7, z1), (x + 1.2 + i * 2.4, y + d - 1.7, z1), fill='rgba(13,24,48,.6)', stroke='#8fb0ea', sw=.9)

def hus_d(x, y, solceller=True):
    """D: flatt tak med takterrasse og rekkverk, 7,0 × 4,4 m, 3,0 m vegg. Lange vindusbånd."""
    w, d, h = 7.0, 4.4, 3.0
    skygge(x, y, w, d)
    boks(x, y, 0, w, d, h, fill=(TOPP, FRONT, SIDE))
    for i in range(5):   # rekkverk langs fronten og høyre side
        line((x + w * i / 4, y + d, h), (x + w * i / 4, y + d, h + .4), stroke=STAAL, sw=1)
        line((x + w, y + d * i / 4, h), (x + w, y + d * i / 4, h + .4), stroke=STAAL, sw=1)
    path((x, y + d, h + .4), (x + w, y + d, h + .4), (x + w, y, h + .4), stroke=STAAL, sw=1.2)
    for i in range(3):
        vindu(x + .5 + i * 1.7, y + d, .9, b=1.4, hh=1.3)
    poly((x + 5.8, y + d, 0), (x + 6.7, y + d, 0), (x + 6.7, y + d, 2.1), (x + 5.8, y + d, 2.1), fill=ORANSJE, stroke='none')
    poly((x + w, y + .6, .9), (x + w, y + 2.6, .9), (x + w, y + 2.6, 2.2), (x + w, y + .6, 2.2), fill='rgba(13,24,48,.65)', sw=1)
    for bx in (x + 2.6, x + 4.4):   # benk på terrassen: fire bein
        for by in (y + 1.3, y + 1.7):
            line((bx, by, h), (bx, by, h + .45), stroke=TRE, sw=1.2)
    boks(x + 2.5, y + 1.25, h + .45, 2.0, .5, .08, fill=(TRE, '#c98d5b', '#c98d5b'), stroke='#f3cf98', sw=.6)
    if solceller:
        for i in range(2):
            poly((x + .4 + i * 1.6, y + .4, h + .02), (x + 1.7 + i * 1.6, y + .4, h + .02), (x + 1.7 + i * 1.6, y + 1.3, h + .5), (x + .4 + i * 1.6, y + 1.3, h + .5), fill='rgba(13,24,48,.7)', stroke='#62c8ff', sw=.9)

def bindingsverk(x, y, tak=True, plate=True):
    """Mikrohuset som reisverk: svill, stendere, toppsvill, takstoler, kryssavstivning."""
    skygge(x, y, HW, HD, .6)
    if plate:
        poly((x - .2, y - .2, 0), (x + HW + .2, y - .2, 0), (x + HW + .2, y + HD + .2, 0), (x - .2, y + HD + .2, 0), fill='rgba(170,180,200,.25)', stroke='#aab6cc', sw=1)
    kw = dict(stroke=TRE, sw=1.4)
    def ramme(x0, y0, w0, d0, h0, r0, langs_x):
        for z in (.12, h0):
            path((x0, y0, z), (x0 + w0, y0, z), (x0 + w0, y0 + d0, z), (x0, y0 + d0, z), lukk=True, **kw)
        n = max(2, int(w0 / 1.1)); m = max(2, int(d0 / 1.1))
        for i in range(n + 1):
            sx = x0 + w0 * i / n
            line((sx, y0, .12), (sx, y0, h0), **kw); line((sx, y0 + d0, .12), (sx, y0 + d0, h0), **kw)
        for j in range(m + 1):
            sy = y0 + d0 * j / m
            line((x0, sy, .12), (x0, sy, h0), **kw); line((x0 + w0, sy, .12), (x0 + w0, sy, h0), **kw)
        line((x0 + w0, y0, .12), (x0 + w0, y0 + d0, h0), stroke=TRE, sw=.9)      # kryss på gavl
        if not tak: return
        if langs_x:
            for i in range(n + 1):
                sx = x0 + w0 * i / n
                path((sx, y0, h0), (sx, y0 + d0 / 2, h0 + r0), (sx, y0 + d0, h0), **kw)
                line((sx, y0 + .7, h0 + r0 * .63), (sx, y0 + d0 - .7, h0 + r0 * .63), stroke=TRE, sw=.8)   # hanebjelke
            line((x0, y0 + d0 / 2, h0 + r0), (x0 + w0, y0 + d0 / 2, h0 + r0), stroke=TRE, sw=1.8)
        else:
            for j in range(m + 1):
                sy = y0 + d0 * j / m
                path((x0, sy, h0), (x0 + w0 / 2, sy, h0 + r0), (x0 + w0, sy, h0), **kw)
            line((x0 + w0 / 2, y0, h0 + r0), (x0 + w0 / 2, y0 + d0, h0 + r0), stroke=TRE, sw=1.8)
    ramme(x, y, HW - TW, HD, HH, HR, True)
    ramme(x + HW - TW, y, TW, HD, TH, TR, False)

def tak(x, y, stroke=STREK):
    """Bare takflatene (til det eksploderte huset), med synlige takstoler under."""
    w = HW - TW
    for i in range(7):
        sx = x + w * i / 6
        path((sx, y, HH), (sx, y + HD / 2, HH + HR), (sx, y + HD, HH), stroke=TRE, sw=1.2)
    poly((x, y, HH), (x + w, y, HH), (x + w, y + HD / 2, HH + HR), (x, y + HD / 2, HH + HR), fill=BAKTAK, stroke=stroke)
    poly((x, y + HD / 2, HH + HR), (x + w, y + HD / 2, HH + HR), (x + w, y + HD, HH), (x, y + HD, HH), fill=TOPP, stroke=stroke)
    tx = x + w
    poly((tx, y, TH), (tx + TW / 2, y, TH + TR), (tx + TW / 2, y + HD, TH + TR), (tx, y + HD, TH), fill=BAKTAK, stroke=stroke)
    poly((tx + TW / 2, y, TH + TR), (tx + TW / 2, y + HD, TH + TR), (tx + TW, y + HD, TH), (tx + TW, y, TH), fill=TOPP, stroke=stroke)

def installasjoner(x, y):
    """VVS og elektro slik de ligger inne i mikrohuset (brukes i snitt og eksplodert)."""
    w = HW - TW
    for dy, farge in ((.5, KALD), (.9, VARM)):      # kaldt og varmt vann opp fra bakken, langs bakveggen til badet
        path((x + .5, y + dy, -.3), (x + .5, y + dy, 2.2), (x + HW - 1.0, y + dy, 2.2), (x + HW - 1.0, y + dy, 1.0), stroke=farge, sw=2.1)
    path((x + HW - 1.0, y + 1.4, .05), (x + 1.2, y + 1.4, .05), (x + 1.2, y + HD + .8, .05), (x + 1.2, y + HD + .8, -.6), stroke='#a7b3c8', sw=3)  # avløp
    boks(x + HW - 2.3, y + .25, 0, 1.8, .7, 1.5, fill=('rgba(255,138,115,.25)', 'rgba(255,138,115,.3)', 'rgba(255,138,115,.2)'), stroke=VARM, sw=1)  # bereder
    poly((x, y + .6, 1.3), (x, y + 1.3, 1.3), (x, y + 1.3, 2.1), (x, y + .6, 2.1), fill='rgba(13,24,48,.6)', stroke=EL, sw=1)   # sikringsskap
    path((x, y + .95, 2.1), (x, y + .95, HH - .15), (x + w - .3, y + .95, HH - .15), stroke=EL, sw=1.5, extra='stroke-dasharray="3 2.5"')
    for lx in (x + 2.0, x + 4.6):
        line((lx, y + .95, HH - .15), (lx, y + .95, HH - .9), stroke=EL, sw=1.1); sirkel(lx, y + .95, HH - 1.05, 3, EL)
    for sx in (x + 3.2, x + 6.0):
        line((sx, y + .15, HH - .15), (sx, y + .15, .7), stroke=EL, sw=1, extra='stroke-dasharray="2 2"')
        poly((sx - .22, y + .15, .5), (sx + .22, y + .15, .5), (sx + .22, y + .15, .9), (sx - .22, y + .15, .9), fill=EL, stroke='none')

def snitt(x, y):
    """Mikrohuset skåret opp: bakvegger, gulv og tak står, fronten er stiplet så installasjonene synes."""
    w = HW - TW
    skygge(x, y, HW, HD)
    poly((x, y, 0), (x + HW, y, 0), (x + HW, y + HD, 0), (x, y + HD, 0), fill='rgba(42,82,154,.35)')
    poly((x, y, 0), (x + HW, y, 0), (x + HW, y, HH), (x, y, HH), fill='rgba(28,55,110,.6)')
    poly((x + w, y, HH), (x + HW, y, HH), (x + HW, y, TH), (x + w, y, TH), fill='rgba(28,55,110,.6)')
    poly((x, y, 0), (x, y + HD, 0), (x, y + HD, HH), (x, y, HH), fill='rgba(42,82,154,.5)')
    poly((x + w, y, 0), (x + w, y + HD, 0), (x + w, y + HD, HH), (x + w, y, HH), fill='rgba(42,82,154,.3)', sw=1)
    poly((x + w, y + 1.2, 0), (x + w, y + 2.1, 0), (x + w, y + 2.1, 2.0), (x + w, y + 1.2, 2.0), fill='rgba(13,24,48,.5)', sw=.8)
    installasjoner(x, y)
    saltak_boks(x, y, w, HD, HH, HR, True, fill=('rgba(130,170,240,.38)', 'none', 'none'), sw=1.1, stroke='rgba(159,188,240,.8)')
    kw = dict(sw=1.1, extra='stroke-dasharray="4 4" opacity=".7"')
    path((x, y + HD, 0), (x + HW, y + HD, 0), (x + HW, y, 0), **kw)
    line((x + HW, y + HD, 0), (x + HW, y + HD, TH), **kw)
    path((x + w, y + HD, HH), (x + w, y + HD, TH), (x + HW, y + HD, TH), **kw)
    path((x + w, y, TH), (x + w + TW / 2, y, TH + TR), (x + HW, y, TH), **kw)
    line((x + w + TW / 2, y, TH + TR), (x + w + TW / 2, y + HD, TH + TR), **kw)
    path((x + w, y + HD, TH), (x + w + TW / 2, y + HD, TH + TR), (x + HW, y + HD, TH), **kw)

def fundament(x, y, grop=True):
    """Byggegrop med forskaling, støpt plate og armeringsnett med oppstikk til stenderne."""
    t = .45
    if grop:
        poly((x - .9, y - .9, 0), (x + HW + .9, y - .9, 0), (x + HW + .9, y + HD + .9, 0), (x - .9, y + HD + .9, 0), fill='rgba(60,50,40,.35)', stroke='rgba(159,188,240,.35)', sw=1)
    boks(x, y, 0, HW, HD, t, fill=('rgba(170,180,200,.25)', 'rgba(150,160,180,.4)', 'rgba(110,120,140,.45)'))
    for i in range(1, 8):
        line((x + HW * i / 8, y + .2, t + .05), (x + HW * i / 8, y + HD - .2, t + .05), stroke='#c98d5b', sw=.8)
    for j in range(1, 5):
        line((x + .2, y + HD * j / 5, t + .08), (x + HW - .2, y + HD * j / 5, t + .08), stroke='#c98d5b', sw=.8)
    for cx, cy in ((x + .4, y + .4), (x + HW - .4, y + .4), (x + .4, y + HD - .4), (x + HW - .4, y + HD - .4), (x + HW / 2, y + .4)):
        line((cx, cy, t), (cx, cy, t + 1.3), stroke='#c98d5b', sw=1.4)
    if grop:
        for i in range(3):
            line((x - .9, y + HD + .9, .15 + i * .22), (x + HW + .9, y + HD + .9, .15 + i * .22), stroke=TRE, sw=1.1)

def brakke(x, y):
    """Byggebrakke: container på klosser, med dør, vindu og trapp."""
    w, d, h = 5.0, 2.4, 2.6
    skygge(x, y, w, d, .8)
    for bx in (x + .3, x + w - .6):
        boks(bx, y + .3, 0, .3, d - .6, .3, fill=('rgba(120,130,150,.5)',) * 3, sw=.6)
    boks(x, y, .3, w, d, h, fill=('rgba(235,240,250,.7)', 'rgba(214,222,236,.55)', 'rgba(160,175,200,.6)'), stroke=STAAL)
    for i in range(1, 5):
        line((x + w * i / 5, y + d, .4), (x + w * i / 5, y + d, h + .2), stroke='rgba(120,135,165,.5)', sw=.7)
    poly((x + .6, y + d, .3), (x + 1.5, y + d, .3), (x + 1.5, y + d, 2.3), (x + .6, y + d, 2.3), fill=ORANSJE, stroke='none')
    poly((x + 2.6, y + d, 1.3), (x + 4.2, y + d, 1.3), (x + 4.2, y + d, 2.3), (x + 2.6, y + d, 2.3), fill='rgba(13,24,48,.65)', stroke=STAAL, sw=.9)
    for i, z in enumerate((.1, .2, .3)):   # trapp: tre trinn
        line((x + .5, y + d + .9 - i * .3, z), (x + 1.6, y + d + .9 - i * .3, z), stroke=TRE, sw=1.4)

def kran(x, y, mast=13.0, utligger=18.0, kontra=6.0, katt=11.0, last_z=5.0):
    """Tårnkran, oppbygd som i virkeligheten: betongfundament, gittermast, svingkrans med førerhus,
    utligger med løpekatt, kontrautligger med motvekt, tårntopp med strekkstag, og last som henger loddrett."""
    a = 1.4
    cx, cy = x + a / 2, y + a / 2
    kw = dict(stroke=STAAL, sw=1.3)
    boks(cx - 1.8, cy - 1.8, 0, 3.6, 3.6, .6, fill=('rgba(170,180,200,.35)', 'rgba(150,160,180,.45)', 'rgba(110,120,140,.5)'), sw=1)
    for dx, dy in ((0, 0), (a, 0), (a, a), (0, a)):
        line((x + dx, y + dy, .6), (x + dx, y + dy, mast), **kw)
    z = .6
    while z < mast - .05:
        z2 = min(z + 1.2, mast)
        line((x, y + a, z), (x + a, y + a, z2), stroke=STAAL, sw=.75); line((x + a, y, z), (x + a, y + a, z2), stroke=STAAL, sw=.75)
        line((x, y + a, z2), (x + a, y + a, z2), stroke=STAAL, sw=.6); line((x + a, y, z2), (x + a, y + a, z2), stroke=STAAL, sw=.6)
        z = z2
    # svingkrans og førerhus (på utliggersiden, hengende under utliggeren)
    boks(x - .1, y - .1, mast, a + .2, a + .2, .5, fill=('rgba(214,222,236,.6)',) * 3, stroke=STAAL, sw=.9)
    boks(cx - 1.6, y + a + .05, mast - .6, 1.3, .9, 1.1, fill=(ORANSJE, ORANSJE, '#c4701a'), stroke='#ffd0a0', sw=.8)
    zu = mast + .5   # underkant utligger
    # utligger (mot -x): to undergurter, én overgurt, gitter
    for dy in (-.45, .45):
        line((cx - utligger, cy + dy, zu), (cx, cy + dy, zu), **kw)
    line((cx - utligger, cy, zu + 1.0), (cx - a / 2, cy, zu + 1.0), **kw)
    i = 0
    while i * 1.0 < utligger:
        sx = cx - i * 1.0
        line((sx, cy + .45, zu), (sx - .5, cy, zu + 1.0), stroke=STAAL, sw=.65); line((sx - .5, cy, zu + 1.0), (sx - 1.0, cy + .45, zu), stroke=STAAL, sw=.65)
        i += 1
    # kontrautligger (mot +x) med motvektsblokker som henger under enden
    for dy in (-.45, .45):
        line((cx, cy + dy, zu), (cx + kontra, cy + dy, zu), **kw)
    line((cx + a / 2, cy, zu + 1.0), (cx + kontra, cy, zu + 1.0), **kw)
    for i in range(int(kontra)):
        line((cx + i, cy + .45, zu), (cx + i + 1, cy, zu + 1.0), stroke=STAAL, sw=.65)
    for i in range(3):
        boks(cx + kontra - 1.9 + i * .55, cy - .7, zu - 1.5, .5, 1.4, 1.5, fill=('rgba(170,180,200,.6)', 'rgba(150,160,180,.7)', 'rgba(110,120,140,.75)'), sw=.8)
    # tårntopp og strekkstag
    topp = (cx, cy, zu + 4.0)
    for dx, dy in ((0, 0), (a, 0), (a, a), (0, a)):
        line((x + dx, y + dy, mast + .5), topp, stroke=STAAL, sw=1)
    line(topp, (cx - utligger * .6, cy, zu + 1.0), stroke=STAAL, sw=1)
    line(topp, (cx - utligger + .4, cy, zu + 1.0), stroke=STAAL, sw=.8)
    line(topp, (cx + kontra - .3, cy, zu + 1.0), stroke=STAAL, sw=1)
    # løpekatt, vaier, krokblokk og last: alt rett under løpekatten
    lx = cx - katt
    boks(lx - .45, cy - .45, zu - .35, .9, .9, .35, fill=('rgba(214,222,236,.7)',) * 3, stroke=STAAL, sw=.7)
    for dy in (-.15, .15):
        line((lx, cy + dy, zu - .35), (lx, cy + dy, last_z + 1.6), stroke=STAAL, sw=.8)
    boks(lx - .2, cy - .2, last_z + 1.2, .4, .4, .4, fill=(ORANSJE, ORANSJE, '#c4701a'), stroke='#ffd0a0', sw=.7)
    line((lx, cy, last_z + 1.2), (lx - 1.7, cy, last_z + .3), stroke=STAAL, sw=.8); line((lx, cy, last_z + 1.2), (lx + 1.7, cy, last_z + .3), stroke=STAAL, sw=.8)
    for i in range(4):   # bunt med stendere i stroppene
        boks(lx - 1.9, cy - .3 + i * .15, last_z - .05 + (i % 2) * .12, 3.8, .12, .12, fill=(TRE, TRE, '#c98d5b'), stroke='#f3cf98', sw=.6)

def totalstasjon(x, y, prisme, koord=True):
    topp = (x, y, 1.6)
    for dx, dy in ((-.9, -.3), (.75, -.65), (.25, .95)):
        line((x + dx, y + dy, 0), topp, stroke=STAAL, sw=1.5)
    boks(x - .4, y - .4, 1.6, .8, .8, .9, fill=('#ffb866', ORANSJE, '#c4701a'), stroke='#ffd0a0', sw=.8)
    px, py = prisme
    line((px, py, 0), (px, py, 2.3), stroke='#e8eef8', sw=1.5)
    sirkel(px, py, 2.3, 3.4, 'none', ORANSJE, 1.6)
    line((x, y, 2.1), (px, py, 2.3), stroke=ORANSJE, sw=1.1, extra='stroke-dasharray="5 4"')
    if koord: tekst(x + .5, y + .5, 0, 'N 60.795  Ø 10.692', size=8.5, fill=STAAL, anchor='start', dy=15)

def maal_x(x0, x1, y, t):
    line((x0, y, 0), (x1, y, 0), stroke=ORANSJE, sw=1.1)
    for x in (x0, x1):
        line((x, y - .35, 0), (x, y + .35, 0), stroke=ORANSJE, sw=1.1); line((x, y - 1.2, 0), (x, y, 0), stroke=ORANSJE, sw=.6, extra='opacity=".6"')
    tekst((x0 + x1) / 2, y, 0, t, size=8.5, fill=ORANSJE, dy=12)
def maal_y(x, y0, y1, t):
    line((x, y0, 0), (x, y1, 0), stroke=ORANSJE, sw=1.1)
    for y in (y0, y1):
        line((x - .35, y, 0), (x + .35, y, 0), stroke=ORANSJE, sw=1.1); line((x - 1.2, y, 0), (x, y, 0), stroke=ORANSJE, sw=.6, extra='opacity=".6"')
    tekst(x, (y0 + y1) / 2, 0, t, size=8.5, fill=ORANSJE, anchor='start', dy=12)

def tre(x, y, h=3.0):
    sirkel(x + .5, y + .5, 0, h * 2.6, 'rgba(0,0,0,.22)')
    line((x, y, 0), (x, y, h * .5), stroke='#8a9bb8', sw=1.6)
    sirkel(x, y, h * .78, h * 3.6, 'rgba(111,191,143,.42)', '#8fd6a1', 1.2)
    sirkel(x - .35, y - .35, h * .92, h * 2.2, 'rgba(160,220,180,.35)')

def benk(x, y, langs_x=True):
    """Benk med fire bein og rygg."""
    L, B, Z = 1.8, .45, .45
    w, d = (L, B) if langs_x else (B, L)
    for bx, by in ((x + .08, y + .06), (x + w - .14, y + .06), (x + .08, y + d - .12), (x + w - .14, y + d - .12)):
        line((bx, by, 0), (bx, by, Z), stroke=TRE, sw=1.5)
    boks(x, y, Z, w, d, .08, fill=(TRE, '#c98d5b', '#c98d5b'), stroke='#f3cf98', sw=.7)
    if langs_x:
        for bx in (x + .08, x + w - .14):
            line((bx, y + .06, Z), (bx, y + .06, Z + .45), stroke=TRE, sw=1.5)
        boks(x, y, Z + .35, w, .08, .14, fill=(TRE, '#c98d5b', '#c98d5b'), stroke='#f3cf98', sw=.7)

def lykt(x, y, h=4.0):
    line((x, y, 0), (x, y, h), stroke=STAAL, sw=1.5)
    line((x, y, h), (x + .7, y, h), stroke=STAAL, sw=1.3)
    sirkel(x + .7, y, h - .15, 3, EL); sirkel(x + .7, y, h - .15, 8, 'rgba(255,211,77,.12)')

def flaggstang(x, y, h=5.5):
    sirkel(x, y, 0, 3, 'rgba(170,180,200,.5)')
    line((x, y, 0), (x, y, h), stroke='#e8eef8', sw=1.3)
    poly((x, y, h), (x + 1.4, y, h - .3), (x, y, h - .9), fill=ORANSJE, stroke='none')

def tomt(w, d):
    poly((0, 0), (w, 0), (w, d), (0, d), fill='rgba(111,147,214,.06)', stroke='rgba(111,147,214,.35)', sw=1, extra='stroke-dasharray="4 5"')

def sti(a, b):
    path(a, b, stroke='rgba(159,188,240,.35)', sw=5); path(a, b, stroke='rgba(111,147,214,.16)', sw=3.4)

# ======================= Forslag =======================
def forslag_1():
    """Gaterekke: fire mikrohus langs en gate, det femte under bygging. Gatelys, trær og benk."""
    global S, OX, OY; S, OX, OY = 9.0, 300.0, 88.0
    tomt(46, 15)
    poly((-1, 7.6), (47, 7.6), (47, 10.4), (-1, 10.4), fill='rgba(111,147,214,.14)', stroke='rgba(159,188,240,.4)', sw=1)
    path((-1, 9.0), (47, 9.0), stroke='rgba(255,255,255,.25)', sw=1, extra='stroke-dasharray="6 6"')
    poly((-1, 10.4), (47, 10.4), (47, 11.4), (-1, 11.4), fill='rgba(159,188,240,.2)', stroke='none')
    mikrohus(1.0, 3.2); sti((5.0, 7.0), (5.0, 7.6))
    hus_b(11.0, 2.8, solceller=True); sti((15.0, 7.0), (15.0, 7.6))
    hus_c(22.0, 1.4); sti((25.0, 7.0), (25.0, 7.6))
    hus_d(31.5, 2.6); sti((35.5, 7.0), (35.5, 7.6))
    fundament(41.0, 3.2)
    for x in (9.3, 19.3, 29.3, 39.3): tre(x, 1.2, 2.6)
    for x in (6.0, 16.0, 26.0, 36.0): lykt(x, 7.2)
    benk(13.0, 11.9); benk(27.0, 11.9)
    tre(3.0, 13.0, 2.4); tre(40.0, 13.2, 2.4)
    poly((-0.6, 11.6, 1.2), (2.4, 11.6, 1.2), (2.4, 11.6, 2.2), (-0.6, 11.6, 2.2), fill='rgba(13,24,48,.8)', stroke=STAAL, sw=1)
    line((0.9, 11.6, 0), (0.9, 11.6, 1.2), stroke=STAAL, sw=1.3)
    tekst(0.9, 11.6, 1.75, 'STUDENTLANDSBYEN', size=6.5, fill='#fff', dy=2)

def forslag_2():
    """Tun: fire ferdige mikrohus og ett i bindingsverk rundt et tun med flaggstang og benker."""
    global S, OX, OY; S, OX, OY = 8.8, 250.0, 56.0
    tomt(42, 28)
    TX, TY, TR_ = 21, 14, 4.2
    for (x1, y1) in ((11, 4.5), (30, 7), (11, 14.5), (29, 19), (15, 22)): sti((TX, TY), (x1, y1))
    tun = [(TX + TR_ * math.cos(math.radians(a)), TY + TR_ * math.sin(math.radians(a))) for a in range(0, 360, 45)]
    poly(*tun, fill='rgba(111,147,214,.16)', stroke='rgba(159,188,240,.45)', sw=1)
    tre(23, 1, 2.6)
    mikrohus(3.5, 2.5, solceller=True); maal_x(3.5, 11, 7.4, '7 500'); maal_y(11.8, 2.5, 6.3, '3 800')
    hus_b(27, 2.6, solceller=True)
    tre(1.5, 8.5, 2.6); tre(41, 9, 2.8)
    hus_c(4, 12.0)
    flaggstang(TX, TY - 2.6)
    benk(18.6, 15.6); benk(22.4, 11.9, langs_x=False)
    hus_d(27.5, 18.2)
    bindingsverk(10, 21.5)
    tre(1, 26, 2.4); tre(16.5, 27.5, 2.2); tre(40.5, 26.5, 2.8)

def forslag_3():
    """Byggeplass: to ferdige hus, reisverk under kranen, hus i snitt, fundament, brakke og landmåling."""
    global S, OX, OY; S, OX, OY = 8.8, 250.0, 56.0
    tomt(42, 28)
    TX, TY, TR_ = 21, 14, 4.2
    for (x1, y1) in ((11, 4.5), (30, 7), (11, 14.5), (29, 19), (15, 22)): sti((TX, TY), (x1, y1))
    tun = [(TX + TR_ * math.cos(math.radians(a)), TY + TR_ * math.sin(math.radians(a))) for a in range(0, 360, 45)]
    poly(*tun, fill='rgba(111,147,214,.16)', stroke='rgba(159,188,240,.45)', sw=1)
    tre(23, 1, 2.6)
    mikrohus(3.5, 2.5, solceller=True); maal_x(3.5, 11, 7.4, '7 500'); maal_y(11.8, 2.5, 6.3, '3 800')
    kran(38.5, 1.0, mast=13.0, utligger=14.0, kontra=5.0, katt=8.5, last_z=5.2)
    bindingsverk(27, 3)
    tre(1.5, 8.5, 2.6)
    snitt(3, 12.5)
    benk(18.6, 15.6)
    hus_d(27.5, 18.2)
    brakke(36.5, 16.5)
    fundament(10, 21.5)
    totalstasjon(34, 26, (20.5, 23))
    tre(1, 26, 2.4); tre(16.5, 27.5, 2.2); tre(40.5, 26.5, 2.8)

def forslag_4():
    """Eksplodert mikrohus: fundament, bindingsverk, installasjoner og tak løftet fra hverandre, med forklaring."""
    global S, OX, OY, ZOFF; S, OX, OY = 12.5, 250.0, 300.0
    x, y = 0, 0
    lag = ((0.0, 'Fundament: plate på mark, armert'), (2.6, 'Bindingsverk 48×148, c/c 600'), (6.6, 'VVS og elektro'), (10.4, 'Tak: takstoler og tekking'))
    poly((x - 2, y - 2), (x + HW + 2, y - 2), (x + HW + 2, y + HD + 2), (x - 2, y + HD + 2), fill='rgba(111,147,214,.06)', stroke='rgba(111,147,214,.35)', sw=1, extra='stroke-dasharray="4 5"')
    for cx, cy in ((x, y), (x + HW, y), (x, y + HD), (x + HW, y + HD)):
        line((cx, cy, 0), (cx, cy, 15.5), stroke='rgba(159,188,240,.35)', sw=.8, extra='stroke-dasharray="3 4"')
    ZOFF = lag[0][0]; fundament(x, y, grop=False)
    ZOFF = lag[1][0]; bindingsverk(x, y, tak=False, plate=False)
    ZOFF = lag[2][0]
    poly((x, y, 0), (x + HW, y, 0), (x + HW, y + HD, 0), (x, y + HD, 0), fill='none', stroke='rgba(159,188,240,.5)', sw=1, extra='stroke-dasharray="3 3"')
    installasjoner(x, y)
    ZOFF = lag[3][0]; tak(x, y)
    ZOFF = 0.0
    for z, navn in lag:
        a, b = iso(x + HW + .3, y - .2, z + 1.0)
        ut.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{a + 40:.1f}" y2="{b:.1f}" stroke="{ORANSJE}" stroke-width="1"/>')
        ut.append(f'<text x="{a + 46:.1f}" y="{b + 3.5:.1f}" font-family="JetBrains Mono, Consolas, monospace" font-size="9.5" font-weight="600" fill="{STAAL}">{navn}</text>')
    tekst(x + HW / 2, y + HD + 1.2, 0, 'GMT MIKROHUS · BRA ≤ 30 m² · TEK17 § 1-2', size=9, fill=ORANSJE, dy=14)

def forslag_5():
    """Terreng ved Mjøsa: tre terrasser i skråningen med mikrohus, høydekoter, trapper og vann foran."""
    global S, OX, OY, ZOFF; S, OX, OY = 9.0, 290.0, 90.0
    tomt(44, 30)
    for r in (5, 9, 13, 17, 21):   # høydekoter rundt toppen (geomatikk)
        p = [(12 + r * math.cos(math.radians(a)), 6 + r * .75 * math.sin(math.radians(a))) for a in range(0, 360, 12)]
        path(*p, stroke='rgba(159,188,240,.28)', sw=.9, extra='stroke-dasharray="3 4"', lukk=True)
    def terrasse(px, py, pw, pd, z):
        poly((px, py + pd, 0), (px + pw, py + pd, 0), (px + pw, py + pd, z), (px, py + pd, z), fill='rgba(90,100,120,.5)', stroke='#aab6cc', sw=1)
        poly((px + pw, py, 0), (px + pw, py + pd, 0), (px + pw, py + pd, z), (px + pw, py, z), fill='rgba(70,80,100,.55)', stroke='#aab6cc', sw=1)
        poly((px, py, z), (px + pw, py, z), (px + pw, py + pd, z), (px, py + pd, z), fill='rgba(111,147,214,.12)', stroke='rgba(159,188,240,.5)', sw=1)
        for i in range(1, int(pw)):   # fuger i støttemuren
            line((px + i, py + pd, 0), (px + i, py + pd, z), stroke='rgba(170,180,200,.25)', sw=.6)
    def trapp(px, py, z0, z1, n=6):
        for i in range(n):
            zz = z0 + (z1 - z0) * i / n
            boks(px, py + i * .45, zz, 1.6, .45, (z1 - z0) / n, fill=('rgba(170,180,200,.5)', 'rgba(150,160,180,.5)', 'rgba(110,120,140,.5)'), sw=.6)
    terrasse(1, 1, 16, 7, 3.0); terrasse(13, 9, 16, 7, 1.5)
    ZOFF = 3.0; hus_c(3, 1.6); tre(14.5, 1.8, 2.4); ZOFF = 0.0
    trapp(10.5, 8.0, 1.5, 3.0)
    ZOFF = 1.5; hus_b(15, 10.0, solceller=True); benk(23.8, 14.6); ZOFF = 0.0
    trapp(22.5, 16.0, 0, 1.5)
    bindingsverk(28, 18.5)
    tre(2, 12, 2.6); tre(38, 10, 2.8); tre(6, 20, 2.4)
    totalstasjon(36, 24.5, (24, 19.5))
    poly((0, 27), (44, 27), (44, 30), (0, 30), fill='rgba(98,200,255,.14)', stroke='none')
    for i in range(6):
        path((2 + i * 7, 28 + (i % 2) * .8), (5 + i * 7, 28 + (i % 2) * .8), stroke='rgba(98,200,255,.5)', sw=1)
    tekst(22, 28.6, 0, 'MJØSA', size=9, fill='rgba(98,200,255,.7)', dy=4)

def forslag_6():
    """Plan og 3D: plantegning av mikrohuset på bakken, det ferdige huset ved siden av, og neste hus stiplet."""
    global S, OX, OY; S, OX, OY = 12.5, 250.0, 120.0
    x, y = 0, 0
    # tegneark på bakken
    poly((x - 1.5, y - 1.5), (x + 29, y - 1.5), (x + 29, y + HD + 2.5), (x - 1.5, y + HD + 2.5), fill='rgba(111,147,214,.06)', stroke='rgba(111,147,214,.35)', sw=1, extra='stroke-dasharray="4 5"')
    # plantegning: yttervegger (dobbel strek), innervegg, dører med slagbue, vinduer, møbler
    t = .2
    poly((x, y), (x + HW, y), (x + HW, y + HD), (x, y + HD), fill='rgba(159,188,240,.08)', stroke='#e8eef8', sw=1.6)
    poly((x + t, y + t), (x + HW - t, y + t), (x + HW - t, y + HD - t), (x + t, y + HD - t), stroke='#e8eef8', sw=.8)
    w = HW - TW
    line((x + w, y + t), (x + w, y + 1.2), stroke='#e8eef8', sw=1.4); line((x + w, y + 2.1, 0), (x + w, y + HD - t, 0), stroke='#e8eef8', sw=1.4)
    def slagbue(px, py, r, a0, a1):
        p = [(px + r * math.cos(math.radians(a)), py + r * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 10)]
        path((px, py), *p, (px, py), stroke='rgba(232,238,248,.7)', sw=.7)
    slagbue(x + w, y + 1.2, .9, 0, 90)                       # innerdør
    line((x + w - 1.5, y + HD, 0), (x + w - .55, y + HD, 0), stroke='#0d1830', sw=2.2); slagbue(x + w - 1.5, y + HD, .95, 180, 270)   # ytterdør
    for vx in (x + .8, x + 2.6, x + w + 1.0):
        line((vx, y + HD, 0), (vx + 1.2, y + HD, 0), stroke='#62c8ff', sw=2)
    poly((x + .25, y + .25), (x + 2.6, y + .25), (x + 2.6, y + .85), (x + .25, y + .85), stroke='rgba(232,238,248,.7)', sw=.7)   # kjøkkenbenk
    poly((x + 2.9, y + .25), (x + 4.0, y + .25), (x + 4.0, y + 1.1), (x + 2.9, y + 1.1), stroke='rgba(232,238,248,.7)', sw=.7)   # bord
    poly((x + .3, y + 1.9), (x + 2.3, y + 1.9), (x + 2.3, y + HD - .3), (x + .3, y + HD - .3), stroke='rgba(232,238,248,.7)', sw=.7)  # seng
    poly((x + w + .3, y + .3), (x + w + 1.2, y + .3), (x + w + 1.2, y + 1.2), (x + w + .3, y + 1.2), stroke='rgba(98,200,255,.8)', sw=.7)  # dusj
    sirkel(x + w + 2.3, y + .8, 0, 3.5, 'none', 'rgba(232,238,248,.7)', .8)   # wc
    line((x + w + 2.0, y + 2.6, 0), (x + w + 2.9, y + 2.6, 0), stroke='rgba(232,238,248,.7)', sw=.8)   # trapp til hems (strek)
    for i in range(5): line((x + w + 2.0 + i * .22, y + 2.5, 0), (x + w + 2.0 + i * .22, y + HD - .3, 0), stroke='rgba(232,238,248,.6)', sw=.6)
    maal_x(x, x + HW, y + HD + 1.1, '7 500'); maal_y(x + HW + 1.0, y, y + HD, '3 800')
    tekst(x, y - .9, 0, 'GMT MIKROHUS · PLAN 1:50 · BRA 23 m²', size=8.5, fill=ORANSJE, anchor='start', dy=-2)
    # det ferdige huset og neste hus
    mikrohus(x + 11.5, y, solceller=True)
    spokelse(x + 21.0, y)
    tekst(x + 24.5, y + HD, 0, 'NESTE', size=8, fill=STAAL, dy=14)
    tre(x + 10.2, y + HD + 1.6, 2.2); tre(x + 28.2, y - .8, 2.4)

FORSLAG = {1: forslag_1, 2: forslag_2, 3: forslag_3, 4: forslag_4, 5: forslag_5, 6: forslag_6}

if __name__ == '__main__':
    nr, utfil = int(sys.argv[1]), sys.argv[2]
    FORSLAG[nr]()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<title>Studentlandsby – forslag {nr}</title>' + ''.join(ut) + '</svg>')
    open(utfil, 'w', encoding='utf-8').write(svg)
    print('skrevet', utfil, len(svg), 'tegn')
