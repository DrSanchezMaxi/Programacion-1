import csv

def leer_csv(nombre_archivo):
    with open(nombre_archivo, "r", newline="", encoding="utf-8") as file:
        lector = csv.reader(file)
        encabezado = next(lector)
        filas = []
        for fila in lector:
            filas.append(fila)
        return encabezado, filas