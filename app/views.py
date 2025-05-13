from kivy.app import App
SENHA_RELATORIO = "Diretoria25"

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from datetime import datetime
from kivy.uix.scrollview import ScrollView

from db import listar_chamados_todos, listar_chamados_periodo, registrar_chamado, excluir_chamado
from report import gerar_pdf, gerar_graficos

class ChamadosApp(App):
    def __init__(self, **kwargs):
        super(ChamadosApp, self).__init__(**kwargs)
        self.descricao_input = None
        self.pessoa_input = None
        self.setor_input = None
        self.hora_input = None

    def build(self):
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        self.title = "Sistema de Chamados"

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(text="Sistema de Chamados", font_size='28sp', color=(1, 0.4, 0.4, 1))
        layout.add_widget(title)

        form_layout = GridLayout(cols=2, size_hint_y=None, height=400, spacing=10)

        form_layout.add_widget(Label(text="Descrição do Problema:", color=(1, 1, 1, 1)))
        self.descricao_input = TextInput(hint_text="Descrição", multiline=False, height=40)
        form_layout.add_widget(self.descricao_input)

        form_layout.add_widget(Label(text="Pessoa que Chamou:", color=(1, 1, 1, 1)))
        self.pessoa_input = TextInput(hint_text="Pessoa", multiline=False, height=40)
        form_layout.add_widget(self.pessoa_input)

        form_layout.add_widget(Label(text="Setor:", color=(1, 1, 1, 1)))
        self.setor_input = TextInput(hint_text="Setor", multiline=False, height=40)
        form_layout.add_widget(self.setor_input)

        form_layout.add_widget(Label(text="Data e Hora (dd/mm/aa HH:MM):", color=(1, 1, 1, 1)))
        self.hora_input = TextInput(hint_text="Ex: 06/05/25 14:30", multiline=False, height=40)
        form_layout.add_widget(self.hora_input)

        layout.add_widget(form_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        registrar_btn = Button(text="Registrar Chamado", background_normal='', background_color=(0.16, 0.58, 0.34, 1), color=(1, 1, 1, 1))
        registrar_btn.bind(on_press=self.registrar_chamado)
        button_layout.add_widget(registrar_btn)

        ver_btn = Button(text="Ver Todos os Chamados", background_normal='', background_color=(0.26, 0.48, 0.93, 1), color=(1, 1, 1, 1))
        ver_btn.bind(on_press=self.mostrar_dados)
        button_layout.add_widget(ver_btn)

        gerar_rel_btn = Button(text="Gerar Relatório", background_normal='', background_color=(0.94, 0.68, 0.24, 1), color=(1, 1, 1, 1))
        gerar_rel_btn.bind(on_press=self.gerar_relatorio)
        button_layout.add_widget(gerar_rel_btn)

        layout.add_widget(button_layout)

        return layout

    def registrar_chamado(self, instance):
        descricao = self.descricao_input.text.strip()
        pessoa = self.pessoa_input.text.strip()
        setor = self.setor_input.text.strip()
        hora = self.hora_input.text.strip()

        if descricao and pessoa and setor and hora:
            try:
                # Converte do formato dd/mm/aa HH:MM para yyyy-mm-dd HH:MM:SS
                dt = datetime.strptime(hora, "%d/%m/%y %H:%M")
                hora_formatada = dt.strftime("%Y-%m-%d %H:%M:%S")

                registrar_chamado(descricao, pessoa, setor, hora_formatada)

                self.descricao_input.text = ""
                self.pessoa_input.text = ""
                self.setor_input.text = ""
                self.hora_input.text = ""

                self.show_info("Chamado registrado com sucesso!")
            except ValueError:
                self.show_error("Data e hora inválidas. Use o formato dd/mm/aa HH:MM.")
        else:
            self.show_error("Todos os campos são obrigatórios!")

    def mostrar_dados(self, instance):
        dados = listar_chamados_todos()
        if not dados:
            self.show_error("Não há chamados registrados para exibir.")
            return

        scroll = ScrollView(size_hint=(1, 1))
        table_layout = GridLayout(cols=1, size_hint_y=None, spacing=5, padding=5)
        table_layout.bind(minimum_height=table_layout.setter('height'))

        header = GridLayout(cols=6, size_hint_y=None, height=30)
        for titulo in ["ID", "Descrição", "Pessoa", "Setor", "Hora", "Ações"]:
            header.add_widget(Label(text=titulo, bold=True, color=(1, 1, 1, 1)))
        table_layout.add_widget(header)

        for dado in dados:
            row = GridLayout(cols=6, size_hint_y=None, height=60)
            row.add_widget(Label(text=str(dado[0]), color=(1, 1, 1, 1)))
            row.add_widget(Label(text=dado[1], text_size=(200, None), halign="left", valign="top", color=(1, 1, 1, 1)))
            row.add_widget(Label(text=dado[2], color=(1, 1, 1, 1)))
            row.add_widget(Label(text=dado[3], color=(1, 1, 1, 1)))
            row.add_widget(Label(text=dado[4], color=(1, 1, 1, 1)))

            excluir_btn = Button(text="Excluir", size_hint_x=None, width=100, background_color=(0.8, 0.2, 0.2, 1))
            excluir_btn.bind(on_press=lambda btn, id=dado[0]: self.confirmar_exclusao(id))
            row.add_widget(excluir_btn)

            table_layout.add_widget(row)

        scroll.add_widget(table_layout)

        self.popup = Popup(title="Dados dos Chamados", content=scroll, size_hint=(None, None), size=(800, 500))
        self.popup.open()

    def confirmar_exclusao(self, chamado_id):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Tem certeza que deseja excluir o chamado ID {chamado_id}?"))

        button_layout = BoxLayout(spacing=10, size_hint_y=None, height=40)
        sim_btn = Button(text="Sim", background_color=(1, 0.3, 0.3, 1))
        nao_btn = Button(text="Não")

        popup = Popup(title="Confirmar Exclusão", content=content, size_hint=(None, None), size=(400, 200))
        button_layout.add_widget(sim_btn)
        button_layout.add_widget(nao_btn)
        content.add_widget(button_layout)

        sim_btn.bind(on_press=lambda x: self.excluir_chamado(chamado_id, popup))
        nao_btn.bind(on_press=popup.dismiss)

        popup.open()

    def excluir_chamado(self, chamado_id, popup):
        try:
            excluir_chamado(chamado_id)
            popup.dismiss()
            self.popup.dismiss()
            self.show_info(f"Chamado ID {chamado_id} excluído com sucesso!")
        except Exception as e:
            self.show_error(f"Erro ao excluir chamado: {e}")

    def gerar_relatorio(self, instance):
        def verificar_senha(inst):
            senha = senha_input.text.strip()
            senha_popup.dismiss()
            if senha == SENHA_RELATORIO:
                abrir_popup_periodo()
            else:
                self.show_error("Senha incorreta!")

        senha_input = TextInput(password=True, hint_text="Digite a senha", multiline=False)
        confirmar_btn = Button(text="Confirmar", size_hint_y=None, height=40)
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(senha_input)
        box.add_widget(confirmar_btn)
        senha_popup = Popup(title="Acesso Restrito", content=box, size_hint=(None, None), size=(400, 200))
        confirmar_btn.bind(on_press=verificar_senha)
        senha_popup.open()

        def abrir_popup_periodo():
                def parse_data_flexivel(data_str):
                    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
                        try:
                            return datetime.strptime(data_str, fmt)
                        except ValueError:
                            continue
                    raise ValueError("Formato de data inválido. Use dd/mm/aaaa ou dd/mm/aa.")

                def continuar(instance):
                    start_date = start_input.text.strip()
                    end_date = end_input.text.strip()
                    popup.dismiss()

                    if not start_date or not end_date:
                        self.show_error("As datas são obrigatórias!")
                        return

                    try:
                        start_dt = parse_data_flexivel(start_date)
                        end_dt = parse_data_flexivel(end_date)
                        start_date_conv = start_dt.strftime('%Y-%m-%d 00:00:00')
                        end_date_conv = end_dt.strftime('%Y-%m-%d 23:59:59')

                        dados = listar_chamados_periodo(start_date_conv, end_date_conv)

                        if not dados:
                            self.show_error("Nenhum chamado encontrado no período informado.")
                            return

                        gerar_graficos(dados)
                        gerar_pdf(dados, start_date, end_date, "relatorio_chamados.pdf")
                        self.show_info("Relatório gerado com sucesso!")

                    except Exception as e:
                        self.show_error(f"Erro ao gerar relatório: {e}")

                content = BoxLayout(orientation='vertical', spacing=10, padding=10)
                start_input = TextInput(hint_text="Data Inicial (DD/MM/AAAA ou AA)", multiline=False)
                end_input = TextInput(hint_text="Data Final (DD/MM/AAAA ou AA)", multiline=False)
                confirmar = Button(text="Gerar Relatório", size_hint_y=None, height=40)
                content.add_widget(start_input)
                content.add_widget(end_input)
                content.add_widget(confirmar)
                popup = Popup(title="Informe o Período", content=content, size_hint=(None, None), size=(400, 250))
                confirmar.bind(on_press=continuar)
                popup.open()

    def show_error(self, message):
        popup = Popup(title="Erro", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_info(self, message):
        popup = Popup(title="Info", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


if __name__ == '__main__':
            ChamadosApp().run()
