# Enteros libres de cuadrados que dividen el producto de sus primos desplazados

<!-- hallazgo:que -->
## Qué se encontró

Dado un entero `b`, la pregunta es qué enteros `n > 1` libres de cuadrados
dividen al producto de sus propios divisores primos desplazados en `b`. La
pertenencia resulta decidida **enteramente por `b` módulo `n`**, primo por
primo, mediante una condición que nombra exactamente qué restos sirven
(Teorema 2).

De ahí salen cinco consecuencias, y son el hallazgo:

1. para **todo** `b >= 1` el conjunto de soluciones es **finito**, y todo primo
   de toda solución es a lo sumo `max((2p* - 1) b, 2p*)`, donde `p*` es el menor
   primo que **no** divide a `b`. La cota es un enunciado sobre **progresiones
   aritméticas de primos**: el mayor primo de una solución arrastra detrás suyo
   una tirada `M, M-b, M-2b, ...` de primos, y `p*` la corta;
2. **para `b` impar esa cota es `b + 2`** — no porque `b` sea impar, sino porque
   la paridad mata la tirada en su primer paso: la cota `b + 2` es el caso
   degenerado de este teorema, no un hecho aparte sobre los impares;
3. los `b` que admiten un `n` dado ocupan exactamente `N(n)` clases de restos
   módulo `n`, con `N(n)` en **forma cerrada**;
4. el conjunto es cerrado por mínimo común múltiplo, así que tiene un **máximo
   al que todo elemento divide**: el producto del *universo efectivo* `E(b)`,
   que es exactamente el conjunto de primos que aparecen en alguna solución;
5. los tamaños son **erráticos en `b`** —`b = 61` y `b = 63` dan **24** y
   **274**— y lo que los gobierna, `|E(b)|`, **no** es `pi(pi(b))`: medido sobre
   10601 valores de `b`, la razón cae de 0,384 a 0,00164 en cinco décadas, y
   `|E(b)|` crece como una potencia `b^0,36`.

<!-- hallazgo:enunciado -->
## Definiciones y enunciados

Para un entero `b`, se escribe

    S_b = { n libre de cuadrados, n > 1 : n divide a prod_{p | n} (p + b) }.

En todo lo que sigue `P` es el conjunto de divisores primos de `n`, y
`omega(n) = #P`.

> **Teorema 1 (cota y finitud).** Sea `b >= 1` y sea `p*` el menor primo que
> **no** divide a `b`. Si `n` está en `S_b`, entonces todo primo de `n` es a lo
> sumo `max((2p* - 1) b, 2p*)`. En particular `S_b` es **finito para todo `b`**.
> Para `b` impar `p* = 2` y la cota se afina a `b + 2`.

> **Teorema 2 (caracterización local).** Para `n > 1` libre de cuadrados con
> conjunto de primos `P` y cualquier entero `b`,
>
>     n en S_b   <=>   para todo p en P:  (b mod p) en R_p := { -q mod p : q en P }.
>
> La pertenencia depende entonces sólo de `b mod n`, y la cantidad de clases de
> restos de `b` módulo `n` que admiten `n` es exactamente
>
>     N(n) = prod_{p | n} #R_p = prod_{p | n} #{ q mod p : q en P },
>
> coincidiendo los dos productos porque `q -> -q` es una biyección módulo `p`.

> **Teorema 3 (dos factores primos).** Para primos distintos `p` y `q`, `pq`
> está en `S_b` si y sólo si `pq` divide a `b(b + p + q)`; y cuando ninguno
> divide a `b`, eso es exactamente `b = phi(pq) - 1 (mod pq)`, equivalentemente
> `(up - 1)(uq - 1) = ub + 1` para un entero positivo `u`. Contar las soluciones
> de dos primos se vuelve así factorizar `ub + 1`.

> **Teorema 4 (estructura de retículo).** Si `n` y `m` están en `S_b`, también
> `lcm(n, m)`. Luego, para todo `b >= 1`, `S_b` tiene un máximo `N(b)` y todo
> elemento lo divide. `N(b)` es el producto del **universo efectivo** `E(b)`
> (Teorema 5).

