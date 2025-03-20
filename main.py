import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Toplevel

def conectar_banco():
    conn = sqlite3.connect('sistema_chamados.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            pessoa TEXT NOT NULL,
            setor TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def registrar_chamado(descricao, pessoa, setor):
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn, cursor = conectar_banco()
    cursor.execute('''
        INSERT INTO chamados (descricao, pessoa, setor, hora)
        VALUES (?, ?, ?, ?)
    ''', (descricao, pessoa, setor, hora_atual))
    conn.commit()
    conn.close()
    messagebox.showinfo("Chamado Registrado", "O chamado foi registrado com sucesso!")

def excluir_chamado(id_chamado):
    conn, cursor = conectar_banco()
    cursor.execute('DELETE FROM chamados WHERE id = ?', (id_chamado,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Chamado Excluído", f"O chamado ID {id_chamado} foi excluído com sucesso!")

def mostrar_dados():
    conn, cursor = conectar_banco()
    cursor.execute("SELECT * FROM chamados")
    dados = cursor.fetchall()
    conn.close()

    janela_dados = Toplevel()
    janela_dados.title("Dados dos Chamados")
    janela_dados.configure(bg="#f4f4f9")
    janela_dados.geometry("600x400")

    tk.Label(janela_dados, text="ID | Descrição | Pessoa | Setor | Hora", font=("Helvetica", 12, "bold"), bg="#f4f4f9", fg="#333").pack(pady=10)

    for dado in dados:
        chamada_str = f"{dado[0]} | {dado[1]} | {dado[2]} | {dado[3]} | {dado[4]}"
        chamada_label = tk.Label(janela_dados, text=chamada_str, font=("Arial", 10), bg="#f4f4f9", fg="#333")
        chamada_label.pack(pady=5)

        excluir_btn = tk.Button(janela_dados, text="Excluir", font=("Arial", 10), bg="#ff6347", fg="white", relief="flat", bd=2, command=lambda id_chamado=dado[0]: excluir_chamado(id_chamado))
        excluir_btn.pack(pady=5)

def criar_interface():
    janela = tk.Tk()
    janela.title("Sistema de Chamados")
    janela.configure(bg="#f4f4f9")
    janela.geometry("500x400")

    tk.Label(janela, text="Sistema de Chamados", font=("Helvetica", 16, "bold"), bg="#ff6347", fg="white", pady=10).pack()

    tk.Label(janela, text="Descrição do Problema", font=("Arial", 12), bg="#f4f4f9", fg="#333").pack(pady=5)
    descricao_entry = tk.Entry(janela, width=40, font=("Arial", 12), bd=2, relief="solid", fg="#333", bg="#fff", highlightthickness=1)
    descricao_entry.pack(pady=5)

    tk.Label(janela, text="Pessoa que Chamou", font=("Arial", 12), bg="#f4f4f9", fg="#333").pack(pady=5)
    pessoa_entry = tk.Entry(janela, width=40, font=("Arial", 12), bd=2, relief="solid", fg="#333", bg="#fff", highlightthickness=1)
    pessoa_entry.pack(pady=5)

    tk.Label(janela, text="Setor", font=("Arial", 12), bg="#f4f4f9", fg="#333").pack(pady=5)
    setor_entry = tk.Entry(janela, width=40, font=("Arial", 12), bd=2, relief="solid", fg="#333", bg="#fff", highlightthickness=1)
    setor_entry.pack(pady=5)

    def on_registrar():
        descricao = descricao_entry.get()
        pessoa = pessoa_entry.get()
        setor = setor_entry.get()

        if descricao and pessoa and setor:
            registrar_chamado(descricao, pessoa, setor)
            descricao_entry.delete(0, tk.END)
            pessoa_entry.delete(0, tk.END)
            setor_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    tk.Button(janela, text="Registrar Chamado", font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat", bd=2, command=on_registrar).pack(pady=15, ipadx=10)

    tk.Button(janela, text="Ver Todos os Chamados", font=("Arial", 12), bg="#ff6347", fg="white", relief="flat", bd=2, command=mostrar_dados).pack(pady=10, ipadx=10)

    janela.mainloop()

if __name__ == '__main__':
    criar_interface()
