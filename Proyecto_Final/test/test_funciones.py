import unittest

from src.funciones import leer_csv, join, heapsort


class TestLeerCsv(unittest.TestCase):
    def test_archivo_inexistente(self): # Se asegura de que tire un FileNotFoundError si le pasamos un archivo que no existe
        with self.assertRaises(FileNotFoundError):
            leer_csv("no_existe.csv")


class TestJoin(unittest.TestCase):
    def test_ejemplo_de_la_consigna(self): # Prueba el join básico usando los archivos reales de la consigna
        enc_a, filas_a = leer_csv("ArchivoA.csv")
        enc_b, filas_b = leer_csv("ArchivoB.csv")
        enc, filas = join(enc_a, filas_a, enc_b, filas_b)
        self.assertEqual(enc, ["Apellido", "Nombre", "Tipo", "Materia", "Nota"])
        self.assertEqual(len(filas), 12)

    def test_sin_coincidencias(self): # Si nadie coincide en las tablas, el resultado nos tiene que dar una lista vacía
        enc, filas = join(["Nombre", "Tipo"], [["Ana", "A"]], ["Nombre", "Nota"], [["Luis", "8"]])
        self.assertEqual(filas, [])

    def test_join_ambos_vacios(self): # Controla que el join no explote si le pasamos las tablas totalmente vacías
        enc, filas = join(["Nombre"], [], ["Nombre", "Edad"], [])
        self.assertEqual(enc, ["Nombre", "Edad"])
        self.assertEqual(filas, [])

    def test_join_columnas_totalmente_distintas(self): # Al no haber columnas compartidas, mezcla cada fila de A con cada fila de B
        enc, filas = join(["ID"], [["1"]], ["Edad"], [["20"]])
        self.assertEqual(enc, ["ID", "Edad"])
        self.assertEqual(filas, [["1", "20"]])


class TestHeapsort(unittest.TestCase):
    def test_ordena_por_columna(self): # El caso clásico: le damos letras desordenadas y las tiene que acomodar de la A a la Z
        filas = [["c"], ["a"], ["b"]]
        heapsort(filas, 0)
        self.assertEqual(filas, [["a"], ["b"], ["c"]])

    def test_lista_vacia(self): # Se asegura de que el algoritmo no falle ni tire error si la lista no tiene datos
        filas = []
        heapsort(filas, 0)
        self.assertEqual(filas, [])

    def test_sort_lista_ya_ordenada(self): # Si la lista ya vino ordenada, el algoritmo la tiene que dejar exactamente igual
        filas = [["a"], ["b"], ["c"]]
        heapsort(filas, 0)
        self.assertEqual(filas, [["a"], ["b"], ["c"]])

    def test_sort_elementos_repetidos(self): # Controla que el ordenamiento funcione bien y no rompa nada si hay valores duplicados
        filas = [["b"], ["a"], ["b"]]
        heapsort(filas, 0)
        self.assertEqual(filas, [["a"], ["b"], ["b"]])

    def test_sort_por_segunda_columna(self): # Prueba ordenar apuntando a la edad (índice 1) en lugar de la primera columna
        filas = [["Juan", 25], ["Ana", 18], ["Luis", 30]]
        heapsort(filas, 1) # Ordenamos por edad
        self.assertEqual(filas, [["Ana", 18], ["Juan", 25], ["Luis", 30]])
