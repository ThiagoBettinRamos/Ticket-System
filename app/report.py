import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

def gerar_graficos(dados):
    setores = {}
    pessoas = {}
    for dado in dados:
        setores[dado[3]] = setores.get(dado[3], 0) + 1
        pessoas[dado[2]] = pessoas.get(dado[2], 0) + 1
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].bar(setores.keys(), setores.values(), color="skyblue")
    ax[0].set_title("Chamados por Setor")
    ax[0].set_xlabel("Setor")
    ax[0].set_ylabel("Número de Chamados")
    ax[1].bar(pessoas.keys(), pessoas.values(), color="salmon")
    ax[1].set_title("Chamados por Pessoa")
    ax[1].set_xlabel("Pessoa")
    ax[1].set_ylabel("Número de Chamados")
    plt.tight_layout()
    fig.savefig("setores_chart.png")
    return fig

def gerar_pdf(dados, start_date, end_date, pdf_path):
    styles = getSampleStyleSheet()
    elements = []
    title = Paragraph(f"Relatório de Chamados de {start_date} até {end_date}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    subtitle = Paragraph("Resumo dos Chamados", styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 12))
    table_data = [['ID', 'Descrição', 'Pessoa', 'Setor', 'Hora']]
    for dado in dados:
        hora_br = datetime.strptime(dado[4], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')
        table_data.append([str(dado[0]), dado[1], dado[2], dado[3], hora_br])
    t = Table(table_data, colWidths=[40, 150, 100, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 24))
    graph_title = Paragraph("Gráfico de Chamados", styles['Heading2'])
    elements.append(graph_title)
    elements.append(Spacer(1, 12))
    img = RLImage("setores_chart.png", width=400, height=300)
    elements.append(img)
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    doc.build(elements)
