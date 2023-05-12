from constants import *
from utils import leitura_input
from pick import pick


temp_inputs = [status['temp'][convert['ss2channel'][i]] for i in ss_ativas]
temp_inputs.insert(0, -1)


def converte_celsius(valor):
    celsius = valor
    return celsius


def define_opcoes():
    opcoes = ['[SS{}]: {}°C'.format(i, converte_celsius(temp_inputs[i])) for i in ss_ativas] + ['CANCELAR']
    opcoes.insert(0, 'Todas as Smart Sleeves')
    return opcoes


def gera_comando():
    comando = 'tempi,'
    
    for i in range(16):
        ss = convert['channel2ss'][i]

        if (ss in ss_ativas):
            comando += f'{temp_inputs[ss]},'
        else:
            comando += f'{status["temp"][i]},'

    return comando + '_!'


def temp():
    temp_opcoes = define_opcoes()
    selecionados = pick(temp_opcoes, titulo, indicator='>>', multiselect=True, min_selection_count=1)

    if (('CANCELAR', temp_opcoes.index('CANCELAR')) not in selecionados):
        if (('Todas as Smart Sleeves', 0) in selecionados):
            selecionados = ss_ativas

        else:
            selecionados = [ selecionados[i][1] for i in range(len(selecionados)) ]
            selecionados.sort()

        for i in selecionados:
            temp_inputs[i] = leitura_input(f'{temp_opcoes[i]} >>> ')

    string_comandos = gera_comando()

    canal.write(str.encode(string_comandos))
    string_recebida = canal.readline().decode('UTF-8')

    inicio = string_recebida.find(",")
    fim = string_recebida.rfind(",")
    string_recebida = string_recebida[inicio+1:fim].split(",")

    broadcast = string_recebida[17:]
    string_recebida = string_recebida[0:16]

    titulo_confirmacao = 'Gostaria de executar este comando?\n'
    titulo_confirmacao += '\n'.join(['[SS{}]: {}°C'.format(i, converte_celsius(string_recebida[convert["ss2channel"][i]])) for i in ss_ativas])
    
    _, confirmacao = pick(['Confirmar', 'Reinserir', 'CANCELAR'], titulo_confirmacao, indicator='>>')

    if (confirmacao == 0):
            canal.write(str.encode("tempa,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!"))
            
            for i in ss_ativas:
                temp_inputs[i] = int(string_recebida[convert["ss2channel"][i]])
                status["temp"][convert["ss2channel"][i]] = temp_inputs[i]
                    
    elif (confirmacao == 1):
        temp()
        
    else:
        return