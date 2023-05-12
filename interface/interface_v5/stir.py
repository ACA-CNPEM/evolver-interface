from constants import *
from utils import *
from pick import pick


stir_inputs = [status['stir'][convert['ss2channel'][i]] for i in ss_ativas]
stir_inputs.insert(0, -1)


def define_opcoes():
    opcoes = ['[SS{}]: {}%'.format(i, stir_inputs[i]) for i in ss_ativas] + ['CANCELAR']
    opcoes.insert(0, 'Todas as Smart Sleeves')
    return opcoes


def gera_comando():
    comando = 'stiri,'
    
    for i in range(16):
        ss = convert['channel2ss'][i]

        if (ss in ss_ativas):
            comando += f'{stir_inputs[ss]},'
        else:
            comando += f'{status["stir"][i]},'

    return comando + '_!'


def stir():
    stir_opcoes = define_opcoes()
    selecionados = pick(stir_opcoes, titulo, indicator='>>', multiselect=True, min_selection_count=1)

    if (('CANCELAR', stir_opcoes.index('CANCELAR')) not in selecionados):
        if (('Todas as Smart Sleeves', 0) in selecionados):
            selecionados = ss_ativas

        else:
            selecionados = [ selecionados[i][1] for i in range(len(selecionados)) ]
            selecionados.sort()

        for i in selecionados:
            stir_inputs[i] = leitura_input(f'{stir_opcoes[i]} >>> ')

        string_comandos = gera_comando()

        canal.write(str.encode(string_comandos))
        string_recebida = canal.readline().decode('UTF-8')

        inicio = string_recebida.find(",")
        fim = string_recebida.rfind(",")
        string_recebida = string_recebida[inicio+1:fim].split(",")

        titulo_confirmacao = 'Gostaria de executar este comando?\n'
        titulo_confirmacao += '\n'.join(['[SS{}]: {}%'.format(i, string_recebida[convert["ss2channel"][i]]) for i in ss_ativas])

        _, confirmacao = pick(['Confirmar', 'Reinserir', 'CANCELAR'], titulo_confirmacao, indicator='>>')
        
        if (confirmacao == 0):
            canal.write(str.encode("stira,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!"))
            
            for i in ss_ativas:
                stir_inputs[i] = int(string_recebida[convert["ss2channel"][i]])
                status["stir"][convert["ss2channel"][i]] = stir_inputs[i]
        
        elif (confirmacao == 1):
            stir()
        
        else:
            return