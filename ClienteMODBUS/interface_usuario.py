from clientemodbus import ClienteMODBUS


def menu():

    cliente = ClienteMODBUS('localhost', 502)

    cliente.conectar()

    while True:

        print("\n==========================")
        print("1 - Ler Holding Register")
        print("2 - Escrever Holding Register")
        print("3 - Ler Float")
        print("4 - Escrever Float")
        print("5 - Ler Bits")
        print("6 - Escrever Bit")
        print("7 - Sair")

        op = input("Escolha: ")

        # ======================================================
        # LEITURA HR
        # ======================================================

        if op == '1':

            endereco = int(input("Endereço: "))

            valor = cliente.ler_holding_register(endereco)

            print(f"Valor lido: {valor}")

        # ======================================================
        # ESCRITA HR
        # ======================================================

        elif op == '2':

            endereco = int(input("Endereço: "))
            valor = int(input("Valor: "))

            ok = cliente.escrever_holding_register(
                endereco,
                valor
            )

            print("Sucesso" if ok else "Erro")

        # ======================================================
        # LEITURA FLOAT
        # ======================================================

        elif op == '3':

            endereco = int(input("Endereço inicial: "))

            valor = cliente.ler_float(endereco)

            print(f"Float lido: {valor}")

        # ======================================================
        # ESCRITA FLOAT
        # ======================================================

        elif op == '4':

            endereco = int(input("Endereço inicial: "))
            valor = float(input("Valor float: "))

            ok = cliente.escrever_float(
                endereco,
                valor
            )

            print("Sucesso" if ok else "Erro")

        # ======================================================
        # LEITURA BITS
        # ======================================================

        elif op == '5':

            endereco = int(input("Endereço: "))

            bits = cliente.ler_bits_registrador(endereco)

            if bits is not None:

                print("\nBits do registrador:")

                for i, bit in enumerate(bits):
                    print(f"Bit {i}: {bit}")

        # ======================================================
        # ESCRITA BIT
        # ======================================================

        elif op == '6':

            endereco = int(input("Endereço: "))
            bit = int(input("Bit [0-15]: "))
            valor = int(input("Valor do bit [0/1]: "))

            ok = cliente.escrever_bit(
                endereco,
                bit,
                valor
            )

            print("Sucesso" if ok else "Erro")

        # ======================================================
        # SAIR
        # ======================================================

        elif op == '7':

            cliente.fechar()

            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    menu()