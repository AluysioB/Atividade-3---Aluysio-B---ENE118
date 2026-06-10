from clientemodbus import ClienteMODBUS

cliente = ClienteMODBUS("localhost", 502)

cliente.conectar()

cliente.escrever_float(2000, 12.34)