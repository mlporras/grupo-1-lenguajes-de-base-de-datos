from datetime import datetime
from conexion_bd import obtener_conexion


def registrar_prestamo(cedula, id_material, fecha_devolucion_esperada):
    if isinstance(fecha_devolucion_esperada, str):
        fecha_devolucion_esperada = datetime.strptime(
            fecha_devolucion_esperada, "%d/%m/%Y"
        )
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_PRESTAMOS.REGISTRAR_PRESTAMO",
                            [cedula, id_material, fecha_devolucion_esperada])
        conexion.commit()


def registrar_devolucion(id_prestamo):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_PRESTAMOS.REGISTRAR_DEVOLUCION",
                            [id_prestamo])
        conexion.commit()


def anular_prestamo(id_prestamo):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_PRESTAMOS.ANULAR_PRESTAMO", [id_prestamo])
        conexion.commit()


def obtener_prestamo(id_prestamo):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_PRESTAMOS.OBTENER_PRESTAMO",
                            [id_prestamo, resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_prestamos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_PRESTAMOS.LISTAR_PRESTAMOS", [resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_prestamos_activos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_PRESTAMOS.LISTAR_PRESTAMOS_ACTIVOS",
                            [resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_historial_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_PRESTAMOS.LISTAR_HISTORIAL_USUARIO",
                            [cedula, resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def prestamos_activos_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return cursor.callfunc(
                "PKG_PRESTAMOS.FN_PRESTAMOS_ACTIVOS_USUARIO", int, [cedula]
            )
