from conexion_bd import obtener_conexion


def crear_tipo_material(nombre, descripcion):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_TIPOS_MATERIAL.CREAR_TIPO_MATERIAL",
                            [nombre, descripcion])
        conexion.commit()


def actualizar_tipo_material(id_tipo, nombre, descripcion):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_TIPOS_MATERIAL.ACTUALIZAR_TIPO_MATERIAL",
                            [id_tipo, nombre, descripcion])
        conexion.commit()


def inactivar_tipo_material(id_tipo):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_TIPOS_MATERIAL.INACTIVAR_TIPO_MATERIAL",
                            [id_tipo])
        conexion.commit()


def obtener_tipo_material(id_tipo):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_TIPOS_MATERIAL.OBTENER_TIPO_MATERIAL",
                            [id_tipo, resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_tipos_material():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_TIPOS_MATERIAL.LISTAR_TIPOS_MATERIAL",
                            [resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas
