import os
import tempfile
import unittest

from funciones_proyecto1 import armar_lista_enteros, promedio_entre_posiciones, EnteroInvalidoError


class TestArmarListaEnteros(unittest.TestCase):
    # Cada test escribe su propio archivo temporal: asi el test no depende de
    # desde que carpeta se lo ejecute.
    def armar_archivo(self, contenido):
        descriptor, ruta = tempfile.mkstemp(suffix=".txt", text=True)
        with os.fdopen(descriptor, "w") as archivo:
            archivo.write(contenido)
        self.addCleanup(os.remove, ruta)
        return ruta

    def test_una_linea(self):
        ruta = self.armar_archivo("10 20 30\n")
        self.assertEqual(armar_lista_enteros(ruta), [10, 20, 30])

    def test_varias_lineas(self):
        ruta = self.armar_archivo("10 20\n30 40\n")
        self.assertEqual(armar_lista_enteros(ruta), [10, 20, 30, 40])

    def test_un_numero_por_linea(self):
        ruta = self.armar_archivo("10\n20\n30\n")
        self.assertEqual(armar_lista_enteros(ruta), [10, 20, 30])

    def test_espacios_de_mas_y_lineas_en_blanco(self):
        ruta = self.armar_archivo("10   20\n\n\t30\n")
        self.assertEqual(armar_lista_enteros(ruta), [10, 20, 30])

    def test_archivo_vacio(self):
        ruta = self.armar_archivo("")
        self.assertEqual(armar_lista_enteros(ruta), [])

    def test_archivo_inexistente(self):
        self.assertRaises(FileNotFoundError, armar_lista_enteros, "no_existe_este_archivo.txt")

    def test_contenido_no_entero(self):
        ruta = self.armar_archivo("10 hola 30\n")
        self.assertRaises(ValueError, armar_lista_enteros, ruta)


class TestPromedioEntrePosiciones(unittest.TestCase):
    def setUp(self):
        self.lista = [10, 20, 30, 40, 50]

    def test_promedio_caso_general(self):
        # Indices 0 a 2, inclusive: (10 + 20 + 30) / 3 = 20.0
        self.assertEqual(promedio_entre_posiciones(self.lista, 0, 2), 20.0)

    def test_promedio_desde_el_cero(self):
        # El enunciado admite el 0: es el primer elemento, no un error.
        self.assertEqual(promedio_entre_posiciones(self.lista, 0, 0), 10.0)

    def test_promedio_lista_completa(self):
        self.assertEqual(promedio_entre_posiciones(self.lista, 0, 4), 30.0)

    def test_entero2_menor_que_entero1(self):
        self.assertEqual(promedio_entre_posiciones(self.lista, 3, 2), 0)

    def test_entero1_mayor_que_longitud(self):
        self.assertEqual(promedio_entre_posiciones(self.lista, 6, 8), 0)

    def test_entero2_mayor_que_longitud(self):
        # Desde el indice 3, el final se recorta al ultimo: (40 + 50) / 2 = 45.0
        self.assertEqual(promedio_entre_posiciones(self.lista, 3, 99), 45.0)

    def test_ultimo_indice(self):
        self.assertEqual(promedio_entre_posiciones(self.lista, 4, 4), 50.0)

    def test_lista_vacia(self):
        self.assertEqual(promedio_entre_posiciones([], 0, 3), 0)

    def test_excepciones_enteros_negativos(self):
        self.assertRaises(EnteroInvalidoError, promedio_entre_posiciones, self.lista, -1, 3)
        self.assertRaises(EnteroInvalidoError, promedio_entre_posiciones, self.lista, 2, -1)


if __name__ == '__main__':
    unittest.main()
