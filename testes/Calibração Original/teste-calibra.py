import json
import matplotlib.pyplot as plt

file = open('calibration_fynch.json')
data = json.load(file)

ss_raw_data = data['vialData']['od135']
od = data['inputData']

ss = [i for i in range(16)]

ss_data = {
    'od': od
}

for i in ss:
    ss_data[f'SS{i+1}'] = []

for line in ss_raw_data:
    for i in ss:
        ss_data[f'SS{i+1}'] += [sum(line[i])/3]
'''

for i in ss:
    ss_data[f'SS{i+1}'] = [sum(raw)/3 for raw in ss_raw_data[i]]'''

for i in ss:
    plt.plot(od, ss_data[f'SS{i+1}'])
    plt.ylabel('Leitura (AD 16 bits)')
    plt.xlabel('OD_600')
    plt.show()


'''
for i in range(len(od)):
    for j in ss:
        ss_data[f'{j}'] += [ss_raw_data[i][j-1]]
    print(ss_data)'''