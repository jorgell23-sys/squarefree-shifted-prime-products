# -*- coding: utf-8 -*-
"""Squarefree integers n dividing the product of their shifted prime divisors.

    S_b = { n squarefree : n | prod_{p | n} (p + b) }

For b = 1 this is `n | sigma(n)` restricted to squarefree n (since sigma(n) =
prod (p+1) there), and for b = -1 it is `n | phi(n)`.

Standard library only. No third-party imports, on purpose: the whole point is
that `verify.py` runs anywhere.

Author: Jorge Ellena Godoy.
"""
from itertools import combinations


# ---------------------------------------------------------------- primes


def primes_up_to(m):
    """Sieve of Eratosthenes."""
    if m < 2:
        return []
    sieve = bytearray([1]) * (m + 1)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= m:
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        i += 1
    return [i for i in range(2, m + 1) if sieve[i]]


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_factors(n):
    """The set of distinct primes dividing n. Trial division, no deps."""
    if n <= 1:
        return set()
    out, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.add(n)
    return out


def is_squarefree(n):
    if n < 1:
        return False
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d += 1 if d == 2 else 2
    return True


def totient(n):
    r = n
    for p in prime_factors(n):
        r = r // p * (p - 1)
    return r


# ------------------------------------------------- membership, directly


def in_S(n, b):
    """n | prod_{p|n} (p+b). The definition, used as ground truth."""
    prod = 1
    for p in prime_factors(n):
        prod *= (p + b)
    return n > 0 and prod % n == 0


# ------------------------------------------------------- Theorem A


def residue_classes(n):
    """The b mod n for which n is in S_b, computed by brute force over b.

    Ground truth for `class_count`.
    """
    P = sorted(prime_factors(n))
    return {b for b in range(n)
            if all(any((q + b) % p == 0 for q in P) for p in P)}


def class_count(n):
    """Theorem A: prod over p|n of #{q mod p : q | n}."""
    P = sorted(prime_factors(n))
    r = 1
    for p in P:
        r *= len({q % p for q in P})
    return r


def two_prime_class(p, q):
    """phi(pq) - 1 mod pq: the class using no loop."""
    return ((p - 1) * (q - 1) - 1) % (p * q)


# --------------------------------------------- the bound, for odd b > 0


def bound(b):
    """C(b) = max(D_f union L_f). Lemma B gives C(b) <= b + 2.

    D = {b+2 if prime} union {p <= b : (-b) mod p is prime and < p}
    L = {p : p | b}
    """
    if b <= 0 or b % 2 == 0:
        raise ValueError("this lemma is for positive odd b")
    D = set()
    if is_prime(b + 2):
        D.add(b + 2)
    for p in primes_up_to(b):
        r = (-b) % p
        if r and r < p and is_prime(r):
            D.add(p)
    L = {p for p in primes_up_to(b) if b % p == 0}
    u = D | L
    return max(u) if u else 0


# ------------------------------------------------------- the digraph


def predecessors(b, cap):
    """p -> {q prime <= cap : p | q + b}."""
    ps = primes_up_to(cap)
    ent = {p: set() for p in ps}
    for q in ps:
        for p in prime_factors(q + b):
            if p in ent:
                ent[p].add(q)
    return {p: frozenset(v) for p, v in ent.items()}


def kernel(ent):
    """Drop, repeatedly, every vertex with no available predecessor."""
    alive = set(ent)
    while True:
        dead = {p for p in alive if not (ent[p] & alive)}
        if not dead:
            break
        alive -= dead
    return {p: (ent[p] & alive) for p in sorted(alive)}


# ------------------------------------------------ exact count, no enumeration


def _components(free, hard, cl):
    parent = {v: v for v in free}

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = root(a), root(b)
        if ra != rb:
            parent[ra] = rb

    for d in hard:
        it = iter(d)
        first = next(it)
        for x in it:
            union(first, x)
    for v in free:
        for u in cl[v]:
            if u in free and u != v:
                union(v, u)
    blocks = {}
    for v in free:
        blocks.setdefault(root(v), set()).add(v)
    return list(blocks.values())


