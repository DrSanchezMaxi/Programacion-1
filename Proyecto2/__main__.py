import sys

from src.programa import programa


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(
            "El programa requiere dos parámetros: el csv de ventas y el csv de salida.\n"
        )
        return -1

    archivo_entrada = sys.argv[1]
    archivo_salida = sys.argv[2]

    if programa(archivo_entrada, archivo_salida) is None:
        return -2

    return 0


if __name__ == "__main__":
    exit(main())
