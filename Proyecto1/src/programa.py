import sys

from src.funciones import armar_lista_enteros, promedio_entre_indices
from src.funciones import EnteroInvalidoError, PromedioInexistenteError


# Resolución del problema: lee el archivo, calcula el promedio entre los dos
# indices y lo informa. Devuelve el promedio, o None si hubo un error.
def programa(nombre_archivo, entero1, entero2):
    try:
        lista = armar_lista_enteros(nombre_archivo)
        resultado = promedio_entre_indices(lista, entero1, entero2)
    except EnteroInvalidoError as error:
        sys.stderr.write(f"No se puede utilizar el valor: {error.valor}\n")
        return None
    except PromedioInexistenteError as error:
        sys.stderr.write(
            f"No hay elementos entre los índices {error.entero1} y {error.entero2}: "
            "no existe el promedio.\n"
        )
        return None
    except FileNotFoundError:
        sys.stderr.write(f"El archivo '{nombre_archivo}' no existe.\n")
        return None
    except ValueError:
        sys.stderr.write("El archivo debe contener únicamente números enteros.\n")
        return None
    else:
        # Salida del programa
        print(f"Promedio entre los índices {entero1} y {entero2}: {resultado}")
        return resultado
