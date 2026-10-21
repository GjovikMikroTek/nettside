# Lager studentlandsby-3d.svg: isometrisk «arbeidstegning» av en studentlandsby under bygging.
# Viser arkitektur (ferdig hus + mållinjer), bindingsverk, konstruksjon (fundament med armering, kran),
# VVS og elektro (hus i snitt) og geomatikk (totalstasjon med måling mot prisme).
import math, sys

S = 10.0                 # piksler per meter
OX, OY = 270.0, 70.0     # origo på lerretet
C30 = math.cos(math.radians(30))
W, H = 640, 420

STREK = '#9fbcf0'
TRE = '#e9b36f'
KALD, VARM, EL = '#62c8ff', '#ff8a73', '#ffd34d'
ORANSJE = '#f39228'

def iso(x, y, z=0.0):
    return (OX + (x - y) * C30 * S, OY + (x + y) * 0.5 * S - z * S)

def pts(*p):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in (iso(*q) for q in p))

ut = []
def poly(*p, fill='none', stroke=STREK, sw=1.4, extra=''):
    ut.append(f'<polygon points="{pts(*p)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
def line(a, b, stroke=STREK, sw=1.4, extra=''):
    (x1, y1), (x2, y2) = iso(*a), iso(*b)
    ut.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" {extra}/>')
def path(*p, stroke=STREK, sw=1.4, extra=''):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in (iso(*q) for q in p))
    ut.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def tekst(x, y, z, t, size=9, fill=STREK, anchor='middle', dy=0):
    a, b = iso(x, y, z)
    ut.append(f'<text x="{a:.1f}" y="{b + dy:.1f}" font-family="JetBrains Mono, Consolas, monospace" font-size="{size}" font-weight="600" fill="{fill}" text-anchor="{anchor}">{t}</text>')

def skygge(x, y, w, d, ox=1.2):
    poly((x + ox, y + ox), (x + w + ox, y + ox), (x + w + ox, y + d + ox), (x + ox, y + d + ox), fill='rgba(0,0,0,.25)', stroke='none')

def hus(x, y, w, d, h, r, vinduer=True):
    """Ferdig hus med saltak (møne langs x)."""
    skygge(x, y, w, d)
    # bakre takflate først
    poly((x, y, h), (x + w, y, h), (x + w, y + d / 2, h + r), (x, y + d / 2, h + r), fill='rgba(130,170,240,.45)')
    # vegger: front (y+d) og gavl (x+w)
    poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, h), (x, y + d, h), fill='rgba(42,82,154,.62)')
    poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, h), (x + w, y, h), fill='rgba(28,55,110,.78)')
    poly((x + w, y, h), (x + w, y + d, h), (x + w, y + d / 2, h + r), fill='rgba(28,55,110,.78)')
    # fremre takflate
    poly((x, y + d / 2, h + r), (x + w, y + d / 2, h + r), (x + w, y + d, h), (x, y + d, h), fill='rgba(130,170,240,.62)')
    if vinduer:
        for vx in (x + 1.2, x + 3.2, x + w - 3.0):
            poly((vx, y + d, 1.4), (vx + 1.4, y + d, 1.4), (vx + 1.4, y + d, 2.8), (vx, y + d, 2.8), fill='rgba(13,24,48,.6)', sw=1.1)
            line((vx + .7, y + d, 1.4), (vx + .7, y + d, 2.8), sw=.8)
            line((vx, y + d, 2.1), (vx + 1.4, y + d, 2.1), sw=.8)
        dx = x + 5.6
        poly((dx, y + d, 0), (dx + 1.0, y + d, 0), (dx + 1.0, y + d, 2.2), (dx, y + d, 2.2), fill=ORANSJE, stroke='none')

