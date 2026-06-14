from conexion_bd import obtener_conexion


def crear_usuario(cedula, nombre, apellidos, correo, telefono):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_USUARIOS.CREAR_USUARIO",
                            [cedula, nombre, apellidos, correo, telefono])
        conexion.commit()


def actualizar_usuario(cedula, nombre, apellidos, correo, telefono):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_USUARIOS.ACTUALIZAR_USUARIO",
                            [cedula, nombre, apellidos, correo, telefono])
        conexion.commit()


def inactivar_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_USUARIOS.INACTIVAR_USUARIO", [cedula])
        conexion.commit()


def obtener_usuario(cedula):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_USUARIOS.OBTENER_USUARIO",
                            [cedula, resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas


def listar_usuarios():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            resultado = conexion.cursor()
            cursor.callproc("PKG_USUARIOS.LISTAR_USUARIOS", [resultado])
            columnas = [col[0] for col in resultado.description]
            filas = resultado.fetchall()
            resultado.close()
            return columnas, filas
