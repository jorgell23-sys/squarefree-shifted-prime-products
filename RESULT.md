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

55 checks, no dependencies, `PASS` or `FAIL` on each. One of them is external:
it recomputes **OEIS A187778** (*numbers `k` dividing `psi(k)`*) from scratch up
to `k = 20000` and confirms its only squarefree term above 1 is `6`, which is
exactly `S_1`. The exact model counter is checked against brute force over all
`2^n` subsets on 35 values of `b`, and against the explicit complete lists on 23.

<!-- hallazgo:nodice -->
## What it does not say

`b = 1` gives `{6}` -- the classical fact that `6` is the only squarefree `n`
with `n | sigma(n)` -- and **that is not claimed here**. "No formula in `b`" is a
statement about the shape of the counting problem that Theorem 2 exhibits,
**not** a proof that no closed form can exist; the exact counts stop at
`b = 2001`. The growth law of the effective universe is **measured and modelled,
not proved**, and the control in Theorem 5 shows the power law is a fact about
peeling, not about the primes. Theorem 1 does bound `S_b` for every `b`, but the
bound is not tight.

---

---

## Theorem 1 (bound, and finiteness) — for **every** `b ≥ 1`

*Let `n > 1` be squarefree with `n ∈ S_b`, let `P` be its set of primes and
`M = max P`. Let `p*` be the smallest prime that does **not** divide `b`. Then*

    M ≤ max( (2p* − 1)·b ,  2p* ).

*In particular `S_b` is finite for every `b ≥ 1`.*

**Proof.**

*(1) The step.* Suppose `p ∈ P` satisfies `p > (M+b)/2`. It has a predecessor
`q ∈ P`, that is `p | q + b`. Since `0 < q + b ≤ M + b < 2p`, the only multiple
of `p` in that range is `p` itself, so `q + b = p`, and therefore `p − b ∈ P`.

*(2) The progression.* Apply (1) to `M`, then to `M − b`, and so on, as long as
the term exceeds `(M+b)/2`. This gives that `M − i·b` is a prime of `P` for
every `i < (M−b)/(2b)`: an **arithmetic progression of primes with common
difference `b`**.

*(3) The cut.* `p*` does not divide `b`, so the residues `M − i·b (mod p*)` run
through every class as `i` varies. If the progression had `p*` consecutive
terms, one of them would be divisible by `p*`; being prime, it would have to
equal `p*`. So if all terms exceed `p*`, the progression has at most `p* − 1`
terms.

*(4)* Combining (2) and (3), `(M−b)/(2b) ≤ p* − 1`, that is `M ≤ (2p*−1)b`. The
hypothesis in (3) holds whenever `(M+b)/2 ≥ p*`; if it does not, then
`M < 2p* − b ≤ 2p*`. ∎

### The odd case is this theorem

For odd `b` we have `p* = 2`, and the progression cannot have two terms: `M` and
`M − b` have opposite parity, and both are prime, so the even one is `2` and
`M = b + 2`. **The bound `b + 2` was never a property of `b` being odd. It is
the statement that parity cuts the progression at its first step.**

### This closes the even case, and without de Polignac

Version 1 of this repository stated the finiteness only for odd `b`, and said
that *"for even `b` the finiteness of `S_b` would need a case of de Polignac's
conjecture and is left open"*. It does not. The argument above never needs any
pair of primes at distance `b` to **exist**; it only needs the progressions to
be **short**, and that follows from a congruence modulo `p*`.

### For even `b` the bound `b + 2` is false, and not narrowly

**149 of the 150 even values `b ≤ 300`** admit a solution with a prime larger
than `b + 2`, and so do **all 2001** even values in `1000 ≤ b ≤ 5000`. The
progressions behind the extreme cases are the classical long runs of primes,
which is why the primorials are the worst offenders:

| `b` | `p*` | bound | largest prime of a solution | the progression of common difference `b` |
|---|---:|---:|---:|---|
| 2 | 3 | 10 | 7 | 3, 5, 7 |
| 6 | 5 | 54 | 29 | 5, 11, 17, 23, 29 |
| 30 | 7 | 390 | 157 | 7, 37, 67, 97, 127, 157 |
| 210 | 11 | 4.410 | 1.063 | 13, 223, 433, 643, 853, 1063 |
| 2310 | 13 | 57.750 | 13.931 | 71, 2381, 4691, 7001, 9311, 11621, 13931 |
| 30030 | 17 | 990.990 | 276.277 | 6007, 36037, 66067, … (10 terms) |

