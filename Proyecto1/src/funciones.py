class EnteroInvalidoError(Exception):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor


class PromedioInexistenteError(Exception):
    def __init__(self, entero1, entero2):
        super().__init__()
        self.entero1 = entero1
        self.entero2 = entero2


# Función que lee un archivo de números enteros y construye una lista con ellos.
#
# Params: nombre_archivo: str
#
# Exception: FileNotFoundError cuando el archivo no existe
#            ValueError cuando el archivo contiene algo que no es un entero
#
def armar_lista_enteros(nombre_archivo):
    lista = []
    with open(nombre_archivo, "r") as entrada:
        for linea in entrada:
            # split() sin argumento parte por cualquier cantidad de espacios o
            # tabs y descarta los vacios, asi que tolera lineas en blanco.
            for numero in linea.split():
                lista.append(int(numero))
    return lista


# Función que calcula el promedio de los valores de la lista entre dos indices.
# Los indices son base 0 (el 0 es el primer elemento) e inclusivos en ambos
# extremos. El enunciado los pide "mayores o iguales que 0", asi que solo los
# negativos son invalidos.
#
# Params: lista: list[int], entero1: int, entero2: int
#
# Exception: EnteroInvalidoError cuando alguno de los enteros es negativo
#            PromedioInexistenteError cuando entre los dos indices no queda
#            ningun elemento: sin elementos no hay promedio
#
def promedio_entre_indices(lista, entero1, entero2):
    if entero1 < 0:
        raise EnteroInvalidoError(entero1)
    if entero2 < 0:
        raise EnteroInvalidoError(entero2)

    # El segundo entero llega o pasa el final: se calcula hasta la ultima
    # posicion existente.
    posicion_final = entero2
    if entero2 >= len(lista):
        posicion_final = len(lista) - 1

    # El slicing es exclusivo en el extremo derecho, por eso sumamos 1 para que
    # el segundo entero quede incluido.
    sublista = lista[entero1:posicion_final + 1]

    # Cubre los tres casos sin elementos: el segundo indice es menor que el
    # primero, el primero cae fuera de la lista, o la lista esta vacia. El
    # promedio de una lista de longitud 0 no existe, no vale 0.
    if len(sublista) == 0:
        raise PromedioInexistenteError(entero1, entero2)

    suma = 0
    for numero in sublista:
        suma += numero

    return suma / len(sublista)
