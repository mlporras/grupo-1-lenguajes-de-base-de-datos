from conexion_bd import obtener_conexion


def validar_prestamo(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = cursor.var(str)
            cursor.callproc("PKG_VALIDACIONES.VALIDAR_PRESTAMO", [cedula, resultado])
            return resultado.getvalue()


def usuario_activo(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_VALIDACIONES.FN_USUARIO_ACTIVO", int, [cedula]
            ))


def usuario_con_multas_pendientes(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_VALIDACIONES.FN_USUARIO_CON_MULTAS_PENDIENTES", int, [cedula]
            ))