In every row the progression is shorter than `p*`, which is what the theorem
asserts. The bound is not tight: it is attained only at `b = 1`, and for even
`b` the median of `M / bound` is 0,35.

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

## Theorem 5 (the effective universe)

*Let `E(b)` be the set obtained from the primes `<= C(b)` by repeatedly deleting
every prime with no predecessor left. Then `E(b)` is the largest source-free
set; `N(b) = prod E(b)` is the largest element of `S_b`; every element of `S_b`
divides `N(b)`; and `E(b)` is **exactly** the set of primes that occur in some
element of `S_b`.*

**Proof.** A prime with no predecessor cannot lie in any solution, so deleting
it removes no solution; deleting it may leave another prime bare, so the
deletion is iterated, and the result still contains every solution. What
remains is source-free by construction, hence is itself a solution (Theorem 2),
and it contains every other one, so by Theorem 4 it is the maximum. Every prime
of `E(b)` therefore occurs in a solution, namely `N(b)`. Conversely a prime
occurring in a solution has a predecessor inside it, so it survives every
deletion round. []

Checked against brute force for `b = 3, 5, 7, 9, 11, 15, 21, 33, 45`.

`E1(b)` denotes the result of a **single** deletion round; the difference
between the two is the whole story of what follows. At `b = 999`, one round
leaves 97 primes and the full peeling leaves 22, after 19 rounds.

## The growth of `|E(b)|` — measured and modelled, not proved

### It is not `π(π(b))`

The natural heuristic says: `p` needs a predecessor in the class `−b mod p`,
there are about `π(b)/(p−1)` prime candidates, so the primes up to `π(b)`
survive — about `π(π(b))` of them. **That heuristic counts as predecessors every
prime of the universe, and a predecessor only counts if it survives too.**

Measured over **10.481 values of `b`** — a complete census of the odd `b ≤ 20001`
plus 120 values drawn at random (seed 20260906, fixed in advance) in each decade
from `10⁴` to `10⁷` — medians per decade:

| decade | n | `\|E\|` | `\|E₁\|` | `π(π(b))` | `\|E\|/π(π(b))` | `\|E₁\|/π(π(b))` | slope of `\|E\|` |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10³ | 4500 | 48 | 313 | 125 | 0,384 | 2,50 | — |
| 10⁴ | 5121 | 70 | 693 | 264 | 0,266 | 2,63 | 0,3734 |
| 10⁵ | 120 | 244 | 14.048 | 4.742 | 0,0516 | 2,96 | 0,3437 |
| 10⁶ | 120 | 578 | 105.603 | 32.999 | 0,0175 | 3,20 | 0,3727 |
| 10⁷ | 120 | 1.278 | 737.310 | 227.112 | 0,0056 | 3,25 | 0,3559 |
| 10⁸ | 120 | 2.844 | 5.864.524 | 1.738.254 | **0,00164** | 3,37 | 0,3468 |

The ratio falls by a factor **234** across five decades and keeps falling.
`π(π(b))` is a decent law for `E₁(b)`, which is a different set: its slope
climbs 0,787 → 0,827 → 0,875 → 0,871 → **0,899** towards 1, exactly as
`b/(log b)^k` must, while the slope of `|E(b)|` stays flat. Both series come
from the same computation over the same `b`.

### Predicting a decade before computing it

Fitting **only** `b ≤ 10⁷`,

    log |E(b)| = 0,3562·log b + 0,981·Σ_{p|b} 1/p + 0,6279

and predicting the median of the decade `[10⁸, 10⁹)` **before computing a single
value**:

| | median `\|E(b)\|` |
|---|---:|
| predicted by the fitted law | **2.870** |
| predicted with the pure `1/e` slope | 3.637 |
| predicted if `\|E\| ∝ π(π(b))` held | ≈ 21.000 |
| **measured** | **2.844** |

**0,9 % error** extrapolating a full decade. `π(π(b))` would be off by a factor
of 7,4.

### The self-consistent model, and the exponent `1/e`

If the surviving set has `m` primes and behaves like an equidistributed set of
residues modulo each `p`, then `p` survives with probability `1 − e^{−m/(p−1)}`,
and `m` must be a fixed point of

    g(m) = Σ_{p ≤ C(b)} ( 1 − e^{−m/(p−1)} )

Splitting the sum at `p = m` gives `m ≈ π(m) + m·(log log b − log log m)`, hence
`log b / log m → e`, that is

    |E(b)| = b^{1/e + o(1)},      1/e = 0,367879…