def bindingsverk(x, y, w, d, h, r):
    """Hus i bindingsverk: svill, stendere, toppsvill og takstoler."""
    skygge(x, y, w, d, .6)
    kw = dict(stroke=TRE, sw=1.5)
    # svill og toppsvill
    for z in (0.15, h):
        path((x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z), (x, y, z), **kw)
    # stendere langs alle fire vegger (c/c ca. 0,6 m skalert)
    n = int(w / 1.25)
    for i in range(n + 1):
        sx = x + w * i / n
        line((sx, y, 0.15), (sx, y, h), **kw)
        line((sx, y + d, 0.15), (sx, y + d, h), **kw)
    m = int(d / 1.4)
    for j in range(m + 1):
        sy = y + d * j / m
        line((x, sy, 0.15), (x, sy, h), **kw)
        line((x + w, sy, 0.15), (x + w, sy, h), **kw)
    # kryssavstivning på gavl
    line((x + w, y, 0.15), (x + w, y + d / 2, h), stroke=TRE, sw=1.1)
    # takstoler og møne
    for i in range(n + 1):
        sx = x + w * i / n
        path((sx, y, h), (sx, y + d / 2, h + r), (sx, y + d, h), **kw)
        line((sx, y + .8, h + r * .8 / (d / 2)), (sx, y + d - .8, h + r * .8 / (d / 2)), stroke=TRE, sw=.9)
    line((x, y + d / 2, h + r), (x + w, y + d / 2, h + r), stroke=TRE, sw=1.8)

def snitt(x, y, w, d, h, r):
    """Hus i snitt: bakvegger og gulv, med VVS (kaldt/varmt vann, avløp) og elektro synlig."""
    skygge(x, y, w, d)
    poly((x, y, 0), (x + w, y, 0), (x + w, y + d, 0), (x, y + d, 0), fill='rgba(42,82,154,.35)')       # gulv
    poly((x, y, 0), (x + w, y, 0), (x + w, y, h), (x, y, h), fill='rgba(28,55,110,.55)')              # bakvegg
    poly((x, y, 0), (x, y + d, 0), (x, y + d, h), (x, y, h), fill='rgba(42,82,154,.45)')              # venstre vegg
    # VVS: kaldt og varmt vann opp i hjørnet, langs bakveggen; avløp i gulvet
    for dy, farge in ((.6, KALD), (1.0, VARM)):
        path((x + .4, y + dy, 0), (x + .4, y + dy, 2.6), (x + w - 1.6, y + dy, 2.6), (x + w - 1.6, y + dy, 1.2), stroke=farge, sw=2.2)
    path((x + w - 2.2, y + 2.8, 0.05), (x + 2.0, y + 2.8, 0.05), (x + 2.0, y + d - .3, 0.05), stroke='#a7b3c8', sw=3, extra='stroke-dasharray="1 0"')
    poly((x + w - 2.6, y + .3, 0.6), (x + w - .8, y + .3, 0.6), (x + w - .8, y + .3, 1.3), (x + w - 2.6, y + .3, 1.3), fill='rgba(255,138,115,.35)', stroke=VARM, sw=1)  # varmtvannsbereder/radiator
    # Elektro: kurs langs venstre vegg, stikkontakter og lampe
    path((x, y + .4, 3.2), (x, y + d - .6, 3.2), (x, y + d - .6, 0.8), stroke=EL, sw=1.6, extra='stroke-dasharray="3 2.5"')
    for sy in (y + 2.4, y + 4.6):
        line((x, sy, 3.2), (x, sy, 0.8), stroke=EL, sw=1.2, extra='stroke-dasharray="2 2"')
        poly((x, sy - .25, .6), (x, sy + .25, .6), (x, sy + .25, 1.0), (x, sy - .25, 1.0), fill=EL, stroke='none')
    line((x + w / 2, y + d / 2, h), (x + w / 2, y + d / 2, h - .9), stroke=EL, sw=1.2)
    a, b = iso(x + w / 2, y + d / 2, h - 1.1)
    ut.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.2" fill="{EL}"/>')
    # stiplet omriss av front, gavl og tak (snittet)
    kw = dict(sw=1.1, extra='stroke-dasharray="4 4" opacity=".75"')
    path((x, y + d, 0), (x + w, y + d, 0), (x + w, y, 0), **kw)
    path((x, y + d, h), (x + w, y + d, h), (x + w, y, h), (x, y, h), **kw)
    line((x + w, y + d, 0), (x + w, y + d, h), **kw)
    path((x, y, h), (x, y + d / 2, h + r), (x, y + d, h), **kw)
    path((x + w, y, h), (x + w, y + d / 2, h + r), (x + w, y + d, h), **kw)
    line((x, y + d / 2, h + r), (x + w, y + d / 2, h + r), **kw)

