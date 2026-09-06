# Squarefree integers dividing the product of their shifted prime divisors

<!-- hallazgo:que -->
## What was found

For an integer `b`, ask which squarefree `n > 1` divide the product of their own
prime divisors shifted by `b`. Membership turns out to be decided **entirely by
`b` modulo `n`**, one prime at a time, by a condition naming exactly which
residues work (Theorem 2).

Five consequences, and they are the finding:

1. for **every** `b >= 1` the solution set is **finite**, with every prime of
   every solution at most `max((2p* - 1) b, 2p*)`, where `p*` is the least prime
   **not** dividing `b`. The bound is a statement about **arithmetic
   progressions of primes**: the largest prime of a solution drags a run
   `M, M-b, M-2b, ...` of primes behind it, and `p*` cuts that run short;
2. **for odd `b` that bound is `b + 2`** -- not because `b` is odd, but because
   parity kills the run at its first step: the bound `b + 2` is this theorem's
   degenerate case, not a separate fact about odd numbers;
3. the `b` admitting a given `n` occupy exactly `N(n)` residue classes modulo
   `n`, with `N(n)` in **closed form**;
4. the set is closed under least common multiple, so it has a **maximum that
   every element divides**: the product of the *effective universe* `E(b)`,
   which is exactly the set of primes occurring in some solution;
5. sizes are **erratic in `b`** -- `b = 61` and `b = 63` give **24** and
   **274** -- and what governs them, `|E(b)|`, is **not** `pi(pi(b))`: measured
   over 10601 values of `b`, the ratio falls from 0.384 to 0.00164 across five
   decades, and `|E(b)|` grows like a power `b^0.36`.

<!-- hallazgo:enunciado -->
## Definitions and statements

For an integer `b`, write

    S_b = { n squarefree, n > 1 : n divides prod_{p | n} (p + b) }.

Throughout, `P` denotes the set of prime divisors of `n`, and `omega(n) = #P`.

> **Theorem 1 (bound, and finiteness).** Let `b >= 1` and let `p*` be the
> smallest prime that does **not** divide `b`. If `n` is in `S_b`, then every
> prime of `n` is at most `max((2p* - 1) b, 2p*)`. In particular `S_b` is
> **finite for every `b`**. For odd `b` we have `p* = 2` and the bound sharpens
> to `b + 2`.

> **Theorem 2 (local characterisation).** For squarefree `n > 1` with prime set
> `P` and any integer `b`,
>
>     n in S_b   <=>   for every p in P:  (b mod p) in R_p := { -q mod p : q in P }.
>
> Membership therefore depends only on `b mod n`, and the number of residue
> classes of `b` modulo `n` that admit `n` is exactly
>
>     N(n) = prod_{p | n} #R_p = prod_{p | n} #{ q mod p : q in P },
>
> the two products agreeing because `q -> -q` is a bijection modulo `p`.

> **Theorem 3 (two prime factors).** For distinct primes `p` and `q`,
> `pq` is in `S_b` if and only if `pq` divides `b(b + p + q)`; and when neither
> divides `b`, that is exactly `b = phi(pq) - 1 (mod pq)`, equivalently
> `(up - 1)(uq - 1) = ub + 1` for a positive integer `u`. This turns counting
> two-prime solutions into factoring `ub + 1`.

> **Theorem 4 (lattice structure).** If `n` and `m` are in `S_b`, so is
> `lcm(n, m)`. Hence for every `b >= 1` the set `S_b` has a maximum `N(b)`, and
> every element divides it. `N(b)` is the product of the **effective universe**
> `E(b)` (Theorem 5).

> **Theorem 5 (the effective universe).** Let `E(b)` be what remains of the
> primes `<= C(b)` after repeatedly deleting every prime with no predecessor.
> Then `E(b)` is the largest source-free set, `N(b) = prod E(b)` is the maximum
> of `S_b`, and `E(b)` is **exactly** the set of primes occurring in some
> solution.

Statements, proofs and tables are in [`RESULT.md`](RESULT.md).

<!-- hallazgo:ejemplo -->
## The smallest case, done by hand

Take `b = 7` and `n = 15 = 3 * 5`, so `P = {3, 5}`. The product to divide is

    (3 + 7) * (5 + 7) = 10 * 12 = 120,   and   120 / 15 = 8,

so `15` is in `S_7`. Theorem 2 gives the same answer without multiplying:

    p = 3:  b mod 3 = 1   and   R_3 = { -3, -5 mod 3 } = { 0, 1 }   -- yes
    p = 5:  b mod 5 = 2   and   R_5 = { -3, -5 mod 5 } = { 2, 0 }   -- yes

and it also counts how many `b` work at all:

    N(15) = #R_3 * #R_5 = #{0,1} * #{2,0} = 2 * 2 = 4,

so exactly **4** of the 15 residue classes of `b` modulo 15 admit `n = 15`, and
`b = 7` is one of them.

<!-- hallazgo:prueba -->
## Why the statements hold

**Theorem 2** is one line. Since `n` is squarefree, `n` divides
`prod_{q in P}(q + b)` if and only if each `p` in `P` divides some `q + b` with
`q` in `P`, that is `b = -q (mod p)`. Collecting over the primes of `n` gives the
condition. Each choice of a covering prime for every `p` pins one residue class
by the Chinese remainder theorem, and two choices give the same class exactly
when they agree modulo every `p`, which is what the product `N(n)` counts.

