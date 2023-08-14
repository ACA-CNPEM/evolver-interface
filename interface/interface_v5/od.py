from constants import *
from utils import leitura_input
from pick import pick


od_inputs = [ status['od_led'][convert['ss2channel'][i]] for i in ss_ativas ]
od_inputs += [ status['od_135'] ]
od_inputs.insert(0, -1)


def define_opcoes():
    opcoes = [ '[SS{}]: {}%'.format(i, od_inputs[i]) for i in ss_ativas ]
    opcoes += [ 'Número de leituras compondo a medida de turbidez: {}'.format(od_inputs[len(ss_ativas) + 1]) ]
    opcoes += ['CANCELAR']
    opcoes.insert(0, 'Todas as Smart Sleeves')
    return opcoes


def gera_comando_led():
    comando = 'od_ledi,'
    
    for i in range(16):
        ss = convert['channel2ss'][i]

        if (ss in ss_ativas):
            comando += f'{od_inputs[ss]},'
        else:
            comando += f'{status["od_led"][i]},'

    return comando + '_!'


def gera_comando_pd():
    return f'od_135i,{od_inputs[len(ss_ativas) + 1]},_!'


def od():
    od_opcoes = define_opcoes()
    selecionados = pick(od_opcoes, titulo, indicator='>>', multiselect=True, min_selection_count=1)

    if (('CANCELAR', od_opcoes.index('CANCELAR')) not in selecionados):

        if ((od_opcoes[len(ss_ativas) + 1], len(ss_ativas) + 1) in selecionados):
            od_inputs[len(ss_ativas) + 1] = leitura_input(f'{od_opcoes[len(ss_ativas) + 1]} >>> ')
            selecionados.remove((od_opcoes[len(ss_ativas) + 1], len(ss_ativas) + 1))

        if (('Todas as Smart Sleeves', 0) in selecionados):
            selecionados = ss_ativas

        else:
            selecionados = [ selecionados[i][1] for i in range(len(selecionados)) ]
            selecionados.sort()

        for i in selecionados:
            od_inputs[i] = leitura_input(f'{od_opcoes[i]} >>> ')

        string_comandos = gera_comando_led() 
        canal.write(str.encode(string_comandos))
        string_recebida_led = canal.readline().decode('UTF-8')

        string_comandos = gera_comando_pd()
        canal.write(str.encode(string_comandos))
        string_recebida_pd = canal.readline().decode('UTF-8')

        inicio = string_recebida_led.find(",")
        fim = string_recebida_led.rfind(",")
        string_recebida_led = string_recebida_led[inicio+1:fim].split(",")

        titulo_confirmacao = 'Gostaria de executar este comando?\n'
        titulo_confirmacao += '\n'.join(['[SS{}]: {}%'.format(i, string_recebida_led[convert["ss2channel"][i]]) for i in ss_ativas])

        _, confirmacao = pick(['Confirmar', 'Reinserir', 'CANCELAR'], titulo_confirmacao, indicator='>>')
        
        if (confirmacao == 0):
            canal.write(str.encode("od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!"))
            canal.write(str.encode(f"od_135a,{od_inputs[len(ss_ativas) + 1]},_!"))
            
            for i in ss_ativas:
                od_inputs[i] = int(string_recebida_led[convert["ss2channel"][i]])
                status["od_led"][convert["ss2channel"][i]] = od_inputs[i]

            status["od_135"] = od_inputs[len(ss_ativas) + 1]
        
        elif (confirmacao == 1):
            od()
        
        else:
            return

