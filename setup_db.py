# setup_db.py
import psycopg2
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS gestores (
        id       SERIAL PRIMARY KEY,
        nome     VARCHAR(100),
        email    VARCHAR(100) UNIQUE,
        senha    VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS funcionarios (
        id        SERIAL PRIMARY KEY,
        matricula VARCHAR(20) UNIQUE,
        nome      VARCHAR(100),
        senha     VARCHAR(255),
        ativo     BOOLEAN DEFAULT FALSE,
        id_gestor INT REFERENCES gestores(id)
    );
""")

conn.commit()
cur.close()
conn.close()
print("Tabelas criadas com sucesso!")