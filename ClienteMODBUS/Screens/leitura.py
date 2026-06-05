from kivy.uix.screenmanager import Screen
from kivy.app import App

from datetime import datetime


class LeituraScreen(Screen):

    def ler(self):

        app = App.get_running_app()

        if app.cliente_modbus is None:

            self.ids.lbl_resultado.text = "Não conectado"
            return

        try:

            endereco = int(
                self.ids.txt_endereco.text
            )

            tipo = self.ids.sp_tipo.text

            valor = None

            if tipo == "Holding Register":

                valor = app.cliente_modbus.ler_holding_register(
                    endereco
                )

            elif tipo == "Input Register":

                valor = app.cliente_modbus.ler_input_register(
                    endereco
                )

            elif tipo == "Coil":

                valor = app.cliente_modbus.ler_coil(
                    endereco
                )

            elif tipo == "Discrete Input":

                valor = app.cliente_modbus.ler_discrete_input(
                    endereco
                )

            self.ids.lbl_resultado.text = str(valor)

            self.ids.lbl_tipo_lido.text = tipo

            horario = datetime.now().strftime(
                "%H:%M:%S"
            )

            self.ids.lbl_horario_leitura.text = horario

            dashboard = (
                app.root.ids.content_manager
                .get_screen("dashboard")
            )

            dashboard.ids.dash_valor.text = str(valor)
            dashboard.ids.dash_atualizacao.text = horario

        except Exception as e:

            self.ids.lbl_resultado.text = f"Erro: {e}"