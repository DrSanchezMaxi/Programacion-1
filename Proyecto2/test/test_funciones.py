import csv
import os
import tempfile
import unittest
from datetime import datetime

from src.funciones import parsear_fecha, validar_encabezado, armar_venta
from src.funciones import leer_ventas, acumular_por_producto, guardar_resumen
from src.funciones import EncabezadoInvalidoError, FilaInvalidaError


ENCABEZADO = ["Fecha", "Producto", "Cantidad", "ValorUnitario"]


# Cada test arma su propio csv temporal. De esa forma los tests quedan
# aislados: no dependen de archivos del proyecto ni de desde que carpeta se
# los ejecute.
class ArchivoTemporalTestCase(unittest.TestCase):
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


# Testing de la funcion parsear_fecha
class TestParsearFecha(unittest.TestCase):
    def test_formato_con_guiones_anio_primero(self):
        self.assertEqual(parsear_fecha("2026-01-05"), datetime(2026, 1, 5))

    def test_formato_con_barras_dia_primero(self):
        self.assertEqual(parsear_fecha("05/01/2026"), datetime(2026, 1, 5))

    def test_formato_con_guiones_dia_primero(self):
        self.assertEqual(parsear_fecha("05-01-2026"), datetime(2026, 1, 5))

    def test_ignora_espacios_alrededor(self):
        self.assertEqual(parsear_fecha("  2026-01-05  "), datetime(2026, 1, 5))

    def test_texto_que_no_es_fecha(self):
        self.assertRaises(ValueError, parsear_fecha, "ayer")

    def test_fecha_inexistente(self):
        # El 30 de febrero no existe: strptime lo rechaza.
        self.assertRaises(ValueError, parsear_fecha, "2026-02-30")

    def test_texto_vacio(self):
        self.assertRaises(ValueError, parsear_fecha, "")


# Testing de la funcion validar_encabezado
class TestValidarEncabezado(unittest.TestCase):
    def test_encabezado_completo(self):
        self.assertIsNone(validar_encabezado(ENCABEZADO))

    def test_no_importa_el_orden(self):
        self.assertIsNone(validar_encabezado(["Producto", "ValorUnitario", "Fecha", "Cantidad"]))

    def test_columnas_de_mas_no_molestan(self):
        self.assertIsNone(validar_encabezado(ENCABEZADO + ["Vendedor"]))

    def test_ignora_espacios(self):
        self.assertIsNone(validar_encabezado([" Fecha ", "Producto", "Cantidad", "ValorUnitario"]))

    def test_falta_una_columna(self):
        self.assertRaises(
            EncabezadoInvalidoError, validar_encabezado, ["Fecha", "Producto", "Cantidad"]
        )

    def test_archivo_sin_encabezado(self):
        self.assertRaises(EncabezadoInvalidoError, validar_encabezado, None)

    def test_informa_cual_falta(self):
        try:
            validar_encabezado(["Fecha", "Producto", "Cantidad"])
        except EncabezadoInvalidoError as error:
            self.assertEqual(error.faltantes, ["ValorUnitario"])
        else:
            self.fail("Se esperaba EncabezadoInvalidoError")


# Testing de la funcion armar_venta
class TestArmarVenta(unittest.TestCase):
    def setUp(self):
        self.fila = {
            "Fecha": "2026-01-05",
            "Producto": "Martillo",
            "Cantidad": "3",
            "ValorUnitario": "4500",
        }

    def test_fila_valida(self):
        venta = armar_venta(self.fila, 2)
        self.assertEqual(venta["producto"], "Martillo")
        self.assertEqual(venta["fecha"], datetime(2026, 1, 5))
        self.assertEqual(venta["cantidad"], 3)
        self.assertEqual(venta["valor_unitario"], 4500.0)

    def test_valor_unitario_con_decimales(self):
        self.fila["ValorUnitario"] = "4500.50"
        self.assertEqual(armar_venta(self.fila, 2)["valor_unitario"], 4500.50)

    def test_cantidad_cero_es_valida(self):
        self.fila["Cantidad"] = "0"
        self.assertEqual(armar_venta(self.fila, 2)["cantidad"], 0)

    def test_producto_vacio(self):
        self.fila["Producto"] = "   "
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_fecha_invalida(self):
        self.fila["Fecha"] = "el martes"
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_cantidad_no_entera(self):
        self.fila["Cantidad"] = "dos"
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_cantidad_con_decimales(self):
        # Son unidades de producto: 2.5 martillos no tiene sentido.
        self.fila["Cantidad"] = "2.5"
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_valor_unitario_no_numerico(self):
        self.fila["ValorUnitario"] = "gratis"
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_cantidad_negativa(self):
        self.fila["Cantidad"] = "-3"
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_valor_unitario_negativo(self):
        self.fila["ValorUnitario"] = "-4500"
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_campo_faltante(self):
        del self.fila["Cantidad"]
        self.assertRaises(FilaInvalidaError, armar_venta, self.fila, 2)

    def test_informa_el_numero_de_fila(self):
        self.fila["Fecha"] = "ayer"
        try:
            armar_venta(self.fila, 7)
        except FilaInvalidaError as error:
            self.assertEqual(error.numero_fila, 7)
        else:
            self.fail("Se esperaba FilaInvalidaError")


