status = {
    "stir": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    "temp": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095],
    "od_135": 1000,
    "od_led": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #[4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095],
    "pump": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47] #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}

channel2ss = [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1]
sair = ['x','X',' x',' X','x ','X ']

opcoes = ['TODAS']
for i in range(16):
    opcoes += [f'SS{i+1}']
opcoes += ['SAIR']

'''string = 'O status atual da agitação é de:\n'
for i in range(8):
    string += "[SS{}]: {}".format(i+1, status['stir'][channel2ss.index(i+1)])
    string += '\t'
    string += "[SS{}]: {}\n".format(i+9, status['stir'][channel2ss.index(i+9)])

print(string)'''