> **Teorema 5 (el universo efectivo).** Sea `E(b)` lo que queda de los primos
> `<= C(b)` al ir borrando, iterando, todo primo sin predecesor. Entonces `E(b)`
> es el mayor conjunto sin fuente, `N(b) = prod E(b)` es el máximo de `S_b`, y
> `E(b)` es **exactamente** el conjunto de primos que aparecen en alguna
> solución.

Enunciados, demostraciones y tablas están en [`RESULT.md`](RESULT.md).

<!-- hallazgo:ejemplo -->
## El caso más chico, hecho a mano

Sea `b = 7` y `n = 15 = 3 * 5`, de modo que `P = {3, 5}`. El producto a dividir
es

    (3 + 7) * (5 + 7) = 10 * 12 = 120,   y   120 / 15 = 8,

así que `15` está en `S_7`. El Teorema 2 da la misma respuesta sin multiplicar:

    p = 3:  b mod 3 = 1   y   R_3 = { -3, -5 mod 3 } = { 0, 1 }   -- sí
    p = 5:  b mod 5 = 2   y   R_5 = { -3, -5 mod 5 } = { 2, 0 }   -- sí

y además cuenta cuántos `b` sirven en total:

    N(15) = #R_3 * #R_5 = #{0,1} * #{2,0} = 2 * 2 = 4,

o sea que exactamente **4** de las 15 clases de restos de `b` módulo 15 admiten
`n = 15`, y `b = 7` es una de ellas.

<!-- hallazgo:prueba -->
## Por qué valen los enunciados

**El Teorema 2 es una línea.** Como `n` es libre de cuadrados, `n` divide a
`prod_{q en P}(q + b)` si y sólo si cada `p` de `P` divide a algún `q + b` con
`q` en `P`, es decir `b = -q (mod p)`. Juntando sobre los primos de `n` sale la
condición. Cada elección de un primo cubridor para cada `p` fija una clase de
restos por el teorema chino, y dos elecciones dan la misma clase exactamente
cuando coinciden módulo todo `p`, que es lo que cuenta el producto `N(n)`.

**El Teorema 1 son tres pasos, y el tercero es una congruencia.** Sea `M` el
mayor primo de `n`.

*El escalón.* Si un primo `p` de `n` supera `(M + b)/2`, su primo cubridor `q`
cumple `p | q + b` con `0 < q + b <= M + b < 2p`, así que el único múltiplo de
`p` en ese rango es `p` mismo: `q + b = p`, y `p - b` es otra vez un primo
de `n`.

*La tirada.* Aplicándolo a `M`, después a `M - b`, y así mientras el término
supere `(M + b)/2`, todos los `M - i*b` son primos de `n`: una progresión
aritmética de primos de diferencia `b`.

*El corte.* `p*` no divide a `b`, así que los restos `M - i*b (mod p*)` recorren
todas las clases; `p*` términos consecutivos contendrían un múltiplo de `p*`,
que siendo primo tendría que ser `p*` mismo. Luego una tirada cuyos términos
superen todos a `p*` es más corta que `p*`, y eso da `(M - b)/(2b) <= p* - 1`.

Para `b` impar esto se derrumba: `p* = 2`, y `M` y `M - b` tienen paridad
distinta, así que el par es `2` y `M = b + 2`. **La paridad nunca fue la razón
por la que valía la cota: fue la razón por la que la tirada no podía tener dos
términos.**

**El Teorema 4 es inmediato del Teorema 2:** en `lcm(n, m)` cada primo conserva
el primo cubridor que ya tenía. La finitud da entonces un máximo, y el mismo
argumento muestra que todo elemento lo divide.

**Por qué el tamaño es errático.** `|S_b|` cuenta los `n` que cumplen `omega(n)`
condiciones locales en las que `R_p` depende de **todos** los primos de `n` y no
sólo de `p`. Por eso no es multiplicativo en `b` ni función de `omega(b)` o de
`pi(b)` — ver los límites más abajo para qué establece y qué no.

<!-- hallazgo:comprobar -->
## Comprobación

```bash
git clone https://github.com/jorgell23-sys/squarefree-shifted-prime-products
cd squarefree-shifted-prime-products
python verify.py
```

