# Libres de cuadrados que dividen al producto de sus primos desplazados

<!-- hallazgo:que -->
## Qué se encontró

Preguntá si un entero libre de cuadrados `n` divide al producto de sus propios
primos desplazados en `b`. La respuesta queda decidida **enteramente por `b`
módulo `n`**, primo por primo, con una condición que nombra exactamente qué
restos sirven.

De ahí salen tres cosas, y ésas son el hallazgo:

1. para `b` impar positivo, todo primo de toda solución es a lo sumo `b + 2`,
   así que el conjunto de soluciones es **finito** —y por lo tanto calculable
   entero—;
2. los `b` que admiten un `n` dado ocupan exactamente `N(n)` clases de restos
   módulo `n`, con `N(n)` en **forma cerrada**;
3. el tamaño del conjunto **no tiene fórmula en `b`**, y la misma condición dice
   por qué: los valores impares consecutivos `b = 61` y `b = 63` dan **24** y
   **274** soluciones.

<!-- hallazgo:enunciado -->
## El enunciado

Para un entero `b`, escribí

    S_b = { n libre de cuadrados, n > 1 : n divide a prod_{p | n} (p + b) }

> **Teorema 2 (caracterización local).** Para `n` libre de cuadrados con
> conjunto de primos `P` y cualquier entero `b`,
>
>     n en S_b   <=>   para todo p en P:  (b mod p) en R_p := { -q mod p : q en P }
>
> Luego la pertenencia depende sólo de `b mod n`, y la cantidad de clases de
> restos de `b` módulo `n` que admiten a `n` es exactamente
>
>     N(n) = prod_{p | n} #{ q mod p : q | n }

> **Teorema 1 (cota, y finitud).** Para `b` impar positivo, todo primo de todo
> `n` de `S_b` es a lo sumo `b + 2`. En particular `S_b` es **finito**.

<!-- hallazgo:ejemplo -->
## El caso más chico, hecho a mano

Tomá `b = 7` y `n = 15 = 3 * 5`. Sus primos son `{3, 5}`, así que el producto a
dividir es

    (3 + 7) * (5 + 7) = 10 * 12 = 120,   y   120 / 15 = 8

o sea que `15` está en `S_7`. El Teorema 2 dice lo mismo sin multiplicar: para
`p = 3` hace falta que `7 mod 3 = 1` esté en `R_3 = { -3, -5 mod 3 } = { 0, 1 }`
—está—; para `p = 5`, que `7 mod 5 = 2` esté en `R_5 = { -3, -5 mod 5 } = { 2, 0 }`
—está—.

Y dice cuántos `b` sirven en total:

    N(15) = #{3 mod 3, 5 mod 3} * #{3 mod 5, 5 mod 5} = #{0,2} * #{3,0} = 2 * 2 = 4

o sea que exactamente **4** de las 15 clases de restos de `b` módulo 15 admiten
`n = 15`, y `b = 7` es una de ellas.

Los conteos que muestran que no hay fórmula, de `data/counts.json`:

    b    ...  55   57   59   61   63
   |S_b| ... 220  130   58   24  274

<!-- hallazgo:prueba -->
## Por qué es cierto

**El Teorema 2 es una línea.** `p` divide a `prod_{q}(q+b)` exactamente cuando
`p | q + b` para algún `q` de `P`, o sea `b = -q (mod p)`. Juntando sobre los
primos de `n` sale la condición, y el teorema chino convierte cada elección de
cubrimiento en una clase de restos, que es lo que `N(n)` cuenta.

**El Teorema 1 es un argumento de paridad.** Sea `M` el mayor primo de `n` y sea
`M | q + b`. Si `q = M` entonces `M | b`, luego `M <= b`. Si `q < M` y `M > b`,
entonces `0 < q + b < 2M`, lo que fuerza `q + b = M`; y con `b` impar un `q`
impar haría `M` par, así que `q = 2` y `M = b + 2`.

**Y por eso no hay fórmula.** `|S_b|` cuenta los `n` que cumplen `omega(n)`
condiciones locales en las que `R_p` depende de *todos* los primos de `n` y no
sólo de `p`, así que no es multiplicativa en `b` ni función de `omega(b)` ni de
`pi(b)`.

<!-- hallazgo:comprobar -->
## Comprobalo vos, en cuatro segundos

```bash
git clone https://github.com/jorgell23-sys/squarefree-shifted-prime-products
cd squarefree-shifted-prime-products
python verify.py
```

30 comprobaciones, sin dependencias, `PASS` o `FAIL` en cada una. Una es
externa: recalcula **OEIS A187778** (*los `k` que dividen a `psi(k)`*) desde
cero hasta `k = 20000` y confirma que su único término libre de cuadrados por
encima de 1 es el `6`, que es exactamente `S_1`. El contador exacto se controla
contra fuerza bruta sobre los `2^n` subconjuntos en 35 valores de `b`, y contra
las listas completas explícitas en 23.

<!-- hallazgo:nodice -->
## Qué NO dice

Con `b = 1` sale `{6}` —el hecho clásico de que `6` es el único libre de
cuadrados con `n | sigma(n)`— y **eso no se reclama acá**. El Teorema 1 cubre
sólo `b` impar positivo: para `b` par la finitud de `S_b` dependería de un caso
de la conjetura de de Polignac y queda abierta. «No hay fórmula en `b`» es una
afirmación sobre la forma del problema de conteo que el Teorema 2 exhibe, **no**
una demostración de que ninguna forma cerrada pueda existir. Y los conteos
llegan hasta `b = 2001`.

---

> **¿Es tu primera vez con esto? Empezá acá:** [**Explicación desde cero**](https://jorgell23-sys.github.io/squarefree-shifted-prime-products/es/) —
> todo contado con peras y manzanas, con dibujos y sin conocimientos previos.

---
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