# Testing de la funcion leer_ventas
class TestLeerVentas(ArchivoTemporalTestCase):
    def test_lee_todas_las_filas(self):
        ruta = self.armar_csv([
            ENCABEZADO,
            ["2026-01-05", "Martillo", "3", "4500"],
            ["2026-01-06", "Pala", "1", "8900"],
        ])
        self.assertEqual(len(leer_ventas(ruta)), 2)

    def test_archivo_solo_con_encabezado(self):
        ruta = self.armar_csv([ENCABEZADO])
        self.assertFalse(leer_ventas(ruta))

    def test_no_importa_el_orden_de_las_columnas(self):
        ruta = self.armar_csv([
            ["Producto", "Cantidad", "ValorUnitario", "Fecha"],
            ["Martillo", "3", "4500", "2026-01-05"],
        ])
        venta = leer_ventas(ruta)[0]
        self.assertEqual(venta["producto"], "Martillo")
        self.assertEqual(venta["cantidad"], 3)

    def test_producto_con_coma_entre_comillas(self):
        # Esto es lo que el modulo csv resuelve y un split(",") no.
        ruta = self.armar_csv([
            ENCABEZADO,
            ["2026-01-05", "Tornillo, cabeza plana", "3", "4500"],
        ])
        self.assertEqual(leer_ventas(ruta)[0]["producto"], "Tornillo, cabeza plana")

    def test_archivo_inexistente(self):
        self.assertRaises(FileNotFoundError, leer_ventas, "no_existe_este_archivo.csv")

    def test_archivo_vacio(self):
        ruta = self.armar_csv([])
        self.assertRaises(EncabezadoInvalidoError, leer_ventas, ruta)

    def test_encabezado_incompleto(self):
        ruta = self.armar_csv([["Fecha", "Producto"], ["2026-01-05", "Martillo"]])
        self.assertRaises(EncabezadoInvalidoError, leer_ventas, ruta)

    def test_fila_con_dato_invalido(self):
        ruta = self.armar_csv([
            ENCABEZADO,
            ["2026-01-05", "Martillo", "tres", "4500"],
        ])
        self.assertRaises(FilaInvalidaError, leer_ventas, ruta)

    def test_numero_de_fila_del_error(self):
        ruta = self.armar_csv([
            ENCABEZADO,
            ["2026-01-05", "Martillo", "3", "4500"],
            ["2026-01-06", "Pala", "mal", "8900"],
        ])
        try:
            leer_ventas(ruta)
        except FilaInvalidaError as error:
            # Encabezado = 1, primera venta = 2, la que falla = 3.
            self.assertEqual(error.numero_fila, 3)
        else:
            self.fail("Se esperaba FilaInvalidaError")


