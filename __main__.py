import sys

from src.programa import programa


def main():
    if len(sys.argv) != 4:
        sys.stderr.write("El programa requiere tres parámetros: archivo, entero, entero.\n")
        return -1

    nombre_archivo = sys.argv[1]

    try:
        entero1 = int(sys.argv[2])
        entero2 = int(sys.argv[3])
    except ValueError:
        sys.stderr.write("El segundo y el tercer parámetro deben ser números enteros.\n")
        return -2

    if programa(nombre_archivo, entero1, entero2) is None:
        return -3

    return 0


if __name__ == "__main__":
    exit(main())
