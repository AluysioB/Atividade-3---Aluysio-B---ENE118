from pyModbusTCP.server import DataBank, ModbusServer
import random
from time import sleep
import numpy as np
import time


class ServidorMODBUS():
    """
    Classe Servidor Modbus
    """

    def __init__(self, host_ip, port):
        """
        Construtor
        """
        self._db = DataBank()

        self._server = ModbusServer(
            host=host_ip,
            port=port,
            no_block=True,
            data_bank=self._db
        )

    def run(self):
        """
        Execução do servidor Modbus
        """
        try:

            self._server.start()

            print("Servidor MODBUS em execução")

            ultimo_print = time.time()

            while True:

                # ==========================================
                # HOLDING REGISTER
                # ==========================================

                self._db.set_holding_registers(
                    1000,
                    [random.randrange(int(0.95 * 400),
                                      int(1.05 * 400))]
                )

                t = time.time()

                valor_seno = round(10 + 5*np.sin(2*np.pi*0.5*t))
                self._db.set_holding_registers(2000,[valor_seno])

                # ==========================================
                # INPUT REGISTER
                # ==========================================

                self._db.set_input_registers(
                    1000,
                    [random.randrange(100, 201)]
                )

                # ==========================================
                # COIL
                # ==========================================

                self._db.set_coils(
                    1000,
                    [random.choice([True, False])]
                )

                # ==========================================
                # DISCRETE INPUT
                # ==========================================

                self._db.set_discrete_inputs(
                    1000,
                    [random.choice([True, False])]
                )

                if time.time() - ultimo_print >= 2:

                    print('======================')
                    print("Tabela MODBUS")

                    print(
                        f'Holding Register'
                        f'\nR1000: {self._db.get_holding_registers(1000)}'
                        f'\nR2000: {self._db.get_holding_registers(2000)}'
                    )

                    print(
                        f'\nInput Register'
                        f'\nR1000: {self._db.get_input_registers(1000)}'
                    )

                    print(
                        f'\nCoil'
                        f'\nR1000: {self._db.get_coils(1000)}'
                    )

                    print(
                        f'\nDiscrete Input'
                        f'\nR1000: {self._db.get_discrete_inputs(1000)}'
                    )

                    ultimo_print = time.time()

                sleep(0.01)

        except Exception as e:

            print("Erro: ", e.args)