# Testing de la funcion acumular_por_producto
class TestAcumularPorProducto(unittest.TestCase):
    def setUp(self):
        self.ventas = [
            {"fecha": datetime(2026, 1, 5), "producto": "Martillo",
             "cantidad": 3, "valor_unitario": 4500.0},
            {"fecha": datetime(2026, 1, 10), "producto": "Martillo",
             "cantidad": 2, "valor_unitario": 4500.0},
            {"fecha": datetime(2026, 1, 6), "producto": "Pala",
             "cantidad": 1, "valor_unitario": 8900.0},
        ]

    def test_una_entrada_por_producto(self):
        self.assertEqual(sorted(acumular_por_producto(self.ventas)), ["Martillo", "Pala"])

    def test_acumula_la_cantidad(self):
        self.assertEqual(acumular_por_producto(self.ventas)["Martillo"]["cantidad"], 5)

    def test_acumula_el_total(self):
        # 3 * 4500 + 2 * 4500 == 22500
        self.assertEqual(acumular_por_producto(self.ventas)["Martillo"]["total"], 22500.0)

    def test_el_total_no_es_la_suma_de_las_cantidades(self):
        self.assertNotEqual(acumular_por_producto(self.ventas)["Martillo"]["total"], 5)

    def test_fecha_de_inicio_es_la_primera(self):
        self.assertEqual(
            acumular_por_producto(self.ventas)["Martillo"]["inicio"], datetime(2026, 1, 5)
        )

    def test_fecha_de_fin_es_la_ultima(self):
        self.assertEqual(
            acumular_por_producto(self.ventas)["Martillo"]["fin"], datetime(2026, 1, 10)
        )

    def test_las_fechas_no_dependen_del_orden(self):
        # Las mismas ventas al reves tienen que dar el mismo inicio y fin.
        resumen = acumular_por_producto(list(reversed(self.ventas)))
        self.assertEqual(resumen["Martillo"]["inicio"], datetime(2026, 1, 5))
        self.assertEqual(resumen["Martillo"]["fin"], datetime(2026, 1, 10))

    def test_producto_con_una_sola_venta(self):
        resumen = acumular_por_producto(self.ventas)
        self.assertEqual(resumen["Pala"]["inicio"], resumen["Pala"]["fin"])

    def test_los_productos_no_se_mezclan(self):
        self.assertEqual(acumular_por_producto(self.ventas)["Pala"]["cantidad"], 1)

    def test_sin_ventas(self):
        self.assertFalse(acumular_por_producto([]))


# Testing de la funcion guardar_resumen
class TestGuardarResumen(ArchivoTemporalTestCase):
    def setUp(self):
        self.resumen = {
            "Pala": {
                "inicio": datetime(2026, 1, 6), "fin": datetime(2026, 3, 3),
                "cantidad": 3, "total": 27300.0,
            },
            "Martillo": {
                "inicio": datetime(2026, 1, 5), "fin": datetime(2026, 2, 20),
                "cantidad": 6, "total": 27200.0,
            },
        }

    def leer_salida(self, ruta):
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            return list(csv.reader(archivo))

    def test_devuelve_la_cantidad_de_productos(self):
        self.assertEqual(guardar_resumen(self.resumen, self.ruta_temporal()), 2)

    def test_escribe_el_encabezado(self):
        ruta = self.ruta_temporal()
        guardar_resumen(self.resumen, ruta)
        self.assertEqual(
            self.leer_salida(ruta)[0],
            ["Producto", "FechaInicio", "FechaFin", "CantidadTotal", "ValorTotal"],
        )

    def test_una_fila_por_producto(self):
        ruta = self.ruta_temporal()
        guardar_resumen(self.resumen, ruta)
        # Encabezado + 2 productos
        self.assertEqual(len(self.leer_salida(ruta)), 3)

    def test_productos_ordenados_alfabeticamente(self):
        ruta = self.ruta_temporal()
        guardar_resumen(self.resumen, ruta)
        filas = self.leer_salida(ruta)
        self.assertEqual([filas[1][0], filas[2][0]], ["Martillo", "Pala"])

    def test_formato_de_las_fechas(self):
        ruta = self.ruta_temporal()
        guardar_resumen(self.resumen, ruta)
        self.assertEqual(self.leer_salida(ruta)[1][1], "2026-01-05")

    def test_resumen_vacio_deja_solo_el_encabezado(self):
        ruta = self.ruta_temporal()
        guardar_resumen({}, ruta)
        self.assertEqual(len(self.leer_salida(ruta)), 1)

    def test_producto_con_coma_se_guarda_entre_comillas(self):
        resumen = {
            "Tornillo, cabeza plana": {
                "inicio": datetime(2026, 1, 5), "fin": datetime(2026, 1, 5),
                "cantidad": 1, "total": 100.0,
            }
        }
        ruta = self.ruta_temporal()
        guardar_resumen(resumen, ruta)
        # Releido con csv vuelve entero, no partido en dos campos.
        self.assertEqual(self.leer_salida(ruta)[1][0], "Tornillo, cabeza plana")


if __name__ == "__main__":
    unittest.main()
