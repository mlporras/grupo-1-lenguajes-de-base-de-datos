from conexion_bd import obtener_conexion


def crear_material(titulo, autor, editorial, anio, isbn, id_tipo, id_categoria):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_MATERIALES.CREAR_MATERIAL",
                            [titulo, autor, editorial, anio, isbn,
                             id_tipo, id_categoria])
        conexion.commit()


def actualizar_material(id_material, titulo, autor, editorial, anio, isbn,
                        id_tipo, id_categoria):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_MATERIALES.ACTUALIZAR_MATERIAL",
                            [id_material, titulo, autor, editorial, anio,
                             isbn, id_tipo, id_categoria])
        conexion.commit()


def inactivar_material(id_material):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_MATERIALES.INACTIVAR_MATERIAL",
                            [id_material])
        conexion.commit()


def obtener_material(id_material):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_MATERIALES.OBTENER_MATERIAL",
                            [id_material, resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_materiales():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_MATERIALES.LISTAR_MATERIALES", [resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def buscar_materiales(texto):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_MATERIALES.BUSCAR_MATERIALES",
                            [texto, resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def material_disponible(id_material):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            return cursor.callfunc(
                "PKG_MATERIALES.FN_MATERIAL_DISPONIBLE", int, [id_material]
            )
