# Lager studentlandsby-3d.svg: isometrisk «arbeidstegning» av en studentlandsby under bygging,
# i samme strek som mikrohus-3d.svg. Kjør: python -I lag-studentlandsby.py ../studentlandsby-3d.svg
#
# Husene har mikrohusets form (lang hoveddel + høyere tilbygg). Rundt et tun i midten står de i
# ulike byggetrinn: fundament med armering (konstruksjon) → bindingsverk → hus i snitt med
# VVS og elektro → ferdige hus med solceller og varmepumpe (arkitektur, mållinjer).
# Tårnkran bak, totalstasjon mot prismestang foran (geomatikk).
import math, sys

S = 8.8                  # piksler per meter
OX, OY = 250.0, 56.0     # origo på lerretet
C30 = math.cos(math.radians(30))
W, H = 660, 430

STREK = '#9fbcf0'
TRE = '#e9b36f'
KALD, VARM, EL = '#62c8ff', '#ff8a73', '#ffd34d'
ORANSJE = '#f39228'
TOPP, FRONT, SIDE = 'rgba(130,170,240,.62)', 'rgba(42,82,154,.62)', 'rgba(28,55,110,.78)'

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
def sirkel(x, y, z, r, fill, stroke='none', sw=1):
    a, b = iso(x, y, z)
    ut.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def skygge(x, y, w, d, ox=1.1):
    poly((x + ox, y + ox), (x + w + ox, y + ox), (x + w + ox, y + d + ox), (x + ox, y + d + ox), fill='rgba(0,0,0,.28)', stroke='none')

# ---------- Mikrohuset: hoveddel (møne langs x) + høyere tilbygg i enden (møne langs y) ----------
def boks_med_saltak(x, y, w, d, h, r, langs_x=True, fill=(TOPP, FRONT, SIDE), sw=1.4, stroke=STREK):
    topp, front, side = fill
    if langs_x:
        poly((x, y, h), (x + w, y, h), (x + w, y + d / 2, h + r), (x, y + d / 2, h + r), fill='rgba(130,170,240,.42)', sw=sw, stroke=stroke)   # bakre takflate
        poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, h), (x, y + d, h), fill=front, sw=sw, stroke=stroke)
        poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, h), (x + w, y, h), fill=side, sw=sw, stroke=stroke)
        poly((x + w, y, h), (x + w, y + d, h), (x + w, y + d / 2, h + r), fill=side, sw=sw, stroke=stroke)
        poly((x, y + d / 2, h + r), (x + w, y + d / 2, h + r), (x + w, y + d, h), (x, y + d, h), fill=topp, sw=sw, stroke=stroke)
    else:
        poly((x, y, h), (x + w / 2, y, h + r), (x + w / 2, y + d, h + r), (x, y + d, h), fill='rgba(130,170,240,.42)', sw=sw, stroke=stroke)
        poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, h), (x, y + d, h), fill=front, sw=sw, stroke=stroke)
        poly((x, y + d, h), (x + w, y + d, h), (x + w / 2, y + d, h + r), fill=front, sw=sw, stroke=stroke)
        poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, h), (x + w, y, h), fill=side, sw=sw, stroke=stroke)
        poly((x + w / 2, y, h + r), (x + w / 2, y + d, h + r), (x + w, y + d, h), (x + w, y, h), fill=topp, sw=sw, stroke=stroke)

def vindu(x, y, z, b=1.2, hh=1.3, gavl=False):
    if gavl:  # i x+w-veggen (varierer y)
        poly((x, y, z), (x, y + b, z), (x, y + b, z + hh), (x, y, z + hh), fill='rgba(13,24,48,.65)', sw=1)
        line((x, y + b / 2, z), (x, y + b / 2, z + hh), sw=.7); line((x, y, z + hh / 2), (x, y + b, z + hh / 2), sw=.7)
    else:
        poly((x, y, z), (x + b, y, z), (x + b, y, z + hh), (x, y, z + hh), fill='rgba(13,24,48,.65)', sw=1)
        line((x + b / 2, y, z), (x + b / 2, y, z + hh), sw=.7); line((x, y, z + hh / 2), (x + b, y, z + hh / 2), sw=.7)

