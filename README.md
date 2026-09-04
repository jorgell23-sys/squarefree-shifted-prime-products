# Squarefree integers dividing the product of their shifted prime divisors

For an integer `b`, let

    S_b = { n squarefree : n | prod_{p | n} (p + b) }

`b = 1` gives the squarefree part of `n | sigma(n)` — whose only member above 1
is **6**, which is classical and **not claimed here**. `b = -1` gives
`n | phi(n)`. This repository is about what happens for general `b`.

> **New to this? Start here:** [**Explained from scratch**](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/) — the whole
> thing in plain words, with pictures and no background needed
> ([en español](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/)).

```
$ python verify.py
...
27 passed, 0 failed
```

No dependencies. About four seconds.

## In two minutes

**A bound.** For odd `b > 0`, every prime of every member is at most `b + 2`,
so `S_b` is **finite**. If `p > b` divides `q + b` with `q < p`, then
`q + b = p`; with `b` odd, an odd `q` would make `p` even, so `q = 2` and
`p = b + 2`.

**A local characterization.** `n ∈ S_b` iff for every `p | n`,
`(b mod p) ∈ { −q mod p : q | n }`. So membership depends only on `b mod n`,
and the number of admissible classes of `b` modulo `n` is exactly

    N(n) = prod_{p | n} #{ q mod p : q | n }

`N(6) = 4`, `N(30) = 12`, `N(105) = 27`, `N(210) = 72`. Checked against the
definition for all 607 squarefree `n ≤ 1000`.

**Two prime factors, closed form.** `pq ∈ S_b` iff `pq | b(b + p + q)`; and if
neither prime divides `b`, iff

    b ≡ φ(pq) − 1   (mod pq)

which is `b + p + q = pqu` and factors as `(up − 1)(uq − 1) = ub + 1`. So the
two-prime members are found by **factoring `ub + 1`**, not by walking primes.
For `u = 1`: `(p−1)(q−1) = b + 1`. Example: `b = 7` gives `(p−1)(q−1) = 8`, so
`{3,5}` and `n = 15` — indeed `15 | 10·12`.

**A lattice.** `S_b` is closed under `lcm`, so it has a **maximum** and every
member divides it.

**The counts.** `data/counts.json` has `|S_b|` for the 1001 odd `b ≤ 2001`:

    b    1   3   5   7   9  11  13  15  17  19  21  23  25  27  29  31
   |S|   1   4   6   8   8  12   8  22  16  28  30  22   8  23  26  32

    b   33  35  37  39  41  43  45  47  49  51  53  55  57  59  61  63
   |S|  46  30  32  90  22  20  54  50  38  62  52 220 130  58  24 274

**There is no formula in `b`.** The local conditions couple `b` with the entire
prime structure of `n`, so `|S_b|` is not multiplicative in `b`, nor a function
of `ω(b)`, nor of `π(b)`: the consecutive odd values 61 and 63 give **24** and
**274**.

## Layout

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | statements, proofs, tables, and **what this does not claim** |
| [`PRIOR_ART.md`](PRIOR_ART.md) | what was searched, where, with what terms — and the positive control that **failed**, plus the one that worked |
| `verify.py` | 27 checks, no dependencies, ~4 s |
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
