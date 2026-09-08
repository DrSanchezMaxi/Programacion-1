import contextlib
import csv
import io
import os
import tempfile
import unittest

from src.programa import programa


# Testing de la funcion programa: prueba las funciones trabajando juntas, desde
# el archivo de entrada hasta el archivo de salida. La salida por pantalla se
# captura para que no ensucie el reporte de tests.
class TestPrograma(unittest.TestCase):
    def setUp(self):
        self.entrada = self.armar_csv([
            ["Fecha", "Producto", "Cantidad", "ValorUnitario"],
            ["2026-01-05", "Martillo", "3", "4500"],
            ["2026-01-06", "Pala", "1", "8900"],
            ["2026-01-10", "Martillo", "2", "4500"],
        ])
        self.salida = self.ruta_temporal()

    def armar_csv(self, filas):
        descriptor, ruta = tempfile.mkstemp(suffix=".csv", text=True)
        with os.fdopen(descriptor, "w", newline="", encoding="utf-8") as archivo:
            csv.writer(archivo).writerows(filas)
        self.addCleanup(os.remove, ruta)
        return ruta

    def ruta_temporal(self):
        descriptor, ruta = tempfile.mkstemp(suffix=".csv", text=True)
        os.close(descriptor)
        self.addCleanup(os.remove, ruta)
        return ruta

    def correr(self, entrada, salida):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return programa(entrada, salida)

    def leer_salida(self):
        with open(self.salida, "r", newline="", encoding="utf-8") as archivo:
            return list(csv.reader(archivo))

    def test_devuelve_el_resumen(self):
        resumen = self.correr(self.entrada, self.salida)
        self.assertEqual(sorted(resumen), ["Martillo", "Pala"])

    def test_acumula_bien_de_punta_a_punta(self):
        resumen = self.correr(self.entrada, self.salida)
        self.assertEqual(resumen["Martillo"]["cantidad"], 5)
        self.assertEqual(resumen["Martillo"]["total"], 22500.0)

    def test_escribe_el_archivo_de_salida(self):
        self.correr(self.entrada, self.salida)
        filas = self.leer_salida()
        # Encabezado + 2 productos
        self.assertEqual(len(filas), 3)
        self.assertEqual(filas[1], ["Martillo", "2026-01-05", "2026-01-10", "5", "22500.0"])

    def test_archivo_inexistente_no_devuelve_resumen(self):
        self.assertIsNone(self.correr("no_existe_este_archivo.csv", self.salida))

    def test_encabezado_invalido_no_devuelve_resumen(self):
        entrada = self.armar_csv([["Fecha", "Producto"], ["2026-01-05", "Martillo"]])
        self.assertIsNone(self.correr(entrada, self.salida))

    def test_fila_invalida_no_devuelve_resumen(self):
        entrada = self.armar_csv([
            ["Fecha", "Producto", "Cantidad", "ValorUnitario"],
            ["2026-01-05", "Martillo", "tres", "4500"],
        ])
        self.assertIsNone(self.correr(entrada, self.salida))

    def test_los_errores_van_a_stderr_y_no_a_stdout(self):
        pantalla, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(pantalla), contextlib.redirect_stderr(errores):
            programa("no_existe_este_archivo.csv", self.salida)
        self.assertFalse(pantalla.getvalue())
        self.assertTrue("no existe" in errores.getvalue())

    def test_el_error_de_fila_dice_que_fila_fue(self):
        entrada = self.armar_csv([
            ["Fecha", "Producto", "Cantidad", "ValorUnitario"],
            ["2026-01-05", "Martillo", "3", "4500"],
            ["2026-01-06", "Pala", "mal", "8900"],
        ])
        errores = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(errores):
            programa(entrada, self.salida)
        self.assertTrue("Fila 3" in errores.getvalue())

    def test_el_error_de_encabezado_dice_que_columna_falta(self):
        entrada = self.armar_csv([["Fecha", "Producto", "Cantidad"], ["2026-01-05", "M", "1"]])
        errores = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(errores):
            programa(entrada, self.salida)
        self.assertTrue("ValorUnitario" in errores.getvalue())

    def test_entrada_solo_con_encabezado_deja_salida_vacia(self):
        entrada = self.armar_csv([["Fecha", "Producto", "Cantidad", "ValorUnitario"]])
        self.assertFalse(self.correr(entrada, self.salida))
        # Se escribio el archivo igual, solo con el encabezado.
        self.assertEqual(len(self.leer_salida()), 1)


if __name__ == "__main__":
    unittest.main()