def mikrohus(x, y, speil=False, solceller=False, varmepumpe=False):
    """Ferdig mikrohus. Hoveddel 7,5 × 3,8 m, tilbygg 3,2 × 3,8 m og en etasje høyere."""
    w, d, h, r = 7.5, 3.8, 2.7, 1.4
    tw, th, tr = 3.2, 3.9, 1.6
    tx = x if speil else x + w - tw
    skygge(x, y, w, d)
    if speil:   # tilbygget til venstre: tegn det først (lengst bak)
        boks_med_saltak(tx, y, tw, d, th, tr, langs_x=False)
        boks_med_saltak(tx + tw, y, w - tw, d, h, r, langs_x=True)
    else:
        boks_med_saltak(x, y, w - tw, d, h, r, langs_x=True)
        boks_med_saltak(tx, y, tw, d, th, tr, langs_x=False)
    # vinduer og dør i fronten
    lav_x0 = x + tw if speil else x
    vindu(lav_x0 + .8, y + d, .9); vindu(lav_x0 + 2.6, y + d, .9)
    dx = lav_x0 + (w - tw) - 1.5
    poly((dx, y + d, 0), (dx + .95, y + d, 0), (dx + .95, y + d, 2.1), (dx, y + d, 2.1), fill=ORANSJE, stroke='none')
    vindu(tx + 1.0, y + d, 1.0, b=1.2, hh=1.2); vindu(tx + 1.0, y + d, 2.6, b=1.2, hh=.9)
    if solceller:  # paneler på den fremre takflaten til hoveddelen (elektro)
        for i in range(3):
            px = lav_x0 + .6 + i * 1.35
            poly((px, y + d - .5, h + r * .5 / (d / 2)), (px + 1.1, y + d - .5, h + r * .5 / (d / 2)),
                 (px + 1.1, y + d - 1.6, h + r * 1.6 / (d / 2)), (px, y + d - 1.6, h + r * 1.6 / (d / 2)),
                 fill='rgba(13,24,48,.7)', stroke='#62c8ff', sw=.9)
    if varmepumpe:  # utedel på gavlen (VVS)
        gx = x + w + .15 if not speil else x - .75
        poly((gx, y + 2.0, .4), (gx + .6, y + 2.0, .4), (gx + .6, y + 3.2, .4), (gx, y + 3.2, .4), fill='rgba(200,215,240,.5)', sw=1)
        poly((gx, y + 2.0, .4), (gx, y + 3.2, .4), (gx, y + 3.2, 1.3), (gx, y + 2.0, 1.3), fill='rgba(200,215,240,.35)', sw=1)
        sirkel(gx, y + 2.6, .85, 2.6, 'none', '#c9d6ef', 1)

