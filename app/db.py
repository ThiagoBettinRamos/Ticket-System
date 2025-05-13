import sqlite3

def conectar_banco():
    conn = sqlite3.connect('sistema_chamados.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            pessoa TEXT NOT NULL,
            setor TEXT NOT NULL,
            data_hora TEXT NOT NULL
        );
    ''')
    conn.commit()
    return conn, cursor

def registrar_chamado(descricao, pessoa, setor, data_hora):
    conn, cursor = conectar_banco()
    cursor.execute('''
        INSERT INTO chamados (descricao, pessoa, setor, data_hora)
        VALUES (?, ?, ?, ?)
    ''', (descricao, pessoa, setor, data_hora))
    conn.commit()
    conn.close()

def excluir_chamado(id_chamado):
    conn, cursor = conectar_banco()
    cursor.execute('DELETE FROM chamados WHERE id = ?', (id_chamado,))
    conn.commit()
    conn.close()

def listar_chamados_periodo(start_date, end_date):
    conn, cursor = conectar_banco()
    cursor.execute("SELECT * FROM chamados WHERE data_hora BETWEEN ? AND ?", (start_date, end_date))
    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_chamados_todos():
    conn, cursor = conectar_banco()
    cursor.execute("SELECT * FROM chamados")
    dados = cursor.fetchall()
    conn.close()
    return dados
