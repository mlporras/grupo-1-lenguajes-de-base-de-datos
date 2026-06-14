import os
from dotenv import load_dotenv

_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_raiz, '.env'))

ORACLE_USUARIO = os.getenv("ORACLE_USUARIO", "biblioteca_user")
ORACLE_CONTRASENA = os.getenv("ORACLE_CONTRASENA", "biblioteca123")
ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
ORACLE_PUERTO = os.getenv("ORACLE_PUERTO", "1521")
ORACLE_SERVICIO = os.getenv("ORACLE_SERVICIO", "XEPDB1")
