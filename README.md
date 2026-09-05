# Squarefree integers dividing the product of their shifted prime divisors

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

> **New to this? Start here:** [**Explained from scratch**](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/) — the whole
> thing in plain words, with pictures and no background needed
> ([en espanol](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/)).

---
## Layout

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | statements, proofs, tables, and **what this does not claim** |
| [`PRIOR_ART.md`](PRIOR_ART.md) | what was searched, where, with what terms — and the positive control that **failed**, plus the one that worked |
| `verify.py` | 30 checks, no dependencies, ~4 s |
| [`docs/`](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/) | the **explainer page**: the same story from scratch, for anyone |
| `src/` | standalone implementation, standard library only |
| `data/` | generated entirely by `src/generate_data.py`; no number typed by hand |

## Verification

`verify.py` cross-checks against work this project did not produce: it
recomputes **OEIS A187778** (*numbers `k` dividing `psi(k)`*) from scratch for
`k ≤ 20000` and confirms it equals `{1} ∪ {2^i·3^j}`, whose only squarefree
term above 1 is 6 — which is exactly `S_1`. The exact model counter is checked
against brute-force enumeration over all `2^n` subsets on 35 values of `b`, and
against the explicit complete lists on 23.

## License

MIT for the code, CC BY 4.0 for text and data.

## Authorship

System design and research direction are the author's. The mathematical results
were produced by an automated system (Claude, Anthropic) under that direction.
All computations were verified by two independent implementations and
cross-checked against published work. The author is responsible for the
correctness of everything published here.

**Jorge Ellena Godoy** — [`README.es.md`](README.es.md) for the Spanish version.
