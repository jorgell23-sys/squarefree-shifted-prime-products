#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerates everything under data/. No hand-typed numbers anywhere.

    python src/generate_data.py [max_b]

Default max_b = 2001, which takes well under a minute.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shifted_primes as S  # noqa: E402


def main():
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 2001
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "data")
    os.makedirs(out, exist_ok=True)

    t0 = time.time()
    rows = []
    for b in range(1, top + 1, 2):
        c = S.bound(b)
        ent = S.predecessors(b, c)
        eff = S.kernel(ent)
        rows.append({"b": b, "bound": c, "primes_up_to_bound": len(ent),
                     "effective": len(eff), "size": S.count(ent),
                     "omega_b": len(S.prime_factors(b))})
    with open(os.path.join(out, "counts.json"), "w") as fh:
        json.dump(rows, fh, indent=1)
    print("counts.json: %d values of b, %.1fs" % (len(rows), time.time() - t0))

    small = {str(b): S.members(b) for b in range(1, 24, 2)}
    with open(os.path.join(out, "sets_small.json"), "w") as fh:
        json.dump(small, fh, indent=1)
    print("sets_small.json: complete S_b for odd b < 24")

    with open(os.path.join(out, "S_55.json"), "w") as fh:
        json.dump(S.members(55), fh, indent=1)
    print("S_55.json: the 220 elements that opened the question")

    classes = {}
    for n in range(2, 1001):
        if S.is_squarefree(n):
            classes[str(n)] = S.class_count(n)
    with open(os.path.join(out, "class_counts.json"), "w") as fh:
        json.dump(classes, fh, indent=1)
    print("class_counts.json: N(n) for %d squarefree n <= 1000" % len(classes))


if __name__ == "__main__":
    main()
