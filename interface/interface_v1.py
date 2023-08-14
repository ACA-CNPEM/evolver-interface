import serial
import time

comm = serial.Serial(
    port = '/dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

channel2ss = [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1]

pump_a = [39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40]
pump_b = [23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24]
pump_c = [7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]


def envia_string(message):
    comm.write(str.encode(message))
    time.sleep(1)

def le_string():
    message = comm.readline().decode()

    while (comm.inWaiting() != 0):
        message += comm.read().decode()

    return message


def ss_inputs(qtd):
    inputs = []
    inputs += [-1]

    for i in range(qtd):
        inputs += [input(f"> [SS{i+1}]: ")]
    print()

    return inputs


def le_inputs(qtd):
    inputs = ss_inputs(qtd)
    print("Você digitou: ", inputs[1:17])

    enviar = input("> Gostaria de enviar isso? [y/n]\n")
    print()

    while (enviar != 'y'):

        if (enviar != 'n'):
            enviar = input("> Responda com [y/n]\n")
            print()

        else:
            novamente = input("> Gostaria de tentar novamente? [y/n]\n")
            print()

            while (novamente != 'y' and novamente != 'n'):
                novamente = input("> Responda com [y/n]\n")

            if (novamente == 'y'):
                print("Tente novamente:")
                inputs = ss_inputs(qtd)

                print("Você digitou: ", inputs[1:17])
                enviar = input("> Gostaria de enivar isso? [y/n]\n")
                print()

            else:
                return -1

    return inputs


def tipo_de_comando():
    tipo = input("> Que tipo de comando gostaria de enviar, instantâneo ou recorrente?\nDigite i para instantâneo e r para recorrente.\n")
    print()

    while (tipo != 'i' and tipo != 'r'):
        tipo = input("> Escolha entre i ou r\n")
        print()

    return tipo


def stir():
    print("Atualize os valores para cada ventoinha:")
    stir_inputs = le_inputs(16)
    tipo = tipo_de_comando()

    input_string = f"stir{tipo},"
    for i in range(16):
        input_string += f"{stir_inputs[channel2ss[i]]},"
    input_string += "_!"

    envia_string(input_string)
    echo_recebido = le_string()

    print("Esse é o comando enviado:")
    print(f"Enviado: {input_string}\nEchoado: {echo_recebido}\n")

    acknowledge = input("> Gostaria de executá-lo? [y/n]\n")
    print()

    while (acknowledge != 'y' and acknowledge != 'n'):
        acknowledge = input("Responda com [y/n]\n")

    if (acknowledge == 'y'):
        envia_string("stira,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!")
        print("Executando...\n")


def temp():
    print("Atualize o setpoint de temperatura de cada Smart Sleeve:")
    temp_inputs = le_inputs(16)
    tipo = tipo_de_comando()

    input_string = f"temp{tipo},"
    for i in range(16):
        input_string += f"{temp_inputs[channel2ss[i]]},"
    input_string += "_!"

    envia_string(input_string)
    texto_recebido = le_string()

    for i in range(len(texto_recebido)):
        if (texto_recebido[i] == 'e'):
            if (i+1 < len(texto_recebido) and texto_recebido[i+1] == 'n'):
                if(i+2 < len(texto_recebido) and texto_recebido[i+2] == 'd'):
                    echo = texto_recebido[0:i+3]
                    broadcast = texto_recebido[i+3:]
                    break

    print(f"Esse é o comando enviado:\nEnviado - {input_string}\nEchoado - {echo}\n")

    print(f"E esse é o estado atual do sistema:\n{broadcast}\n")

    acknowledge = input("> Gostaria de executar o comando? [y/n]\n")
    print()

    while (acknowledge != 'y' and acknowledge != 'n'):
        acknowledge = input("> Responda com [y/n]\n")

    if (acknowledge == 'y'):
        envia_string("tempa,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!")
        print("Executando...\n")


def od_led():
    print("Atualize o ciclo de trabalho da alimentação de cada LED:")
    od_led_inputs = le_inputs(16)
    tipo = tipo_de_comando()

    input_string = f"od_led{tipo},"
    for i in range(16):
        input_string += f"{od_led_inputs[channel2ss[i]]},"
    input_string += "_!"

    envia_string(input_string)
    echo_recebido = le_string()

    print("Esse é o comando enviado:")
    print(f"Enviado: {input_string}\nEchoado: {echo_recebido}\n")

    acknowledge = input("> Gostaria de executar o comando? [y/n]\n")
    print()

    while (acknowledge != 'y' and acknowledge != 'n'):
        acknowledge = input("> Responda com [y/n]\n")

    if (acknowledge == 'y'):
        envia_string("od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!")
        print("Executando...\n")


def od_135():
    od_135_inputs = input("Atualize quantas leituras devem contribuir na média de uma medida de OD:\n> ")
    print()

    enviar = input("> Gostaria de enviar isso? [y/n]\n")
    print()

    while(enviar != 'y'):
        if (enviar != 'n'):
            enviar = input("> Responda com [y/n]\n")
            print()

        else:
            novamente = input("> Gostaria de tentar novamente? [y/n]\n")
            print()

            while (novamente != 'y' and novamente != 'n'):
                novamente = input("> Responda com [y/n]\n")

            if (novamente == 'y'):
                od_135_inputs = input("Tente novamente: ")
                enviar = input("> Gostaria de enviar isso? [y/n]\n")
                print()

            else:
                return

    tipo = tipo_de_comando()
    input_string = f"od_135{tipo},{od_135_inputs},_!"
    envia_string(input_string)

    broadcast_recebido = le_string()
    print(f"Esse é o estado atual do sistema:\n{broadcast_recebido}\n")

    acknowledge = input("> Gostaria de executar o comando? [y/n]\n")
    print()

    while (acknowledge != 'y' and acknowledge != 'n'):
        acknowledge = input("> Responda com [y/n]\n")

    if (acknowledge == 'y'):
        envia_string(f"od_135a,{od_135_inputs},_!")
        print("Executando...")



def pump(ss2pump):
    print("Insira o regime de fluxo desejado para cada Smart Sleeve:\n(Lembre-se que para não alterar algum regime não deve-se inserir nada como input)\n")
    pump_inputs = le_inputs(16)
    tipo = tipo_de_comando()

    pump_string = []
    for i in range(48):
        pump_string += ["--,"]

    for i in range(16):
        pump_string[ss2pump[i]] = f"{pump_inputs[i+1]},"

    input_string = f"pump{tipo},"
    input_string += "".join(pump_string)
    input_string += "_!"

    envia_string(input_string)
    echo_recebido = le_string()

    print("Esse é o comando enviado:")
    print(f"Enviado: {input_string}\nEchoado: {echo_recebido}\n")

    acknowledge = input("> Gostaria de executá-lo? [y/n]\n")
    print()

    while (acknowledge != 'y' and acknowledge != 'n'):
        acknowledge = input("> Responda com [y/n]\n")

    if (acknowledge == 'y'):
        envia_string("pumpa,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,_!")
        print("Executando...\n")




def atualizar_parametro():
    parametro = input("Qual parâmetro gostaria de alterar?\n1 - Agitação\n2 - Temperatura\n3 - Turbidez\n4 - Fuxo de fluidos\n")
    print()

    while (parametro != '1' and parametro != '2' and parametro != '3' and parametro != '4'):
        parametro = input("Escolha dentre as opções possíveis:\n1 - Agitação\n2 - Temperatura\n3 - Turbidez\n4 - Fuxo de fluidos\n")
        print()

    if (parametro == '1'):
        stir()

    elif (parametro == '2'):
        temp()

    elif (parametro == '3'):
        escolha = input("Gostaria de alterar a alimentação do LED emissor? [y/n]\n")
        print()

        while (escolha != 'y' and escolha != 'n'):
            escolha = input("Responda com [y/n]\n")

        if (escolha == 'y'):
            od_led()

        escolha = input("Gostaria de alterar a média do PD detector? [y/n]\n")
        print()

        while (escolha != 'y' and escolha != 'n'):
            escolha = input("Responda com [y/n]\n")

        if (escolha == 'y'):
            od_135()

    elif (parametro == '4'):
        # A
        escolha = input("Gostaria de inserir o líquido A? [y/n]\n")
        print()

        while (escolha != 'y' and escolha != 'n'):
            escolha = input("Responda com [y/n]\n")

        if(escolha == 'y'):
            pump(pump_a)

        # B
        escolha = input("Gostaria de inserir o líquido B? [y/n]\n")
        print()

        while (escolha != 'y' and escolha != 'n'):
            escolha = input("Responda com [y/n]\n")

        if(escolha == 'y'):
            pump(pump_b)

        # C
        escolha = input("Gostaria de remover esgoto? [y/n]\n")
        print()

        while (escolha != 'y' and escolha != 'n'):
            escolha = input("Responda com [y/n]\n")

        if(escolha == 'y'):
            pump(pump_c)



print("\n****** Inicializando o eVOLVER! ******\n")

while True:
    atualizar = input("> Gostaria de atualizar algum parâmetro? [y/n]\n")
    print()

    while (atualizar != 'y' and atualizar != 'n'):
        atualizar = input("Responda com [y/n]\n")

    if (atualizar == 'n'):
        print("OK, a interação foi encerrada.")
        break

    elif (atualizar == 'y'):
        atualizar_parametro()


