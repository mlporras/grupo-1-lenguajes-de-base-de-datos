-- Crea el usuario del proyecto. Si ya existe, no lo borra.
-- Ejecutar como SYS o SYSTEM en orclpdb, no en CDB$ROOT.

DECLARE
  v_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_count FROM all_users WHERE username = 'BIBLIOTECA_USER';
  IF v_count = 0 THEN
    EXECUTE IMMEDIATE q'[CREATE USER biblioteca_user IDENTIFIED BY biblioteca123
      DEFAULT TABLESPACE USERS
      TEMPORARY TABLESPACE TEMP
      QUOTA UNLIMITED ON USERS]';
  END IF;
END;
/

GRANT CONNECT, RESOURCE TO biblioteca_user;
GRANT CREATE SESSION TO biblioteca_user;
GRANT CREATE TABLE TO biblioteca_user;
GRANT CREATE SEQUENCE TO biblioteca_user;
GRANT CREATE PROCEDURE TO biblioteca_user;
GRANT CREATE VIEW TO biblioteca_user;
GRANT CREATE TRIGGER TO biblioteca_user;
