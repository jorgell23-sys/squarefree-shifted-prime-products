#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every claim in RESULT.md, checked. One command, no dependencies.

    python verify.py

Exit code 0 if everything passes, 1 otherwise.
"""
import json
import os
import re
import sys
from math import gcd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import shifted_primes as S  # noqa: E402

FAILED = []
PASSED = 0


def check(cond, label):
    global PASSED
    print(("PASS  " if cond else "FAIL  ") + label)
    if cond:
        PASSED += 1
    else:
        FAILED.append(label)


def data(name):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "data", name)) as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
def external_control():
    """The control that is cross-checked against published work.

    OEIS A187778, "Numbers k dividing psi(k)" (Dedekind psi), states that the
    terms are 1 together with the numbers 2^i * 3^j, i,j >= 1. We recompute it
    from scratch and compare. The only squarefree term above 1 is 6, which is
    exactly our S_1 -- so a bug that inflated or emptied S_b would show here
    against a sequence we did not produce.
    """
    print("\n== external control: OEIS A187778, recomputed ==")
    ours = []
    for k in range(1, 20001):
        psi = k
        for p in S.prime_factors(k):
            psi = psi // p * (p + 1)
        if psi % k == 0:
            ours.append(k)
    published = [1]
    for i in range(1, 20):
        for j in range(1, 20):
            v = (2 ** i) * (3 ** j)
            if v <= 20000:
                published.append(v)
    published.sort()
    check(ours == published,
          "k | psi(k) for k <= 20000 is exactly {1} u {2^i 3^j}: %d terms"
          % len(ours))
    check([k for k in ours if k > 1 and S.is_squarefree(k)] == [6],
          "its only squarefree term above 1 is 6")
    check(S.members(1) == [6],
          "and S_1 = {6}, the classical result on n | sigma(n)")


def theorem_A():
    print("\n== Theorem A: membership depends only on b mod n ==")
    bad = []
    seen = 0
    for n in range(2, 1001):
        if not S.is_squarefree(n):
            continue
        seen += 1
        cls = S.residue_classes(n)
        if len(cls) != S.class_count(n):
            bad.append(("count", n))
        for b in sorted(cls)[:3]:
            if not (S.in_S(n, b) and S.in_S(n, b + n) and S.in_S(n, b + 7 * n)):
                bad.append(("period", n, b))
        P = sorted(S.prime_factors(n))
        if len(P) == 2 and S.two_prime_class(*P) not in cls:
            bad.append(("phi-1", n))
    check(not bad, "%d squarefree n <= 1000: class count = prod_p #{q mod p}, "
                   "period n, and phi(n)-1 is a class (%d failures)"
                   % (seen, len(bad)))
    check(S.class_count(6) == 4 and S.class_count(30) == 12
          and S.class_count(105) == 27 and S.class_count(210) == 72,
          "N(6)=4, N(30)=12, N(105)=27, N(210)=72")


def two_primes():
    print("\n== two prime factors: closed form ==")
    ps = S.primes_up_to(60)
    bad = []
    for b in range(1, 120, 2):
        for i, p in enumerate(ps):
            for q in ps[i + 1:]:
                if S.in_S(p * q, b) != ((b * (b + p + q)) % (p * q) == 0):
                    bad.append((b, p, q))
    check(not bad, "pq in S_b <=> pq | b(b+p+q)  (%d failures)" % len(bad))

    bad = []
    for b in range(1, 200, 2):
        for i, p in enumerate(ps):
            if p > 50:
                break
            for q in ps[i + 1:]:
                if q > 50:
                    break
                n = p * q
                if b % p == 0 or b % q == 0:
                    continue
                if S.in_S(n, b) != (b % n == (S.totient(n) - 1) % n):
                    bad.append((b, p, q))
    check(not bad, "and with no loop <=> b = phi(n) - 1 (mod n)  (%d failures)"
          % len(bad))

    bad = []
    for b in range(1, 400, 2):
        cap = S.bound(b)
        direct = set()
        prs = S.primes_up_to(cap)
        for i, p in enumerate(prs):
            for q in prs[i + 1:]:
                if S.in_S(p * q, b) and b % p and b % q:
                    direct.add((p, q))
        if direct != S.two_prime_members(b):
            bad.append(b)
    check(not bad, "and (up-1)(uq-1) = ub+1 finds exactly those, for the 200 "
                   "odd b < 400, by factoring ub+1 instead of walking primes")


def lemma_B():
    print("\n== Lemma B: every prime of every element is <= b+2 ==")
    bad = []
    for b in range(1, 160, 2):
        if S.bound(b) > b + 2:
            bad.append(b)
    check(not bad, "C(b) <= b+2 for every odd b < 160")
    bad = []
    for b in range(1, 46, 2):
        for n in S.members(b):
            if max(S.prime_factors(n)) > b + 2:
                bad.append((b, n))
    check(not bad, "and no element of S_b exceeds it (complete lists, b < 46)")


def counting():
    print("\n== the exact counter agrees with brute force ==")
    bad = []
    for b in range(1, 70, 2):
        ent = S.predecessors(b, S.bound(b))
        if S.count(ent) != S.count_brute_force(ent):
            bad.append(b)
    check(not bad, "35 values of b, model counting vs 2^n enumeration")
    bad = [b for b in range(1, 46, 2) if S.size(b) != len(S.members(b))]
    check(not bad, "and with the explicit complete list, 23 values")


def published_table():
    print("\n== the published table reproduces ==")
    rows = data("counts.json")
    bad = [r["b"] for r in rows if r["b"] <= 63 and S.size(r["b"]) != r["size"]]
    check(not bad, "data/counts.json matches recomputation for b <= 63")
    by_b = {r["b"]: r["size"] for r in rows}
    check([by_b[b] for b in (1, 3, 5, 7, 9, 11)] == [1, 4, 6, 8, 8, 12],
          "the six values that opened the question: 1, 4, 6, 8, 8, 12")
    check(by_b[55] == 220, "and |S_55| = 220")

    print("\n== there is no jump at b = 55 ==")
    between = {b: by_b[b] for b in range(13, 55, 2)}
    check(max(between.values()) >= 90,
          "b = 39 already gives %d, before b = 55" % between[39])
    check(by_b[63] > by_b[55],
          "and |S_63| = %d > 220 = |S_55|" % by_b[63])
    check(by_b[61] == 24 and by_b[63] == 274,
          "consecutive odd b with the same pi give 24 and 274: not a function "
          "of pi(b)")


def structure():
    print("\n== structure: closed under lcm, so there is a maximum ==")
    bad = []
    for b in (3, 5, 7, 15, 21, 55):
        ns = S.members(b)
        st = set(ns)
        for x in ns:
            for y in ns:
                if x * y // gcd(x, y) not in st:
                    bad.append((b, x, y))
        top = max(ns)
        if any(top % x for x in ns):
            bad.append(("not a maximum", b))
    check(not bad, "lcm-closed and every element divides the largest")

    bad = []
    for b in range(1, 200, 2):
        for p in S.prime_factors(b + 2):
            if not S.in_S(2 * p, b):
                bad.append((b, p))
        for p in S.prime_factors(b):
            if not S.in_S(p, b):
                bad.append((b, p))
    check(not bad, "2p in S_b for every p | b+2, and p in S_b for every p | b")


def explainer():
    """The explainer page cannot go stale in silence.

    Every live number in `docs/*.html` is tagged `data-fact="..."`, and this
    compares each one against the recomputed data. The figures are compared
    against what their generator produces right now, character for character.
    So if a datum improves and the explanation is not updated, THIS FAILS --
    which is the whole point: a rule written in prose gets broken again.
    """
    print("")
    print("== the explainer page is in sync with the data ==")
    here = os.path.dirname(os.path.abspath(__file__))
    rows = data("counts.json")
    by_b = {r["b"]: r["size"] for r in rows}
    expected = {
        "odd_b_count": len(rows),
        "max_b": rows[-1]["b"],
        "classes_210": S.class_count(210),
        "size_55": by_b[55],
        "size_39": by_b[39],
        "size_63": by_b[63],
    }
    pages = [os.path.join("docs", "index.html"),
             os.path.join("docs", "es", "index.html")]
    for page in pages:
        path = os.path.join(here, page)
        if not os.path.exists(path):
            check(False, "%s exists" % page)
            continue
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        facts = dict(re.findall(r'data-fact="([a-z_0-9]+)">([^<]+)<', html))
        wrong = {k: (facts.get(k), str(v)) for k, v in expected.items()
                 if facts.get(k) != str(v)}
        check(not wrong, "%s: every tagged number matches the data%s"
              % (page, "" if not wrong else " -- %s" % wrong))
        missing = [src for src in re.findall(r'<img src="([^"]+)"', html)
                   if not os.path.exists(os.path.normpath(
                       os.path.join(os.path.dirname(path), src)))]
        check(not missing, "%s: every figure it references exists%s"
              % (page, "" if not missing else " -- missing %s" % missing))

    sys.path.insert(0, os.path.join(here, "src"))
    import make_figures as MF
    stale = []
    for name, fn in (("recipe", MF.fig_recipe), ("covering", MF.fig_covering),
                     ("clock", MF.fig_clock)):
        for es, suf in ((False, ""), (True, ".es")):
            f = os.path.join(here, "docs", "figures", "%s%s.svg" % (name, suf))
            if not os.path.exists(f):
                stale.append(os.path.basename(f))
                continue
            with open(f, encoding="utf-8") as fh:
                if fh.read() != fn(es=es):
                    stale.append(os.path.basename(f))
    for es, suf in ((False, ""), (True, ".es")):
        f = os.path.join(here, "docs", "figures", "counts%s.svg" % suf)
        if not os.path.exists(f):
            stale.append(os.path.basename(f))
            continue
        with open(f, encoding="utf-8") as fh:
            if fh.read() != MF.fig_counts(rows, es=es):
                stale.append(os.path.basename(f))
    check(not stale, "the 8 figures are what their generator produces today%s"
          % ("" if not stale else " -- stale: %s" % stale))


#: Las seis partes de la portada, por su ancla. Este control vive **dentro del
#: repositorio** a proposito: un estandar que solo comprueba la herramienta que
#: publica se rompe en cuanto alguien edita el README despues de publicar, o
#: clona el repo y lo modifica. Aca falla donde sea que este.
FRONT_PAGE_PARTS = (
    ("hallazgo:que", "what was found, in one sentence"),
    ("hallazgo:enunciado", "the exact statement"),
    ("hallazgo:ejemplo", "the smallest case, with numbers"),
    ("hallazgo:prueba", "why it is proved"),
    ("hallazgo:comprobar", "the command that checks it"),
    ("hallazgo:nodice", "what it does not say"),
)


def front_page():
    """The front page states the finding, in six parts, before anything else.

    A reader who opens this repository must be able to say what was found and
    why it is true without scrolling past the first screen. That is a rule
    about the artifact, so it is checked by the artifact.

    What is required, and why each item: the six parts, in order, at the top;
    no version history before them (the change log is real and goes at the end,
    but in front it takes the result's place); at least three numerals in the
    example, because a finding is shown happening rather than described; and an
    executable command in the check part, because otherwise "verifiable" is a
    word.
    """
    print("\n== front page: the finding, in six parts, before anything else ==")
    here = os.path.dirname(os.path.abspath(__file__))
    historia = re.compile(
        r"(what changed in version|qu[e\u00e9] cambi[o\u00f3] en la versi[o\u00f3]n|"
        r"version \d|versi[o\u00f3]n \d|release \d)", re.I)
    leccion = re.compile(
        r"(la regla que sale|the rule that comes out|the rule this leaves|"
        r"lo que esto ense[n\u00f1]a|what this teaches|the lesson)", re.I)
    for name in ("README.md", "README.es.md", "RESULT.md"):
        path = os.path.join(here, name)
        if not os.path.exists(path):
            check(False, "%s exists" % name)
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        at = [text.find("<!-- %s -->" % a) for a, _ in FRONT_PAGE_PARTS]
        missing = [q for (a, q), i in zip(FRONT_PAGE_PARTS, at) if i < 0]
        if not check(not missing, "%s: has all six parts%s"
                     % (name, "" if not missing else " -- missing %s" % missing)):
            continue
        check(at == sorted(at), "%s: the six parts are in order" % name)
        head = text[: at[0]]
        check(len(head.splitlines()) <= 12,
              "%s: the finding is at the top (line %d)"
              % (name, len(head.splitlines()) + 1))
        m = historia.search(head)
        check(m is None, "%s: no version history before the finding%s"
              % (name, "" if m is None else " -- found %r" % m.group(0)))
        numerals = len(re.findall(r"\d[\d.,]{2,}", text[at[2]:at[3]]))
        check(numerals >= 3,
              "%s: the example carries numbers (%d found)" % (name, numerals))
        checkpart = text[at[4]:at[5]]
        check("```" in checkpart or "\n    " in checkpart,
              "%s: the check part carries an executable command" % name)
        m = leccion.search(text)
        check(m is None, "%s: no methodological aside%s"
              % (name, "" if m is None else " -- found %r" % m.group(0)))


def main():
    external_control()
    lemma_B()
    theorem_A()
    two_primes()
    counting()
    published_table()
    structure()
    explainer()
    front_page()
    #: **Autorreferencial a propósito.** La página anuncia cuántos controles
    #: corre este archivo; si se agrega uno y no se actualiza el texto, la
    #: cuenta deja de cerrar y la verificación falla. Se mide al final, con el
    #: total ya conocido, sumando los que este mismo bloque va a agregar.
    total = PASSED + len(FAILED) + 2
    here = os.path.dirname(os.path.abspath(__file__))
    for page in (os.path.join("docs", "index.html"),
                 os.path.join("docs", "es", "index.html")):
        path = os.path.join(here, page)
        if not os.path.exists(path):
            check(False, "%s exists" % page)
            continue
        with open(path, encoding="utf-8") as fh:
            m = re.search(r'data-fact="checks">([^<]+)<', fh.read())
        check(m is not None and int(m.group(1)) == total,
              "%s: the number of checks it announces is right (%s, expected %d)"
              % (page, m.group(1) if m else "absent", total))
    print("\n%d passed, %d failed" % (PASSED, len(FAILED)))
    for f in FAILED:
        print("  - " + f)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