def _assign(u, val, free, presat, hard, cl):
    satisfied = (u in presat) or (u in cl[u])
    free = set(free) - {u}
    presat = set(presat) - {u}
    if val:
        hard = {d for d in hard if u not in d}
        if not satisfied:
            new = frozenset(set(cl[u]) & free)
            if not new:
                return free, presat, hard, False
            hard = set(hard)
            hard.add(new)
        for w in free:
            if u in cl[w]:
                presat.add(w)
    else:
        fresh = set()
        for d in hard:
            e = d - {u}
            if not e:
                return free, presat, hard, False
            fresh.add(e)
        hard = fresh
    return free, presat, hard, True


def _solve(free, presat, hard, cl, cache):
    free, presat, hard = set(free), set(presat) & set(free), set(hard)
    changed = True
    while changed:
        changed = False
        for d in hard:
            if not d:
                return 0
        unit = next((d for d in hard if len(d) == 1), None)
        if unit is not None:
            u = next(iter(unit))
            free, presat, hard, good = _assign(u, True, free, presat, hard, cl)
            if not good:
                return 0
            changed = True
            continue
        for v in list(free):
            if v in presat or v in cl[v]:
                continue
            if not (set(cl[v]) & free):
                free, presat, hard, good = _assign(v, False, free, presat,
                                                   hard, cl)
                if not good:
                    return 0
                changed = True
                break
    if not free:
        return 0 if hard else 1
    blocks = _components(free, hard, cl)
    if len(blocks) > 1:
        r = 1
        for bl in blocks:
            sub = frozenset(d for d in hard if d & bl)
            r *= _solve(frozenset(bl), frozenset(presat & bl), sub, cl, cache)
            if r == 0:
                return 0
        return r
    key = (frozenset(free), frozenset(presat), frozenset(hard))
    if key in cache:
        return cache[key]
    v = max(free, key=lambda x: len(set(cl[x]) & free))
    r = 0
    for val in (False, True):
        f2, p2, h2, good = _assign(v, val, set(free), set(presat), set(hard), cl)
        if good:
            r += _solve(f2, p2, h2, cl, cache)
    cache[key] = r
    return r


def count(ent):
    """How many non-empty P have no source in the induced subdigraph."""
    ent = kernel(ent)
    if not ent:
        return 0
    vs = sorted(ent)
    idx = {p: i for i, p in enumerate(vs)}
    cl = [frozenset(idx[u] for u in ent[p]) for p in vs]
    total = _solve(frozenset(range(len(vs))), frozenset(), frozenset(), cl, {})
    return total - 1


def count_brute_force(ent):
    """The control for `count`: walks all 2^n subsets."""
    vs = sorted(ent)
    idx = {p: i for i, p in enumerate(vs)}
    pred = [sum(1 << idx[u] for u in ent[p]) for p in vs]
    n = len(vs)
    total = 0
    for m in range(1, 1 << n):
        good = True
        for i in range(n):
            if (m >> i) & 1 and not (pred[i] & m):
                good = False
                break
        if good:
            total += 1
    return total


def size(b):
    """|S_b| for odd b > 0, without enumerating subsets."""
    return count(predecessors(b, bound(b)))


def members(b):
    """The complete list of S_b. Exhaustive over all of N, not a search."""
    c = bound(b)
    ps = primes_up_to(c)
    H = {q: prime_factors(q + b) for q in ps}
    out = []
    for k in range(1, len(ps) + 1):
        for P in combinations(ps, k):
            s = set(P)
            covered = set()
            for q in P:
                covered |= (H[q] & s)
            if covered == s:
                n = 1
                for q in P:
                    n *= q
                out.append(n)
    return sorted(out)


def two_prime_members(b, u_max=None):
    """Pairs {p,q} with p,q coprime to b, via (u*p-1)(u*q-1) = u*b+1.

    Does not walk primes: walks u and factors u*b+1.
    """
    if u_max is None:
        u_max = (b + 6) // 6 + 2
    out = set()
    for u in range(1, u_max + 1):
        N = u * b + 1
        d = 1
        while d * d <= N:
            if N % d == 0:
                for A in (d, N // d):
                    B = N // A
                    if A > B:
                        continue
                    if (A + 1) % u or (B + 1) % u:
                        continue
                    p, q = (A + 1) // u, (B + 1) // u
                    if p == q or p < 2 or q < 2:
                        continue
                    if not (is_prime(p) and is_prime(q)):
                        continue
                    if b % p == 0 or b % q == 0:
                        continue
                    out.add((min(p, q), max(p, q)))
            d += 1
    return out