**Theorem 1** is three steps, and the third is a congruence. Let `M` be the
largest prime of `n`.

*The step.* If a prime `p` of `n` exceeds `(M + b)/2`, its covering prime `q`
satisfies `p | q + b` with `0 < q + b <= M + b < 2p`, so the only multiple of `p`
in range is `p` itself: `q + b = p`, and `p - b` is again a prime of `n`.

*The run.* Applying that to `M`, then to `M - b`, and onwards while the term
exceeds `(M + b)/2`, every `M - i*b` is a prime of `n` -- an arithmetic
progression of primes of common difference `b`.

*The cut.* `p*` does not divide `b`, so the residues `M - i*b (mod p*)` run
through every class; `p*` consecutive terms would contain a multiple of `p*`,
which being prime would have to be `p*` itself. So a run whose terms all exceed
`p*` is shorter than `p*`, giving `(M - b)/(2b) <= p* - 1`.

For odd `b` this collapses: `p* = 2`, and `M` and `M - b` have opposite parity,
so the even one is `2` and `M = b + 2`. **Parity was never the reason the bound
held -- it was the reason the run could not have two terms.**

**Theorem 4** is immediate from Theorem 2: in `lcm(n, m)` every prime keeps the
covering prime it already had. Finiteness then gives a maximum, and the same
argument shows every element divides it.

**Why the size is erratic.** `|S_b|` counts the `n` satisfying `omega(n)` local
conditions in which `R_p` depends on *all* the primes of `n`, not on `p` alone.
That is why it is neither multiplicative in `b` nor a function of `omega(b)` or
`pi(b)` — see the limits below for what this does and does not establish.

<!-- hallazgo:comprobar -->
## Verification

```bash
git clone https://github.com/jorgell23-sys/squarefree-shifted-prime-products
cd squarefree-shifted-prime-products
python verify.py
```

55 checks, no dependencies, `PASS` or `FAIL` on each, exit code 1 if any fails.
They re-derive the statements from the definitions, check the exact model counter
against brute-force enumeration over all `2^n` subsets on 35 values of `b` and
against the explicit complete lists on 23, and include one external control: they
recompute **OEIS [A187778](https://oeis.org/A187778)** — the `k` dividing
`psi(k)`, with `psi` the Dedekind function `psi(k) = k * prod_{p | k}(1 + 1/p)` —
from scratch up to `k = 20000` and confirm that its only squarefree term above 1
is `6`, which is exactly `S_1`.

<!-- hallazgo:nodice -->
## What is not claimed

**The growth law `|E(b)| ~ b^0.36` is measured and modelled, not proved — and it
is not a fact about the primes.** Replacing the primes by a *random* set of the
same density and parity, leaving divisibility untouched, reproduces the medians
to within 3%. So the power law belongs to the peeling, not to the primes, and it
is stated that way. What does *not* survive that control, and is therefore
arithmetic, is the structural term: each prime dividing `b` raises `log|E(b)|` by
about `1/p`.

**Theorem 1's bound is not tight.** It is proved for every `b >= 1`, but for even
`b` the largest prime sits at a median of 0.35 of the bound; what pins it exactly
is the longest run of primes in arithmetic progression with common difference
`b`, which is not determined here.

`b = 1` gives `S_1 = {6}`, the classical fact that `6` is the only squarefree `n`
with `n | sigma(n)`, and **that is not claimed here**; the standard proof is the
argument of Theorem 1. That `|S_b|` is *erratic* is a statement about the shape
of the counting problem Theorem 2 exhibits — **not** a proof that no closed form
can exist. The exact counts stop at `b = 2001`, and the sum `sum_{b<=X} |S_b|`
is not estimated at all: a few `b` dominate it.

---

> New to this? [**Explained from scratch**](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/),
> with pictures and no background assumed
> ([español](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/)).

---

## The counts

`|S_b|` for odd `b`, from `data/counts.json`, which holds all 1001 odd
`b <= 2001`:

| `b` | 1 | 3 | 5 | 7 | 9 | ... | 55 | 57 | 59 | 61 | 63 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `\|S_b\|` | 1 | 4 | 6 | 8 | 8 | | 220 | 130 | 58 | **24** | **274** |

The jump from `b = 61` to `b = 63` is the point of item 5 above: an elevenfold
increase between consecutive odd values. The counts are computed with an exact
model counter — unit propagation, component decomposition, caching — rather than
by enumerating the `2^{pi(C(b))}` subsets, which is hopeless past `b` around 100.

## Contents

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | statements, proofs, tables, and what is not claimed |
| [`PRIOR_ART.md`](PRIOR_ART.md) | what was searched, where, with what terms — including a positive control that **failed**, and the one that worked |
| `verify.py` | every check, one command, no dependencies |
| [`docs/`](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/) | the same material explained from scratch |
| `src/` | standalone implementation, standard library only |
| `data/` | generated entirely by `src/generate_data.py`; no number typed by hand |

A Spanish version of this page: [`README.es.md`](README.es.md).

## Citing

See [`CITATION.cff`](CITATION.cff). Licence: MIT for the code, CC BY 4.0 for text
and data.

## Author

**Jorge Ellena Godoy**.

System design and research direction are the author's. The mathematical results
were produced by an automated system (Claude, Anthropic) under that direction.
All computations were verified by two independent implementations and
cross-checked against published work. The author is responsible for the
correctness of everything published here.
