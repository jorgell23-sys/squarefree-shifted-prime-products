#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draws the figures for the explainer page, as SVG, from the real data.

    python src/make_figures.py

Standard library only. SVG on purpose: it stays sharp at any zoom, prints well,
reads in light and dark themes, and -- unlike a bitmap -- every number in it can
be checked against `data/`, which is what `verify.py` does.

Output: docs/figures/*.svg
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shifted_primes as S  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "docs", "figures")

# A palette that survives both themes: mid-tone hues on a transparent ground,
# never pure black or pure white.
INK = "#1f2933"
MUTED = "#6b7785"
LINE = "#9aa5b1"
BLUE = "#2f6fb5"
GREEN = "#2e7d52"
AMBER = "#c8871a"
RED = "#c0442e"
FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,"
        "'Helvetica Neue',Arial,sans-serif")


def head(w, h, title, desc):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="100%%" role="img" aria-labelledby="t d">\n'
        '<title id="t">%s</title><desc id="d">%s</desc>\n'
        '<style>\n'
        '  text{font-family:%s;fill:%s}\n'
        '  .m{fill:%s}.s{font-size:13px}.xs{font-size:11px}\n'
        '  .lbl{font-size:14px;font-weight:600}\n'
        '  .big{font-size:20px;font-weight:700}\n'
        '  .mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}\n'
        '  @media (prefers-color-scheme:dark){\n'
        '    text{fill:#e4e7eb}.m{fill:#9aa5b1}\n'
        '    .stroke{stroke:#7b8794}\n'
        '  }\n'
        '</style>\n' % (w, h, title, desc, FONT, INK, MUTED))


def tail():
    return "</svg>\n"


def write(name, body):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("  " + os.path.relpath(path, HERE).replace("\\", "/"))


# --------------------------------------------------------------------------
# Figure 1: the recipe, on one worked example


def fig_recipe(b=7, n=15, es=False):
    ps = sorted(S.prime_factors(n))
    prod = 1
    for p in ps:
        prod *= (p + b)
    w, h = 760, 300
    T = {
        "title": ("La receta, con n = 15 y b = 7" if es
                  else "The recipe, with n = 15 and b = 7"),
        "desc": ("Se toman los primos de 15, se les suma 7, se multiplican, y "
                 "el resultado se divide por 15 sin resto." if es else
                 "Take the primes of 15, add 7 to each, multiply them, and the "
                 "result divides by 15 with no remainder."),
        "s1": "1. " + ("los primos de n" if es else "the primes of n"),
        "s2": "2. " + ("a cada uno le sumo b" if es else "add b to each"),
        "s3": "3. " + ("los multiplico" if es else "multiply them"),
        "s4": "4. " + ("¿divide n al resultado?" if es else "does n divide it?"),
        "yes": ("SÍ: 120 = 15 × 8" if es else "YES: 120 = 15 x 8"),
        "so": ("entonces 15 pertenece a S₇" if es
               else "so 15 belongs to S_7"),
    }
    o = [head(w, h, T["title"], T["desc"])]
    ys = 74
    xs = [90, 265, 445, 630]
    for i, s in enumerate(("s1", "s2", "s3", "s4")):
        o.append('<text class="xs m" x="%d" y="34" text-anchor="middle">%s</text>'
                 % (xs[i], T[s]))
    # step 1: n and its primes
    o.append('<text class="big" x="%d" y="%d" text-anchor="middle">15</text>'
             % (xs[0], ys))
    o.append('<text class="xs m" x="%d" y="%d" text-anchor="middle">= 3 x 5</text>'
             % (xs[0], ys + 20))
    for j, p in enumerate(ps):
        cy = 150 + j * 62
        o.append('<circle cx="%d" cy="%d" r="24" fill="none" stroke="%s" '
                 'stroke-width="2" class="stroke"/>' % (xs[0], cy, BLUE))
        o.append('<text class="lbl" x="%d" y="%d" text-anchor="middle">%d</text>'
                 % (xs[0], cy + 5, p))
    # step 2: +b
    for j, p in enumerate(ps):
        cy = 150 + j * 62
        o.append('<path d="M %d %d L %d %d" stroke="%s" stroke-width="2" '
                 'marker-end="url(#a)" class="stroke"/>'
                 % (xs[0] + 30, cy, xs[1] - 44, cy, LINE))
        o.append('<text class="xs" x="%d" y="%d" text-anchor="middle" '
                 'fill="%s">+7</text>' % ((xs[0] + xs[1]) // 2, cy - 8, GREEN))
        o.append('<rect x="%d" y="%d" width="72" height="40" rx="8" fill="none" '
                 'stroke="%s" stroke-width="2" class="stroke"/>'
                 % (xs[1] - 36, cy - 20, GREEN))
        o.append('<text class="lbl" x="%d" y="%d" text-anchor="middle">%d</text>'
                 % (xs[1], cy + 5, p + b))
    # step 3: product
    o.append('<text class="big" x="%d" y="%d" text-anchor="middle">%d</text>'
             % (xs[2], 186, prod))
    o.append('<text class="xs m" x="%d" y="%d" text-anchor="middle">'
             '10 x 12</text>' % (xs[2], 208))
    for j in range(len(ps)):
        cy = 150 + j * 62
        o.append('<path d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="2" '
                 'fill="none" marker-end="url(#a)" class="stroke"/>'
                 % (xs[1] + 40, cy, xs[2] - 40, cy, xs[2] - 26, 180, LINE))
    # step 4: divides
    o.append('<path d="M %d %d L %d %d" stroke="%s" stroke-width="2" '
             'marker-end="url(#a)" class="stroke"/>'
             % (xs[2] + 34, 180, xs[3] - 78, 180, LINE))
    o.append('<rect x="%d" y="%d" width="150" height="56" rx="10" fill="none" '
             'stroke="%s" stroke-width="2.5"/>' % (xs[3] - 72, 152, AMBER))
    o.append('<text class="lbl" x="%d" y="%d" text-anchor="middle" fill="%s">'
             '%s</text>' % (xs[3] + 3, 178, AMBER, T["yes"]))
    o.append('<text class="xs m" x="%d" y="%d" text-anchor="middle">%s</text>'
             % (xs[3] + 3, 198, T["so"]))
    o.append('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
             'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
             '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker></defs>' % LINE)
    o.append(tail())
    return "\n".join(o)


# --------------------------------------------------------------------------
# Figure 2: who covers whom


def fig_covering(es=False):
    w, h = 700, 260
    T = {
        "title": ("Quién cubre a quién" if es else "Who covers whom"),
        "desc": ("Cada primo tiene que aparecer en la suma de otro. Con b = 7, "
                 "3 cubre a 5 y 5 cubre a 3." if es else
                 "Every prime must show up in someone's sum. With b = 7, 3 "
                 "covers 5 and 5 covers 3."),
        "rule": ("REGLA: cada primo del número tiene que dividir a la suma de "
                 "alguno (puede ser la suya)"
                 if es else
                 "RULE: every prime of the number must divide someone's sum "
                 "(its own counts)"),
        "ok": ("15 = 3 x 5 SIRVE: nadie queda solo"
               if es else "15 = 3 x 5 WORKS: nobody is left out"),
        "bad": ("21 = 3 x 7 NO SIRVE: al 7 no lo cubre nadie"
                if es else "21 = 3 x 7 FAILS: nothing covers 7"),
        "c1": "3 + 7 = 10, " + ("y 5 divide a 10" if es else "and 5 divides 10"),
        "c2": "5 + 7 = 12, " + ("y 3 divide a 12" if es else "and 3 divides 12"),
        "c3": "3 + 7 = 10, 7 + 7 = 14",
        "c4": ("7 divide a 14, pero 3 no divide ni a 10 ni a 14"
               if es else "7 divides 14, but 3 divides neither 10 nor 14"),
    }
    o = [head(w, h, T["title"], T["desc"])]
    o.append('<text class="xs m" x="350" y="24" text-anchor="middle">%s</text>'
             % T["rule"])
    # left: works
    o.append('<text class="s" x="30" y="66" fill="%s" font-weight="600">%s</text>'
             % (GREEN, T["ok"]))
    for cx, val in ((90, 3), (250, 5)):
        o.append('<circle cx="%d" cy="120" r="26" fill="none" stroke="%s" '
                 'stroke-width="2.5" class="stroke"/>' % (cx, GREEN))
        o.append('<text class="lbl" x="%d" y="126" text-anchor="middle">%d</text>'
                 % (cx, val))
    o.append('<path d="M 118 108 Q 170 78 222 108" stroke="%s" stroke-width="2" '
             'fill="none" marker-end="url(#b)" class="stroke"/>' % GREEN)
    o.append('<path d="M 222 134 Q 170 164 118 134" stroke="%s" stroke-width="2" '
             'fill="none" marker-end="url(#b)" class="stroke"/>' % GREEN)
    o.append('<text class="xs m" x="30" y="192">%s</text>' % T["c1"])
    o.append('<text class="xs m" x="30" y="210">%s</text>' % T["c2"])
    # right: fails
    o.append('<text class="s" x="400" y="66" fill="%s" font-weight="600">%s</text>'
             % (RED, T["bad"]))
    o.append('<circle cx="450" cy="120" r="26" fill="none" stroke="%s" '
             'stroke-width="2.5" stroke-dasharray="4 3" class="stroke"/>' % RED)
    o.append('<text class="lbl" x="450" y="126" text-anchor="middle">3</text>')
    o.append('<circle cx="610" cy="120" r="26" fill="none" stroke="%s" '
             'stroke-width="2.5" class="stroke"/>' % LINE)
    o.append('<text class="lbl" x="610" y="126" text-anchor="middle">7</text>')
    o.append('<path d="M 636 100 a 26 26 0 1 1 -20 -6" stroke="%s" '
             'stroke-width="2" fill="none" marker-end="url(#b)" class="stroke"/>'
             % LINE)
    o.append('<text class="big" x="450" y="88" text-anchor="middle" fill="%s">'
             '?</text>' % RED)
    o.append('<text class="xs m" x="400" y="192">%s</text>' % T["c3"])
    o.append('<text class="xs m" x="400" y="210">%s</text>' % T["c4"])
    o.append('<defs><marker id="b" viewBox="0 0 10 10" refX="9" refY="5" '
             'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
             '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker></defs>' % LINE)
    o.append(tail())
    return "\n".join(o)


# --------------------------------------------------------------------------
# Figure 3: the counts, and the jump that was not there


def fig_counts(rows, es=False):
    top = 63
    vals = [(r["b"], r["size"]) for r in rows if r["b"] <= top]
    w, h = 760, 372
    #: `pad_b` es grande a proposito: las tres aclaraciones van DEBAJO del eje y
    #: no flotando sobre las barras. La primera version las ponia encima con un
    #: desplazamiento fijo hacia arriba, y sobre la barra mas alta -b = 63, que
    #: es el maximo y por lo tanto toca el techo- la etiqueta caia en y = -2, o
    #: sea fuera del lienzo. Una figura no puede depender de que ningun dato sea
    #: el maximo.
    pad_l, pad_b, pad_t, pad_r = 56, 108, 34, 20
    gw, gh = w - pad_l - pad_r, h - pad_t - pad_b
    mx = max(v for _, v in vals)
    T = {
        "title": ("Cuántos hay, para cada b" if es
                  else "How many there are, for each b"),
        "desc": ("La barra de b = 55 parecía un salto, pero b = 39 y b = 63 ya "
                 "son altas: sólo faltaba mirar el medio." if es else
                 "The bar at b = 55 looked like a jump, but b = 39 and b = 63 "
                 "are high too: the middle had simply never been looked at."),
        "y": ("cuántos números hay en S" if es else "how many numbers in S"),
        "x": "b",
        "note55": ("55: el que parecía un salto" if es
                   else "55: the one that looked like a jump"),
        "note39": ("39: ya era alto" if es else "39: already high"),
        "note63": ("63: más alto todavía" if es else "63: higher still"),
    }
    o = [head(w, h, T["title"], T["desc"])]
    o.append('<text class="xs m" x="%d" y="%d" text-anchor="middle" '
             'transform="rotate(-90 14 %d)">%s</text>'
             % (14, pad_t + gh // 2, pad_t + gh // 2, T["y"]))
    o.append('<text class="xs m" x="%d" y="%d" text-anchor="middle">%s</text>'
             % (pad_l + gw // 2, h - 10, T["x"]))
    # axis
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
             'stroke-width="1.5" class="stroke"/>'
             % (pad_l, pad_t + gh, pad_l + gw, pad_t + gh, LINE))
    for frac in (0, 0.5, 1.0):
        yy = pad_t + gh - frac * gh
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                 'stroke-width="1" stroke-dasharray="3 4" opacity="0.5" '
                 'class="stroke"/>' % (pad_l, yy, pad_l + gw, yy, LINE))
        o.append('<text class="xs m" x="%d" y="%.1f" text-anchor="end">%d</text>'
                 % (pad_l - 8, yy + 4, int(frac * mx)))
    bw = gw / len(vals)
    for i, (bv, sv) in enumerate(vals):
        x = pad_l + i * bw
        bh = gh * sv / mx
        col = AMBER if bv == 55 else (GREEN if bv in (39, 63) else BLUE)
        op = "1" if bv in (39, 55, 63) else "0.5"
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                 'fill="%s" opacity="%s"/>'
                 % (x + 1.5, pad_t + gh - bh, bw - 3, bh, col, op))
        if bv % 10 == 1 or bv in (39, 55, 63):
            o.append('<text class="xs m" x="%.1f" y="%d" text-anchor="middle">'
                     '%d</text>' % (x + bw / 2, pad_t + gh + 16, bv))
    def xat(bv):
        for i, (v, _) in enumerate(vals):
            if v == bv:
                return pad_l + i * bw + bw / 2
        return 0
    # el valor, encima de la barra o adentro si la barra llega al techo
    for bv in (39, 55, 63):
        sv = dict(vals)[bv]
        yy = pad_t + gh - gh * sv / mx
        col = AMBER if bv == 55 else GREEN
        if yy - pad_t < 18:
            o.append('<text class="xs" x="%.1f" y="%.1f" text-anchor="middle" '
                     'fill="#fff" font-weight="700">%d</text>'
                     % (xat(bv), yy + 16, sv))
        else:
            o.append('<text class="xs" x="%.1f" y="%.1f" text-anchor="middle" '
                     'fill="%s" font-weight="700">%d</text>'
                     % (xat(bv), yy - 6, col, sv))
    # y las aclaraciones, debajo del eje, en su propia franja
    ly = pad_t + gh + 40
    for i, (bv, key) in enumerate(((39, "note39"), (55, "note55"),
                                   (63, "note63"))):
        col = AMBER if bv == 55 else GREEN
        yy = ly + i * 20
        o.append('<rect x="%d" y="%.1f" width="10" height="10" rx="2" '
                 'fill="%s"/>' % (pad_l, yy - 9, col))
        o.append('<text class="xs" x="%d" y="%.1f" fill="%s">%s</text>'
                 % (pad_l + 18, yy, col, T[key]))
    o.append(tail())
    return "\n".join(o)


# --------------------------------------------------------------------------
# Figure 4: the clock


def fig_clock(n=6, es=False):
    ok = sorted(S.residue_classes(n))
    w, h = 560, 300
    cx, cy, r = 150, 155, 92
    T = {
        "title": ("El reloj de 6" if es else "The clock of 6"),
        "desc": ("Que 6 pertenezca sólo depende del resto de b al dividir por "
                 "6: sirven 0, 1, 3 y 4." if es else
                 "Whether 6 belongs depends only on the remainder of b modulo "
                 "6: 0, 1, 3 and 4 work."),
        "hd": ("Sólo importa el RESTO de b al dividir por 6"
               if es else "Only the REMAINDER of b modulo 6 matters"),
        "l1": ("verde = b con ese resto SIRVE" if es
               else "green = a b with that remainder WORKS"),
        "l2": ("b = 1, 7, 13, 19, 25 ... todos dejan resto 1"
               if es else "b = 1, 7, 13, 19, 25 ... all leave remainder 1"),
        "l3": ("y los cinco sirven, sin excepción"
               if es else "and all five work, with no exception"),
        "l4": ("4 de los 6 restos sirven" if es else "4 of the 6 remainders work"),
    }
    o = [head(w, h, T["title"], T["desc"])]
    o.append('<text class="xs m" x="150" y="26" text-anchor="middle">%s</text>'
             % T["hd"])
    o.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" '
             'stroke-width="1.5" opacity="0.6" class="stroke"/>' % (cx, cy, r, LINE))
    import math
    for k in range(n):
        ang = -math.pi / 2 + 2 * math.pi * k / n
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        good = k in ok
        o.append('<circle cx="%.1f" cy="%.1f" r="21" fill="none" stroke="%s" '
                 'stroke-width="%s" class="stroke"/>'
                 % (x, y, GREEN if good else LINE, "2.5" if good else "1.5"))
        o.append('<text class="lbl" x="%.1f" y="%.1f" text-anchor="middle" '
                 'opacity="%s">%d</text>' % (x, y + 5, "1" if good else "0.45", k))
    o.append('<text class="s" x="%d" y="%d" text-anchor="middle" fill="%s" '
             'font-weight="600">%s</text>' % (cx, cy + 6, GREEN, T["l4"]))
    x0 = 300
    o.append('<text class="xs" x="%d" y="96" fill="%s">%s</text>'
             % (x0, GREEN, T["l1"]))
    o.append('<text class="xs m" x="%d" y="146">%s</text>' % (x0, T["l2"]))
    o.append('<text class="xs m" x="%d" y="168">%s</text>' % (x0, T["l3"]))
    o.append('<text class="s mono" x="%d" y="212" fill="%s">6 | (2+b)(3+b)</text>'
             % (x0, BLUE))
    o.append('<text class="xs m" x="%d" y="232">b = 0, 1, 3, 4 (mod 6)</text>' % x0)
    o.append(tail())
    return "\n".join(o)


def main():
    with open(os.path.join(HERE, "data", "counts.json")) as fh:
        rows = json.load(fh)
    print("figures:")
    for es, suf in ((False, ""), (True, ".es")):
        write("recipe%s.svg" % suf, fig_recipe(es=es))
        write("covering%s.svg" % suf, fig_covering(es=es))
        write("counts%s.svg" % suf, fig_counts(rows, es=es))
        write("clock%s.svg" % suf, fig_clock(es=es))


if __name__ == "__main__":
    main()
