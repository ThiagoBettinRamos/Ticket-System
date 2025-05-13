import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from dateutil.parser import parse

def gerar_graficos(dados):
    import matplotlib.pyplot as plt

    setores = {}
    pessoas = {}
    for dado in dados:
        setores[dado[3]] = setores.get(dado[3], 0) + 1
        pessoas[dado[2]] = pessoas.get(dado[2], 0) + 1

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))  # 2 linhas, 1 coluna

    # Gráfico por setor
    ax[0].bar(setores.keys(), setores.values(), color="skyblue")
    ax[0].set_title("Chamados por Setor")
    ax[0].set_xlabel("Setor")
    ax[0].set_ylabel("Número de Chamados")
    ax[0].tick_params(axis='x', rotation=45)

    # Gráfico por pessoa
    ax[1].bar(pessoas.keys(), pessoas.values(), color="orchid")  # Roxo claro
    ax[1].set_title("Chamados por Pessoa")
    ax[1].set_xlabel("Pessoa")
    ax[1].set_ylabel("Número de Chamados")
    ax[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig.savefig("setores_chart.png")
    plt.close(fig)  # Fecha o gráfico para não travar em ambientes com muitos PDFs

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

    # Tabela
    table_data = [['ID', 'Descrição', 'Pessoa', 'Setor', 'Data/Hora']]
    for dado in dados:
        try:
            data_formatada = parse(dado[4]).strftime('%d/%m/%Y %H:%M')
        except:
            data_formatada = dado[4]
        table_data.append([
            str(dado[0]),
            Paragraph(dado[1], styles['Normal']),
            Paragraph(dado[2], styles['Normal']),
            Paragraph(dado[3], styles['Normal']),
            Paragraph(data_formatada, styles['Normal'])
        ])

    t = Table(table_data, colWidths=[40, 200, 100, 100, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 24))

    # Gráfico
    graph_title = Paragraph("Gráfico de Chamados", styles['Heading2'])
    elements.append(graph_title)
    elements.append(Spacer(1, 12))

    img = RLImage("setores_chart.png", width=400, height=300)
    elements.append(img)
    elements.append(Spacer(1, 24))

    # Resumo Descritivo
    desc_title = Paragraph("Resumo Descritivo dos Chamados", styles['Heading2'])
    elements.append(desc_title)
    elements.append(Spacer(1, 12))

    for dado in dados:
        try:
            data_formatada = parse(dado[4]).strftime('%d/%m/%Y %H:%M')
        except:
            data_formatada = dado[4]
        texto = f"<b>Local:</b> {dado[3]} - {dado[2]} | <b>Serviço:</b> {dado[1]} | <b>Data/Hora:</b> {data_formatada}"
        elements.append(Paragraph(texto, styles['Normal']))
        elements.append(Spacer(1, 6))

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    doc.build(elements)
