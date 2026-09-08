import csv
from datetime import datetime

# Formatos de fecha aceptados en la columna Fecha del archivo de entrada.
FORMATOS_FECHA = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]

# Columnas que tiene que traer el encabezado del archivo de entrada.
COLUMNAS = ["Fecha", "Producto", "Cantidad", "ValorUnitario"]

# Columnas del archivo de salida.
COLUMNAS_SALIDA = ["Producto", "FechaInicio", "FechaFin", "CantidadTotal", "ValorTotal"]


class EncabezadoInvalidoError(Exception):
    def __init__(self, faltantes):
        super().__init__()
        self.faltantes = faltantes


class FilaInvalidaError(Exception):
    def __init__(self, numero_fila, motivo):
        super().__init__()
        self.numero_fila = numero_fila
        self.motivo = motivo


# Función que convierte un texto a una fecha probando los formatos aceptados.
#
# Params: texto: str
#
# Return: datetime
#
# Exception: ValueError cuando el texto no coincide con ningun formato
#
def parsear_fecha(texto):
    texto = texto.strip()
    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            # Este formato no era, se prueba con el siguiente.
            continue
    raise ValueError(f"fecha invalida: {texto}")


# Función que revisa que el encabezado traiga las columnas que el programa
# necesita. Como se lee con DictReader, el orden en que vengan no importa.
#
# Params: nombres: list[str] o None
#
# Exception: EncabezadoInvalidoError cuando falta alguna columna
#
def validar_encabezado(nombres):
    if nombres is None:
        raise EncabezadoInvalidoError(COLUMNAS)

    presentes = []
    for nombre in nombres:
        presentes.append(nombre.strip())

    faltantes = []
    for columna in COLUMNAS:
        if columna not in presentes:
            faltantes.append(columna)

    if faltantes:
        raise EncabezadoInvalidoError(faltantes)


# Función que convierte una fila del csv en una venta ya validada.
#
# Params: fila: dict, numero_fila: int
#
# Return: dict con las claves fecha, producto, cantidad y valor_unitario
#
# Exception: FilaInvalidaError cuando algun campo falta o no se puede convertir
#
def armar_venta(fila, numero_fila):
    for columna in COLUMNAS:
        if fila.get(columna) is None:
            raise FilaInvalidaError(numero_fila, f"falta el campo {columna}")

    producto = fila["Producto"].strip()
    if not producto:
        raise FilaInvalidaError(numero_fila, "el producto no puede estar vacio")

    try:
        fecha = parsear_fecha(fila["Fecha"])
    except ValueError:
        raise FilaInvalidaError(numero_fila, "la fecha no tiene un formato valido")

    try:
        cantidad = int(fila["Cantidad"].strip())
    except ValueError:
        raise FilaInvalidaError(numero_fila, "la cantidad tiene que ser un numero entero")

    try:
        valor_unitario = float(fila["ValorUnitario"].strip())
    except ValueError:
        raise FilaInvalidaError(numero_fila, "el valor unitario tiene que ser un numero")

    if cantidad < 0:
        raise FilaInvalidaError(numero_fila, "la cantidad no puede ser negativa")
    if valor_unitario < 0:
        raise FilaInvalidaError(numero_fila, "el valor unitario no puede ser negativo")

    return {
        "fecha": fecha,
        "producto": producto,
        "cantidad": cantidad,
        "valor_unitario": valor_unitario,
    }


# Función que lee el archivo csv de ventas y devuelve una lista de ventas.
#
# Params: nombre_archivo: str
#
# Return: list[dict]
#
# Exception: FileNotFoundError cuando el archivo no existe
#            EncabezadoInvalidoError cuando el encabezado no tiene las columnas
#            FilaInvalidaError cuando una fila tiene datos que no se entienden
#
def leer_ventas(nombre_archivo):
    ventas = []

    with open(nombre_archivo, "r", newline="", encoding="utf-8") as entrada:
        lector = csv.DictReader(entrada)
        validar_encabezado(lector.fieldnames)

        # La fila 1 es el encabezado, por eso los datos arrancan en la 2.
        numero_fila = 1
        for fila in lector:
            numero_fila += 1
            ventas.append(armar_venta(fila, numero_fila))

    return ventas


# Función que acumula las ventas por producto. Para cada producto guarda la
# fecha de la primera y de la ultima venta, la cantidad total vendida y el
# valor total vendido.
#
# Params: ventas: list[dict]
#
# Return: dict[str, dict]
#
def acumular_por_producto(ventas):
    resumen = {}

    for venta in ventas:
        producto = venta["producto"]
        total_venta = venta["cantidad"] * venta["valor_unitario"]

        if producto not in resumen:
            resumen[producto] = {
                "inicio": venta["fecha"],
                "fin": venta["fecha"],
                "cantidad": venta["cantidad"],
                "total": total_venta,
            }
        else:
            acumulado = resumen[producto]
            # Los datetime se comparan directamente, asi que min y max alcanzan
            # para ir quedandose con la primera y con la ultima fecha.
            acumulado["inicio"] = min(acumulado["inicio"], venta["fecha"])
            acumulado["fin"] = max(acumulado["fin"], venta["fecha"])
            acumulado["cantidad"] += venta["cantidad"]
            acumulado["total"] += total_venta

    return resumen


# Función que guarda el resumen en un archivo csv, una fila por producto y los
# productos ordenados alfabeticamente.
#
# Params: resumen: dict[str, dict], nombre_archivo: str
#
# Return: int, la cantidad de productos escritos
#
def guardar_resumen(resumen, nombre_archivo):
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.writer(salida)
        escritor.writerow(COLUMNAS_SALIDA)

        for producto in sorted(resumen):
            datos = resumen[producto]
            escritor.writerow([
                producto,
                datos["inicio"].strftime("%Y-%m-%d"),
                datos["fin"].strftime("%Y-%m-%d"),
                datos["cantidad"],
                round(datos["total"], 2),
            ])

    return len(resumen)
