import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def registrar_evento(funcionario, inicio, fim, duracao, ear_medio, camera_id=0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO eventos_sonolencia 
            (funcionario, inicio, fim, duracao_seg, ear_medio, camera_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        funcionario,
        inicio,
        fim,
        float(duracao),      # conversão aqui
        float(ear_medio),    # e aqui
        camera_id
    ))
    conn.commit()
    cur.close()
    conn.close()

def buscar_eventos_hoje():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT funcionario, inicio, fim, duracao_seg, ear_medio
        FROM eventos_sonolencia
        WHERE DATE(inicio) = CURRENT_DATE
        ORDER BY inicio DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows