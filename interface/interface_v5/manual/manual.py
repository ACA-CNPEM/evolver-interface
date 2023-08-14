import time

from stir import stir
from temp import temp
from pump import pump
from od import od

from constants import *
from pick import pick

print("Smart Sleeves ativas: ", ss_ativas)

parametros = ['Agitação', 'Temperatura', 'Turbidez', 'Fluxo de fluidos', 'SAIR']

while True:
    time.sleep(1)
    parametro_selecionado = pick(parametros, 'Selecione o parâmetro com o qual deseja trabalhar: ', indicator='>>')

    if (parametro_selecionado[1] == 0):
        print("\n* Agitação")
        stir()

    elif (parametro_selecionado[1] == 1):
        print("\n* Temperatura")
        temp()

    elif (parametro_selecionado[1] == 2):
        print("\n* Turbidez")
        od()

    elif (parametro_selecionado[1] == 3):
        print("\n* Fluxo de fluidos")
        pump()
    
    else:
        break