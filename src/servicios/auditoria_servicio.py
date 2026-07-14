from conexion_bd import obtener_conexion


def listar_cambios_tabla(tabla):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            total = cursor.var(int)
            resultado = conexion.cursor()
            cursor.callproc("PKG_AUDITORIA.LISTAR_CAMBIOS_TABLA",
                            [tabla, total, resultado])
            columnas = [col[0] for col in resultado.description] if resultado.description else []
            filas = resultado.fetchall()
            resultado.close()
            return total.getvalue(), columnas, filas


def purgar_auditoria(dias):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.callproc("PKG_AUDITORIA.PURGAR_AUDITORIA", [dias])
        conexion.commit()