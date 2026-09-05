# Squarefree integers dividing the product of their shifted prime divisors

**Jorge Ellena Godoy** — 2026-09-04

<!-- hallazgo:que -->
## What was found

Ask whether a squarefree integer `n` divides the product of its own prime
divisors shifted by `b`. The answer is decided **entirely by `b` modulo `n`**,
one prime at a time, by a condition that names exactly which residues work.

Three things follow, and they are the finding:

1. for odd `b > 0` every prime of every solution is at most `b + 2`, so the set
   of solutions is **finite** -- and therefore computable in full;
2. the `b` that admit a given `n` occupy exactly `N(n)` residue classes modulo
   `n`, with `N(n)` in **closed form**;
3. the size of the solution set has **no formula in `b`**, and the same
   condition says why: consecutive odd values `b = 61` and `b = 63` give **24**
   and **274** solutions.

<!-- hallazgo:enunciado -->
## The statement

For an integer `b`, write

    S_b = { n squarefree, n > 1 : n divides prod_{p | n} (p + b) }

> **Theorem 2 (local characterization).** For squarefree `n` with prime set `P`
> and any integer `b`,
>
>     n in S_b   <=>   for every p in P:  (b mod p) in R_p := { -q mod p : q in P }
>
> Hence membership depends only on `b mod n`, and the number of residue classes
> of `b` modulo `n` that admit `n` is exactly
>
>     N(n) = prod_{p | n} #{ q mod p : q | n }

> **Theorem 1 (bound, and finiteness).** For odd `b > 0`, every prime of every
> `n` in `S_b` is at most `b + 2`. In particular `S_b` is **finite**.

<!-- hallazgo:ejemplo -->
## The smallest case, done by hand

Take `b = 7` and `n = 15 = 3 * 5`. Its primes are `{3, 5}`, so the product to
divide is

    (3 + 7) * (5 + 7) = 10 * 12 = 120,   and   120 / 15 = 8

so `15` is in `S_7`. Theorem 2 says the same thing without multiplying: for
`p = 3` we need `7 mod 3 = 1` to lie in `R_3 = { -3, -5 mod 3 } = { 0, 1 }` --
it does; for `p = 5` we need `7 mod 5 = 2` in `R_5 = { -3, -5 mod 5 } = { 2, 0 }`
-- it does.

And it says how many `b` work at all:

    N(15) = #{3 mod 3, 5 mod 3} * #{3 mod 5, 5 mod 5} = #{0,2} * #{3,0} = 2 * 2 = 4

so exactly **4** of the 15 residue classes of `b` modulo 15 admit `n = 15`, and
`b = 7` is one of them.

The counts that show there is no formula, from `data/counts.json`:

    b    ...  55   57   59   61   63
   |S_b| ... 220  130   58   24  274

<!-- hallazgo:prueba -->
## Why it is proved

**Theorem 2 is one line.** `p` divides `prod_{q}(q+b)` exactly when `p | q + b`
for some `q` in `P`, that is `b = -q (mod p)`. Collecting over the primes of
`n` gives the condition, and the Chinese remainder theorem turns each covering
choice into one residue class, which is what `N(n)` counts.

**Theorem 1 is a parity argument.** Let `M` be the largest prime of `n` and let
`M | q + b`. If `q = M` then `M | b`, so `M <= b`. If `q < M` and `M > b` then
`0 < q + b < 2M`, forcing `q + b = M`; with `b` odd an odd `q` would make `M`
even, so `q = 2` and `M = b + 2`.

**And that is why there is no formula.** `|S_b|` counts the `n` satisfying
`omega(n)` local conditions in which `R_p` depends on *all* the primes of `n`,
not just on `p`, so it is not multiplicative in `b` nor a function of
`omega(b)` or `pi(b)`.

<!-- hallazgo:comprobar -->
## Check it yourself, in four seconds

