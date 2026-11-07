import csv
import sys

from src.funciones import leer_csv, join, heapsort


def mostrar_csv(encabezado, filas):
    escritor = csv.writer(sys.stdout, lineterminator="\n")
    escritor.writerow(encabezado)
    escritor.writerows(filas)


def programa_join(archivo_a, archivo_b):
    try:
        enc_a, filas_a = leer_csv(archivo_a)#se usa enc como abreviatura de encabezado tanto para a como par
        enc_b, filas_b = leer_csv(archivo_b)
    except FileNotFoundError as error:
        sys.stderr.write(f"El archivo '{error.filename}' no existe.\n")
        return -1
    enc, filas = join(enc_a, filas_a, enc_b, filas_b)
    mostrar_csv(enc, filas)
    return 0


def programa_sort(archivo, nombre_columna):
    try:
        enc, filas = leer_csv(archivo)
    except FileNotFoundError:
        sys.stderr.write(f"El archivo '{archivo}' no existe.\n")
        return -1
    if nombre_columna not in enc:
        sys.stderr.write(f"La columna '{nombre_columna}' no existe en el archivo.\n")
        return -2
    heapsort(filas, enc.index(nombre_columna))
    mostrar_csv(enc, filas)
    return 0