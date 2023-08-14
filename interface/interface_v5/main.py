from constants import *
from manual import interface_manual
from communication import leitura
import time
from pick import pick
import multiprocessing as mp


print("\n ****** Inicializando a interface! ******\n")
lendo = mp.Process(target=leitura, args=[evolver_canal, evolver_delay])
lendo.start()
lendo.join()

titulo = "Escolha o modo de operação"
opcoes = ['1. Script', '2. Gerador de Script', '3. Manual', 'SAIR']

if __name__ == '__main__':
    try:
        selecionado = pick(opcoes, titulo, indicator='>>')

        if(selecionado[1] == 0):
                print(selecionado)

        elif(selecionado[1] == 1):
                print(selecionado)

        elif(selecionado[1] == 2):
                interface = mp.Process(target=interface_manual)
                interface.start()
                interface.join()
            
        print("\n ****** Encerrando a iteração. Volte logo! ******\n")

    except KeyboardInterrupt:
        print("\nInterface interrompida manualmente através de KeyboardInterrupt.\n")