def bindingsverk(x, y):
    """Mikrohuset som reisverk: svill, stendere, toppsvill, takstoler, gavl med kryss."""
    w, d, h, r = 7.5, 3.8, 2.7, 1.4
    tw, th, tr = 3.2, 3.9, 1.6
    skygge(x, y, w, d, .6)
    kw = dict(stroke=TRE, sw=1.4)
    # fundament under (ferdig plate)
    poly((x - .2, y - .2, 0), (x + w + .2, y - .2, 0), (x + w + .2, y + d + .2, 0), (x - .2, y + d + .2, 0), fill='rgba(170,180,200,.25)', stroke='#aab6cc', sw=1)
    def ramme(x0, y0, w0, d0, h0, r0, langs_x):
        for z in (.12, h0):
            path((x0, y0, z), (x0 + w0, y0, z), (x0 + w0, y0 + d0, z), (x0, y0 + d0, z), (x0, y0, z), **kw)
        n = max(2, int(w0 / 1.1)); m = max(2, int(d0 / 1.1))
        for i in range(n + 1):
            sx = x0 + w0 * i / n
            line((sx, y0, .12), (sx, y0, h0), **kw); line((sx, y0 + d0, .12), (sx, y0 + d0, h0), **kw)
        for j in range(m + 1):
            sy = y0 + d0 * j / m
            line((x0, sy, .12), (x0, sy, h0), **kw); line((x0 + w0, sy, .12), (x0 + w0, sy, h0), **kw)
        if langs_x:
            for i in range(n + 1):
                sx = x0 + w0 * i / n
                path((sx, y0, h0), (sx, y0 + d0 / 2, h0 + r0), (sx, y0 + d0, h0), **kw)
                line((sx, y0 + .7, h0 + r0 * .63), (sx, y0 + d0 - .7, h0 + r0 * .63), stroke=TRE, sw=.8)
            line((x0, y0 + d0 / 2, h0 + r0), (x0 + w0, y0 + d0 / 2, h0 + r0), stroke=TRE, sw=1.8)
            line((x0 + w0, y0, .12), (x0 + w0, y0 + d0, h0), stroke=TRE, sw=.9)
        else:
            for j in range(m + 1):
                sy = y0 + d0 * j / m
                path((x0, sy, h0), (x0 + w0 / 2, sy, h0 + r0), (x0 + w0, sy, h0), **kw)
            line((x0 + w0 / 2, y0, h0 + r0), (x0 + w0 / 2, y0 + d0, h0 + r0), stroke=TRE, sw=1.8)
            line((x0, y0 + d0, .12), (x0 + w0, y0 + d0, h0), stroke=TRE, sw=.9)
    ramme(x, y, w - tw, d, h, r, True)
    ramme(x + w - tw, y, tw, d, th, tr, False)
    # en bunt stendere på bakken
    for i in range(4):
        line((x + 1 + i * .35, y + d + 1.2, .1 + (i % 2) * .15), (x + 4.5 + i * .35, y + d + 1.2, .1 + (i % 2) * .15), stroke=TRE, sw=2)

