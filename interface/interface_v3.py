import serial
import time

status = {
    "stir": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    "temp": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095],
    "od_135": 1000,
    "od_led": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095],
    "pump": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47] #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}

op_1 = ['1',' 1','1 ']
op_2 = ['2',' 2','2 ']
op_3 = ['3',' 3','3 ']
op_4 = ['4',' 4','4 ']

op_a = ['a','A',' a',' A','a ','A ']
op_b = ['b','B',' b',' B','b ','B ']
op_c = ['c','C',' c',' C','c ','C ']


yes = ['y','Y',' y',' Y','y ','Y ']
no = ['n','N',' n',' N','n ','N ']
todos = ['t','T',' t',' T','t ','T ']
exit = ['x','X',' x',' X','x ','X ']

instant = ['i','I',' i',' I','i ','I ']
recurrent = ['r','R',' r',' R','r ','R ']

ss = ['1',' 1','1 ','2',' 2','2 ','3',' 3','3 ','4',' 4','4 ','5',' 5','5 ','6',' 6','6 ','7',' 7','7 ','8',' 8','8 ','9',' 9','9 ',
      '10',' 10','10 ','11',' 11','11 ','12',' 12','12 ','12',' 12','12 ','13',' 13','13 ','14',' 14','14 ','15',' 15','15 ','16',' 16','16 ']

comm = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

channel2ss = [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1]
channel2pump = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] #[8,7,6,5,4,3,2,1,16,15,14,13,12,11,10,9]

pump_a = [39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40]
pump_b = [23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24]
pump_c = [7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]


def print_comando(string,channel,unit):
    for i in range(8):
        print("[SS{}]: {}".format(i+1, string[channel.index(i+1)]) + 
              f" {unit}          " + 
              "[SS{}]: {}".format(i+9, string[channel.index(i+9)]) +
              f" {unit}")
    print()


def print_resposta(string):
    inicio = string.find(",")
    fim = string.rfind(",")

    return string[inicio+1:fim].split(",")


def envia_string(message):
    comm.write(str.encode(message))
    time.sleep(1)


def le_string():
    message = comm.readline().decode()

    while (comm.inWaiting() != 0):
        message += comm.read().decode()
    
    return message


'''def todos_inputs():
    inputs = []

    for i in range(16):
        raw_input = input(f"> [SS{i+1}]: ")

        if (raw_input in exit):
            while (i < 16):
                inputs += 0
                i += 1
            break
        else:
            inputs += raw_input

    print()
    return inputs


def le_inputs():
    inputs = ss_inputs()
    if (len(ss_inputs) != 16):
        inputs = [0 for i in range(16)]

    print("Você digitou: ", inputs)
    
    enviar = input("> Era isso que gostaria de ter digitado? [y/n]\n> ")
    print()

    while (enviar not in yes):
        if (enviar not in no):
            enviar = input("> Responda com [y/n]\n> ")
            print()

        else:
            novamente = input("> Gostaria de tentar novamente? [y/n]\n> ")
            print()

            while (novamente not in yes and novamente not in 'n'):
                novamente = input("> Responda com [y/n]\n> ")

            if (novamente in 'y'):
                print("Tente novamente:")
                inputs = ss_inputs()

                print("Você digitou: ", inputs)
                enviar = input("> Era isso que gostaria de ter digitado? [y/n]\n> ")
                print()
            
            else:
                return -1

    return inputs'''


def le_comandos(inputs, channel):
    print(inputs)
    comando = input("> Digite o número da Smart Sleeve que você deseja comandar, 'T' se for comandar todas, e 'X' para finalizar a inserção de comandos.\n> ")
    print()

    while (comando not in exit):
        if (comando in todos):
            leitura = []

            for i in range(16):
                raw_input = input(f"> [SS{i+1}]: ")

                if (raw_input in exit):
                    break
                else:
                    leitura += [raw_input]
            print()

            for i in range(len(leitura)):
                inputs[channel.index(i+1)] = leitura[i] 
            break

        elif (comando in ss):
            inputs[channel.index(int(comando))] = input("> [SS" + comando + "]: ")
            print()

            comando = input("Próximo:\n> Digite o número da Smart Sleeve que você deseja comandar, 'T' se for comandar todas, e 'X' para finalizar a inserção de comandos.\n> ")
            print()
        
        else: 
            print("Comando inválido, reveja.")
            comando = input("> Digite o número da Smart Sleeve que você deseja comandar, 'T' se for comandar todas, e 'X' para finalizar a inserção de comandos.\n> ")
            print()
    
    return inputs


