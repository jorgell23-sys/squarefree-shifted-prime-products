# Libres de cuadrados que dividen al producto de sus primos desplazados

Para un entero `b`, sea

    S_b = { n libre de cuadrados : n | prod_{p | n} (p + b) }

Con `b = 1` esto es la parte libre de cuadrados de `n | sigma(n)` —cuyo único
miembro por encima de 1 es el **6**, que es clásico y **no se reclama acá**—.
Con `b = -1` es `n | phi(n)`. Este repositorio trata de lo que pasa para `b`
general.

> **¿Es tu primera vez con esto? Empezá acá:** [**Explicación desde cero**](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/) —
> todo contado con peras y manzanas, con dibujos y sin conocimientos previos.

```
$ python verify.py
...
27 passed, 0 failed
```

Sin dependencias. Unos cuatro segundos.

## En dos minutos

**Una cota.** Para `b` impar positivo, todo primo de todo miembro es a lo sumo
`b + 2`, así que `S_b` es **finito**. Si `p > b` divide a `q + b` con `q < p`,
entonces `q + b = p`; con `b` impar, un `q` impar haría `p` par, así que
`q = 2` y `p = b + 2`.

**Una caracterización local.** `n ∈ S_b` si y sólo si para todo `p | n` vale
`(b mod p) ∈ { −q mod p : q | n }`. O sea que la pertenencia depende **sólo de
`b mod n`**, y la cantidad de clases admisibles de `b` módulo `n` es exactamente

    N(n) = prod_{p | n} #{ q mod p : q | n }

`N(6) = 4`, `N(30) = 12`, `N(105) = 27`, `N(210) = 72`. Comprobado contra la
definición para los 607 libres de cuadrados hasta 1000.

**Dos factores primos, forma cerrada.** `pq ∈ S_b` si y sólo si
`pq | b(b + p + q)`; y si ninguno de los dos divide a `b`, si y sólo si

    b ≡ φ(pq) − 1   (mod pq)

que es `b + p + q = pqu` y factoriza como `(up − 1)(uq − 1) = ub + 1`. Así que
los miembros de dos primos se encuentran **factorizando `ub + 1`**, sin recorrer
primos. Para `u = 1`: `(p−1)(q−1) = b + 1`. Ejemplo: `b = 7` da
`(p−1)(q−1) = 8`, o sea `{3,5}` y `n = 15` — en efecto `15 | 10·12`.

**Un retículo.** `S_b` es cerrado bajo `lcm`, así que tiene un **máximo** y todo
miembro lo divide.

**Los conteos.** `data/counts.json` tiene `|S_b|` para los 1001 valores impares
de `b` hasta 2001:

    b    1   3   5   7   9  11  13  15  17  19  21  23  25  27  29  31
   |S|   1   4   6   8   8  12   8  22  16  28  30  22   8  23  26  32

    b   33  35  37  39  41  43  45  47  49  51  53  55  57  59  61  63
   |S|  46  30  32  90  22  20  54  50  38  62  52 220 130  58  24 274

**No hay fórmula en `b`.** Las condiciones locales acoplan `b` con la estructura
entera de los primos de `n`, así que `|S_b|` no es multiplicativa en `b`, ni
función de `ω(b)`, ni de `π(b)`: los impares consecutivos 61 y 63 dan **24** y
**274**.

## Contenido

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | enunciados, demostraciones, tablas y **lo que esto no afirma** |
| [`PRIOR_ART.md`](PRIOR_ART.md) | qué se buscó, dónde y con qué términos — con el control positivo que **falló** y el que funcionó |
| `verify.py` | 27 controles, sin dependencias, ~4 s |
| [`docs/`](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/) | la **página explicativa**: lo mismo desde cero, para cualquiera |
| `src/` | implementación autónoma, sólo biblioteca estándar |
| `data/` | generado íntegramente por `src/generate_data.py`; ningún número escrito a mano |

## Verificación

`verify.py` cruza contra trabajo que este proyecto no produjo: recalcula
**OEIS A187778** (*números `k` que dividen a `psi(k)`*) desde cero para
`k ≤ 20000` y confirma que es `{1} ∪ {2^i·3^j}`, cuyo único término libre de
cuadrados por encima de 1 es el 6 — que es exactamente `S_1`. El contador exacto
se compara contra la enumeración por fuerza bruta de los `2^n` subconjuntos en
35 valores de `b`, y contra las listas completas explícitas en 23.

## Licencia

MIT para el código, CC BY 4.0 para texto y datos.

## Autoría

El diseño del sistema y la dirección de la investigación son del autor. Los
resultados matemáticos fueron producidos por un sistema automatizado (Claude,
Anthropic) bajo esa dirección. Todos los cómputos fueron verificados por dos
implementaciones independientes y cruzados contra trabajo publicado. El autor es
responsable de la corrección de todo lo publicado acá.

**Jorge Ellena Godoy**
