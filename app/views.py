import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, filedialog, simpledialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.db import registrar_chamado, excluir_chamado, listar_chamados_todos, listar_chamados_periodo
from app.report import gerar_graficos, gerar_pdf

def mostrar_dados():
    dados = listar_chamados_todos()
    janela_dados = Toplevel()
    janela_dados.title("Dados dos Chamados")
    janela_dados.configure(bg="#f4f4f9")
    janela_dados.geometry("700x500")
    tk.Label(janela_dados, text="ID | Descrição | Pessoa | Setor | Hora", font=("Helvetica", 12, "bold"), bg="#f4f4f9", fg="#333").pack(pady=10)
    for dado in dados:
        hora_br = datetime.strptime(dado[4], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')
        chamada_str = f"{dado[0]} | {dado[1]} | {dado[2]} | {dado[3]} | {hora_br}"
        chamada_frame = tk.Frame(janela_dados, bg="#ffffff", bd=2, relief="solid", padx=10, pady=10)
        chamada_frame.pack(pady=5, fill="x")
        tk.Label(chamada_frame, text=chamada_str, font=("Arial", 10), bg="#ffffff", fg="#333").pack(side="left", fill="x", expand=True)
        excluir_btn = tk.Button(chamada_frame, text="Excluir", font=("Arial", 10), bg="#ff6347", fg="white", relief="flat", command=lambda id_chamado=dado[0]: excluir_chamado(id_chamado))
        excluir_btn.pack(side="right", padx=10)

def gerar_relatorio(janela):
    start_date = simpledialog.askstring("Data Inicial", "Informe a data inicial (DD/MM/YYYY):")
    end_date = simpledialog.askstring("Data Final", "Informe a data final (DD/MM/YYYY):")
    try:
        start_date_conv = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        end_date_conv = datetime.strptime(end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        dados = listar_chamados_periodo(start_date_conv, end_date_conv)
        if not dados:
            messagebox.showinfo("Relatório", "Nenhum dado encontrado nesse período.")
            return
        fig = gerar_graficos(dados)
        canvas = FigureCanvasTkAgg(fig, master=janela)
        canvas.get_tk_widget().pack()
        canvas.draw()
        pdf_dir = filedialog.askdirectory(title="Escolha o diretório para salvar o relatório")
        if pdf_dir:
            pdf_path = f"{pdf_dir}/relatorio_chamados.pdf"
            gerar_pdf(dados, start_date_conv, end_date_conv, pdf_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o relatório: {e}")

def criar_interface():
    janela = tk.Tk()
    janela.title("Sistema de Chamados")
    janela.configure(bg="#f4f4f9")
    janela.geometry("500x400")
    header_label = tk.Label(janela, text="Sistema de Chamados", font=("Arial", 18, "bold"), bg="#ff6347", fg="white", pady=10)
    header_label.pack(fill="x")
    tk.Label(janela, text="Descrição do Problema", font=("Arial", 12), bg="#f4f4f9", fg="#333").pack(pady=5)
    descricao_entry = ttk.Entry(janela, width=40, font=("Arial", 12), style="TEntry")
    descricao_entry.pack(pady=5)
    tk.Label(janela, text="Pessoa que Chamou", font=("Arial", 12), bg="#f4f4f9", fg="#333").pack(pady=5)
    pessoa_entry = ttk.Entry(janela, width=40, font=("Arial", 12), style="TEntry")
    pessoa_entry.pack(pady=5)
    tk.Label(janela, text="Setor", font=("Arial", 12), bg="#f4f4f9", fg="#333").pack(pady=5)
    setor_entry = ttk.Entry(janela, width=40, font=("Arial", 12), style="TEntry")
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
    ttk.Button(janela, text="Registrar Chamado", command=on_registrar).pack(pady=15, ipadx=10)
    ttk.Button(janela, text="Ver Todos os Chamados", command=mostrar_dados).pack(pady=10, ipadx=10)
    ttk.Button(janela, text="Gerar Relatório", command=lambda: gerar_relatorio(janela)).pack(pady=10, ipadx=10)
    janela.mainloop()