def tipo_de_comando():
    tipo = input("Que tipo de comando gostaria de enviar, instantâneo ou recorrente?\n> Digite i para instantâneo e r para recorrente.\n> ")
    print()

    while (tipo not in instant and tipo not in recurrent):
        tipo = input("> Escolha entre i ou r\n> ")
        print()

    return tipo.lower()





#### CONTROLE DE AGITAÇÃO
def stir():
    stir_inputs = [round(float(status["stir"][i])*100/97, 2) for i in range(16)]

    print("O status atual da agitação é de:")
    print_comando(stir_inputs, channel2ss, '%')

    print("Atualize a agitação desejada: ")
    stir_inputs = le_comandos(status["stir"],channel2ss)
    print(stir_inputs)

    stir_command = []
    for input in stir_inputs:
        stir_command += [int(input)*97/100 if input != "" else 0]
    
    print(stir_command)
    # tipo = tipo_de_comando()
    tipo = 'i'

    input_string = f"stir{tipo},"
    for i in range(16):
        input_string += f"{stir_inputs[i]},"
    input_string += "_!"

    print(f"Enviando o comando. Esse é o comando enviado: '{input_string}'")
    envia_string(input_string)

    echo_recebido = le_string()
    if (echo_recebido != ""):
        print(f"Esse é o comando recebido e echoado pelo sistema: '{echo_recebido}'\nIsso se traduz em (%): ")
        inicio = echo_recebido.find(",")
        fim = echo_recebido.rfind(",")
        echo_recebido = echo_recebido[inicio+1:fim].split(",")
        string = [round(float(echo_recebido[i])*100/90,2) for i in range(16)]
        print_comando(string,channel2ss,'%')

        #echo_recebido = print_resposta(echo_recebido,channel2ss)

        acknowledge = input("> Gostaria de executá-lo? [y/n]\n> ")
        print()

        while (acknowledge not in yes and acknowledge not in no):
            acknowledge = input("> Responda com [y/n]\n> ")
            print()

        if (acknowledge in yes):
            envia_string("stira,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!")
            print("Executando...\n")
            status["stir"] = echo_recebido

    else:
        print("\n[!!!]\nNada foi echoado, houve algum problema. Tente novamente!\n[!!!]\n")


#### CONTROLE DE TEMPERATURA
def temp():
    print("O setpoint de temperatura atualmente é:")
    print_comando(status["temp"],channel2ss)

    print("Atualize o setpoint de temperatura de cada Smart Sleeve.")
    temp_inputs = le_comandos(status['temp'],channel2ss)
    tipo = tipo_de_comando()

    input_string = f"temp{tipo},"
    for i in range(16):
        input_string += f"{temp_inputs[i]},"
    input_string += "_!"

    print(f"Enviando o comando. Esse é o comando enviado: '{input_string}'")
    envia_string(input_string)

    texto_recebido = le_string()
    if (texto_recebido != ""):
    
        for i in range(len(texto_recebido)):
            if (texto_recebido[i] == 'e'):
                if (i+1 < len(texto_recebido) and texto_recebido[i+1] == 'n'):
                    if(i+2 < len(texto_recebido) and texto_recebido[i+2] == 'd'):
                        echo = texto_recebido[0:i+3]
                        broadcast = texto_recebido[i+3:]
                        break
                    
        print(f"Esse é o comando recebido e echoado pelo sistema: '{echo}'\nIsso se traduz em (%): ")
        #echo = print_resposta(echo,channel2ss)
        inicio = echo.find(",")
        fim = echo.rfind(",")
        echo = echo[inicio+1:fim].split(",")
        string = [round(float(echo[i])*100/4095,2) for i in range(16)]
        print_comando(string,channel2ss)

        print(f"O estado atual do sistema é: '{broadcast}'\nIsso se traduz em (°C): ")
        # broadcast = print_resposta(broadcast,channel2ss)
        inicio = broadcast.find(",")
        fim = broadcast.rfind(",")
        broadcast = broadcast[inicio+1:fim].split(",")
        string = [round(float(broadcast[i])*22/2048,1) for i in range(16)]
        print_comando(string,channel2ss)

        acknowledge = input("> Gostaria de executar o comando? [y/n]\n> ")
        print()

        while (acknowledge not in yes and acknowledge not in no):
            acknowledge = input("> Responda com [y/n]\n> ")
            print()

        if (acknowledge in yes):
            envia_string("tempa,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!")
            print("Executando...\n")
            status["temp"] = echo

    else:
        print("\n[!!!]\nNada foi echoado, houve algum problema. Tente novamente!\n[!!!]\n")


