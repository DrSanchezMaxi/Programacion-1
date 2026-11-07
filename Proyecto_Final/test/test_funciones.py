import unittest

from src.funciones import leer_csv, join, heapsort


class TestLeerCsv(unittest.TestCase):
    def test_archivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            leer_csv("no_existe.csv")


class TestJoin(unittest.TestCase):
    def test_ejemplo_de_la_consigna(self):
        enc_a, filas_a = leer_csv("ArchivoA.csv")
        enc_b, filas_b = leer_csv("ArchivoB.csv")
        enc, filas = join(enc_a, filas_a, enc_b, filas_b)
        self.assertEqual(enc, ["Apellido", "Nombre", "Tipo", "Materia", "Nota"])
        self.assertEqual(len(filas), 12)

    def test_sin_coincidencias(self):
        enc, filas = join(["Nombre", "Tipo"], [["Ana", "A"]], ["Nombre", "Nota"], [["Luis", "8"]])
        self.assertEqual(filas, [])


class TestHeapsort(unittest.TestCase):
    def test_ordena_por_columna(self):
        filas = [["c"], ["a"], ["b"]]
        heapsort(filas, 0)
        self.assertEqual(filas, [["a"], ["b"], ["c"]])

    def test_lista_vacia(self):
        filas = []
        heapsort(filas, 0)
        self.assertEqual(filas, [])