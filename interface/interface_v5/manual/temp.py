from interface_v5.constants import *

temp_inputs = [status['temp'].index(i) for i in ss_ativas]
temp_opcoes = ['[SS{}]: {}°C'.format(ss_ativas[i], temp_inputs[i]) for i in range(len(ss_ativas))]

string = 'STATUS ATUAL: TEMPERATURA\n'
for i in temp_opcoes:
    string += f'{i}\n'

def temp():
    print(ss_ativas)
    print(string)