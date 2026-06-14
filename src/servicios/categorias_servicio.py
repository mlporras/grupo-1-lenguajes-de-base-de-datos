from conexion_bd import obtener_conexion


def crear_categoria(nombre, descripcion):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_CATEGORIAS.CREAR_CATEGORIA",
                            [nombre, descripcion])
        conexion.commit()


def actualizar_categoria(id_categoria, nombre, descripcion):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_CATEGORIAS.ACTUALIZAR_CATEGORIA",
                            [id_categoria, nombre, descripcion])
        conexion.commit()


def inactivar_categoria(id_categoria):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_CATEGORIAS.INACTIVAR_CATEGORIA",
                            [id_categoria])
        conexion.commit()


def obtener_categoria(id_categoria):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_CATEGORIAS.OBTENER_CATEGORIA",
                            [id_categoria, resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_categorias():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_CATEGORIAS.LISTAR_CATEGORIAS",
                            [resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas
