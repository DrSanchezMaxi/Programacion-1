import contextlib
import io
import os
import tempfile
import unittest

from src.programa import programa


# Testing de la función programa: prueba las dos funciones trabajando juntas.
# La salida por pantalla se captura para que no ensucie el reporte de tests.
class TestPrograma(unittest.TestCase):
    def setUp(self):
        descriptor, self.ruta = tempfile.mkstemp(suffix=".txt", text=True)
        with os.fdopen(descriptor, "w") as archivo:
            archivo.write("10 20 30\n40 50\n")
        self.addCleanup(os.remove, self.ruta)

    def correr(self, nombre_archivo, entero1, entero2):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return programa(nombre_archivo, entero1, entero2)

    def test_caso_general(self):
        self.assertEqual(self.correr(self.ruta, 1, 3), 30.0)

    def test_desde_el_cero(self):
        self.assertEqual(self.correr(self.ruta, 0, 0), 10.0)

    def test_lista_completa(self):
        self.assertEqual(self.correr(self.ruta, 0, 4), 30.0)

    def test_segundo_mayor_que_longitud(self):
        self.assertEqual(self.correr(self.ruta, 3, 99), 45.0)

    def test_segundo_menor_que_primero_no_devuelve_resultado(self):
        self.assertIsNone(self.correr(self.ruta, 3, 2))

    def test_primero_fuera_de_rango_no_devuelve_resultado(self):
        self.assertIsNone(self.correr(self.ruta, 9, 12))

    def test_archivo_inexistente_no_devuelve_resultado(self):
        self.assertIsNone(self.correr("no_existe_este_archivo.txt", 1, 3))

    def test_entero_negativo_no_devuelve_resultado(self):
        self.assertIsNone(self.correr(self.ruta, -1, 3))

    def test_mensaje_de_error_va_a_stderr(self):
        salida, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            programa(self.ruta, -5, 3)
        self.assertFalse(salida.getvalue())
        self.assertTrue("-5" in errores.getvalue())

    def test_promedio_inexistente_informa_por_stderr(self):
        salida, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            programa(self.ruta, 3, 2)
        self.assertFalse(salida.getvalue())
        self.assertTrue("no existe el promedio" in errores.getvalue())


if __name__ == "__main__":
    unittest.main()
