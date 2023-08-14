import matplotlib.pyplot as plt
import statistics
import csv
from utils import *
from organize_logs import graph_data, ss2channel

pt_100_1 = [
    [
        1510,
        1565,
        1601,
        1630,
        1687,
        1770,
        1780,
        1790,
        1800,
        1810,
        1820,
        1830,
        1840,
        1850,
        1860,
        1870,
        1880,
        1890,
        1900,
        1910,
        1920,
        1930,
        1940,
        1950,
        1960,
        1970,
        1980,
        1990,
        2000
    ],
    [
        42.2,
        41.4,
        40.5,
        39.9,
        38.8,
        35.9,
        35.7,
        35.5,
        35.2,
        35.0,
        34.7,
        34.4,
        34.1,
        33.8,
        33.5,
        33.2,
        32.8,
        32.5,
        32.2,
        31.8,
        31.5,
        31.2,
        30.8,
        30.5,
        30.2,
        29.9,
        29.6,
        29.3,
        29.0
    ]
] # Dados retirados do excel

pt_100_2 = [
    [
        1295,
        1350,
        1360,
        1370,
        1380,
        1390,
        1400,
        1410,
        1420,
        1430,
        1440,
        1450,
        1460,
        1470,
        1480,
        1490,
        1500,
        1510,
        1520,
        1530,
        1540,
        1550,
        1560,
        1570,
        1580,
        1590,
        1620,
        1630,
        1640,
        1650,
        1660,
        1670,
        1680,
        1690,
        1700,
        1710,
        1720
    ],
    [
        49.3,
        49.0,
        48.9,
        48.8,
        48.7,
        48.5,
        48.3,
        48.1,
        47.9,
        47.6,
        47.4,
        47.1,
        46.8,
        46.6,
        46.2,
        46.0,
        45.6,
        45.3,
        44.9,
        44.6,
        44.3,
        44.0,
        43.6,
        43.3,
        42.9,
        42.5,
        41.3,
        41.1,
        40.9,
        40.9,
        40.2,
        39.9,
        39.6,
        39.2,
        38.9,
        38.5,
        38.3,
    ]
] # Dados retirados do excel

formula = [
    [
        1950,
        1900,
        1850,
        1800,
        1750,
        1700,
        1650,
        1600,
        1550,
        1500
    ],
    [
        29.9,
        30.0,
        31.5,
        32.5,
        33.4,
        34.5,
        35.7,
        36.5,
        37.1,
        38.0,
    ]
] # Dados retirados do excel

calibracao = {
    'measured': [
        [26.8, 36.6],
        [29.6, 36.4],
        [30.4, 34.8],
        [31.8, 33.5],
        [32.2, 33.5],
        [31.2, 35.3],
        [28.1, 35.2],
        [27.3, 37.0],
    ],
    'vial_data': [
        [2082, 1716],
        [1973, 1718],
        [1937, 1782],
        [1881, 1830],
        [1876, 1826],
        [1919, 1767],
        [2024, 1765],
        [2060, 1700],
    ],
    'coeficientes': [
        [-37.34693877551022, 3082.8979591836737], 
        [-37.5, 3083.0],
        [-35.22727272727273, 3007.909090909091], 
        [-30.000000000000018, 2835.0000000000005], 
        [-38.46153846153859, 3114.4615384615427], 
        [-37.073170731707336, 3075.682926829269], 
        [-36.4788732394366, 3049.0563380281687], 
        [-37.11340206185568, 3073.19587628866]
    ]
} # Dados retirados do excel

logs = {
    'normal': 'logs/temp-curves/EVOLVER-1/Kapton/log_24-05-23_13:19:23/raw.csv',
    'kapton': 'logs/temp-curves/EVOLVER-1/Kapton/log_25-05-23_09:09:41/raw.csv',
    'resfriando': {
        'normal': 'logs/temp-curves/EVOLVER-1/Kapton/log_24-05-23_14:18:56/raw.csv',
        'kapton': 'logs/temp-curves/EVOLVER-1/Kapton/log_25-05-23_10:08:29/raw.csv'
    }
}