def fundament(x, y, w, d):
    """Plate på mark med armeringsnett og oppstikk."""
    t = .45
    poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, t), (x, y + d, t), fill='rgba(150,160,180,.35)')
    poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, t), (x + w, y, t), fill='rgba(110,120,140,.4)')
    poly((x, y, t), (x + w, y, t), (x + w, y + d, t), (x, y + d, t), fill='rgba(170,180,200,.22)')
    for i in range(1, 10):
        line((x + w * i / 10, y + .2, t + .05), (x + w * i / 10, y + d - .2, t + .05), stroke='#c98d5b', sw=.8)
    for j in range(1, 7):
        line((x + .2, y + d * j / 7, t + .08), (x + w - .2, y + d * j / 7, t + .08), stroke='#c98d5b', sw=.8)
    for cx, cy in ((x + .5, y + .5), (x + w - .5, y + .5), (x + .5, y + d - .5), (x + w - .5, y + d - .5)):
        line((cx, cy, t), (cx, cy, t + 1.4), stroke='#c98d5b', sw=1.4)

def kran(x, y, hoyde, til_x, last):
    """Tårnkran med gitterverk, utligger langs x og en limtrebjelke i kroken."""
    kw = dict(sw=1.2, stroke='#c9d6ef')
    a = .9
    for dx, dy in ((0, 0), (a, 0), (a, a), (0, a)):
        line((x + dx, y + dy, 0), (x + dx, y + dy, hoyde), **kw)
    k = 0
    z = 0.0
    while z < hoyde - .1:
        z2 = min(z + 1.2, hoyde)
        line((x, y + a, z), (x + a, y + a, z2), stroke='#c9d6ef', sw=.8)
        line((x + a, y, z), (x + a, y + a, z2), stroke='#c9d6ef', sw=.8)
        line((x, y + a, z2), (x + a, y + a, z2), stroke='#c9d6ef', sw=.6)
        z = z2
    # utligger og motvekt
    for dz in (0, .9):
        line((til_x, y + a / 2, hoyde + dz * 0), (x + 4.5, y + a / 2, hoyde), **kw)
    line((til_x, y + a / 2, hoyde), (x + a / 2, y + a / 2, hoyde + 2.2), **kw)
    line((x + 4.5, y + a / 2, hoyde), (x + a / 2, y + a / 2, hoyde + 2.2), **kw)
    poly((x + 3.2, y, hoyde - .9), (x + 4.6, y, hoyde - .9), (x + 4.6, y, hoyde), (x + 3.2, y, hoyde), fill='rgba(150,160,180,.6)', sw=1)
    # førerhus
    poly((x - .1, y + a, hoyde - 1.2), (x + a + .1, y + a, hoyde - 1.2), (x + a + .1, y + a, hoyde - .2), (x - .1, y + a, hoyde - .2), fill=ORANSJE, stroke='none')
    # vaier og last
    lx, ly, lz = last
    line((lx, y + a / 2, hoyde), (lx, y + a / 2, lz + .5), sw=1, stroke='#c9d6ef')
    line((lx, y + a / 2, lz + .5), (lx - 1.6, ly, lz), sw=.8, stroke='#c9d6ef')
    line((lx, y + a / 2, lz + .5), (lx + 1.6, ly, lz), sw=.8, stroke='#c9d6ef')
    poly((lx - 2.2, ly - .2, lz), (lx + 2.2, ly - .2, lz), (lx + 2.2, ly + .2, lz), (lx - 2.2, ly + .2, lz), fill=TRE, stroke=TRE, sw=2.2)

