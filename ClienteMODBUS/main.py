# Pra funcionar na UF
# import os 
# os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from datetime import datetime

from clientemodbus import ClienteMODBUS


# =====================================================
# CONFIGURAÇÃO DA JANELA
# =====================================================

Window.size = (1100, 650)


# =====================================================
# CARREGAMENTO DOS KV
# =====================================================

Builder.load_file("kv/dashboard.kv")
Builder.load_file("kv/conexao.kv")
Builder.load_file("kv/leitura.kv")
Builder.load_file("kv/escrita.kv")
Builder.load_file("kv/graficos.kv")
Builder.load_file("kv/sobre.kv")
Builder.load_file("kv/main.kv")


# =====================================================
# DASHBOARD
# =====================================================

class DashboardScreen(Screen):
    pass


# =====================================================
# CONEXÃO
# =====================================================

class ConexaoScreen(Screen):

    def conectar(self):

        app = App.get_running_app()

        try:

            ip = self.ids.txt_ip.text
            porta = int(self.ids.txt_porta.text)

            app.cliente_modbus = ClienteMODBUS(
                ip_servidor=ip,
                porta=porta
            )

            if app.cliente_modbus.conectar():

                self.ids.lbl_conexao.text = "Conectado"
                self.ids.lbl_conexao.color = (0, 1, 0, 1)

                self.ids.lbl_ip_conectado.text = ip
                self.ids.lbl_porta_conectada.text = str(porta)
                self.ids.lbl_estado.text = "Online"

                app.root.ids.lb_status.text = "Conectado"
                app.root.ids.lb_status.color = (0, 1, 0, 1)

                dashboard = app.root.ids.content_manager.get_screen(
                    "dashboard"
                )

                dashboard.ids.dash_status.text = "Conectado"
                dashboard.ids.dash_ip.text = ip
                dashboard.ids.dash_porta.text = str(porta)

            else:

                self.ids.lbl_conexao.text = "Falha na conexão"
                self.ids.lbl_conexao.color = (1, 0, 0, 1)

        except Exception as e:

            self.ids.lbl_conexao.text = f"Erro: {e}"
            self.ids.lbl_conexao.color = (1, 0, 0, 1)


# =====================================================
# LEITURA
# =====================================================

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

            dashboard = app.root.ids.content_manager.get_screen(
                "dashboard"
            )

            dashboard.ids.dash_valor.text = str(valor)
            dashboard.ids.dash_atualizacao.text = horario

        except Exception as e:

            self.ids.lbl_resultado.text = f"Erro: {e}"


# =====================================================
# PLACEHOLDERS
# =====================================================

class EscritaScreen(Screen):

    def escrever(self):

        app = App.get_running_app()

        if app.cliente_modbus is None:

            self.ids.lbl_status_escrita.text = "Não conectado"
            return

        try:

            tipo = self.ids.sp_tipo_escrita.text

            endereco = int(
                self.ids.txt_endereco_escrita.text
            )

            sucesso = False

            if tipo == "Holding Register":

                valor = int(
                    self.ids.txt_valor.text
                )

                sucesso = app.cliente_modbus.escrever_holding_register(
                    endereco,
                    valor
                )

            elif tipo == "Float":

                valor = float(
                    self.ids.txt_valor.text
                )

                sucesso = app.cliente_modbus.escrever_float(
                    endereco,
                    valor
                )

            elif tipo == "Coil":

                valor = (
                    self.ids.sp_valor_coil.text == "True"
                )

                sucesso = app.cliente_modbus.escrever_coil(
                    endereco,
                    valor
                )

            elif tipo == "Bit de Holding":

                bit = int(
                    self.ids.txt_bit.text
                )

                valor = int(
                    self.ids.txt_valor_bit.text
                )

                sucesso = app.cliente_modbus.escrever_bit(
                    endereco,
                    bit,
                    valor
                )

            if sucesso:

                self.ids.lbl_status_escrita.text = (
                    "Escrita realizada com sucesso"
                )

                self.ids.lbl_status_escrita.color = (
                    0,
                    1,
                    0,
                    1
                )

            else:

                self.ids.lbl_status_escrita.text = (
                    "Falha na escrita"
                )

                self.ids.lbl_status_escrita.color = (
                    1,
                    0,
                    0,
                    1
                )

        except Exception as e:

            self.ids.lbl_status_escrita.text = str(e)

            self.ids.lbl_status_escrita.color = (
                1,
                0,
                0,
                1
            )
    def atualizar_campos(self):

        tipo = self.ids.sp_tipo_escrita.text

        # =====================================
        # Esconde tudo inicialmente
        # =====================================

        self.ids.box_valor.opacity = 0
        self.ids.box_valor.disabled = True

        self.ids.box_coil.opacity = 0
        self.ids.box_coil.disabled = True

        self.ids.box_bit.opacity = 0
        self.ids.box_bit.disabled = True

        self.ids.box_valor_bit.opacity = 0
        self.ids.box_valor_bit.disabled = True

        # =====================================
        # Holding Register
        # =====================================

        if tipo == "Holding Register":

            self.ids.box_valor.opacity = 1
            self.ids.box_valor.disabled = False

            self.ids.lbl_valor.text = "Valor:"

        # =====================================
        # Float
        # =====================================

        elif tipo == "Float":

            self.ids.box_valor.opacity = 1
            self.ids.box_valor.disabled = False

            self.ids.lbl_valor.text = "Valor Float:"

        # =====================================
        # Coil
        # =====================================

        elif tipo == "Coil":

            self.ids.box_coil.opacity = 1
            self.ids.box_coil.disabled = False

        # =====================================
        # Bit de Holding
        # =====================================

        elif tipo == "Bit de Holding":

            self.ids.box_bit.opacity = 1
            self.ids.box_bit.disabled = False

            self.ids.box_valor_bit.opacity = 1
            self.ids.box_valor_bit.disabled = False

class GraficosScreen(Screen):
    pass


class SobreScreen(Screen):
    pass


# =====================================================
# SCREEN MANAGER
# =====================================================

class ContentManager(ScreenManager):
    pass


# =====================================================
# TELA PRINCIPAL
# =====================================================

class MainScreen(Screen):

    def on_kv_post(self, base_widget):

        Clock.schedule_interval(
            self.atualizar_hora,
            1
        )

    def atualizar_hora(self, dt):

        agora = datetime.now()

        self.ids.lbl_hora.text = agora.strftime(
            "%H:%M:%S"
        )

        self.ids.lbl_data.text = agora.strftime(
            "%d/%m/%Y"
        )


# =====================================================
# APP
# =====================================================

class MeuApp(App):

    def build(self):

        self.cliente_modbus = None

        return MainScreen()


# =====================================================
# EXECUÇÃO
# =====================================================

if __name__ == "__main__":

    MeuApp().run()