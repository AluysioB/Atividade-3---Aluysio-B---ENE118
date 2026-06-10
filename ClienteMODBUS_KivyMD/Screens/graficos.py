from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from kivy.graphics.texture import Texture
from kivy.uix.image import Image


class GraficosScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self._evento_leitura = None
        self._evento_grafico = None

        self.historico = []

        self.fig = Figure(figsize=(18, 7))
        self.ax = self.fig.add_subplot(111)

        self.img = Image()

    def on_kv_post(self, base_widget):

        self.ids.grafico_area.add_widget(
            self.img
        )

    # ==========================================
    # INICIAR
    # ==========================================

    def iniciar(self):

        if self._evento_leitura is not None:
            return

        self.historico.clear()

        self._evento_leitura = Clock.schedule_interval(
            self.coletar_dado,
            0.05
        )

        self._evento_grafico = Clock.schedule_interval(
            self.atualizar_grafico,
            0.1
        )

    # ==========================================
    # PARAR
    # ==========================================

    def parar(self):

        if self._evento_leitura is not None:

            self._evento_leitura.cancel()
            self._evento_leitura = None

        if self._evento_grafico is not None:

            self._evento_grafico.cancel()
            self._evento_grafico = None

    # ==========================================
    # COLETA
    # ==========================================

    def coletar_dado(self, dt):

        app = App.get_running_app()

        if app.cliente_modbus is None:
            return

        try:

            endereco = int(
                self.ids.txt_endereco_grafico.text
            )

            valor = (
                app.cliente_modbus
                .ler_holding_register(endereco)
            )

            if valor is not None:

                self.historico.append(valor)

                if len(self.historico) > 500:
                    self.historico.pop(0)

        except:

            pass

    # ==========================================
    # ATUALIZAÇÃO GRÁFICA
    # ==========================================

    def atualizar_grafico(self, dt):

        self.ax.clear()

        self.ax.plot(
        self.historico,
        color='red',
        linewidth=2.5)

        self.ax.set_xlim(
            0,
            500
        )

        endereco = self.ids.txt_endereco_grafico.text

        self.ax.set_title(
            f"Holding Register {endereco}"
        )

        self.ax.grid(
        True,
        linestyle='--',
        alpha=0.4)

        canvas = FigureCanvasAgg(
            self.fig
        )

        canvas.draw()

        renderer = canvas.get_renderer()

        raw_data = renderer.buffer_rgba().tobytes()

        w, h = self.fig.canvas.get_width_height()

        texture = Texture.create(
            size=(w, h),
            colorfmt="rgba"
        )

        texture.blit_buffer(
            raw_data,
            colorfmt="rgba",
            bufferfmt="ubyte"
        )

        texture.flip_vertical()

        self.img.texture = texture

    # ==========================================
    # AO SAIR DA TELA
    # ==========================================

    def on_leave(self):

        self.parar()