```bash
git clone https://github.com/jorgell23-sys/squarefree-shifted-prime-products
cd squarefree-shifted-prime-products
python verify.py
```

30 checks, no dependencies, `PASS` or `FAIL` on each. One of them is external:
it recomputes **OEIS A187778** (*numbers `k` dividing `psi(k)`*) from scratch up
to `k = 20000` and confirms its only squarefree term above 1 is `6`, which is
exactly `S_1`. The exact model counter is checked against brute force over all
`2^n` subsets on 35 values of `b`, and against the explicit complete lists on 23.

<!-- hallazgo:nodice -->
## What it does not say

`b = 1` gives `{6}` -- the classical fact that `6` is the only squarefree `n`
with `n | sigma(n)` -- and **that is not claimed here**. Theorem 1 covers odd
`b > 0` only: for even `b` the finiteness of `S_b` would need a case of de
Polignac's conjecture and is left open. "No formula in `b`" is a statement about
the shape of the counting problem that Theorem 2 exhibits, **not** a proof that
no closed form can exist. And the counts stop at `b = 2001`.

---

---

## Theorem 1 (bound, and finiteness) — for odd `b > 0`

*If `n > 1` is squarefree and `n ∈ S_b`, then every prime of `n` is at most
`b + 2`. In particular `S_b` is finite.*

**Proof.** Write `P` for the primes of `n`. Since `n` is squarefree, `n | prod
(p+b)` holds iff every `p ∈ P` divides some `q + b` with `q ∈ P`. Let `M = max
P` and let `q ∈ P` with `M | q + b`.

- If `q = M`, then `M | b`, so `M ≤ b`.
- If `q < M` and `M > b`, then `0 < q + b < M + b < 2M`, hence `q + b = M`.
  With `b` odd, an odd `q` would make `M` even, impossible for `M > b ≥ 1`.
  So `q = 2` and `M = b + 2`.

Either way `M ≤ b + 2`. ∎

The exact bound is `C(b) = max(D ∪ L)` with `L = {p : p | b}` and
`D = {b+2 if prime} ∪ {p ≤ b : (−b) mod p is prime}` — for `p ≤ b` the residue
class `−b mod p` has a single representative below `p`, so a prime has at most
**one** possible smaller predecessor.

> **The case `b = 1` is not new.** It gives `S_1 = {6}` — the classical fact
> that 6 is the only squarefree `n > 1` with `n | sigma(n)` — and the standard
> proof is this same argument. See `PRIOR_ART.md`.

## Theorem 2 (local characterization)

*For squarefree `n` with prime set `P` and any integer `b`,*

    n ∈ S_b   ⟺   for every p ∈ P:  (b mod p) ∈ R_p := { −q mod p : q ∈ P }

**Proof.** `p | prod_{q∈P}(q+b)` iff `p | q + b` for some `q ∈ P`, i.e.
`b ≡ −q (mod p)`. ∎

Elementary, but it is what settles the counting question. Three consequences:

**(a) Membership depends only on `b mod n`.**

**(b) The number of residue classes of `b` modulo `n` is exactly**

    N(n) = prod_{p | n} #{ q mod p : q | n }

Each choice of a covering map `c : P → P` pins one class by the Chinese
remainder theorem, and two choices give the same class exactly when they agree
modulo every `p` — which is what the product counts. Checked against the
definition for all 607 squarefree `n ≤ 1000`: `N(6) = 4`, `N(30) = 12`,
`N(105) = 27`, `N(210) = 72`.

**(c) The set of admissible `b` has density `N(n)/n ≤ ω(n)^{ω(n)}/n`.**

## Theorem 3 (two prime factors, closed form)

*For distinct primes `p, q`:*

    pq ∈ S_b   ⟺   pq | b·(b + p + q)

*and when neither divides `b`, this is exactly*

    b ≡ φ(pq) − 1   (mod pq)

*equivalently `b + p + q = pqu` for a positive integer `u`, which factors as*

    (up − 1)(uq − 1) = ub + 1

