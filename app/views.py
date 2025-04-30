from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from datetime import datetime

from db import listar_chamados_todos, listar_chamados_periodo, registrar_chamado
from report import gerar_pdf, gerar_graficos

class ChamadosApp(App):
    def __init__(self, **kwargs):
        super(ChamadosApp, self).__init__(**kwargs)
        self.descricao_input = None
        self.pessoa_input = None
        self.setor_input = None
        self.registrar_btn = None
        self.ver_btn = None
        self.gerar_rel_btn = None

    def build(self):
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        self.title = "Sistema de Chamados"

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(text="Sistema de Chamados", font_size='28sp', color=(1, 0.4, 0.4, 1))
        layout.add_widget(title)

        form_layout = GridLayout(cols=2, size_hint_y=None, height=300, spacing=10)

        form_layout.add_widget(Label(text="Descrição do Problema:", color=(1, 1, 1, 1)))
        self.descricao_input = TextInput(hint_text="Descrição", multiline=False, size_hint=(0.8, None), height=40)
        form_layout.add_widget(self.descricao_input)

        form_layout.add_widget(Label(text="Pessoa que Chamou:", color=(1, 1, 1, 1)))
        self.pessoa_input = TextInput(hint_text="Pessoa", multiline=False, size_hint=(0.8, None), height=40)
        form_layout.add_widget(self.pessoa_input)

        form_layout.add_widget(Label(text="Setor:", color=(1, 1, 1, 1)))
        self.setor_input = TextInput(hint_text="Setor", multiline=False, size_hint=(0.8, None), height=40)
        form_layout.add_widget(self.setor_input)

        layout.add_widget(form_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        self.registrar_btn = Button(text="Registrar Chamado", background_normal='', background_color=(0.16, 0.58, 0.34, 1), color=(1, 1, 1, 1), font_size='16sp')
        self.registrar_btn.bind(on_press=self.registrar_chamado)
        button_layout.add_widget(self.registrar_btn)

        self.ver_btn = Button(text="Ver Todos os Chamados", background_normal='', background_color=(0.26, 0.48, 0.93, 1), color=(1, 1, 1, 1), font_size='16sp')
        self.ver_btn.bind(on_press=self.mostrar_dados)
        button_layout.add_widget(self.ver_btn)

        self.gerar_rel_btn = Button(text="Gerar Relatório", background_normal='', background_color=(0.94, 0.68, 0.24, 1), color=(1, 1, 1, 1), font_size='16sp')
        self.gerar_rel_btn.bind(on_press=self.gerar_relatorio)
        button_layout.add_widget(self.gerar_rel_btn)

        layout.add_widget(button_layout)

        return layout

    def registrar_chamado(self, instance):
        descricao = self.descricao_input.text
        pessoa = self.pessoa_input.text
        setor = self.setor_input.text
        if descricao and pessoa and setor:
            registrar_chamado(descricao, pessoa, setor)
            self.descricao_input.text = ""
            self.pessoa_input.text = ""
            self.setor_input.text = ""
            self.show_info("Chamado registrado com sucesso!")
        else:
            self.show_error("Todos os campos são obrigatórios!")

    def mostrar_dados(self, instance):
        dados = listar_chamados_todos()
        if not dados:
            self.show_error("Não há chamados registrados para exibir.")
            return

        table_layout = GridLayout(cols=5, size_hint_y=None, height=300)

        table_layout.add_widget(Label(text="ID", bold=True))
        table_layout.add_widget(Label(text="Descrição", bold=True))
        table_layout.add_widget(Label(text="Pessoa", bold=True))
        table_layout.add_widget(Label(text="Setor", bold=True))
        table_layout.add_widget(Label(text="Hora", bold=True))

        for dado in dados:
            table_layout.add_widget(Label(text=str(dado[0])))
            table_layout.add_widget(Label(text=dado[1]))
            table_layout.add_widget(Label(text=dado[2]))
            table_layout.add_widget(Label(text=dado[3]))
            table_layout.add_widget(Label(text=dado[4]))

        popup = Popup(title="Dados dos Chamados", content=table_layout, size_hint=(None, None), size=(700, 400))
        popup.open()

    def gerar_relatorio(self, instance):
        def continuar(instance):
            start_date = start_input.text
            end_date = end_input.text
            popup.dismiss()

            if not start_date or not end_date:
                self.show_error("As datas são obrigatórias!")
                return

            try:
                start_date_conv = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
                end_date_conv = datetime.strptime(end_date, '%d/%m/%Y').strftime('%Y-%m-%d 23:59:59')
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
        start_input = TextInput(hint_text="Data Inicial (DD/MM/YYYY)", multiline=False)
        end_input = TextInput(hint_text="Data Final (DD/MM/YYYY)", multiline=False)
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
