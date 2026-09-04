#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every claim in RESULT.md, checked. One command, no dependencies.

    python verify.py

Exit code 0 if everything passes, 1 otherwise.
"""
import json
import os
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


def main():
    external_control()
    lemma_B()
    theorem_A()
    two_primes()
    counting()
    published_table()
    structure()
    print("\n%d passed, %d failed" % (PASSED, len(FAILED)))
    for f in FAILED:
        print("  - " + f)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
