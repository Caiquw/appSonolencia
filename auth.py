import bcrypt
import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def cadastrar_gestor(nome, email, senha):
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gestores (nome, email, senha) VALUES (%s, %s, %s)",
        (nome, email, senha_hash)
    )
    conn.commit()
    cur.close()
    conn.close()

def login_funcionario(matricula, senha):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nome, senha, ativo FROM funcionarios WHERE matricula = %s",
        (matricula,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None, "Matrícula não encontrada"
    
    id_func, nome, senha_hash, ativo = row

    if not ativo:
        return None, "Acesso não liberado pelo gestor"

    if not bcrypt.checkpw(senha.encode(), senha_hash.encode()):
        return None, "Senha incorreta"

    return nome, "OK"

def listar_funcionarios(id_gestor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, matricula, nome, ativo FROM funcionarios WHERE id_gestor = %s",
        (id_gestor,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def cadastrar_funcionario(matricula, nome, senha, id_gestor):
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO funcionarios (matricula, nome, senha, ativo, id_gestor) VALUES (%s, %s, %s, FALSE, %s)",
        (matricula, nome, senha_hash, id_gestor)
    )
    conn.commit()
    cur.close()
    conn.close()

def alternar_acesso(id_funcionario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE funcionarios SET ativo = NOT ativo WHERE id = %s",
        (id_funcionario,)
    )
    conn.commit()
    cur.close()
    conn.close()