def organize_temp_curves_kapton(active_ss):
    columns = ['time(s)']
    for i in range(16):
            columns += [f'SS{i+1}']

    data = {
        'com': {
            'aquecendo': {
                'time(s)': [],
                '1': {
                    'SS1': [],
                    'SS2': [],
                    'avg': [],
                },
                '2': {
                    'SS3': [],
                    'SS4': [],
                    'avg': [],
                },
                '3': {
                    'SS5': [],
                    'SS6': [],
                    'avg': [],
                },
                '6': {
                    'SS7': [],
                    'SS8': [],
                    'avg': [],
                },
            },

            'resfriando': {
                'time(s)': [],
                '1': {
                    'SS1': [],
                    'SS2': [],
                    'avg': [],
                },
                '2': {
                    'SS3': [],
                    'SS4': [],
                    'avg': [],
                },
                '3': {
                    'SS5': [],
                    'SS6': [],
                    'avg': [],
                },
                '6': {
                    'SS7': [],
                    'SS8': [],
                    'avg': [],
                },
            }
        },
        'sem': {
            'time(s)': [],
            'setpoint': [],
            'aquecendo': {
                'avg': {},
            },
            'resfriando': {
                'avg': {},
            },
        }
    }

    for i in range(16):
        data['sem']['aquecendo'][f'SS{i+1}'] = []
        data['sem']['resfriando'][f'SS{i+1}'] = []

    with open(logs['normal'], 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    raw_data = raw_data[1:]
    inicial_time = float(raw_data[0][0])
    setpoint = 2050

    for line in raw_data:
        if line[1][-1] == 'e':
            setpoint = float(line[2])

        else:
            data['sem']['time(s)'] += [float(line[0]) - inicial_time]
            line = line[2:]  
            data['sem']['setpoint'] += [setpoint]

            for i in range(16):
                data['sem']['aquecendo'][f'SS{i+1}'] += [float(line[ss2channel[i]])]

    with open(logs['resfriando']['normal'], 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    inicial_time = float(raw_data[0][0])

    for line in raw_data[:len(data['sem']['time(s)'])]:
        data['sem']['time(s)'] += [float(line[0]) - inicial_time]
        line = line[1:]  

        for i in range(16):
            data['sem']['resfriando'][f'SS{i+1}'] += [float(line[ss2channel[i]])]

    with open(logs['kapton'], 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    raw_data = raw_data[1:]
    inicial_time = float(raw_data[0][0])
    
    for line in raw_data:
        if line[1][-1] != 'e':
            data['com']['aquecendo']['time(s)'] += [float(line[0]) - inicial_time]
            line = line[2:]

            data['com']['aquecendo']['1']['SS1'] += [float(line[ss2channel[0]])]
            data['com']['aquecendo']['1']['SS2'] += [float(line[ss2channel[1]])]
            data['com']['aquecendo']['2']['SS3'] += [float(line[ss2channel[2]])]
            data['com']['aquecendo']['2']['SS4'] += [float(line[ss2channel[3]])]
            data['com']['aquecendo']['3']['SS5'] += [float(line[ss2channel[4]])]
            data['com']['aquecendo']['3']['SS6'] += [float(line[ss2channel[5]])]
            data['com']['aquecendo']['6']['SS7'] += [float(line[ss2channel[6]])]
            data['com']['aquecendo']['6']['SS8'] += [float(line[ss2channel[7]])]

    with open(logs['resfriando']['kapton'], 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]

    inicial_time = float(raw_data[0][0])

    for line in raw_data[::len(data['com']['aquecendo']['time(s)'])]:
        data['com']['resfriando']['time(s)'] += [float(line[0]) - inicial_time]
        line = line[1:]  

        data['com']['resfriando']['1']['SS1'] += [float(line[ss2channel[0]])]
        data['com']['resfriando']['1']['SS2'] += [float(line[ss2channel[1]])]
        data['com']['resfriando']['2']['SS3'] += [float(line[ss2channel[2]])]
        data['com']['resfriando']['2']['SS4'] += [float(line[ss2channel[3]])]
        data['com']['resfriando']['3']['SS5'] += [float(line[ss2channel[4]])]
        data['com']['resfriando']['3']['SS6'] += [float(line[ss2channel[5]])]
        data['com']['resfriando']['6']['SS7'] += [float(line[ss2channel[6]])]
        data['com']['resfriando']['6']['SS8'] += [float(line[ss2channel[7]])]

    print(data['com']['aquecendo'])

    '''for i in range(len(data['time(s)'])):
        aux = [data[f'SS{ss}'][i] for ss in active_ss]
        data['avg'] += [statistics.fmean(aux)]

    for i in range(len(data['time(s)'])):
        data['avg_1'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [1,2]])]
        data['avg_2'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [3,4]])]
        data['avg_3'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [5,6]])]
        data['avg_6'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [7,8]])]

    figure = plt.figure()
    figure.set_figwidth(12)
    figure.set_figheight(7)

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    plt.plot(data['time(s)'], ad_temp(data['setpoint']), label=f'Setpoint', linestyle='--', alpha=1)
    plt.plot(data['time(s)'], ad_temp(data['avg']), label=f'Sem Kapton, média das 8 SSs', alpha=1)

    for v in [[1,[1,2]],[2,[3,4]],[3,[5,6]],[6,[7,8]]]:
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'avg_{v[0]}']), label=f'{v[0]} voltas de Kapton, média das SSs {v[1]}')
    
    plt.title(f'Log de Temp: Aquecendo tubos envoltos por Kapton, eVOLVER 1')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/Gráficos/Aquecendo-Média.png')
    plt.show()
    

    figure, axs = plt.subplots(2,2)
    figure.set_figwidth(12)
    figure.set_figheight(7)

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    figure.suptitle('Log de Temp: Aquecendo tubos envoltos com Kapton, eVOLVER 1')
    plt.subplots_adjust(bottom=0.07, top=0.9, hspace=0.25)

    axs[0,0].set(title='1 volta de Kapton, SS1 e SS2')
    axs[0,0].plot(data['time(s)'], ad_temp(data['setpoint']), label=f'Setpoint', linestyle='--')

    for ss in [1,2]:
        axs[0,0].plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss} sem Kapton')
        axs[0,0].plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} com Kapton')
    
    axs[1,0].set(title='2 voltas de Kapton, SS3 e SS4')
    axs[1,0].plot(data['time(s)'], ad_temp(data['setpoint']), label=f'Setpoint', linestyle='--')

    for ss in [3,4]:
        axs[1,0].plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}  sem Kapton')
        axs[1,0].plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} com Kapton')
    
    axs[0,1].set(title='3 voltas de Kapton, SS5 e SS6')
    axs[0,1].plot(data['time(s)'], ad_temp(data['setpoint']), label=f'Setpoint', linestyle='--')

    for ss in [5,6]:
        axs[0,1].plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss} sem Kapton')
        axs[0,1].plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} com Kapton')

    axs[1,1].set(title='6 voltas de Kapton, SS7 e SS8')
    axs[1,1].plot(data['time(s)'], ad_temp(data['setpoint']), label=f'Setpoint', linestyle='--')

    for ss in [7,8]:
        axs[1,1].plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss} sem Kapton', linestyle='--')
        axs[1,1].plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} com Kapton')
    
    for ax in axs.flat:
        ax.set(xlabel='Tempo (s)', ylabel='Temperatura (°C)')
        ax.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/Gráficos/Aquecendo-PorSS.png')
    plt.show()'''



def organize_temp_curves_realtime_kapton(active_ss):
    columns = ['time(s)']
    for i in range(16):
            columns += [f'SS{i+1}']

    data_k = {
        'avg_1': [],
        'avg_2': [],
        'avg_3': [],
        'avg_6': [],
    }
    data = {
        'avg': [],
    }

    for column in columns:
        data[column] = []
        data_k[column] = []

    with open('logs/temp-curves-realtime/EVOLVER-1/log_24-05-23_14:18:56/raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    with open(f'logs/temp-curves-realtime/EVOLVER-1/log_25-05-23_10:08:29/raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data_k = [row for row in log_reader]

    inicial_time = float(raw_data[0][0])
    inicial_time_k = float(raw_data_k[0][0])

    for line in raw_data[:3550]:
        data['time(s)'] += [float(line[0]) - inicial_time]
        line = line[1:]  

        for i in range(16):
            data[f'SS{i+1}'] += [float(line[ss2channel[i]])]

    for line in raw_data_k[:3370]:
        data_k['time(s)'] += [float(line[0]) - inicial_time_k]
        line = line[1:]  

        for i in range(16):
            data_k[f'SS{i+1}'] += [float(line[ss2channel[i]])]
    
    for i in range(len(data['time(s)'])):
        aux = [data[f'SS{ss}'][i] for ss in active_ss]
        data['avg'] += [statistics.fmean(aux)]

    for i in range(len(data['time(s)'])):
        data_k['avg_1'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [1,2]])]
        data_k['avg_2'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [3,4]])]
        data_k['avg_3'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [5,6]])]
        data_k['avg_6'] += [statistics.fmean([data[f'SS{ss}'][i] for ss in [7,8]])]

    figure = plt.figure()
    figure.set_figwidth(12)
    figure.set_figheight(7)

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    plt.plot(data['time(s)'][::100], ad_temp(data['avg'])[::100], label=f'Sem Kapton, média das 8 SSs', alpha=1)

    for v in [[1,[1,2]],[2,[3,4]],[3,[5,6]],[6,[7,8]]]:
        plt.plot(data_k['time(s)'][::100], ad_temp(data_k[f'avg_{v[0]}'])[:3370:100], label=f'{v[0]} voltas de Kapton, média das SSs {v[1]}')
    
    plt.title(f'Log de Temp: Resfriando tubos envoltos por Kapton, eVOLVER 1')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/Média-Resfriando.png')
    plt.show()

    figure, axs = plt.subplots(2,2)
    figure.set_figwidth(12)
    figure.set_figheight(7)

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    figure.suptitle('Log de Temp: Resfriando tubos envoltos por Kapton, eVOLVER 1')
    plt.subplots_adjust(bottom=0.08, top=0.9, hspace=0.25)

    axs[0,0].set(title='1 volta de Kapton, SS1 e SS2')
    axs[1,0].set(title='2 voltas de Kapton, SS3 e SS4')
    axs[0,1].set(title='3 voltas de Kapton, SS5 e SS6')
    axs[1,1].set(title='6 voltas de Kapton, SS7 e SS8')

    for ss in [1,2]:
        axs[0,0].plot(data['time(s)'][::100], ad_temp(data[f'SS{ss}'])[::100], label=f'SS{ss} sem Kapton')
        axs[0,0].plot(data_k['time(s)'][::100], ad_temp(data_k[f'SS{ss}'])[::100], label=f'SS{ss} com Kapton')

    for ss in [3,4]:
        axs[1,0].plot(data['time(s)'][::100], ad_temp(data[f'SS{ss}'])[::100], label=f'SS{ss} sem Kapton')
        axs[1,0].plot(data_k['time(s)'][::100], ad_temp(data_k[f'SS{ss}'])[::100], label=f'SS{ss} com Kapton')

    for ss in [5,6]:
        axs[0,1].plot(data['time(s)'][::100], ad_temp(data[f'SS{ss}'])[::100], label=f'SS{ss} sem Kapton')
        axs[0,1].plot(data_k['time(s)'][::100], ad_temp(data_k[f'SS{ss}'])[::100], label=f'SS{ss} com Kapton')

    for ss in [7,8]:
        axs[1,1].plot(data['time(s)'][::100], ad_temp(data[f'SS{ss}'])[::100], label=f'SS{ss} sem Kapton')
        axs[1,1].plot(data_k['time(s)'][::100], ad_temp(data_k[f'SS{ss}'])[::100], label=f'SS{ss} com Kapton')
    
    for ax in axs.flat:
        ax.set(xlabel='Tempo (s)', ylabel='Temperatura (°C)')
        ax.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/Individualmente-Resfriando.png')
    plt.show()


def linear_i(x,a,b):
    return (np.array(x) - b)/a

def analise():
    figure = plt.figure()
    figure.set_figwidth(12)
    figure.set_figheight(7)

    plt.title('Log de Temperatura: Refriamento - SS8, eVOLVER 1')

    plt.scatter(pt_100_1[0], pt_100_1[1], label='Medida com Pt100, a partir de 42.2°C')
    plt.scatter(pt_100_2[0], pt_100_2[1], label='Medida com Pt100, a partir de 49.3°C')

    plt.scatter(pt_100_1[0]+ pt_100_2[0], linear_i(pt_100_1[0] + pt_100_2[0], *calibracao['coeficientes'][7]), label='Medida com a calibração')
    plt.scatter(pt_100_1[0]+ pt_100_2[0], ad_temp(pt_100_1[0] + pt_100_2[0]), label='Medida com a equação característica')

    plt.xlabel('Leitura AD do termistor (12 bits)')
    plt.ylabel('Temperatuura (°C)')
    plt.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Calibração.png')
    plt.show()



if __name__ == '__main__':
    #organize_temp_curves_kapton([1,2,3,4,5,6,7,8])
    #organize_temp_curves_realtime_kapton( [1,2,3,4,5,6,7,8])
    analise()