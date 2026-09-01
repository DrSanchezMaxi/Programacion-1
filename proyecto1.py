import sys

from funciones_proyecto1 import armar_lista_enteros, promedio_entre_posiciones, EnteroInvalidoError


def main():
    if not len(sys.argv) == 4:
        sys.stderr.write("Uso indebido del programa. Debe recibir tres parámetros.\n")
        return -1

    nombre_archivo = sys.argv[1]

    try:
        entero1 = int(sys.argv[2])
        entero2 = int(sys.argv[3])
        lista = armar_lista_enteros(nombre_archivo)
        resultado = promedio_entre_posiciones(lista, entero1, entero2)
    except EnteroInvalidoError as e:
        sys.stderr.write(f"No se puede utilizar el valor: {e.valor}!\n")
        return -2
    except FileNotFoundError:
        sys.stderr.write(f"Error: El archivo '{nombre_archivo}' no existe.\n")
        return -3
    except ValueError:
        sys.stderr.write("Error: Se esperaba que el archivo y los argumentos contengan únicamente números enteros.\n")
        return -4
    else:
        print(f"El resultado es: {resultado}!")
        return 0
    finally:
        print("Goodbye World!")


if __name__ == "__main__":
    exit(main())