#### MEDIÇÃO DE TURBIDEZ - LED
def od_led():
    print("Os LEDs estão sendo alimentados com ciclo de trabalho:")
    print_comando(status["od_led"],channel2ss)

    print("Atualize o ciclo de trabalho da alimentação de cada LED.")
    od_led_inputs = le_comandos(status["od_led"],channel2ss)
    tipo = tipo_de_comando()

    input_string = f"od_led{tipo},"
    for i in range(16):
        input_string += f"{od_led_inputs[i]},"
    input_string += "_!"

    print(f"Enviando o comando. Esse é o comando enviado: '{input_string}'")
    envia_string(input_string)

    echo_recebido = le_string()
    if (echo_recebido != ""):
        print(f"Esse é o comando recebido e echoado pelo sistema: '{echo_recebido}'\nIsso se traduz em: ")
        echo_recebido = print_resposta(echo_recebido,channel2ss)

        acknowledge = input("> Gostaria de executá-lo? [y/n]\n> ")
        print()

        while (acknowledge not in yes and acknowledge not in no):
            acknowledge = input("> Responda com [y/n]\n> ")
            print()

        if (acknowledge in yes):
            envia_string("od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!")
            print("Executando...\n")
            status["od_led"] = echo_recebido

    else:
        print("\n[!!!]\nNada foi echoado, houve algum problema. Tente novamente!\n[!!!]\n")


#### MEDIÇÃO DE TURBIDEZ - PD 
def od_135():
    print(f"A medida de OD é uma média de {status['od_135']} leituras atualmente.")
    od_135_inputs = input("Atualize quantas leituras devem contribuir na média de uma medida de OD:\n> ")
    print()

    enviar = input("> Gostaria de enviar isso? [y/n]\n> ")
    print()

    while(enviar not in yes):
        if (enviar not in no):
            enviar = input("> Responda com [y/n]\n> ")
            print()

        else:
            novamente = input("> Gostaria de tentar novamente? [y/n]\n> ")
            print()

            while (novamente not in yes and novamente not in no):
                novamente = input("> Responda com [y/n]\n> ")
                print()
            
            if (novamente in yes):
                od_135_inputs = input("Tente novamente: ")
                enviar = input("> Gostaria de enviar isso? [y/n]\n> ")
                print()

            else: 
                return
    
    tipo = tipo_de_comando()
    input_string = f"od_135{tipo},{od_135_inputs},_!"
    envia_string(input_string)

    broadcast_recebido = le_string()
    if (broadcast_recebido != ""):
        print(f"O estado atual do sistema é: '{broadcast_recebido}'\nIsso se traduz em: ")
        broadcast_recebido = print_resposta(broadcast_recebido,channel2ss)

        acknowledge = input(f"A média nova média enviada é de {od_135_inputs}.\n> Gostaria de executar o comando? [y/n]\n> ")
        print()

        while (acknowledge not in yes and acknowledge not in no):
            acknowledge = input("> Responda com [y/n]\n> ")

        if (acknowledge in yes):
            envia_string(f"od_135a,{od_135_inputs},_!")
            print("Executando...\n")
            status["od_135"] = od_135_inputs

    else:
        print("\n[!!!]\nNada foi echoado, houve algum problema. Tente novamente!\n[!!!]\n")