def snitt(x, y):
    """Mikrohuset skåret opp: bakvegger, gulv og tak står; fronten er tatt bort så VVS og elektro synes."""
    w, d, h, r = 7.5, 3.8, 2.7, 1.4
    tw, th, tr = 3.2, 3.9, 1.6
    skygge(x, y, w, d)
    poly((x, y, 0), (x + w, y, 0), (x + w, y + d, 0), (x, y + d, 0), fill='rgba(42,82,154,.35)')       # gulv
    poly((x, y, 0), (x + w, y, 0), (x + w, y, h), (x, y, h), fill='rgba(28,55,110,.6)')               # bakvegg hoveddel
    poly((x + w - tw, y, h), (x + w, y, h), (x + w, y, th), (x + w - tw, y, th), fill='rgba(28,55,110,.6)')  # bakvegg tilbygg (høyere)
    poly((x, y, 0), (x, y + d, 0), (x, y + d, h), (x, y, h), fill='rgba(42,82,154,.5)')               # venstre gavl
    # innervegg mellom hoveddel og tilbygg, med døråpning
    poly((x + w - tw, y, 0), (x + w - tw, y + d, 0), (x + w - tw, y + d, h), (x + w - tw, y, h), fill='rgba(42,82,154,.3)', sw=1)
    poly((x + w - tw, y + 1.2, 0), (x + w - tw, y + 2.1, 0), (x + w - tw, y + 2.1, 2.0), (x + w - tw, y + 1.2, 2.0), fill='rgba(13,24,48,.5)', sw=.8)
    # VVS: kaldt/varmt vann fra bakken opp langs bakveggen til bad i tilbygget; avløp i gulvet
    for dy, farge in ((.5, KALD), (.9, VARM)):
        path((x + .5, y + dy, -.3), (x + .5, y + dy, 2.2), (x + w - 1.0, y + dy, 2.2), (x + w - 1.0, y + dy, 1.0), stroke=farge, sw=2.1)
    path((x + w - 1.0, y + 1.4, .05), (x + 1.2, y + 1.4, .05), (x + 1.2, y + d + .8, .05), (x + 1.2, y + d + .8, -.6), stroke='#a7b3c8', sw=3)
    poly((x + w - 2.3, y + .25, .5), (x + w - .5, y + .25, .5), (x + w - .5, y + .25, 1.6), (x + w - 2.3, y + .25, 1.6), fill='rgba(255,138,115,.3)', stroke=VARM, sw=1)  # bereder
    # Elektro: kurs fra sikringsskap på gavlen, opp og langs taket til lamper, ned til stikk
    poly((x, y + .6, 1.3), (x, y + 1.3, 1.3), (x, y + 1.3, 2.1), (x, y + .6, 2.1), fill='rgba(13,24,48,.6)', stroke=EL, sw=1)
    path((x, y + .95, 2.1), (x, y + .95, h - .15), (x + w - tw - .3, y + .95, h - .15), stroke=EL, sw=1.5, extra='stroke-dasharray="3 2.5"')
    for lx in (x + 2.0, x + 4.6):
        line((lx, y + .95, h - .15), (lx, y + .95, h - .9), stroke=EL, sw=1.1)
        sirkel(lx, y + .95, h - 1.05, 3, EL)
    for sx in (x + 3.2, x + 6.0):
        line((sx, y + .15, h - .15), (sx, y + .15, .7), stroke=EL, sw=1, extra='stroke-dasharray="2 2"')
        poly((sx - .22, y + .15, .5), (sx + .22, y + .15, .5), (sx + .22, y + .15, .9), (sx - .22, y + .15, .9), fill=EL, stroke='none')
    # taket står, fronten og gavlen er stiplet
    boks_med_saltak(x, y, w - tw, d, h, r, True, fill=('rgba(130,170,240,.38)', 'none', 'none'), sw=1.1, stroke='rgba(159,188,240,.8)')
    kw = dict(sw=1.1, extra='stroke-dasharray="4 4" opacity=".7"')
    path((x, y + d, 0), (x + w, y + d, 0), (x + w, y, 0), **kw)
    line((x + w, y + d, 0), (x + w, y + d, th), **kw)
    path((x + w - tw, y + d, h), (x + w - tw, y + d, th), (x + w, y + d, th), **kw)
    path((x + w - tw, y, th), (x + w - tw + tw / 2, y, th + tr), (x + w, y, th), **kw)
    line((x + w - tw + tw / 2, y, th + tr), (x + w - tw + tw / 2, y + d, th + tr), **kw)
    path((x + w - tw, y + d, th), (x + w - tw + tw / 2, y + d, th + tr), (x + w, y + d, th), **kw)

def fundament(x, y):
    """Byggegrop med forskaling, ferdig støpt plate og armeringsnett med oppstikk."""
    w, d, t = 7.5, 3.8, .45
    poly((x - .9, y - .9, 0), (x + w + .9, y - .9, 0), (x + w + .9, y + d + .9, 0), (x - .9, y + d + .9, 0), fill='rgba(60,50,40,.35)', stroke='rgba(159,188,240,.35)', sw=1)
    poly((x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, t), (x, y + d, t), fill='rgba(150,160,180,.4)')
    poly((x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, t), (x + w, y, t), fill='rgba(110,120,140,.45)')
    poly((x, y, t), (x + w, y, t), (x + w, y + d, t), (x, y + d, t), fill='rgba(170,180,200,.25)')
    for i in range(1, 8):
        line((x + w * i / 8, y + .2, t + .05), (x + w * i / 8, y + d - .2, t + .05), stroke='#c98d5b', sw=.8)
    for j in range(1, 5):
        line((x + .2, y + d * j / 5, t + .08), (x + w - .2, y + d * j / 5, t + .08), stroke='#c98d5b', sw=.8)
    for cx, cy in ((x + .4, y + .4), (x + w - .4, y + .4), (x + .4, y + d - .4), (x + w - .4, y + d - .4), (x + w / 2, y + .4)):
        line((cx, cy, t), (cx, cy, t + 1.3), stroke='#c98d5b', sw=1.4)
    # forskalingsbord langs fronten
    for i in range(3):
        line((x - .9, y + d + .9, .15 + i * .22), (x + w + .9, y + d + .9, .15 + i * .22), stroke=TRE, sw=1.1)