**A power, against the nearly linear `π(π(b)) ~ b/(log b)²`.** The four measured
slopes — 0,3734 / 0,3437 / 0,3727 / 0,3559, mean 0,361 — sit inside the interval
`[0,33 , 0,42]` declared before measuring.

The model has **no fitted constant**; its only input is `C(b)`. Median relative
error against measurement:

| `b ~` | 10² | 10³ | 2·10³ | 10⁴ | 10⁵ | 10⁶ | 10⁷ |
|---|---:|---:|---:|---:|---:|---:|---:|
| error | −30,6 % | −27,1 % | −19,0 % | −14,6 % | −14,8 % | +10,5 % | **+0,6 %** |

Solving the fixed point with the integral `∫₂^C (1−e^{−m/t})/log t dt` — which
reaches far past what can be computed with actual primes — confirms the
derivation: `log C / log m` goes 2,098 → 2,388 → 2,577 → 2,683 → **2,716** at
`C = 10¹⁰⁰`, converging to `e`. The convergence is extremely slow, which is why
the model itself predicts a local slope of 0,353–0,360 over the measured range
rather than its own limit.

### The control that says what this is *not* about

Repeat everything over a **fake** universe: a random set with the same density
(`2/log n`) and the same parity as the primes, leaving divisibility untouched.
Only membership changes.

**The power law survives.** So `b^{1/e}` is not a fact about the primes; it is a
fact about peeling a divisibility digraph whose universe has density `1/log`.

### The part that *is* about the primes

Each prime dividing `b` raises `log|E(b)|` by about `1/p`:

| `p` | measured effect | `1/p` |
|---:|---:|---:|
| 3 | +0,314 | 0,333 |
| 5 | +0,212 | 0,200 |
| 7 | +0,144 | 0,143 |
| 11 | +0,103 | 0,091 |

Fitting over 10.361 values,

    log |E(b)| = 0,3562·log b + 0,981·Σ_{p|b} 1/p + 0,628

with the structural coefficient equal to 1 within error. Multiples of 105 sit
`+0,515` above their neighbourhood: **1,67 times** the typical `|E|` for their
size.

**The mechanism runs against the counting intuition.** `p | b` *reduces* the
number of arcs (−0,137 in log for `p = 3`) yet *increases* `|E|`; the
correlation of `log|E|` with `log(arcs)` is **−0,736**. The lost arcs pointed at
`p`, which was already alive: they were redundant. What decides lives at the
edge. For `p > C/2` the only possible predecessor is `q = 2p − b`, and if
`p₀ | b` then `2p − b` is never divisible by `p₀`. Over 400 values of `b ~ 10⁵`
and 2,5 million candidates:

| | candidates | with `2p−b` prime | rate |
|---|---:|---:|---:|
| `3 \| b` | 2.567.543 | 710.005 | **0,2765** |
| `3 ∤ b` | 2.537.637 | 347.935 | **0,1371** |

The ratio is **2,017**, against the `(p−1)/(p−2) = 2` predicted by the local
Hardy–Littlewood factor for "`p` and `2p−b` both prime". This term does **not**
reproduce in the fake universe.

### And `|S_b|` follows `|E(b)|` exponentially

Over the 1001 exact counts (`b ≤ 2001`):

    log₂ |S_b| = 0,374·|E(b)| + 3,81      R² = 0,886

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
- **The bound for even `b` is not tight.** Theorem 1 proves finiteness for every
  `b`, but for even `b` the median of `M / bound` is 0.35; the exact largest
  prime is governed by the longest arithmetic progression of primes with common
  difference `b`, which is not determined here.
- **It does not give an asymptotic** for `|S_b|` or for `|E(b)|`. The 0.941
  correlation is a measurement over 1001 values, not a theorem, and it is
  reported as such.
- **It does not claim the table is maximal in any sense** beyond `b ≤ 2001`,
  which is where the computation was run.
- **The bound `p ≤ b+2` is proved only for odd positive `b`.** The parity step
  is essential and there is no claim without it.

## Reproducing

    python verify.py                 # 55 checks, ~4 s, no dependencies
    python src/generate_data.py      # regenerates everything under data/

`data/` is produced entirely by `src/generate_data.py`; no number in this
document was typed by hand.

## Authorship

System design and research direction are the author's. The mathematical results
were produced by an automated system (Claude, Anthropic) under that direction.
All computations were verified by two independent implementations and
cross-checked against published work. The author is responsible for the
correctness of everything published here.
