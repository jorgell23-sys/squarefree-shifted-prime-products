# -*- coding: utf-8 -*-
"""The effective universe E(b), and the bound that holds for every b.

Standard library only, no dependencies.

For an integer b and a squarefree n > 1 with prime set P,

    n | prod_{p in P} (p + b)

holds if and only if, in the digraph H_b whose arrows are q -> p whenever
p | q + b, the subdigraph induced by P **has no source**: every prime in P has
a predecessor inside P.

Three sets are computed here:

* ``bound_C(b)``  -- for odd b, the proved bound: every prime of every solution
  is at most C(b) <= b + 2.
* ``first_round`` -- the primes with at least one predecessor in the universe.
* ``core``        -- the **effective universe** E(b): what is left after
  repeatedly deleting primes with no surviving predecessor. It is the largest
  source-free set, its product is the largest element of S_b, and every element
  of S_b divides it.
"""


def sieve(n):
    """Return a bytearray ``s`` of length n+1 with s[i] = 1 iff i is prime."""
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if s[i]:
            s[i * i:: i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1
    return s


def primes_up_to(n, s=None):
    s = s or sieve(n)
    return [i for i in range(2, n + 1) if s[i]]


def bound_C(b, s=None):
    """C(b) = max(D u L) for odd b > 0.

    D are the "ascending targets": p is in D when the single residue
    (-b) mod p is itself a prime below p, and also b+2 when it is prime.
    L are the loops: p | p + b happens exactly when p | b.
    """
    if b <= 0 or b % 2 == 0:
        raise ValueError("bound_C is stated for odd positive b")
    s = s or sieve(b + 2)
    best = 0
    for p in range(2, b + 1):
        if not s[p]:
            continue
        r = (-b) % p
        if (r and s[r]) or b % p == 0:
            best = p
    if b + 2 < len(s) and s[b + 2]:
        best = max(best, b + 2)
    return best


def predecessors(b, top, s=None):
    """Map each prime p <= top to the sorted primes q <= top with p | q + b.

    Works for any integer b (the caller picks ``top``). ``q = k*p - b`` is
    walked directly instead of factoring q + b, which is what makes this run
    for large b.
    """
    s = s or sieve(max(top, abs(b)) + 2)
    out = {}
    for p in range(2, top + 1):
        if not s[p]:
            continue
        got = []
        k = -((-(b + 2)) // p) if b + 2 > 0 else 1
        q = k * p - b
        while q <= top:
            if q >= 2 and s[q]:
                got.append(q)
            q += p
        out[p] = got
    return out


def first_round(pred):
    """The primes with at least one predecessor: one peeling round."""
    return {p for p, qs in pred.items() if qs}


def core(pred):
    """The effective universe E(b), and how many rounds it took.

    A prime with no predecessor cannot belong to any solution; removing it can
    leave another one bare, so the removal is iterated. What remains is the
    largest source-free set.
    """
    alive = set(pred)
    rounds = 0
    while True:
        dead = {p for p in alive if not any(q in alive for q in pred[p])}
        if not dead:
            return alive, rounds
        alive -= dead
        rounds += 1


def least_prime_not_dividing(b):
    """The smallest prime p* that does not divide b."""
    p = 2
    while True:
        if b % p:
            return p
        p += 1
        while not is_prime(p):
            p += 1


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def theorem_bound(b):
    """max((2p* - 1) b, 2p*): the bound on the largest prime of a solution.

    Proof sketch. Let M be the largest prime of a solution. If a prime p of the
    solution exceeds (M+b)/2, its predecessor q satisfies 0 < q+b <= M+b < 2p,
    so q+b = p and p-b is again a prime of the solution. Iterating from M gives
    an arithmetic progression of primes M, M-b, M-2b, ... of common difference
    b. Since p* does not divide b, p* consecutive terms would include a multiple
    of p*, which being prime would have to equal p*; so the progression is
    shorter than p*, and (M-b)/(2b) <= p*-1.

    For odd b this gives p* = 2: M and M-b have opposite parity, both are prime,
    so the even one is 2 and M = b+2 -- the bound proved in the first release,
    now the degenerate case in which the progression cannot have two terms.
    """
    pe = least_prime_not_dividing(b)
    return max((2 * pe - 1) * b, 2 * pe)


def progression_at(b, M):
    """The run M, M-b, M-2b, ... of primes ending at M (downwards)."""
    out = []
    x = M
    while x >= 2 and is_prime(x):
        out.append(x)
        x -= b
    return out[::-1]


def fixed_point(C, s=None):
    """The parameter-free model: the fixed point of

        g(m) = sum over primes p <= C of (1 - exp(-m/(p-1)))

    Its asymptotic solution has log C / log m -> e, that is m = C^(1/e+o(1)).
    """
    import math

    ps = primes_up_to(C, s)
    m = float(len(ps))
    for _ in range(500):
        nxt = sum(-math.expm1(-m / (p - 1.0)) for p in ps)
        if abs(nxt - m) < 1e-9:
            break
        m = nxt
    return m


def brute_force_S(b, top, s=None):
    """Every squarefree n > 1 in S_b, by direct check. Only for small b."""
    from itertools import combinations

    s = s or sieve(top + 2)
    ps = [p for p in range(2, top + 1) if s[p]]
    found = []
    for k in range(1, len(ps) + 1):
        for combo in combinations(ps, k):
            n = 1
            for p in combo:
                n *= p
            prod = 1
            for p in combo:
                prod *= p + b
            if prod % n == 0:
                found.append(n)
    return sorted(found)
