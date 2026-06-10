# Pra funcionar na UF
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from datetime import datetime

# =====================================================
# IMPORTAÇÃO DAS TELAS
# =====================================================

from Screens.dashboard import DashboardScreen
from Screens.conexao import ConexaoScreen
from Screens.leitura import LeituraScreen
from Screens.escrita import EscritaScreen
from Screens.graficos import GraficosScreen
from Screens.sobre import SobreScreen

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

        self.ids.lbl_hora.text = (
            agora.strftime("%H:%M:%S")
        )

        self.ids.lbl_data.text = (
            agora.strftime("%d/%m/%Y")
        )

# =====================================================
# APP
# =====================================================

class MeuApp(App):

    def build(self):

        self.cliente_modbus = None
        self.historico = []

        return MainScreen()
    
# =====================================================
# EXECUÇÃO
# =====================================================

if __name__ == "__main__":

    MeuApp().run()