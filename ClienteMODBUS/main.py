from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from clientemodbus import ClienteMODBUS
from kivy.core.window import Window

Window.size = (900, 600)

class ModbusWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._cliente = None

    def conectar(self):

        ip = self.ids.txt_ip.text
        porta = int(self.ids.txt_porta.text)

        self._cliente = ClienteMODBUS(
            ip,
            porta
        )

        if self._cliente.conectar():

            self.ids.lb_status.text = "Conectado"
            self.ids.lb_status.color = (0, 1, 0, 1)

        else:

            self.ids.lb_status.text = "Falha na conexão"
            self.ids.lb_status.color = (1, 0, 0, 1)



    def ler(self):

        if self._cliente is None:

            self.ids.lb_resultado.text = "Não conectado"
            return

        endereco = int(
            self.ids.txt_endereco.text
        )

        tipo = self.ids.sp_tipo.text

        valor = None

        if tipo == "Holding Register":

            valor = self._cliente.ler_holding_register(
                endereco
            )

        elif tipo == "Input Register":

            valor = self._cliente.ler_input_register(
                endereco
            )

        elif tipo == "Coil":

            valor = self._cliente.ler_coil(
                endereco
            )

        elif tipo == "Discrete Input":

            valor = self._cliente.ler_discrete_input(
                endereco
            )

        self.ids.lb_resultado.text = str(valor)


class ModbusApp(App):

    def build(self):
        return ModbusWidget()


if __name__ == "__main__":
    ModbusApp().run()