from pick import pick
from interface_v4.constants import *

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