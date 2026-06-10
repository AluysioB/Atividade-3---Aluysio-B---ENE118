from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock

from datetime import datetime


class LeituraScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self._evento = None

    # =================================================
    # COMANDO DO BOTÃO
    # =================================================

    def comando_leitura(self):

        # -----------------------------
        # Leitura simples
        # -----------------------------

        if not self.ids.cb_continuo.active:

            self.ler()
            return

        # -----------------------------
        # Iniciar leitura contínua
        # -----------------------------

        if self._evento is None:

            self._evento = Clock.schedule_interval(
                self.ler_continua,
                1.0
            )

            self.ids.bt_ler.text = "Parar"

        # -----------------------------
        # Parar leitura contínua
        # -----------------------------

        else:

            self._evento.cancel()

            self._evento = None

            self.ids.bt_ler.text = "Iniciar"

    # =================================================
    # LEITURA CONTÍNUA
    # =================================================

    def ler_continua(self, dt):

        self.ler()

    # =================================================
    # LEITURA MODBUS
    # =================================================

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

            elif tipo == "Float":

                valor = app.cliente_modbus.ler_float(
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

    # =================================================
    # AO SAIR DA TELA
    # =================================================

    def on_leave(self):

        if self._evento is not None:

            self._evento.cancel()

            self._evento = None

            self.ids.bt_ler.text = "Ler"
