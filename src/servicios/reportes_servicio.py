from conexion_bd import obtener_conexion


def listar_materiales_disponibles():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_REPORTES.REPORTE_MATERIALES_DISPONIBLES",
                            [resultado])
            columnas = [col[0] for col in resultado.description] if resultado.description else []
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_prestamos_vencidos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_REPORTES.REPORTE_PRESTAMOS_VENCIDOS",
                            [resultado])
            columnas = [col[0] for col in resultado.description] if resultado.description else []
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def marcar_prestamos_vencidos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_REPORTES.MARCAR_PRESTAMOS_VENCIDOS", [])
        conexion.commit()


def total_materiales_disponibles():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_REPORTES.FN_TOTAL_MATERIALES_DISPONIBLES", int, []
            ))


def total_prestamos_activos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_REPORTES.FN_TOTAL_PRESTAMOS_ACTIVOS", int, []
            ))


def total_usuarios_activos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_REPORTES.FN_TOTAL_USUARIOS_ACTIVOS", int, []
            ))


def total_prestamos_vencidos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_REPORTES.FN_PRESTAMOS_VENCIDOS", int, []
            ))


def total_materiales_por_tipo(id_tipo_material):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_REPORTES.FN_TOTAL_MATERIALES_POR_TIPO", int,
                [id_tipo_material]
            ))


def dias_retraso(id_prestamo):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_REPORTES.FN_DIAS_RETRASO", int, [id_prestamo]
            ))


def material_mas_prestado():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_REPORTES.FN_MATERIAL_MAS_PRESTADO", int, []
            ))


def consultar_materiales_por_categoria(id_categoria):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_CONSULTAS.CONSULTAR_MATERIALES_POR_CATEGORIA",
                            [id_categoria, resultado])
            columnas = [col[0] for col in resultado.description] if resultado.description else []
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def consultar_historial_por_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_CONSULTAS.CONSULTAR_HISTORIAL_POR_USUARIO",
                            [cedula, resultado])
            columnas = [col[0] for col in resultado.description] if resultado.description else []
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def total_prestamos_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_CONSULTAS.FN_TOTAL_PRESTAMOS_USUARIO", int, [cedula]
            ))


def existe_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_CONSULTAS.FN_EXISTE_USUARIO", int, [cedula]
            ))


def total_materiales_inactivos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_CONSULTAS.FN_TOTAL_MATERIALES_INACTIVOS", int, []
            ))


def total_prestamos_devueltos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return int(cursor.callfunc(
                "PKG_CONSULTAS.FN_TOTAL_PRESTAMOS_DEVUELTOS", int, []
            ))
