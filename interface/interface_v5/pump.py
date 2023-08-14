from constants import *
from utils import leitura_pump_input
from pick import pick

pump_inputs = [[], [], []]
for i in liquidos_ativos:
    pump_inputs[i] = [status['pump'][convert['ss2pump'][i][j]] for j in ss_ativas]
    pump_inputs[i].insert(0, -1)


def define_opcoes():
    opcoes = []
    for i in ss_ativas:
        string_auxiliar = f'[SS{i}]\t'

        for j in liquidos_ativos:
            string_auxiliar += f'{liquidos[j]}: {pump_inputs[j][i]}\t'

        opcoes += [string_auxiliar]

    opcoes += ["CANCELAR"]
    opcoes.insert(0, 'Todas as Smart Sleeves')
    return opcoes


def gera_comando():
    comando = 'pumpi,'

    if (2 in liquidos_ativos):
        for i in range(16):
            ss = convert['pump2ss'][i]

            if (ss in ss_ativas):
                comando += f'{pump_inputs[2][ss]},'
            else:
                 comando += '--,'
    else:
        comando += '--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,'

    if (1 in liquidos_ativos):
        for i in range(16):
            ss = convert['pump2ss'][i]

            if (ss in ss_ativas):
                comando += f'{pump_inputs[1][ss]},'
            else:
                 comando += '--,'
    else:
        comando += '--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,'
    
    if (0 in liquidos_ativos):
        for i in range(16):
            ss = convert['pump2ss'][i]

            if (ss in ss_ativas):
                comando += f'{pump_inputs[0][ss]},'
            else:
                 comando += '--,'
    else:
        comando += '--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,'

    return comando + '_!'


def pump():
    pump_opcoes = define_opcoes()
    selecionados = pick(pump_opcoes, titulo, indicator='>>', multiselect=True, min_selection_count=1)

    if (('CANCELAR', pump_opcoes.index('CANCELAR')) not in selecionados):
        if (('Todas as Smart Sleeves', 0) in selecionados):
            selecionados = ss_ativas

        else:
            selecionados = [ selecionados[i][1] for i in range(len(selecionados)) ]
            selecionados.sort()

        for i in selecionados:
            print(f'[SS{i}]')
            for j in liquidos_ativos:
                pump_inputs[j][i] = leitura_pump_input(f'    {liquidos[j]}: {pump_inputs[j][i]} >>> ')

        string_comandos = gera_comando()

        canal.write(str.encode(string_comandos))
        string_recebida = canal.readline().decode('UTF-8')

        inicio = string_recebida.find(",")
        fim = string_recebida.rfind(",")
        string_recebida = string_recebida[inicio+1:fim].split(",")
        
        titulo_confirmacao = 'Gostaria de executar este comando?\n'
        for i in ss_ativas:
            titulo_confirmacao += f'\n[SS{i}]\t'
            for j in liquidos_ativos:
                titulo_confirmacao += f'{liquidos[j]}: {string_recebida[convert["ss2pump"][j][i]]}\t'

        _, confirmacao = pick(['Confirmar', 'Reinserir', 'CANCELAR'], titulo_confirmacao, indicator='>>')
        
        if (confirmacao == 0):
            canal.write(str.encode("pumpa,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,_!"))
            
            for i in ss_ativas:
                for j in liquidos_ativos:
                    pump_inputs[j][i] = string_recebida[convert["ss2pump"][j][i]]
                    status["pump"][convert["ss2pump"][j][i]] = pump_inputs[j][i]
        
        elif (confirmacao == 1):
            pump()
        
        else:
            return

