class EnteroInvalidoError(Exception):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor


def armar_lista_enteros(nombre_archivo):
    lista = []
    with open(nombre_archivo, "r") as entrada:
        for linea in entrada:
            # split() sin argumento parte por cualquier cantidad de espacios o
            # tabs y descarta los vacios, asi que tolera lineas en blanco.
            for numero in linea.split():
                lista.append(int(numero))
    return lista


def promedio_entre_posiciones(lista, entero1, entero2):
    # Los enteros son indices en base 0 (el 0 es el primer elemento), tal como
    # los indices de Python, e inclusivos en ambos extremos. El enunciado los
    # pide "mayores o iguales que 0", asi que solo los negativos son invalidos.

    if entero1 < 0:
        raise EnteroInvalidoError(entero1)
    if entero2 < 0:
        raise EnteroInvalidoError(entero2)

    # El segundo entero es menor que el primero: el valor es 0.
    if entero2 < entero1:
        return 0

    # El primer entero es mayor que la longitud de la lista: el valor es 0.
    if entero1 > len(lista):
        return 0

    # El segundo entero llega o pasa el final: se calcula hasta la ultima
    # posicion existente.
    posicion_final = entero2
    if entero2 >= len(lista):
        posicion_final = len(lista) - 1

    # El slicing es exclusivo en el extremo derecho, por eso sumamos 1 para que
    # el segundo entero quede incluido.
    sublista = lista[entero1:posicion_final + 1]

    if len(sublista) == 0:
        return 0

    suma = 0
    for numero in sublista:
        suma += numero

    return suma / len(sublista)
