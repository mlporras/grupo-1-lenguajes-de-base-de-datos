from conexion_bd import obtener_conexion


def listar_multas_pendientes():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_MULTAS_ATRASOS.LISTAR_MULTAS_PENDIENTES", [resultado])
            columnas = [col[0] for col in resultado.description] if resultado.description else []
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def pagar_multa(id_multa):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_MULTAS_ATRASOS.PAGAR_MULTA", [id_multa])
        conexion.commit()


def generar_multas_automaticas():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_MULTAS_ATRASOS.GENERAR_MULTAS_AUTOMATICAS", [])
        conexion.commit()


def total_multas_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_MULTAS_ATRASOS.FN_TOTAL_MULTAS_USUARIO", int, [cedula]
            )) if False else int(cursor.callfunc(
                "FN_TOTAL_MULTAS_USUARIO", int, [cedula]
            ))