def brakke(x, y):
    """Byggebrakke (anleggskontor): lys container med dør, vindu og trapp."""
    w, d, h = 5.0, 2.4, 2.6
    skygge(x, y, w, d, .8)
    for z in (0,):
        poly((x, y + d, z), (x + w, y + d, z), (x + w, y + d, h), (x, y + d, h), fill='rgba(214,222,236,.55)', stroke='#d2dcf0', sw=1.2)
        poly((x + w, y, z), (x + w, y + d, z), (x + w, y + d, h), (x + w, y, h), fill='rgba(160,175,200,.6)', stroke='#d2dcf0', sw=1.2)
        poly((x, y, h), (x + w, y, h), (x + w, y + d, h), (x, y + d, h), fill='rgba(235,240,250,.7)', stroke='#d2dcf0', sw=1.2)
    for i in range(1, 5):   # riller i veggen
        line((x + w * i / 5, y + d, .1), (x + w * i / 5, y + d, h - .1), stroke='rgba(120,135,165,.5)', sw=.7)
    poly((x + .6, y + d, 0), (x + 1.5, y + d, 0), (x + 1.5, y + d, 2.0), (x + .6, y + d, 2.0), fill=ORANSJE, stroke='none')
    poly((x + 2.6, y + d, 1.0), (x + 4.2, y + d, 1.0), (x + 4.2, y + d, 2.0), (x + 2.6, y + d, 2.0), fill='rgba(13,24,48,.65)', stroke='#d2dcf0', sw=.9)
    line((x + .4, y + d + .9, .4), (x + 1.7, y + d + .9, .4), stroke=TRE, sw=1.4)   # trapp
    line((x + .4, y + d + .5, .2), (x + 1.7, y + d + .5, .2), stroke=TRE, sw=1.4)

