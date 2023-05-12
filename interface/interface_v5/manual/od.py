from interface_v5.constants import *

od_inputs = [status['od_led'].index(i) for i in ss_ativas]
od_inputs += [status['od_135']]

od_opcoes = ['[SS{}]: {}%'.format(ss_ativas[i], od_inputs[i]) for i in range(len(ss_ativas))]
od_opcoes += ['Número de leituras compondo a medida de turbidez: {}'.format(od_inputs[len(ss_ativas)])]

string = 'STATUS ATUAL: TURBIDEZ\n'

for i in range(len(ss_ativas) + 1):
    string += f'{od_opcoes[i]}\n'




def od():
    print(ss_ativas)
    print(string)