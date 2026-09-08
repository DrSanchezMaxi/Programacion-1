import os
import tempfile
import unittest

from src.funciones import armar_lista_enteros, promedio_entre_indices
from src.funciones import EnteroInvalidoError, PromedioInexistenteError


# Cada test arma su propio archivo temporal. De esa forma los tests quedan
# aislados: no dependen del sistema de archivos del proyecto ni de desde qué
# carpeta se los ejecute.
class ArchivoTemporalTestCase(unittest.TestCase):
    def armar_archivo(self, contenido):
        descriptor, ruta = tempfile.mkstemp(suffix=".txt", text=True)
        with os.fdopen(descriptor, "w") as archivo:
            archivo.write(contenido)
        self.addCleanup(os.remove, ruta)
        return ruta


# Testing de la función armar_lista_enteros
class TestArmarListaEnteros(ArchivoTemporalTestCase):
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

    def test_numeros_negativos(self):
        ruta = self.armar_archivo("-10 20 -30\n")
        self.assertEqual(armar_lista_enteros(ruta), [-10, 20, -30])

    def test_archivo_vacio(self):
        ruta = self.armar_archivo("")
        self.assertFalse(armar_lista_enteros(ruta))

    def test_archivo_inexistente(self):
        self.assertRaises(FileNotFoundError, armar_lista_enteros, "no_existe_este_archivo.txt")

    def test_contenido_no_entero(self):
        ruta = self.armar_archivo("10 hola 30\n")
        self.assertRaises(ValueError, armar_lista_enteros, ruta)


# Testing de la función promedio_entre_indices
class TestPromedioEntreIndices(unittest.TestCase):
    def setUp(self):
        self.lista = [10, 20, 30, 40, 50]

    def test_caso_general(self):
        # Índices 0 a 2, inclusive: (10 + 20 + 30) / 3 == 20.0
        self.assertEqual(promedio_entre_indices(self.lista, 0, 2), 20.0)

    def test_desde_el_cero(self):
        # El enunciado admite el 0: es el primer elemento, no un error.
        self.assertEqual(promedio_entre_indices(self.lista, 0, 0), 10.0)

    def test_lista_completa(self):
        self.assertEqual(promedio_entre_indices(self.lista, 0, 4), 30.0)

    def test_un_solo_indice(self):
        self.assertEqual(promedio_entre_indices(self.lista, 2, 2), 30.0)

    def test_promedio_no_es_la_suma(self):
        self.assertNotEqual(promedio_entre_indices(self.lista, 0, 1), 30)

    def test_ultimo_indice_valido(self):
        # Caso límite: el índice len - 1 sí existe.
        self.assertEqual(promedio_entre_indices(self.lista, 4, 4), 50.0)

    def test_segundo_mayor_que_longitud(self):
        # Desde el índice 3, el final se recorta al último: (40 + 50) / 2 == 45.0
        self.assertEqual(promedio_entre_indices(self.lista, 3, 99), 45.0)

    def test_promedio_con_negativos(self):
        self.assertTrue(promedio_entre_indices([-10, -20, -30], 0, 2) < 0)

    # Sin elementos entre los dos índices no hay promedio: no devuelve 0, falla.
    def test_segundo_menor_que_primero(self):
        self.assertRaises(PromedioInexistenteError, promedio_entre_indices, self.lista, 3, 2)

    def test_primero_mayor_que_longitud(self):
        self.assertRaises(PromedioInexistenteError, promedio_entre_indices, self.lista, 6, 8)

    def test_primero_fuera_de_rango_por_uno(self):
        # Caso límite: el índice len ya no existe, no hay nada que promediar.
        self.assertRaises(PromedioInexistenteError, promedio_entre_indices, self.lista, 5, 7)

    def test_lista_vacia(self):
        self.assertRaises(PromedioInexistenteError, promedio_entre_indices, [], 0, 3)

    def test_indices_reportados_en_la_excepcion(self):
        try:
            promedio_entre_indices(self.lista, 4, 1)
        except PromedioInexistenteError as error:
            self.assertEqual((error.entero1, error.entero2), (4, 1))
        else:
            self.fail("Se esperaba PromedioInexistenteError")

    def test_primero_negativo(self):
        self.assertRaises(EnteroInvalidoError, promedio_entre_indices, self.lista, -1, 3)

    def test_segundo_negativo(self):
        self.assertRaises(EnteroInvalidoError, promedio_entre_indices, self.lista, 2, -1)

    def test_valor_reportado_en_la_excepcion(self):
        try:
            promedio_entre_indices(self.lista, -7, 3)
        except EnteroInvalidoError as error:
            self.assertEqual(error.valor, -7)
        else:
            self.fail("Se esperaba EnteroInvalidoError")


if __name__ == "__main__":
    unittest.main()
