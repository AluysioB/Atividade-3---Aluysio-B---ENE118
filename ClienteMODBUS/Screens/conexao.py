from kivy.uix.screenmanager import Screen
from kivy.app import App

from clientemodbus import ClienteMODBUS


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

                dashboard = (
                    app.root.ids.content_manager
                    .get_screen("dashboard")
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