55 comprobaciones, sin instalar nada, `PASS` o `FAIL` en cada una y código de
salida 1 si alguna falla. Rederivan los enunciados desde las definiciones,
contrastan el contador exacto de modelos contra la enumeración por fuerza bruta
de los `2^n` subconjuntos en 35 valores de `b` y contra las listas completas
explícitas en 23, e incluyen un control externo: recalculan **OEIS
[A187778](https://oeis.org/A187778)** —los `k` que dividen a `psi(k)`, con `psi`
la función de Dedekind `psi(k) = k * prod_{p | k}(1 + 1/p)`— desde cero hasta
`k = 20000` y confirman que su único término libre de cuadrados mayor que 1 es
`6`, que es exactamente `S_1`.

<!-- hallazgo:nodice -->
## Qué no se afirma

**La ley de crecimiento `|E(b)| ~ b^0,36` está medida y modelada, no demostrada
— y no es un hecho sobre los primos.** Reemplazando los primos por un conjunto
*aleatorio* de la misma densidad y la misma paridad, dejando intacta la
divisibilidad, se reproducen las medianas dentro del 3 %. La ley de potencia es
del pelado y no de los primos, y así se dice. Lo que **no** sobrevive a ese
control, y por lo tanto sí es aritmético, es el término estructural: cada primo
que divide a `b` sube `log|E(b)|` en aproximadamente `1/p`.

**La cota del Teorema 1 no es ajustada.** Está demostrada para todo `b >= 1`,
pero con `b` par el mayor primo queda en una mediana del 0,35 de la cota; lo que
lo fija exactamente es la tirada más larga de primos en progresión aritmética de
diferencia `b`, que acá no se determina.

`b = 1` da `S_1 = {6}`, el hecho clásico de que `6` es el único `n` libre de
cuadrados con `n | sigma(n)`, y **eso no se reclama acá**; la demostración
estándar es el argumento del Teorema 1. Que `|S_b|` sea *errático* es una
afirmación sobre la forma del problema de conteo que el Teorema 2 exhibe, **no**
una demostración de que no pueda existir forma cerrada. Los conteos exactos
llegan hasta `b = 2001`, y la suma `sum_{b<=X} |S_b|` no se estima en absoluto:
unos pocos `b` la dominan.

---

> ¿Recién llegás? [**Explicado desde cero**](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/),
> con dibujos y sin dar nada por sabido
> ([English](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/)).

---

## Los conteos

`|S_b|` para `b` impar, de `data/counts.json`, que trae los 1001 impares
`b <= 2001`:

| `b` | 1 | 3 | 5 | 7 | 9 | ... | 55 | 57 | 59 | 61 | 63 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `\|S_b\|` | 1 | 4 | 6 | 8 | 8 | | 220 | 130 | 58 | **24** | **274** |

El salto de `b = 61` a `b = 63` es el punto 5 de arriba: once veces más entre
dos impares consecutivos. Los conteos se calculan con un contador exacto de
modelos —propagación unitaria, descomposición en componentes, memoria— y no
enumerando los `2^{pi(C(b))}` subconjuntos, que es inviable pasando `b` de 100.

## Qué hay acá

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | enunciados, demostraciones, tablas y qué no se afirma |
| [`PRIOR_ART.md`](PRIOR_ART.md) | qué se buscó, dónde y con qué términos — incluido un control positivo que **falló** y el que funcionó |
| `verify.py` | todas las comprobaciones, una orden, sin dependencias |
| [`docs/`](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/) | el mismo material explicado desde cero |
| `src/` | implementación autónoma, sólo biblioteca estándar |
| `data/` | generado entero por `src/generate_data.py`; ningún número tipeado a mano |

La versión en inglés de esta página: [`README.md`](README.md).

## Cómo citar

Ver [`CITATION.cff`](CITATION.cff). Licencia: MIT para el código, CC BY 4.0 para
texto y datos.

## Autor

**Jorge Ellena Godoy**.

El diseño del sistema y la dirección de la investigación son del autor. Los
resultados matemáticos fueron producidos por un sistema automatizado (Claude,
Anthropic) bajo esa dirección. Todos los cálculos fueron verificados por dos
implementaciones independientes y contrastados contra trabajo publicado. El
autor es responsable de la corrección de todo lo publicado acá.
