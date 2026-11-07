import sys

from src.programa import programa_join, programa_sort


def main():
    if len(sys.argv) != 4:
        sys.stderr.write("Uso: join archivoA.csv archivoB.csv  |  sort archivo.csv columna\n")
        return -3

    comando = sys.argv[1]

    if comando == "join":
        return programa_join(sys.argv[2], sys.argv[3])
    elif comando == "sort":
        return programa_sort(sys.argv[2], sys.argv[3])
    else:
        sys.stderr.write(f"Comando '{comando}' desconocido. Usá join o sort.\n")
        return -4


if __name__ == "__main__":
    exit(main())