def kran(x, y, hoyde, jib, last):
    """Tårnkran: gittermast, utligger med strekkstag, motvekt, førerhus og krok med limtrebjelke."""
    a = 1.1
    kw = dict(stroke='#d2dcf0', sw=1.3)
    for dx, dy in ((0, 0), (a, 0), (a, a), (0, a)):
        line((x + dx, y + dy, 0), (x + dx, y + dy, hoyde), **kw)
    z = 0.0
    while z < hoyde - .05:
        z2 = min(z + 1.1, hoyde)
        line((x, y + a, z), (x + a, y + a, z2), stroke='#d2dcf0', sw=.75)
        line((x + a, y, z), (x + a, y + a, z2), stroke='#d2dcf0', sw=.75)
        line((x, y + a, z2), (x + a, y + a, z2), stroke='#d2dcf0', sw=.6)
        line((x + a, y, z2), (x + a, y + a, z2), stroke='#d2dcf0', sw=.6)
        z = z2
    ym = y + a / 2
    # utligger (to gurter) fra motvekt til spiss, med gitter
    for dz in (0, .7):
        line((x - jib, ym, hoyde + dz), (x + 5.0, ym, hoyde + dz), **kw)
    for i in range(int((jib + 5) / 1.2)):
        sx = x - jib + i * 1.2
        line((sx, ym, hoyde), (sx + .6, ym, hoyde + .7), stroke='#d2dcf0', sw=.7)
        line((sx + .6, ym, hoyde + .7), (sx + 1.2, ym, hoyde), stroke='#d2dcf0', sw=.7)
    # tårnspiss og strekkstag
    line((x + a / 2, ym, hoyde), (x + a / 2, ym, hoyde + 3.2), **kw)
    line((x + a / 2, ym, hoyde + 3.2), (x - jib + .5, ym, hoyde + .7), stroke='#d2dcf0', sw=1)
    line((x + a / 2, ym, hoyde + 3.2), (x + 4.6, ym, hoyde + .7), stroke='#d2dcf0', sw=1)
    # motvekt og førerhus
    poly((x + 3.3, y - .1, hoyde - 1.1), (x + 5.0, y - .1, hoyde - 1.1), (x + 5.0, y - .1, hoyde), (x + 3.3, y - .1, hoyde), fill='rgba(150,160,180,.7)', sw=1)
    poly((x - .2, y + a + .05, hoyde - 1.3), (x + a + .2, y + a + .05, hoyde - 1.3), (x + a + .2, y + a + .05, hoyde - .1), (x - .2, y + a + .05, hoyde - .1), fill=ORANSJE, stroke='none')
    # løpekatt, vaier og last
    lx, ly, lz = last
    poly((lx - .4, ym - .2, hoyde), (lx + .4, ym - .2, hoyde), (lx + .4, ym + .2, hoyde), (lx - .4, ym + .2, hoyde), fill='#d2dcf0', stroke='none')
    line((lx, ym, hoyde), (lx, ym, lz + .6), stroke='#d2dcf0', sw=1)
    line((lx, ym, lz + .6), (lx - 1.8, ly, lz), stroke='#d2dcf0', sw=.8)
    line((lx, ym, lz + .6), (lx + 1.8, ly, lz), stroke='#d2dcf0', sw=.8)
    poly((lx - 2.4, ly - .25, lz - .3), (lx + 2.4, ly - .25, lz - .3), (lx + 2.4, ly + .25, lz - .3), (lx - 2.4, ly + .25, lz - .3), fill=TRE, stroke='#f3cf98', sw=1)
    poly((lx - 2.4, ly + .25, lz - .3), (lx + 2.4, ly + .25, lz - .3), (lx + 2.4, ly + .25, lz), (lx - 2.4, ly + .25, lz), fill='#c98d5b', stroke='#f3cf98', sw=1)

def totalstasjon(x, y, prisme):
    topp = (x, y, 1.9)
    for dx, dy in ((-1.0, -.3), (.8, -.7), (.3, 1.0)):
        line((x + dx, y + dy, 0), topp, stroke='#d2dcf0', sw=1.5)
    b, z0, z1 = .45, 1.9, 2.8
    poly((x - b, y + b, z0), (x + b, y + b, z0), (x + b, y + b, z1), (x - b, y + b, z1), fill=ORANSJE, stroke='#ffd0a0', sw=.8)
    poly((x + b, y - b, z0), (x + b, y + b, z0), (x + b, y + b, z1), (x + b, y - b, z1), fill='#c4701a', stroke='#ffd0a0', sw=.8)
    poly((x - b, y - b, z1), (x + b, y - b, z1), (x + b, y + b, z1), (x - b, y + b, z1), fill='#ffb866', stroke='#ffd0a0', sw=.8)
    px, py = prisme
    line((px, py, 0), (px, py, 2.4), stroke='#e8eef8', sw=1.5)
    sirkel(px, py, 2.4, 3.4, 'none', ORANSJE, 1.6)
    line((x, y, 2.35), (px, py, 2.4), stroke=ORANSJE, sw=1.1, extra='stroke-dasharray="5 4"')
    tekst(x + .5, y + .5, 0, 'N 60.795  Ø 10.692', size=8.5, fill='#d2dcf0', anchor='start', dy=15)

def maal_x(x0, x1, y, t):
    line((x0, y, 0), (x1, y, 0), stroke=ORANSJE, sw=1.1)
    for x in (x0, x1):
        line((x, y - .35, 0), (x, y + .35, 0), stroke=ORANSJE, sw=1.1)
        line((x, y - 1.2, 0), (x, y, 0), stroke=ORANSJE, sw=.6, extra='opacity=".6"')
    tekst((x0 + x1) / 2, y, 0, t, size=8.5, fill=ORANSJE, dy=12)