def totalstasjon(x, y, prisme):
    """Landmåling: stativ med totalstasjon, stiplet målestråle mot prismestang."""
    topp = (x, y, 2.0)
    for dx, dy in ((-1.0, -.3), (.8, -.7), (.3, 1.0)):
        line((x + dx, y + dy, 0), topp, stroke='#c9d6ef', sw=1.5)
    # instrumentet: liten boks med oransje sider
    b, z0, z1 = .45, 2.0, 2.9
    poly((x - b, y + b, z0), (x + b, y + b, z0), (x + b, y + b, z1), (x - b, y + b, z1), fill=ORANSJE, stroke='#ffd0a0', sw=.8)
    poly((x + b, y - b, z0), (x + b, y + b, z0), (x + b, y + b, z1), (x + b, y - b, z1), fill='#c4701a', stroke='#ffd0a0', sw=.8)
    poly((x - b, y - b, z1), (x + b, y - b, z1), (x + b, y + b, z1), (x - b, y + b, z1), fill='#ffb866', stroke='#ffd0a0', sw=.8)
    px, py = prisme
    line((px, py, 0), (px, py, 2.3), stroke='#e8eef8', sw=1.5)
    a, b = iso(px, py, 2.3)
    ut.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.4" fill="none" stroke="{ORANSJE}" stroke-width="1.6"/>')
    line((x, y, 2.5), (px, py, 2.3), stroke=ORANSJE, sw=1.1, extra='stroke-dasharray="5 4"')
    tekst(x + .6, y + .6, 0, 'N 60.795  Ø 10.692', size=8.5, fill='#c9d6ef', anchor='start', dy=14)

def maal(a, b, z, tekst_, forskyv=(0, 1.6)):
    """Mållinje med endestreker (arkitektur)."""
    fx, fy = forskyv
    p1, p2 = (a[0] + fx, a[1] + fy, z), (b[0] + fx, b[1] + fy, z)
    line(p1, p2, stroke=ORANSJE, sw=1.1)
    for p in (p1, p2):
        line((p[0] - .4 * (fy > 0), p[1] - .4 * (fx > 0), z), (p[0] + .4 * (fy > 0), p[1] + .4 * (fx > 0), z), stroke=ORANSJE, sw=1.1)
    m = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, z)
    tekst(*m, tekst_, size=9, fill=ORANSJE, dy=13)

def tre(x, y, h=3.2):
    line((x, y, 0), (x, y, h * .45), stroke='#8a9bb8', sw=1.6)
    a, b = iso(x, y, h * .75)
    ut.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{h * 4.2:.1f}" fill="rgba(111,191,143,.45)" stroke="#8fd6a1" stroke-width="1.2"/>')

# Tomt med stiplet omriss og veinett
poly((0, 0), (40, 0), (40, 28), (0, 28), fill='rgba(111,147,214,.06)', stroke='rgba(111,147,214,.35)', sw=1, extra='stroke-dasharray="4 5"')
poly((13.5, 0), (15, 0), (15, 28), (13.5, 28), fill='rgba(111,147,214,.10)', stroke='none')
poly((0, 11.2), (40, 11.2), (40, 12.7), (0, 12.7), fill='rgba(111,147,214,.10)', stroke='none')

# Bakerst til forrest (tegnes i rekkefølge etter x+y)
hus(2, 2, 10, 7, 3.6, 2.4)
maal((12, 2), (12, 9), 0, '7 000', forskyv=(1.3, 0))
bindingsverk(17, 2, 10, 7, 3.6, 2.4)
kran(31.5, 3.5, 15.5, 19.5, (22, 6.0, 9.5))
tre(36.5, 9.5)
snitt(2, 15, 10, 7, 3.6, 2.4)
fundament(17, 15, 10, 7)
totalstasjon(33, 20, (25.5, 18.5))
tre(1, 26, 2.6)
tre(37.5, 25.5, 2.8)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       '<title>Studentlandsby under bygging</title>' + ''.join(ut) + '</svg>')
open(sys.argv[1], 'w', encoding='utf-8').write(svg)
print('skrevet', len(svg), 'tegn')
