CREATE TABLE audit_log (
    audit_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_name VARCHAR2(100),
    action_type VARCHAR2(50),
    table_name VARCHAR2(100),
    sql_text CLOB,
    action_time TIMESTAMP DEFAULT SYSTIMESTAMP
);
