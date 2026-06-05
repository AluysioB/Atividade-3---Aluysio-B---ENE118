from kivy.uix.screenmanager import Screen
from kivy.app import App


class EscritaScreen(Screen):

    def on_enter(self):

        self.atualizar_campos()

    # =================================================
    # ATUALIZA INTERFACE
    # =================================================

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

    # =================================================
    # ESCRITA
    # =================================================

    def escrever(self):

        app = App.get_running_app()

        if app.cliente_modbus is None:

            self.ids.lbl_status_escrita.text = (
                "Não conectado"
            )

            self.ids.lbl_status_escrita.color = (
                1,
                0,
                0,
                1
            )

            return

        try:

            tipo = self.ids.sp_tipo_escrita.text

            endereco = int(
                self.ids.txt_endereco_escrita.text
            )

            sucesso = False

            # =================================
            # HOLDING REGISTER
            # =================================

            if tipo == "Holding Register":

                valor = int(
                    self.ids.txt_valor.text
                )

                sucesso = (
                    app.cliente_modbus
                    .escrever_holding_register(
                        endereco,
                        valor
                    )
                )

            # =================================
            # FLOAT
            # =================================

            elif tipo == "Float":

                valor = float(
                    self.ids.txt_valor.text
                )

                sucesso = (
                    app.cliente_modbus
                    .escrever_float(
                        endereco,
                        valor
                    )
                )

            # =================================
            # COIL
            # =================================

            elif tipo == "Coil":

                valor = (
                    self.ids.sp_valor_coil.text
                    == "True"
                )

                sucesso = (
                    app.cliente_modbus
                    .escrever_coil(
                        endereco,
                        valor
                    )
                )

            # =================================
            # BIT DE HOLDING
            # =================================

            elif tipo == "Bit de Holding":

                bit = int(
                    self.ids.txt_bit.text
                )

                valor = int(
                    self.ids.sp_valor_bit.text
                )

                sucesso = (
                    app.cliente_modbus
                    .escrever_bit(
                        endereco,
                        bit,
                        valor
                    )
                )

            # =================================
            # RESULTADO
            # =================================

            if sucesso:

                self.ids.lbl_status_escrita.text = (
                    "Escrita realizada com sucesso"
                )

                self.ids.lbl_status_escrita.color = (
                    0,
                    0.7,
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