from constantes import *
from pick import pick


# CONSTANTES
qtd_ativa = len(status["ativas"])
ss_ativas = status["ativas"]
canais_ativos = [ status["ss2channel"][i] for i in ss_ativas]
comandos = [ status["stir"][i] for i in canais_ativos ]
'''print(qtd_ativa)
print(ss_ativas)
print(canais_ativos)
print(comandos)'''


# MENU DE AÇÕES
titulo = f'STATUS ATUAL:\n'
for i in range(qtd_ativa):
    titulo += f'[SS{ss_ativas[i]}]: {comandos[i]}%\n'
print(titulo)
titulo += '\nSelecione o comando desejado:\n(use ESPAÇO para selecionar e ENTER para continuar)'

opcoes = [f'R0: Alterar a agitação de todas as {qtd_ativa} Smart Sleeves']
for i in ss_ativas:
    opcoes += [f'R{i}: Alterar a agitação da Smart Sleeve {i}']
opcoes += ['CANCELAR']

comandos_selecionados = pick(opcoes, titulo, indicator='>>', multiselect=True, min_selection_count=1)


# AGINDO COM BASE NA ESCOLHA
if (('CANCELAR', qtd_ativa + 1) not in comandos_selecionados):

    if ((opcoes[0], 0) in comandos_selecionados):
        print("ler_todas")
        for i in ss_ativas:
            input_bruto = input(f"> [SS{i}]: ")
        print()

    else:
        print("ler apenas selecionadas")
        ss_selecionadas = [ i[1] for i in comandos_selecionados ]
        ss_selecionadas.sort()
        
        for i in ss_selecionadas:
            input_bruto = input(f"> [SS{i}]: ")
        print()




'''string = []
for i in range(17):
    string += [f"R{i}"]
print(string)'''