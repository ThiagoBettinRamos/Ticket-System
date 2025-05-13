import sqlite3
from datetime import datetime


def corrigir_datas_antigas():
    conn = sqlite3.connect('sistema_chamados.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, data_hora FROM chamados")
    chamados = cursor.fetchall()

    for chamado in chamados:
        id_chamado, data_str = chamado
        try:
            # Tenta converter do formato antigo dd/mm/yy HH:MM
            dt_obj = datetime.strptime(data_str, "%d/%m/%y %H:%M")
            data_formatada = dt_obj.strftime("%Y-%m-%d %H:%M:%S")

            # Atualiza no banco
            cursor.execute("UPDATE chamados SET data_hora = ? WHERE id = ?", (data_formatada, id_chamado))
            print(f"Chamado {id_chamado}: convertido para {data_formatada}")
        except ValueError:
            # Ignora se já estiver no formato correto ou inválido
            print(f"Chamado {id_chamado}: formato já compatível ou inválido ({data_str})")
            continue

    conn.commit()
    conn.close()
    print("Conversão concluída.")


if __name__ == "__main__":
    corrigir_datas_antigas()
