import serial
import time
from pick import pick

############################ VARIAVEIS
status = {
    "stir": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    "temp": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095],
    "od_135": 1000,
    "od_led": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095],
    "pump": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47] #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}

channel2ss = [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1]
sair = ['x','X',' x',' X','x ','X ']

opcoes = ['TODAS']
for i in range(16):
    opcoes += [f'SS{i+1}']
opcoes += ['SAIR']

comm = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

'''string = 'O status atual da agitação é de:\n'
for i in range(8):
    string += "[SS{}]: {}".format(i+1, status['stir'][channel2ss.index(i+1)])
    string += '\t'
    string += "[SS{}]: {}\n".format(i+9, status['stir'][channel2ss.index(i+9)])

print(string)'''

def envia_string(message):
    comm.write(str.encode(message))
    time.sleep(1)

def recebe_string():
    message = comm.readline().decode()

    while (comm.inWaiting() != 0):
        message += comm.read().decode()

    return message

def selecao_de_ss(string):
    titulo = f'{string}\nSelecione as Smart Sleeves que deseja alterar:\n(use ESPAÇO para selecionar e ENTER para continuar)'
    selecionadas = pick(opcoes, titulo, multiselect=True, indicator='>>', min_selection_count=1)
    return selecionadas

def confirma_input(string):
    titulo = f'{string}\nConfirme a execução do comando:'
    confirmacao = pick(['Confirmo', 'Não confirmo'], titulo, indicator='>>', min_selection_count=1)
    return confirmacao

def print_comando(string,channel,unit):
    for i in range(8):
        print("[SS{}]: {}".format(i+1, string[channel.index(i+1)]) + 
              f"{unit}          " + 
              "[SS{}]: {}".format(i+9, string[channel.index(i+9)]) +
              f"{unit}")
    print()


def stir():
    stir_commands = status["stir"]
    stir_inputs = [round(stir_commands[i]*100/97, 0) for i in range(16)]

    string_status = 'O status atual da agitação é de:\n'
    for i in range(8):
        string_status += "[SS{}]: {}%\t".format(i+1, stir_inputs[channel2ss.index(i+1)])
        string_status += "[SS{}]: {}%\n".format(i+9, stir_inputs[channel2ss.index(i+9)])
    selecionadas = selecao_de_ss(string_status) 

    if (selecionadas == []):
        return
    
    elif (('SAIR', 17) not in selecionadas):
        if (('TODAS', 0) in selecionadas):
            print(string_status)

            for i in range(16):
                stir_inputs[channel2ss.index(i+1)] = input(f"> [SS{i+1}]: ")
            print()

        else:
            print(string_status)
            selecionadas = [selecionadas[i][1] for i in range(len(selecionadas))]

            for i in selecionadas:
                stir_inputs[channel2ss.index(i)] = round(float(input(f"> [SS{i}]: ")), 0)
            print()
        
        input_string = "stiri,"
        for i in range(16):
            stir_commands[i] = int(round(float(stir_inputs[i])*97/100, 0)) if stir_inputs[i] != '' else 0
            input_string += f"{stir_commands[i]},"
            
        input_string += '_!'
        envia_string(input_string)
        resposta = recebe_string()

        if (resposta != ""):
            inicio = resposta.find(",")
            fim = resposta.rfind(",")

            resposta = resposta[inicio+1:fim].split(",")
            stir_commands = [int(resposta[i]) for i in range(16)]
            stir_inputs = [round(stir_commands[i]*100/97, 0) for i in range(16)]

            string_status = 'O comando recebido é de:\n'
            for i in range(8):
                string_status += "[SS{}]: {}%\t".format(i+1, stir_inputs[channel2ss.index(i+1)])
                string_status += "[SS{}]: {}%\n".format(i+9, stir_inputs[channel2ss.index(i+9)])
                
            confirmacao = confirma_input(string_status)
            print_comando(stir_inputs, channel2ss, "%")

            if (confirmacao[1] == 0):
                envia_string("stira,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!")
                status['stir'] = [int(resposta[i]) for i in range(16)]
            




def temp():
    selecionadas = selecao_de_ss()


def od():
    titulo = 'O que gostaria de alterar:\n(use ESPAÇO para selecionar e ENTER para continuar)'
    opcoes = ['Alimentação do LED', 'Média de leituras do PD', 'Ambos']
    opcao_turb, indice_turb = pick(opcoes, titulo, indicator='>>')
    

def pump():
    titulo = 'O que gostaria de alterar:\n(use ESPAÇO para selecionar e ENTER para continuar)'
    opcoes = ['Inserir líquido A', 'Inserir líquido B', 'Remover esgoto']
    selecionados_fluid= pick(opcoes, titulo, multiselect=True, min_selection_count=1, indicator='>>')


def atualizar_parametro(indice):
    if (indice == 0):
        stir()

    elif (indice == 1):
        temp()

    elif (indice == 2):
        od()

    elif (indice == 3):
        pump()

    else:
        print('FIM')

'''title = 'Please choose your favorite programming language (press SPACE to mark, ENTER to continue): '
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
selected = pick(options, title, multiselect=True, min_selection_count=1)
print(selected)'''


print("\n ****** Inicializando a interface! ******\n")

while True:
    parametros = ['Agitação', 'Temperatura', 'Turbidez', 'Fluxo de fluidos', 'SAIR']
    parametro, indice = pick(parametros, 'Selecione o parâmetro que deseja alterar: ', indicator='>>')

    if (indice == 4):
        break
    else:
        atualizar_parametro(indice)

print("\n ****** Encerrando a iteração. Volte logo! ******\n")