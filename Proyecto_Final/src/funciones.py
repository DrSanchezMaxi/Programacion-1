import csv

def leer_csv(nombre_archivo):
    with open(nombre_archivo, "r", newline="", encoding="utf-8") as file:
        lector = csv.reader(file)
        encabezado = next(lector)
        filas = []
        for fila in lector:
            filas.append(fila)
        return encabezado, filas


def join(encabezado_a, filas_a, encabezado_b, filas_b):
    comunes = set(encabezado_a) & set(encabezado_b)
    encabezado_nuevo = list(encabezado_a)
    for columna in encabezado_b:
        if columna not in comunes:
            encabezado_nuevo.append(columna)
    filas_nuevas = []
    for fila_a in filas_a:
        for fila_b in filas_b:
            coinciden = True
            for columna in comunes:
                valor_a = fila_a[encabezado_a.index(columna)]
                valor_b = fila_b[encabezado_b.index(columna)]
                if valor_a != valor_b:
                    coinciden = False
            if coinciden:
                fila_combinada = list(fila_a)

                for columna in encabezado_b:
                    if columna not in comunes:
                        posicion = encabezado_b.index(columna)
                        fila_combinada.append(fila_b[posicion])

                filas_nuevas.append(fila_combinada)
                
    return encabezado_nuevo, filas_nuevas