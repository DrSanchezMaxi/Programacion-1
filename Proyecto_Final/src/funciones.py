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

def hundir(filas, padre, tamano, columna): # uso tamano por la falta de ñ
    seguir = True
    while seguir:
        hijo_izq = 2 * padre + 1
        hijo_der = 2 * padre + 2
        mayor = padre
        if hijo_izq < tamano and filas[hijo_izq][columna] > filas[mayor][columna]:
            mayor = hijo_izq
        if hijo_der < tamano and filas[hijo_der][columna] > filas[mayor][columna]:
            mayor = hijo_der
        if mayor == padre:
            seguir = False
        else:
            filas[padre], filas[mayor] = filas[mayor], filas[padre]
            padre = mayor

def heapsort(filas,columna):
    n = len(filas)
    for padre in range(n // 2 - 1, -1, -1):
        hundir(filas, padre, n, columna)
    for fin in range(n - 1, 0, -1):
        filas[0], filas[fin]= filas[fin], filas[0]
        hundir(filas, 0, fin, columna)