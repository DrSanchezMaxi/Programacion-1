# Proyecto 2 — Acumulador de ventas por producto

Programación I (B0200) — Maximiliano Sánchez

El programa toma por parámetro un archivo csv con el encabezado
`Fecha,Producto,Cantidad,ValorUnitario`, acumula las ventas por producto y
guarda el resultado en otro archivo csv.

Para cada producto se guarda la fecha de la primera venta, la fecha de la
última venta, la cantidad total vendida y el valor total vendido.

## Uso

```bash
python . ventas_ejemplo.csv resumen_ventas.csv
```

El primer parámetro es el csv de entrada y el segundo el csv de salida.
Se ejecuta parado en la carpeta del proyecto (`python .` corre `__main__.py`).

Las fechas de la columna `Fecha` se aceptan en tres formatos: `AAAA-MM-DD`,
`DD/MM/AAAA` y `DD-MM-AAAA`. Las columnas del encabezado pueden venir en
cualquier orden.

## Correr los tests

```bash
python -m unittest discover -s test -t .
```

Son 62 tests: 7 de `parsear_fecha`, 7 de `validar_encabezado`, 12 de
`armar_venta`, 9 de `leer_ventas`, 10 de `acumular_por_producto`, 7 de
`guardar_resumen` y 10 del programa completo.

## Estructura

```
Proyecto 2/
├── __main__.py            programa principal: parámetros y código de salida
├── ventas_ejemplo.csv     archivo de prueba
├── src/
│   ├── __init__.py
│   ├── funciones.py       las funciones que resuelven el problema
│   └── programa.py        resolución: encadena las funciones y maneja errores
└── test/
    ├── __init__.py
    ├── test_funciones.py  testing de cada función por separado
    └── test_programa.py   testing del programa completo, de punta a punta
```

## Decisiones

- **El diccionario acumulador**: la clave es el nombre del producto y el valor
  es otro diccionario con `inicio`, `fin` (los dos `datetime`), `cantidad` y
  `total`. La primera vez que aparece un producto se lo carga con la fecha de
  esa venta en `inicio` y en `fin`; después se compara con `min()` y `max()`
  contra lo que ya estaba guardado.

- **Excepciones propias**: `EncabezadoInvalidoError` (faltan columnas) y
  `FilaInvalidaError` (fecha, cantidad o valor mal formados, producto vacío,
  valores negativos). Cada una guarda el dato que hace falta para el mensaje:
  qué columnas faltan, o en qué fila estuvo el problema y por qué.
  `programa()` las atrapa, informa por `sys.stderr` y devuelve `None`, así el
  programa no termina con un traceback en la cara del usuario.

- **Manejo del csv con el módulo `csv`**: `csv.DictReader` para leer y
  `csv.writer` para escribir. Además de ser lo pedido, resuelve solo el caso
  de un producto con una coma en el nombre (`"Tornillo, cabeza plana"`), que
  con `split(",")` se partiría en dos campos. Hay un test para eso.

- **Cantidad como entero**: son unidades de producto, así que `2.5` se
  rechaza con `FilaInvalidaError`. El valor unitario sí es `float`, porque
  tiene centavos.

- **Errores por `sys.stderr` y códigos de salida distintos** (`-1` si los
  parámetros están mal, `-2` si falló el procesamiento), para poder saber
  desde afuera qué pasó.

- **Testing con archivos temporales**: cada test escribe su propio csv con
  `tempfile` y lo borra al terminar con `addCleanup`. Así los tests no
  dependen de archivos del proyecto ni se pisan entre sí.

## Resumen de la biblioteca `datetime`

`datetime` es la biblioteca estándar de Python para trabajar con fechas y
horas. En este proyecto se usa para la columna `Fecha`: convertir el texto del
csv a fecha, comparar fechas para saber cuál es la primera y cuál la última, y
volver a convertirlas a texto para escribir el resumen.

### Tipos principales

| Tipo | Qué representa | Ejemplo |
|---|---|---|
| `date` | una fecha: año, mes y día | `date(2026, 1, 5)` |
| `time` | una hora: hora, minuto, segundo, microsegundo | `time(14, 30)` |
| `datetime` | fecha y hora juntas | `datetime(2026, 1, 5, 14, 30)` |
| `timedelta` | una duración, la diferencia entre dos fechas u horas | `timedelta(days=7)` |

### Crear fechas

```python
from datetime import datetime, date, timedelta

datetime(2026, 1, 5)      # una fecha puntual (hora 00:00:00)
date.today()              # la fecha de hoy
datetime.now()            # la fecha y hora de este momento
```

### De texto a fecha: `strptime`

Es el que se usa en `parsear_fecha()` para leer la columna `Fecha`.

```python
datetime.strptime("2026-01-05", "%Y-%m-%d")   # datetime(2026, 1, 5)
```

El segundo parámetro es el formato, armado con códigos: `%Y` año de 4 dígitos,
`%m` mes, `%d` día, `%H` hora, `%M` minutos, `%S` segundos. Si el texto no
coincide con el formato, `strptime` lanza `ValueError` — por eso
`parsear_fecha()` prueba los tres formatos aceptados dentro de un `try/except`
y se queda con el primero que funcione.

También valida que la fecha exista de verdad: `"2026-02-30"` tiene el formato
correcto pero el 30 de febrero no existe, así que también lanza `ValueError`.

### De fecha a texto: `strftime`

Es la operación inversa, con los mismos códigos. Se usa en
`guardar_resumen()` para escribir las fechas en el csv de salida:

```python
fecha.strftime("%Y-%m-%d")    # "2026-01-05"
```

### Comparar y ordenar

Los objetos `datetime` y `date` se comparan directamente con `<`, `>`, `==`, y
funcionan con `min()` y `max()`. Por eso en `acumular_por_producto()` alcanza
con:

```python
acumulado["inicio"] = min(acumulado["inicio"], venta["fecha"])
acumulado["fin"] = max(acumulado["fin"], venta["fecha"])
```

No hace falta ordenar las ventas ni recorrerlas dos veces: con una sola pasada
quedan la primera y la última fecha de cada producto, sin importar en qué
orden vengan las filas en el archivo.

### Aritmética de fechas

Restar dos fechas da un `timedelta`, y sumarle un `timedelta` a una fecha la
desplaza:

```python
fin - inicio                    # timedelta: cuánto duró
(fin - inicio).days             # esa duración en días
fecha + timedelta(days=7)       # la fecha de una semana después
```

### Naive vs. aware

Por defecto los objetos son *naive*: no saben en qué zona horaria están. Para
que sean *aware* hay que asociarles un `tzinfo`, por ejemplo con
`zoneinfo.ZoneInfo("America/Argentina/Buenos_Aires")` (desde Python 3.9). Para
este proyecto no hace falta, porque solo se manejan fechas de venta sin hora y
todas del mismo lugar.