def maal_y(x, y0, y1, t):
    line((x, y0, 0), (x, y1, 0), stroke=ORANSJE, sw=1.1)
    for y in (y0, y1):
        line((x - .35, y, 0), (x + .35, y, 0), stroke=ORANSJE, sw=1.1)
        line((x - 1.2, y, 0), (x, y, 0), stroke=ORANSJE, sw=.6, extra='opacity=".6"')
    tekst(x, (y0 + y1) / 2, 0, t, size=8.5, fill=ORANSJE, anchor='start', dy=12)

def tre(x, y, h=3.0):
    sirkel(x + .5, y + .5, 0, h * 2.6, 'rgba(0,0,0,.22)')
    line((x, y, 0), (x, y, h * .5), stroke='#8a9bb8', sw=1.6)
    sirkel(x, y, h * .78, h * 3.6, 'rgba(111,191,143,.42)', '#8fd6a1', 1.2)
    sirkel(x - .35, y - .35, h * .92, h * 2.2, 'rgba(160,220,180,.35)')

# ---------- Tomt, tun og stier (tomta er 42 × 28 m, tunet midt på) ----------
poly((0, 0), (42, 0), (42, 28), (0, 28), fill='rgba(111,147,214,.06)', stroke='rgba(111,147,214,.35)', sw=1, extra='stroke-dasharray="4 5"')
TX, TY, TR = 21, 14, 4.2
tun = [(TX + TR * math.cos(math.radians(a)), TY + TR * math.sin(math.radians(a))) for a in range(0, 360, 45)]
for (x1, y1) in ((11, 4.5), (30, 7), (11, 14.5), (29, 19), (15, 22)):
    path((TX, TY), (x1, y1), stroke='rgba(159,188,240,.35)', sw=5)
    path((TX, TY), (x1, y1), stroke='rgba(111,147,214,.16)', sw=3.4)
poly(*tun, fill='rgba(111,147,214,.16)', stroke='rgba(159,188,240,.45)', sw=1)
for (gx, gy) in ((20, 13), (22.5, 15), (19.5, 15.5), (22, 12.5), (21, 16.2), (23.3, 13.8)):
    sirkel(gx, gy, 0, 1.1, 'rgba(159,188,240,.35)')
# benk og flaggstang på tunet
for i in range(3):
    line((19.6 + i * .25, 14.0, .45), (19.6 + i * .25, 15.4, .45), stroke=TRE, sw=1.3)
line((19.7, 14.1, 0), (19.7, 14.1, .45), stroke=TRE, sw=1); line((20.0, 15.3, 0), (20.0, 15.3, .45), stroke=TRE, sw=1)
line((TX, TY, 0), (TX, TY, 5.5), stroke='#e8eef8', sw=1.3)
poly((TX, TY, 5.5), (TX + 1.6, TY, 5.2), (TX, TY, 4.6), fill=ORANSJE, stroke='none')

# ---------- Bebyggelse, bakerst først ----------
tre(23, 1, 2.6)
mikrohus(3.5, 2.5, solceller=True)              # ferdig hus med solceller (elektro)
maal_x(3.5, 11, 7.4, '7 500'); maal_y(11.8, 2.5, 6.3, '3 800')
kran(38.5, 1.0, 14.5, 12.0, (30.5, 5.0, 7.4))    # kran bak, løfter en limtrebjelke inn over reisverket
bindingsverk(27, 3)
tre(1.5, 8.5, 2.6); tre(41, 9, 2.8)
snitt(3, 12.5)
mikrohus(27.5, 18.5, varmepumpe=True)   # ferdig hus med varmepumpe (VVS)
brakke(36.5, 16.5)
fundament(10, 21.5)
totalstasjon(34, 26, (20.5, 23))
tre(1, 26, 2.4); tre(16.5, 27.5, 2.2); tre(40.5, 26.5, 2.8)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       '<title>Studentlandsby under bygging</title>' + ''.join(ut) + '</svg>')
open(sys.argv[1], 'w', encoding='utf-8').write(svg)
print('skrevet', len(svg), 'tegn')
