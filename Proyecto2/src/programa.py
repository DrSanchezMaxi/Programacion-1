import sys

from src.funciones import leer_ventas, acumular_por_producto, guardar_resumen
from src.funciones import EncabezadoInvalidoError, FilaInvalidaError


# Resolución del problema: lee el csv de ventas, acumula por producto y guarda
# el resumen en otro csv. Devuelve el diccionario del resumen, o None si hubo
# un error.
def programa(archivo_entrada, archivo_salida):
    try:
        ventas = leer_ventas(archivo_entrada)
        resumen = acumular_por_producto(ventas)
        guardar_resumen(resumen, archivo_salida)
    except FileNotFoundError:
        sys.stderr.write(f"El archivo '{archivo_entrada}' no existe.\n")
        return None
    except EncabezadoInvalidoError as error:
        faltantes = ", ".join(error.faltantes)
        sys.stderr.write(f"El encabezado del csv no tiene las columnas: {faltantes}.\n")
        return None
    except FilaInvalidaError as error:
        sys.stderr.write(f"Fila {error.numero_fila}: {error.motivo}.\n")
        return None
    except PermissionError:
        sys.stderr.write(f"No se puede escribir el archivo '{archivo_salida}'.\n")
        return None
    else:
        # Salida del programa
        print(f"Se acumularon {len(ventas)} ventas de {len(resumen)} productos.")
        print(f"Resumen guardado en: {archivo_salida}")
        return resumen
