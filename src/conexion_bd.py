import oracledb
from configuracion import (
    ORACLE_USUARIO, ORACLE_CONTRASENA,
    ORACLE_HOST, ORACLE_PUERTO, ORACLE_SERVICIO
)


def obtener_conexion():
    dsn = f"{ORACLE_HOST}:{ORACLE_PUERTO}/{ORACLE_SERVICIO}"
    return oracledb.connect(
        user=ORACLE_USUARIO,
        password=ORACLE_CONTRASENA,
        dsn=dsn
    )


def probar_conexion():
    try:
        conexion = obtener_conexion()
        conexion.close()
        return True, "Conexion exitosa"
    except Exception as e:
        return False, str(e)