#### CONTROLE DO FLUXO DE FLUIDOS
def pump(ss2pump, liquido):
    print(f"Atualmente as Smart Sleeves estão com regime de atuação do líquido {liquido} igual a:")
    print_comando([status['pump'][i] for i in ss2pump],channel2pump)

    print(f"Insira o regime de fluxo de {liquido} desejado para cada Smart Sleeve:")
    pump_inputs = le_comandos(['--' for i in range(16)],channel2pump)
    tipo = tipo_de_comando()

    input_string = f"pump{tipo},"
    for i in range(48):
        if (i >= min(ss2pump) and i <= max(ss2pump)):
            input_string += f"{pump_inputs[ss2pump.index(i)]},"

        else:
            input_string += '--,'
    input_string += "_!"

    print(f"Enviando o comando. Esse é o comando enviado: '{input_string}'")
    envia_string(input_string)

    echo_recebido = le_string()
    if (echo_recebido != ""):
        print(f"Esse é o comando recebido e echoado pelo sistema: '{echo_recebido}'\nIsso se traduz em (segundos): ")
        inicio = echo_recebido.find(",")
        fim = echo_recebido.rfind(",")

        echo_recebido = [echo_recebido[inicio+1:fim].split(",")[ss2pump[i]] for i in range(16)]
        print_comando(echo_recebido,channel2pump)

        acknowledge = input("> Gostaria de executá-lo? [y/n]\n> ")
        print()

        while (acknowledge not in yes and acknowledge not in no):
            acknowledge = input("> Responda com [y/n]\n> ")
            print()

        if (acknowledge in yes):
            envia_string("pumpa,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,_!")
            print("Executando...\n")

            for i in range(16):
                if (echo_recebido[i] != '--'):
                    status["pump"][ss2pump[i]] = echo_recebido[i]            

    else:
        print("\n[!!!]\nNada foi echoado, houve algum problema. Tente novamente!\n[!!!]\n")





################################ ALTERAÇÃO DE PARÂMETROS ################################
def atualizar_parametro():
    parametro = input("Qual parâmetro gostaria de alterar?\n\t1 - Agitação\n\t2 - Temperatura\n\t3 - Turbidez\n\t4 - Fluxo de fluidos\n(Digite 'X' pra sair)\n> ")
    print()

    if (parametro in op_1):
        stir()
    
    elif (parametro in exit):
        return False

    return True
        
'''
    elif (parametro in op_2):
        temp()

    elif (parametro in op_3):
        escolha = input("Gostaria de alterar a\n a. alimentação do LED emissor\nou \n b. média do PD detector?\n> ")
        print()

        while (escolha not in op_a and escolha not in op_b):
            escolha = input("> Responda com 'a' ou 'b'.\n> ")
            print()

        if (escolha in op_a):
            od_led()
        else:
            od_135()

    elif (parametro in op_4):
        escolha = input("Gostaria de\n a. inserir o líquido A,\n b. inserir o líquido B,\nou\n c. remover esgoto?\n> ")
        print()

        while (escolha not in op_a and escolha not in op_b and escolha not in op_c):
            escolha = input("> Responda com 'a', 'b', ou 'c'.\n> ")
            print()

        if (escolha in op_a):
            pump(pump_a,'A')

        elif (escolha in op_b):
            pump(pump_b,'B')

        else:
            pump(pump_c,'C')''' 

######################################### MAIN #########################################
print("\n ****** Inicializando a interface! ******\n")
interagindo = True

while interagindo:
    interagindo = atualizar_parametro()

print("\n ****** Encerrando a interface. Volte logo! ******\n")