For `u = 1` that reads `(p−1)(q−1) = b + 1`. This turns the count of
two-prime elements into a **factorization problem**: enumerate `u` and factor
`ub + 1`, instead of walking primes. Verified against direct enumeration for
all 200 odd `b < 400`.

## Theorem 4 (lattice structure)

*If `n, m ∈ S_b` are squarefree then `lcm(n,m) ∈ S_b`.* Each prime keeps its
covering prime. Since `S_b` is finite for odd `b > 0`, it has a **maximum** and
**every element divides it**. The maximum is the product of the *effective
universe* `E(b)`: the primes left after repeatedly discarding those with no
possible predecessor.

Also, unconditionally: `p ∈ S_b` for every prime `p | b`, and `2p ∈ S_b` for
every prime `p | b + 2`.

---

## The counting question, and the answer

`data/counts.json` has `|S_b|` for the 1001 odd `b ≤ 2001`, computed with an
exact model counter (unit propagation, component decomposition, caching) rather
than by enumerating the `2^{π(C(b))}` subsets, which is hopeless past `b ≈ 100`.

    b    1   3   5   7   9  11  13  15  17  19  21  23  25  27  29  31
   |S|   1   4   6   8   8  12   8  22  16  28  30  22   8  23  26  32

    b   33  35  37  39  41  43  45  47  49  51  53  55  57  59  61  63
   |S|  46  30  32  90  22  20  54  50  38  62  52 220 130  58  24 274

**There is no formula in `b`, and Theorem 2 says why:** `|S_b|` counts the `n`
satisfying `ω(n)` local conditions in which `R_p` depends on *all* the primes of
`n`, not just on `p`. It is not multiplicative in `b`, nor a function of `ω(b)`,
nor of `π(b)` — consecutive odd values `b = 61` and `b = 63` give 24 and 274.

What does govern the size is the **effective universe**, not `π(b)`:
`log|S_b|` correlates 0.941 with `|E(b)|`, against 0.773 with `π(C(b))` and
0.527 with `ω(b)`; at `b = 2001` those are 51 against 304. The six largest
values up to 2001 are all multiples of `105 = 3·5·7`: `b = 1155` (79,725,358),
`1785` (77,188,718), `1995` (72,449,578), `1365` (43,018,238), `1701`
(32,475,138), `1815` (26,124,880).

---

## What this does not claim

- **It does not claim `b = 1` is new.** `S_1 = {6}` is classical, and Theorem 1
  specialized to `b = 1` is the standard argument. What we did not find in the
  literature is the family studied **as a function of `b`**.
- **Theorem 2 is elementary** — one line of the Chinese remainder theorem. We
  searched and did not find it stated for this object (see `PRIOR_ART.md`), but
  a one-line consequence can be folklore that no index records. We claim we did
  not find it, not that nobody knew it.
- **It does not claim anything for even `b`.** There `S_b` need not be finite,
  and deciding it runs into de Polignac-type questions. Not touched.
- **It does not give an asymptotic** for `|S_b|` or for `|E(b)|`. The 0.941
  correlation is a measurement over 1001 values, not a theorem, and it is
  reported as such.
- **It does not claim the table is maximal in any sense** beyond `b ≤ 2001`,
  which is where the computation was run.
- **The bound `p ≤ b+2` is proved only for odd positive `b`.** The parity step
  is essential and there is no claim without it.

## Reproducing

    python verify.py                 # 30 checks, ~4 s, no dependencies
    python src/generate_data.py      # regenerates everything under data/

`data/` is produced entirely by `src/generate_data.py`; no number in this
document was typed by hand.

## Authorship

System design and research direction are the author's. The mathematical results
were produced by an automated system (Claude, Anthropic) under that direction.
All computations were verified by two independent implementations and
cross-checked against published work. The author is responsible for the
correctness of everything published here.
