from interface_v4.utils import *
from interface_v4.constants import *
from pick import pick
from interface_v4.communication import *


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
        print(f"{input_string}\n{resposta}")

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