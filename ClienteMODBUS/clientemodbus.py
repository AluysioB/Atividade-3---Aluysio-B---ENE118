from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian


class ClienteMODBUS:
    """
    Classe responsável SOMENTE
    pela comunicação Modbus.
    """

    def __init__(self, ip_servidor='localhost', porta=502):

        self._cliente = ModbusTcpClient(
            host=ip_servidor,
            port=porta
        )

    # ==========================================================
    # CONEXÃO
    # ==========================================================

    def conectar(self):
        return self._cliente.connect()

    def fechar(self):
        self._cliente.close()

    # ==========================================================
    # LEITURA E ESCRITA SIMPLES
    # ==========================================================

    def ler_holding_register(self, endereco):

        resposta = self._cliente.read_holding_registers(
            address=endereco,
            count=1,
            slave=1
        )

        if resposta.isError():
            return None

        return resposta.registers[0]

    def escrever_holding_register(self, endereco, valor):

        resposta = self._cliente.write_register(
            address=endereco,
            value=valor,
            slave=1
        )

        return not resposta.isError()

    # ==========================================================
    # FLOAT
    # ==========================================================

    def escrever_float(self, endereco, valor_float):


        registradores = self._cliente.convert_to_registers(valor_float,self._cliente.DATATYPE.FLOAT32)

        resposta = self._cliente.write_registers(
            address=endereco,
            values=registradores,
            slave=1
        )

        return not resposta.isError()

    def ler_float(self, endereco):

        resposta = self._cliente.read_holding_registers(
        address=endereco,
        count=2,
        slave=1
        )

        if resposta.isError():
            return None

        valor = self._cliente.convert_from_registers(
        resposta.registers,
        self._cliente.DATATYPE.FLOAT32
        )

        return valor

    # ==========================================================
    # BITS
    # ==========================================================

    def ler_bits_registrador(self, endereco):

        valor = self.ler_holding_register(endereco)

        if valor is None:
            return None

        bits = []

        for i in range(16):
            bit = (valor >> i) & 1
            bits.append(bit)

        return bits

    def escrever_bit(self, endereco, bit_index, bit_valor):

        valor_atual = self.ler_holding_register(endereco)

        if valor_atual is None:
            return False

        if bit_valor == 1:
            novo_valor = valor_atual | (1 << bit_index)

        else:
            novo_valor = valor_atual & ~(1 << bit_index)

        return self.escrever_holding_register(
            endereco,
            novo_valor
        )