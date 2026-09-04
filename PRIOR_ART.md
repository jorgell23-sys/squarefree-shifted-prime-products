# Prior art: what was searched, where, when, and with what terms

**Searched on 2026-09-04.** Everything below is reported as found, including
the searches that failed and the one that failed *while looking for something we
knew was there* — which is the reason this file has a positive control at the
top instead of at the bottom.

---

## The positive control, first

> **A search that finds nothing is worth nothing unless you can show it would
> find something that is there.**

**Control A — a search that FAILED, and what we did about it.** We queried four
bibliographic sources (zbMATH Open, OpenAlex, Crossref, arXiv) for the case
`b = 1`, which we knew is published, with obligatory terms `radical` +
`divisors`. All four returned *no match*. The case `b = 1` **is** in the
literature. So those four sources, with those terms, cannot support any
statement of absence, and every negative result from them below is reported as
uninformative rather than as evidence.

**Control B — a search that SUCCEEDED.** Querying OEIS for the sequence
`k | psi(k)` returns **A187778**, *"Numbers k dividing psi(k)"*, with the
comment that the terms are 1 together with `2^i·3^j`, `i,j ≥ 1`. That is
exactly our `b = 1` case, and `verify.py` recomputes it from scratch for
`k ≤ 20000` and compares. So the OEIS route does find the known case, and its
negative answers below carry weight that the bibliographic ones do not.

---

## What is known, and is not claimed here

| known result | where |
|---|---|
| 6 is the only squarefree `n > 1` with `n \| sigma(n)` | classical; OEIS **A187778** for the unrestricted version `k \| psi(k)` |
| the standard proof of that fact is the same argument as Theorem 1 specialized to `b = 1` — *the largest prime factor is at most one more than the second largest* | folklore / textbook |
| products of shifted primes `prod_{p\|n}(p+a)` over squarefree `n` **are** an object of study | T. Freiberg, *Products of shifted primes simultaneously taking perfect power values*, J. Aust. Math. Soc. (2012), [arXiv:1008.1978](https://arxiv.org/abs/1008.1978) — but the question there is when the product is a perfect `r`-th power, **not** when `n` divides it |
| `sigma(n) = prod(p+1)` on squarefree `n`; Dedekind `psi` | standard |
| generalized Dedekind `psi_k(n) = n^k prod(1 + p^{-k})` | standard — it generalizes by **exponent**, not by an additive **shift**, so it is a different family from `prod(p+b)` |
| counting `n ≤ x` with `rad(n) \| sigma(n)` (prime-abundant), bound `x^{1/3+o(1)}` | Pollack & Pomerance, *Prime-perfect numbers*, INTEGERS 12A (2012), paper A14 |

## OEIS

| query | terms | result |
|---|---|---|
| by sequence | `\|S_b\|` = 1, 4, 6, 8, 8, 12, 8, 22, 16, 28, … | **not in OEIS** under any of the 6 transformations OEIS asks for (as is, without the first term, without the first two, each +1, each −1, doubled) |
| by sequence | the complete sets `S_5`, `S_7`, `S_9`, `S_11`, `S_15` | **not in OEIS** |
| by sequence | the complete sets `S_3` and `S_55` | prefix-only matches (A001465, A056606, A080506, A130760; A018396 *Divisors of 330*), all classified `SOLO_PREFIJO` — our lists are **complete and finite**, so a match that only shares a prefix with an infinite sequence is a false positive |
| by text | *"n divides the product of p+b over the primes p dividing n"* | entries returned, none about this object (closest: A126865, a gcd of two shifted products) |
| by text | *"squarefree numbers n dividing Product_{p\|n} (p+2)"* and *"(p+3)"* | entries returned, none about this object |
| by text | *"numbers k dividing Dedekind psi shifted prime divisors"* | **not in OEIS** |

## Bibliographic sources — reported, and discounted

zbMATH Open, OpenAlex, Crossref, arXiv, all four responding, on 2026-09-04:

| query | obligatory terms | result |
|---|---|---|
| squarefree integers `n` dividing the product of shifted primes `p+b` | `squarefree` + `shifted prime` | one hit: Freiberg (above), different question |
| pairs of primes `p q` with `pq` dividing `p+q+b` | `primes` + `pq divides` | no match |
| radical of `n` divides sum of divisors, prime-abundant | `radical` + `divisors` | **no match — and this is Control A, the case we knew is published** |

## Web searches, with the exact queries

Run on 2026-09-04:

1. `squarefree n divides product (p+b) over primes p dividing n shifted primes`
2. `primes p q "pq divides" p+q+b characterization pairs`
3. `"squarefree" number n divides sigma(n) only 6 multiperfect squarefree proof`
4. `"n divides" product of "p+1" over primes dividing n squarefree generalization b shift finite`
5. `"squarefree" n divides "product" of "p+k" over primes p dividing n generalization multiperfect`
6. `Giuga numbers generalization squarefree n divides product (p+b) shifted prime divisors`
7. `"pq divides" "p + q + 1" primes problem "(p-1)(q-1)" characterization diophantine`
8. `OEIS "n divides" "Product_{p|n}" "(p+1)" squarefree Dedekind psi`
9. `"generalized Dedekind psi" OR "shifted" arithmetic function "prod (p+b)" divisibility n squarefree study`

**What they returned:** the classical `b = 1` fact (search 3, with the same
proof idea), the Freiberg paper (searches 1, 5, 6), A187778 and the Dedekind
`psi` literature (search 8), Giuga numbers and Carmichael generalizations
(search 6 — related in flavour, different condition: Giuga is `p | n/p − 1`),
and the Pollack–Pomerance counting bound. **None of them states the family
`S_b` for general `b`, the bound `p ≤ b+2`, the class count `N(n)`, or the
two-prime characterization.**

## Nearby objects that are NOT this one

- **Giuga numbers** — `p | n/p − 1` for all `p | n`. Different condition.
- **Carmichael / Korselt** — `p − 1 | n − 1`. Different condition.
- **Primary pseudoperfect numbers** — `sum 1/p + 1/n = 1`. Different condition.
- **Multiperfect numbers** — `n | sigma(n)` without the squarefree restriction.
  Our `b = 1` is its squarefree part, and that is the known case.
- **Freiberg's object** — the same product `prod(p+a)`, asking whether it is a
  perfect power. Same object, different question.

## Conclusion, stated at the strength the evidence supports

The case `b = 1` **is known**, and Theorem 1 specialized to it is the standard
argument; that is declared in `RESULT.md` and not claimed.

For general `b`, the searches above did not find the family `S_b`, the bound
`p ≤ b + 2`, the class count `N(n) = prod_p #{q mod p}`, or the two-prime
characterization `pq | b(b+p+q)` / `b ≡ φ(n) − 1 (mod n)`.

**That is an absence, not a proof of novelty.** Theorem 2 in particular is one
line of the Chinese remainder theorem, and elementary consequences can be
folklore that no index records. What we assert is what we did: we looked, in the
places listed, with the terms listed, on the date listed, with a positive
control that works (OEIS) and one that does not (the bibliographic four), and we
did not find it.
