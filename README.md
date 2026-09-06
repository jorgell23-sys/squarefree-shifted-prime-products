# Squarefree integers dividing the product of their shifted prime divisors

<!-- hallazgo:que -->
## What was found

For an integer `b`, ask which squarefree `n > 1` divide the product of their own
prime divisors shifted by `b`. Membership turns out to be decided **entirely by
`b` modulo `n`**, one prime at a time, by a condition naming exactly which
residues work (Theorem 2).

Four consequences, and they are the finding:

1. for **every** `b >= 1` the primes of every solution are bounded, so the
   solution set is **finite**, and therefore computable in full -- for odd `b`
   the bound is `b + 2`, and in general it is governed by the length of an
   arithmetic progression of primes with common difference `b`;
2. the `b` admitting a given `n` occupy exactly `N(n)` residue classes modulo
   `n`, with `N(n)` in **closed form**;
3. the solution set is closed under least common multiple, so for odd `b > 0` it
   has a **maximum that every element divides**;
4. its size is **erratic in `b`**: consecutive odd values `b = 61` and `b = 63`
   give **24** and **274** solutions.

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

**Theorem 1** is a parity argument. Let `M` be the largest prime of `n` and let
`q` in `P` satisfy `M | q + b`. If `q = M`, then `M | b` and so `M <= b`.
Otherwise `q < M`; and if moreover `M > b`, then `0 < q + b < M + b < 2M`, which
forces `q + b = M`. With `b` odd, an odd `q` would make `M` even, impossible
since `M > b >= 1`; hence `q = 2` and `M = b + 2`. In every case `M <= b + 2`,
and since a squarefree `n` in `S_b` is a product of distinct primes bounded by
`b + 2`, there are finitely many.

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

`b = 1` gives `S_1 = {6}`, the classical fact that `6` is the only squarefree `n`
with `n | sigma(n)`, and **that is not claimed here**; the standard proof is the
argument of Theorem 1. Theorem 1 now covers every `b >= 1`, but its bound is
**not tight** for even `b`: the exact largest prime is governed by the longest
arithmetic progression of primes with common difference `b`, which is not
determined here. That `|S_b|` is *erratic* is a statement about the shape of the counting
problem Theorem 2 exhibits — **not** a proof that no closed form can exist. The
computed counts stop at `b = 2001`.

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

The jump from `b = 61` to `b = 63` is the point of item 4 above: an elevenfold
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
