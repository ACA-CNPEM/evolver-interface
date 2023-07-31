import matplotlib.pyplot as plt
from organize_logs import graph_data
from utils import *
import statistics
from scipy.optimize import curve_fit
import json
import glob

logs_repetibilidade = {
    '1': {
        '100': [
            'logs/od-curves/EVOLVER-1/Repetibilidade/log_16-06-23_14:37:47',
            'logs/od-curves/EVOLVER-1/Repetibilidade/log_19-06-23_08:24:59',
            'logs/od-curves/EVOLVER-1/Repetibilidade/log_19-06-23_09:16:49',
            'logs/od-curves/EVOLVER-1/Repetibilidade/log_20-06-23_11:16:05',
            'logs/od-curves/EVOLVER-1/Repetibilidade/log_20-06-23_11:42:40',
            'logs/od-curves/EVOLVER-1/Repetibilidade/log_20-06-23_13:17:10'
        ]
    },

    '2': {
        '10': [
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_13-06-23_08:39:40', 
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_13-06-23_09:10:18', 
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_13-06-23_11:26:38',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_13-06-23_12:28:03', 
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_09:01:19',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_09:20:53',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_09:32:05',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_09:36:53',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_09:50:28',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_09:54:22',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_10:02:54',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_10:55:03',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_11:14:23',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_11:48:40',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_13:06:22'
        ],

        '100': [
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_13:21:39',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_16-06-23_14:33:37',
            'logs/od-curves/EVOLVER-2/Repetibilidade/log_19-06-23_08:24:04'
        ]
    },
}

logs_tampas = {
    'sem': 'logs/od-curves/EVOLVER-2/Tampa/log_31-05-23_14:46:41',
    'com': 'logs/od-curves/EVOLVER-2/Tampa/log_14-06-23_13:21:39'
}

logs_vol = [
    'logs/od-curves/EVOLVER-2/VolumeMin/log_27-06-23_10:15:12',
    'logs/od-curves/EVOLVER-2/VolumeMin/log_27-06-23_10:31:07',
    'logs/od-curves/EVOLVER-2/VolumeMin/log_27-06-23_10:43:42',
    'logs/od-curves/EVOLVER-2/VolumeMin/log_27-06-23_11:01:57',
    'logs/od-curves/EVOLVER-2/VolumeMin/log_27-06-23_12:54:09',
    'logs/od-curves/EVOLVER-2/VolumeMin/log_28-06-23_08:44:49'
]

logs_crescimento = [
    'logs/od-curves/EVOLVER-2/log_30-06-23_11:37:59',
    'logs/od-curves/EVOLVER-2/log_30-06-23_15:06:18',
    'od_evolver2.json'
]

logs_angle = {
    '1':[
        {
        '0': 'logs/od-curves/EVOLVER-1/Rot-1/log_25-07-23_10:03:33',
        '45': 'logs/od-curves/EVOLVER-1/Rot-1/log_25-07-23_10:09:34',
        '90': 'logs/od-curves/EVOLVER-1/Rot-1/log_25-07-23_10:15:06',
        '180': 'logs/od-curves/EVOLVER-1/Rot-1/log_25-07-23_10:20:54',
        '270': 'logs/od-curves/EVOLVER-1/Rot-1/log_25-07-23_10:26:31',
        '360': 'logs/od-curves/EVOLVER-1/Rot-1/log_25-07-23_10:33:03'
        },
        {
        '0': 'logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_09:38:20',
        '45': 'logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_09:44:01',
        '90': 'logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_09:50:08',
        '180': 'logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_09:56:08',
        '270': 'logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_10:02:59',
        '360': 'logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_10:12:08'
        },
        {
        '0': 'logs/od-curves/EVOLVER-1/Rot-3/log_28-07-23_10:25:17',
        '45': 'logs/od-curves/EVOLVER-1/Rot-3/log_28-07-23_10:32:12',
        '90': 'logs/od-curves/EVOLVER-1/Rot-3/log_28-07-23_10:39:21',
        '180': 'logs/od-curves/EVOLVER-1/Rot-3/log_28-07-23_10:45:23',
        '270': 'logs/od-curves/EVOLVER-1/Rot-3/log_28-07-23_10:53:20',
        '360': 'logs/od-curves/EVOLVER-1/Rot-3/log_28-07-23_10:58:59'
        }
    ],
    '2': []
}



# INFLUÊNCIA DO VIAL NAS MEDIDAS DE OD
def data_revesa(n, evolver):
    ss_map = {'SS1': 15, 'SS2': 14, 'SS3': 11, 'SS4': 10, 'SS5': 7, 'SS6': 6, 'SS7': 3, 'SS8': 2, 'SS9': 13, 'SS10': 12, 'SS11': 9, 'SS12': 8, 'SS13': 5, 'SS14': 4, 'SS15': 1, 'SS16': 0}
    logs_table = []
    n_samples = 5

    with open('logs/od-curves/EVOLVER-{}/Revesa-{}/revesa.csv'.format(evolver,n), 'r') as file:
        csv_file =  csv.DictReader(file)
        for row in csv_file:
            logs_table.append(dict(row))

    active_ss = list(logs_table[0].keys())
    active_ss.remove('time')

    vial_ref = [i+1 for i in range(8)]
    led_sets = []

    log0 = glob.glob('logs/od-curves/EVOLVER-{}/Revesa-{}/*'.format(evolver, n)+logs_table[0]['time']+'*')[0]
    with open(log0+'/od_lede_raw.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            led_sets.append(float(row[2]))
    n_leds = len(led_sets)

    od_data = {
        'n': n_leds,
        'vials': vial_ref,
        'led': led_sets
    }

    for ss in active_ss:
        od_data[ss] = {}
        for value in od_data['vials']:
            od_data[ss]['{}'.format(value)] = [[] for _ in range(n_leds)]

    for log in logs_table:
        path = glob.glob('logs/od-curves/EVOLVER-{}/Revesa-{}/*'.format(evolver, n)+log['time']+'*')[0]

        with open(path+'/od_135b_raw.csv', 'r') as file:
            reader = csv.reader(file)
            i_sample = 0
            i_led = 0

            for row in reader:
                del row[0:2]

                for ss in active_ss:
                    value = row[ss_map[ss]]

                    if log[ss] != '--':
                        od_data[ss][log[ss]][i_led].append(int(value))

                i_sample += 1
                
                if i_sample == n_samples:
                    i_sample = 0
                    i_led += 1

    return od_data


def graph_revesa(n, evolver):
    data = data_revesa(n, evolver)
    vials = data['vials']

    fig, ax = plt.subplots(2, 4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Variação da medida de OD com troca de vials - eVOLVER{}".format(evolver))

    for j in range(8):
        '''
        maxs = []
        mins = []
        vars = []

        for i in range(data['n']):
            maxs += [max([max(data[f'SS{j+1}'][f'{v+1}'][i]) for v in range(8)])]
            mins += [min([min(data[f'SS{j+1}'][f'{v+1}'][i]) for v in range(8)])]
            vars += [maxs[i] - mins[i]]
        '''

        for v in range(8):
            x = [100*k/4095 for k in data['led']]
            median = [np.median(data[f'SS{j+1}'][f'{v+1}'][i]) for i in range(data['n'])]
            std = [np.std(data[f'SS{j+1}'][f'{v+1}'][i]) for i in range(data['n'])]
                       
            ax[j//4, (j%4)].errorbar(x, median, yerr=std, fmt='none', capsize=2)
            ax[j//4, (j%4)].plot(x, median, 'o', markersize=3.5, alpha=0.9, label='Vial {}'.format(v+1))

            ax[j//4, (j%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax[j//4, (j%4)].set(title=f'SS{j+1}', xlabel='PWM LED (%)', ylabel='Leitura AD (16 bits)')
            ax[j//4, (j%4)].legend(loc='best', fontsize=9)

    plt.subplots_adjust(left=0.083, bottom=0.11, right=0.948, top=0.879, wspace=0.24, hspace=0.317)
    plt.show()

    for i in range(data['n']):
        fig, ax = plt.subplots(2, 4)
        fig.set_figwidth(16)
        fig.set_figheight(8)

        plt.suptitle("Variação da medida de OD com rotação - LED {:.1f}%, eVOLVER{}".format(100*data['led'][i]/4095, evolver))

        for j in range(8):
            median = [np.median(data[f'SS{j+1}'][f'{a}'][i]) for a in vials]
            std = [np.std(data[f'SS{j+1}'][f'{a}'][i]) for a in vials]
            
            ax[j//4, (j%4)].errorbar(median, vials, xerr=std, fmt='none', capsize=2, color='k')
            ax[j//4, (j%4)].plot(median, vials, 'o', color='k')
            
            for k,a in enumerate(vials):
                ax[j//4, (j%4)].plot(data[f'SS{j+1}'][f'{a}'][i], [a]*5, 'o', markersize=3.5, alpha=0.6)

            ax[j//4, (j%4)].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            ax[j//4, (j%4)].set(title=f'SS{j+1}', ylabel='Vial', xlabel='Leitura AD (16 bits)')
            
        plt.subplots_adjust(left=0.086, bottom=0.083, right=0.962, top=0.912, wspace=0.3, hspace=0.248)
        plt.show()


def data_angles(n,evolver):
    active_ss = [f'SS{i+1}' for i in range(8)]
    ss_map = {'SS1': 15, 'SS2': 14, 'SS3': 11, 'SS4': 10, 'SS5': 7, 'SS6': 6, 'SS7': 3, 'SS8': 2, 'SS9': 13, 'SS10': 12, 'SS11': 9, 'SS12': 8, 'SS13': 5, 'SS14': 4, 'SS15': 1, 'SS16': 0}
    angles = [0,45,90,180,270,360]
    n_samples = 5
    led_sets = []

    with open('{}/od_lede_raw.csv'.format(logs_angle[f'{evolver}'][n-1]['0']), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            led_sets.append(float(row[2]))
    n_leds = len(led_sets)

    od_data = {
        'n': n_leds,
        'led': led_sets
    }

    for ss in active_ss:
        od_data[ss] = {}
        for a in angles:
            od_data[ss]['{}'.format(a)] = [[] for _ in range(n_leds)]

    for a in angles:
        with open('{}/od_135b_raw.csv'.format(logs_angle[f'{evolver}'][n-1][f'{a}']), 'r') as file:
            reader = csv.reader(file)
            i_sample = 0
            i_led = 0

            for row in reader:
                del row[0:2]

                for ss in active_ss:
                    value = row[ss_map[ss]]
                    od_data[ss][f'{a}'][i_led].append(int(value))

                i_sample += 1
                if i_sample == n_samples:
                    i_sample = 0
                    i_led += 1
    
    return angles, od_data


def graph_angles(n, evolver):
    angles, data = data_angles(n, evolver)

    for i in range(data['n']):
        fig, ax = plt.subplots(2, 4)
        fig.set_figwidth(16)
        fig.set_figheight(8)

        plt.suptitle("Variação da medida de OD com rotação - LED {:.1f}%, eVOLVER{}".format(100*data['led'][i]/4095, evolver))

        for j in range(8):
            median = [np.median(data[f'SS{j+1}'][f'{a}'][i]) for a in angles]
            std = [np.std(data[f'SS{j+1}'][f'{a}'][i]) for a in angles]
            
            ax[j//4, (j%4)].errorbar(median, angles, xerr=std, fmt='none', capsize=2, color='k')
            ax[j//4, (j%4)].plot(median, angles, 'o', color='k')
            ax[j//4, (j%4)].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            ax[j//4, (j%4)].set(title=f'SS{j+1}', ylabel='Rotação (deg)', xlabel='Leitura AD (16 bits)')
            for k,a in enumerate(angles):
                ax[j//4, (j%4)].plot(data[f'SS{j+1}'][f'{a}'][i], [a]*5, 'o', markersize=3.5, alpha=0.6)
        
        plt.subplots_adjust(left=0.086, bottom=0.083, right=0.962, top=0.912, wspace=0.3, hspace=0.248)
        plt.show()


def graph_rot(n, evolver):
    data1 = data_revesa(n, evolver)
    angles, data = data_angles(n, evolver)

    for i in range(data['n']):
        fig, ax = plt.subplots(2, 4)
        fig.set_figwidth(16)
        fig.set_figheight(8)

        plt.suptitle("Variação da medida de OD com rotação e mudança de vials- LED {:.1f}%, eVOLVER{}".format(100*data['led'][i]/4095, evolver))

        for j in range(8):
            median = [np.median(data[f'SS{j+1}'][f'{a}'][i]) for a in angles]
            std = [np.std(data[f'SS{j+1}'][f'{a}'][i]) for a in angles]

            median1 = [np.median(data1[f'SS{j+1}'][f'{a}'][i]) for a in data1['vials']]
            std1 = [np.std(data1[f'SS{j+1}'][f'{a}'][i]) for a in data1['vials']]

            axs = ax[j//4, (j%4)].twinx()
            
            ax[j//4, (j%4)].errorbar(median, angles, xerr=std, fmt='none', capsize=2, color='tab:blue')
            axs.errorbar(median1, data1['vials'], xerr=std1, fmt='none', capsize=2, color='tab:red')

            ax[j//4, (j%4)].plot(median, angles, 'o', color='tab:blue')
            axs.plot(median1, data1['vials'], 'o', color='tab:red')

            ax[j//4, (j%4)].tick_params(axis='y', labelcolor='tab:blue')
            axs.tick_params(axis='y', labelcolor='tab:red')

            ax[j//4, (j%4)].set_ylabel('Rotação (deg)', color='tab:blue')
            axs.set_ylabel('Vial number', color='tab:red')

            ax[j//4, (j%4)].set(title=f'SS{j+1}', xlabel='Leitura AD (16 bits)')
            ax[j//4, (j%4)].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            
            '''
            for k,a in enumerate(angles):
                ax[j//4, (j%4)].plot(data[f'SS{j+1}'][f'{a}'][i], [a]*5, 'o', markersize=3.5, alpha=0.6, label='Δ({:.0f}°) = {:.1f}%'.format(a, 100*(max(data[f'SS{j+1}'][f'{a}'][i]) - min(data[f'SS{j+1}'][f'{a}'][i]))/np.median(data[f'SS{j+1}'][f'{a}'][i])))

            for k,v in enumerate(data1['vials']):
                axs.plot(data1[f'SS{j+1}'][f'{v}'][i], [v]*5, 'o', markersize=3.5, alpha=0.6, label='Δ({:.0f}°) = {:.1f}%'.format(a, 100*(max(data[f'SS{j+1}'][f'{a}'][i]) - min(data[f'SS{j+1}'][f'{a}'][i]))/np.median(data[f'SS{j+1}'][f'{a}'][i])))
            '''

        plt.subplots_adjust(left=0.086, bottom=0.083, right=0.962, top=0.912, wspace=0.443, hspace=0.302)
        plt.show()


# ***
def graph_pump(n, evolver):
    logs = ['logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_09:33:11', 
            'logs/od-curves/EVOLVER-1/Rot-2/log_26-07-23_09:38:20']
    
    active_ss = [f'SS{i+1}' for i in range(8)]
    ss_map = {'SS1': 15, 'SS2': 14, 'SS3': 11, 'SS4': 10, 'SS5': 7, 'SS6': 6, 'SS7': 3, 'SS8': 2, 'SS9': 13, 'SS10': 12, 'SS11': 9, 'SS12': 8, 'SS13': 5, 'SS14': 4, 'SS15': 1, 'SS16': 0}
    
    pumps = [0, 1]
    n_samples = 5
    led_sets = []
    
    with open(f'{logs[0]}/od_lede_raw.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            led_sets.append(float(row[2]))
    n_leds = len(led_sets)

    od_data = {
        'n': n_leds,
        'led': led_sets
    }

    for ss in active_ss:
        od_data[ss] = {}
        for a in pumps:
            od_data[ss]['{}'.format(a)] = [[] for _ in range(n_leds)]

    for a in pumps:
        with open('{}/od_135b_raw.csv'.format(logs[a]), 'r') as file:
            reader = csv.reader(file)
            i_sample = 0
            i_led = 0

            for row in reader:
                del row[0:2]

                for ss in active_ss:
                    value = row[ss_map[ss]]
                    od_data[ss][f'{a}'][i_led].append(int(value))

                i_sample += 1
                if i_sample == n_samples:
                    i_sample = 0
                    i_led += 1
    
    fig, ax = plt.subplots(2, 4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Variação da medida de OD com o Regime de inserção de Líquidos - eVOLVER{}".format(evolver))
    legend = ['Bombas atuando em 0.1|1', 'Bombas atuando em 0.1|10']
    colors = ['tab:blue', 'tab:red']

    for j in range(8):
        for p in pumps:
            x = [100*k/4095 for k in od_data['led']]
            median = [np.median(od_data[f'SS{j+1}'][f'{p}'][i]) for i in range(od_data['n'])]
            std = [np.std(od_data[f'SS{j+1}'][f'{p}'][i]) for i in range(od_data['n'])]

            ax[j//4, (j%4)].errorbar(x, median, yerr=std, fmt='none', capsize=2, color='k')
            ax[j//4, (j%4)].plot(x, median, 'o', markersize=3, color=colors[p], label=f'{legend[p]}')

            ax[j//4, (j%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax[j//4, (j%4)].set(title=f'SS{j+1}', xlabel='PWM LED (%)', ylabel='Leitura AD (16 bits)')
            ax[j//4, (j%4)].legend(loc='best', fontsize=9)

    plt.subplots_adjust(left=0.098, bottom=0.088, right=0.938, wspace=0.22, hspace=0.345)        
    plt.show()
                

def graphs_rot_subs(n1, n2, evolver):
    legs = ['Vazia', 'Água']
    types = ['Revesamento', 'Rotação']
    ys = ['Vial number', 'Rotação (deg)']

    data = [data_revesa(n1, evolver), data_revesa(n2, evolver), data_angles(n1, evolver)[1], data_angles(n2, evolver)[1]]
    values = [[1,2,3,4,5,6,7,8], [0,45,90,180,270,360]]
    all_maxs = []

    for i in range(8):
        maxs = []

        fig, ax = plt.subplots(2, 5)
        fig.set_figwidth(16)
        fig.set_figheight(8)

        plt.suptitle("Variação da medida de OD devido aos vials - SS{} com resistor R=100kΩ, eVOLVER{}".format(i+1, evolver))
            
        for j in range(data[0]['n']):
            median = []
            std = []
            vars = []

            for k in range(4):
                median += [[np.median(data[k][f'SS{i+1}'][f'{a}'][j]) for a in values[k//2]]]
                std += [[np.std(data[k][f'SS{i+1}'][f'{a}'][j]) for a in values[k//2]]]
                vars += [[max(data[k][f'SS{i+1}'][f'{a}'][j]) - min(data[k][f'SS{i+1}'][f'{a}'][j]) for a in values[k//2]]]

            ax[j//5, (j%5)].errorbar(median[0], values[0], xerr=std[0], fmt='o', markersize=3.5, capsize=2, color='tab:blue', label=legs[0]) #\n  Δ: {:.0f}\n  δ: {:.0f}'.format(max(vars[0]), max(std[0])))
            ax[j//5, (j%5)].errorbar(median[1], values[0], xerr=std[1], fmt='o', markersize=3.5, capsize=2, color='tab:red', label=legs[1]) #\n  Δ: {:.0f}\n  δ: {:.0f}'.format(max(vars[1]), max(std[1])))

            for a in values[0]:
                ax[j//5, (j%5)].scatter(data[0][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:blue', s=3, alpha=0.5)
                ax[j//5, (j%5)].scatter(data[1][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:red', s=3, alpha=0.5)

            ax[j//5, (j%5)].legend(title=types[0], loc='upper center', fontsize=9, title_fontsize=9)

            axs = ax[j//5, (j%5)].twinx()

            axs.errorbar(median[2], values[1], xerr=std[2], fmt='o', markersize=3.5, capsize=2, color='tab:green', label=legs[0]) #\n  Δ: {:.0f}\n  δ: {:.0f}'.format(max(vars[2]), max(std[2])))
            axs.errorbar(median[3], values[1], xerr=std[3], fmt='o', markersize=3.5, capsize=2, color='tab:orange', label=legs[1]) #\n  Δ: {:.0f}\n  δ: {:.0f}'.format(max(vars[3]), max(std[3])))

            for a in values[1]:
                axs.scatter(data[2][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:green', s=3, alpha=0.5)
                axs.scatter(data[3][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:orange', s=3, alpha=0.5)

            axs.legend(title=types[1], loc='lower center', fontsize=9, title_fontsize=9)

            all_max = max(max(max(vars[0]), max(vars[2])), max(max(vars[1]), max(vars[3])))

            ax[j//5, (j%5)].set_title('PWM LED {:.0f}%\nMáx_Δ: {:.0f}'.format(100*data[0]['led'][j]/4095, all_max), fontsize=10)
            ax[j//5, (j%5)].set_xlabel('Leitura AD (16 bits)', fontsize=10)
            ax[j//5, (j%5)].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            
            if j%5 == 0:
                ax[j//5, (j%5)].set_ylabel(ys[0], fontsize=10)
            
            if j%5 == 4:
                axs.set_ylabel(ys[1], fontsize=10)

            ax[j//5, (j%5)].tick_params(axis='both', labelsize=8)
            axs.tick_params(axis='y', labelsize=8)

            maxs += [all_max]

        plt.subplots_adjust(left=0.07, bottom=0.083, right=0.92, top=0.88, wspace=0.4, hspace=0.398)
        plt.show()

        all_maxs += [maxs]
    
    return all_maxs


def graphs_rot_r(n1, n2, evolver):
    legs = ['100 kΩ', '1 MΩ']
    types = ['Revesamento', 'Rotação']
    ys = ['Vial number', 'Rotação (deg)']

    data = [data_revesa(n1, evolver), data_revesa(n2, evolver), data_angles(n1, evolver)[1], data_angles(n2, evolver)[1]]
    values = [[1,2,3,4,5,6,7,8], [0,45,90,180,270,360]]
    all_maxs = []

    for i in range(8):
        maxs = []

        fig, ax = plt.subplots(2, 5)
        fig.set_figwidth(16)
        fig.set_figheight(8)

        plt.suptitle("Variação da medida de OD devido aos vials (com água) para diferentes resistores - SS{}, eVOLVER{}".format(i+1, evolver))
            
        for j in range(data[0]['n']):
            median = []
            std = []
            vars = []

            for k in range(4):
                median += [[np.median(data[k][f'SS{i+1}'][f'{a}'][j]) for a in values[k//2]]]
                std += [[np.std(data[k][f'SS{i+1}'][f'{a}'][j]) for a in values[k//2]]]
                vars += [[max(data[k][f'SS{i+1}'][f'{a}'][j]) - min(data[k][f'SS{i+1}'][f'{a}'][j]) for a in values[k//2]]]

            ax[j//5, (j%5)].errorbar(median[0], values[0], xerr=std[0], fmt='o', markersize=3.5, capsize=2, color='tab:blue', label='{}\n  Δ: {:.0f}\n  δ: {:.0f}'.format(legs[0], max(vars[0]), max(std[0])))
            ax[j//5, (j%5)].errorbar(median[1], values[0], xerr=std[1], fmt='o', markersize=3.5, capsize=2, color='tab:red', label='{}\n  Δ: {:.0f}\n  δ: {:.0f}'.format(legs[1], max(vars[1]), max(std[1])))

            for a in values[0]:
                ax[j//5, (j%5)].scatter(data[0][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:blue', s=3, alpha=0.5)
                ax[j//5, (j%5)].scatter(data[1][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:red', s=3, alpha=0.5)

            ax[j//5, (j%5)].legend(title=types[0], loc='upper center', fontsize=8, title_fontsize=9)

            axs = ax[j//5, (j%5)].twinx()

            axs.errorbar(median[2], values[1], xerr=std[2], fmt='o', markersize=3.5, capsize=2, color='tab:green', label='{}\n  Δ: {:.0f}\n  δ: {:.0f}'.format(legs[0], max(vars[2]), max(std[2])))
            axs.errorbar(median[3], values[1], xerr=std[3], fmt='o', markersize=3.5, capsize=2, color='tab:orange', label='{}\n  Δ: {:.0f}\n  δ: {:.0f}'.format(legs[1], max(vars[3]), max(std[3])))

            for a in values[1]:
                axs.scatter(data[2][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:green', s=3, alpha=0.5)
                axs.scatter(data[3][f'SS{i+1}'][f'{a}'][j], [a]*5, color='tab:orange', s=3, alpha=0.5)

            axs.legend(title=types[1], loc='lower center', fontsize=8, title_fontsize=9)

            all_max = max(max(max(vars[0]), max(vars[2])), max(max(vars[1]), max(vars[3])))

            ax[j//5, (j%5)].set_title('PWM LED {:.0f}%'.format(100*data[0]['led'][j]/4095), fontsize=10)
            ax[j//5, (j%5)].set_xlabel('Leitura AD (16 bits)', fontsize=10)
            ax[j//5, (j%5)].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            
            if j%5 == 0:
                ax[j//5, (j%5)].set_ylabel(ys[0], fontsize=10)
            
            if j%5 == 4:
                axs.set_ylabel(ys[1], fontsize=10)

            ax[j//5, (j%5)].tick_params(axis='both', labelsize=8)
            axs.tick_params(axis='y', labelsize=8)

            maxs += [all_max]

        plt.subplots_adjust(left=0.07, bottom=0.083, right=0.92, top=0.88, wspace=0.4, hspace=0.398)
        plt.show()

        all_maxs += [maxs]
    
    return all_maxs


def teste_influence_subs(n, n1, n2, evolver, leds):
    vars = graphs_rot_subs(n1, n2, evolver)
    data = [data_od(n, evolver, led) for led in leds]

    for i in range(8):
        fig, ax = plt.subplots(2, 5)
        fig.set_figwidth(16)
        fig.set_figheight(8)

        plt.suptitle("SS{}, eVOLVER{}".format(i+1, 1))
        
        for j,led in enumerate(leds):
            ods = data[j]['measuredData'][:-1]
            median = [np.median(data[j]['raw'][i][k]) for k in range(len(ods))]
            std = [np.std(data[j]['raw'][i][k]) for k in range(len(ods))]

            params, cov = curve_fit(sigmoid, ods, median, sigma=std, p0=[62721, 62721, 0, -1], maxfev=1000000000)
            linspace = np.linspace(0, max(ods), 500)
            cal = sigmoid(linspace, *params)

            err_od = [[0.01]*len(ods), [0.01]*len(ods)]
            err_med = [std, std]

            ax[j//5, (j%5)].errorbar(ods, median, xerr=err_od, yerr=err_med, fmt='o', label='Measured Data', markersize=4, capsize=2)
            ax[j//5, (j%5)].plot(linspace, cal, label='Calibration Curve')

            mais = [max(median[k] + vars[i][j]/2, math.ceil(params[0])) for k in range(len(ods))]
            menos = [min(median[k] - vars[i][j]/2, math.floor(params[1])) for k in range(len(ods))]
            var_fit = ad_od135(menos, *params) - ad_od135(mais, *params)

            erry = [[vars[i][j]/2]*len(ods),[vars[i][j]/2]*len(ods)]
            errx = [(var_fit/2)*len(ods), (var_fit/2)*len(ods)]
            
            fit = ad_od135(median, *params)
            ax[j//5, (j%5)].set_xlim(-0.1, 1.1)
            ax[j//5, (j%5)].errorbar(fit, median, xerr=errx, yerr=erry, fmt='o', markersize=4, capsize=2, label='Fitted Data')
 
            ax[j//5, (j%5)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax[j//5, (j%5)].set(title='LED {:.0f}%'.format(100*led/4095), ylabel='AD', xlabel='OD')
            ax[j//5, (j%5)].legend(fontsize=9)

        plt.subplots_adjust(left=0.06,bottom=0.08,right=0.97,top=0.91,wspace=0.25,hspace=0.27)
        plt.show()
    

def influ_agita(evolver):
    logs = {
        '0': 'logs/od-curves/EVOLVER-1/log_31-07-23_13:03:51',
        '10': 'logs/od-curves/EVOLVER-1/Agita-1/log_31-07-23_10:20:14',
        '15': 'logs/od-curves/EVOLVER-1/Agita-1/log_31-07-23_11:26:16',
        '20': 'logs/od-curves/EVOLVER-1/Agita-1/log_31-07-23_10:32:30',
        '25': 'logs/od-curves/EVOLVER-1/Agita-1/log_31-07-23_11:15:06',
        '30': 'logs/od-curves/EVOLVER-1/Agita-1/log_31-07-23_10:43:53',
        '35': 'logs/od-curves/EVOLVER-1/Agita-1/log_31-07-23_11:04:27',
        '40': 'logs/od-curves/EVOLVER-1/Agita-1/log_31-07-23_10:54:12',
    }

    active_ss = [f'SS{i+1}' for i in range(8)]
    ss_map = {'SS1': 15, 'SS2': 14, 'SS3': 11, 'SS4': 10, 'SS5': 7, 'SS6': 6, 'SS7': 3, 'SS8': 2, 'SS9': 13, 'SS10': 12, 'SS11': 9, 'SS12': 8, 'SS13': 5, 'SS14': 4, 'SS15': 1, 'SS16': 0}
    agitas = logs.keys()
    n_samples = 5
    led_sets = []

    with open('{}/od_lede_raw.csv'.format(logs['10']), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            led_sets.append(float(row[2]))
    n_leds = len(led_sets)

    od_data = {
        'n': n_leds,
        'led': led_sets
    }

    for ss in active_ss:
        od_data[ss] = {}
        for a in agitas:
            od_data[ss]['{}'.format(a)] = [[] for _ in range(n_leds)]

    for a in agitas:
        with open('{}/od_135b_raw.csv'.format(logs[f'{a}']), 'r') as file:
            reader = csv.reader(file)
            i_sample = 0
            i_led = 0

            for row in reader:
                del row[0:2]

                for ss in active_ss:
                    value = row[ss_map[ss]]
                    od_data[ss][f'{a}'][i_led].append(int(value))

                i_sample += 1
                if i_sample == n_samples:
                    i_sample = 0
                    i_led += 1
    
    fig, ax = plt.subplots(2, 4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Variação da medida de OD com rotação - eVOLVER{}".format(evolver))
    for j in range(8):
        x = [100*od_data['led'][i]/4095 for i in range(od_data['n'])]

        for a in agitas:
            median = [np.median(od_data[f'SS{j+1}'][f'{a}'][i]) for i in range(len(od_data['led']))]
            std = [np.std(od_data[f'SS{j+1}'][f'{a}'][i]) for i in range(len(od_data['led']))]

            ax[j//4, (j%4)].errorbar(x, median, yerr=std, fmt='o', capsize=2, label=f'{a}%', markersize=4)
        
        ax[j//4, (j%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax[j//4, (j%4)].set(title=f'SS{j+1}', xlabel='PWM LED (%)', ylabel='Leitura AD (16 bits)')
        ax[j//4, (j%4)].legend(title='Rotação:')

    for i in range(od_data['n']):
        fig, ax = plt.subplots(2, 4)
        fig.set_figwidth(16)
        fig.set_figheight(8)

        plt.suptitle("Variação da medida de OD Agitação - LED {:.1f}%, eVOLVER{}".format(100*od_data['led'][i]/4095, evolver))

        for j in range(8):
            median = [np.median(od_data[f'SS{j+1}'][f'{a}'][i]) for a in agitas]
            std = [np.std(od_data[f'SS{j+1}'][f'{a}'][i]) for a in agitas]
            
            ax[j//4, (j%4)].errorbar(median, agitas, xerr=std, fmt='none', capsize=2, color='k')
            ax[j//4, (j%4)].plot(median, agitas, 'o', color='k')
            ax[j//4, (j%4)].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            ax[j//4, (j%4)].set(title=f'SS{j+1}', ylabel='Rotação (deg)', xlabel='Leitura AD (16 bits)')
            for k,a in enumerate(agitas):
                ax[j//4, (j%4)].plot(od_data[f'SS{j+1}'][f'{a}'][i], [a]*5, 'o', markersize=3.5, alpha=0.6)
        
        plt.subplots_adjust(left=0.086, bottom=0.083, right=0.962, top=0.912, wspace=0.3, hspace=0.248)
        plt.show()



# CALIBRAÇÃO
def data_od(n, evolver, led):
    with open('logs/od-curves/EVOLVER-{}/Amostras-{}/json/cal_od_{}.json'.format(evolver,n,led), "r") as file:
        data = json.load(file)
    
    return data


def graficos_od(n, evolver, leds):
    data = [data_od(n, evolver, led) for led in leds]

    param = {}
    for i in range(8):
        param[f'SS{i+1}'] = {}

        for led in leds:
            param[f'SS{i+1}'][f'{led}'] = {
                'min_ad': 0,
                'max_od': 0,
                'r_sq': 0,
                'rms': 0
            }


    fig, ax = plt.subplots(2, 4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Fit sigmoide de calibração para OD_600 - eVOLVER{}".format(evolver))

    for i in range(8):
        for j in range(len(leds)):
        
            x = [[i]*5 for i in data[j]['measuredData']]
            linspace = np.linspace(0, max(data[j]['measuredData']), 500)
            median = [np.median(data[j]['raw'][i][k]) for k in range(len(data[j]['measuredData']))]
            std = [np.std(data[j]['raw'][i][k]) for k in range(len(data[j]['measuredData']))]

            plot = sigmoid(linspace, *data[j]['fits'][i])
            deriv = d_sigmoid(np.array(data[j]['measuredData']), *data[j]['fits'][i])
            fit = sigmoid(np.array(data[j]['measuredData']), *data[j]['fits'][i])

            condition = [-1*deriv[k] > std[k] for k in range(len(data[j]['measuredData']))]
            aux = condition.index(False) - 1 if False in condition else len(data[j]['measuredData'])-1
            min_ad = max(median[aux], data[j]['fits'][i][0])
            max_od = ad_od135(np.array([math.ceil(min_ad)]), *data[j]['fits'][i])[0]
      
            residual = median - fit
            rms = np.sqrt(np.mean(np.square(residual)))
            sum_sq_res = sum(np.square(residual))
            total_sum_sq = sum(np.square(median - np.mean(median)))
            r_sq = 1 - sum_sq_res/total_sum_sq
        
            ax[i//4, (i%4)].plot(x, data[j]['raw'][i], 'o', markersize=3.5, color='black', alpha=0.6)
            ax[i//4, (i%4)].plot(data[j]['measuredData'], median, 'o', markersize=2, color='yellow')
            #ax[i//4, (i%4)].errorbar(data[j]['measuredData'], median, yerr=std, fmt='none', capsize=2, color='red')
            ax[i//4, (i%4)].plot(linspace, plot, markersize = 1.5, label = "{:.0f}%: Máx OD {:.2f}\nRMS: {} | R²: {:.5f}".format(100*leds[j]/4095, max_od, math.ceil(rms), r_sq))

            ax[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax[i//4, (i%4)].set(title=f'SS{i+1}', xlabel='OD600', ylabel='Leitura AD do sensor PT (16 bits)')
            ax[i//4, (i%4)].legend(loc='best', fontsize=9)

            print('SS{} -> LED {:.0f}%'.format(i+1, 100*leds[j]/4095))
            for k in range(len(data[j]['measuredData'])):
                print("OD {:.2f} | d: {:.2e} | std_dev: {:.2e} | OK: {}".format(data[j]['measuredData'][k], -1*deriv[k], std[k], condition[k]))
            print()

            param[f'SS{i+1}'][f'{leds[j]}']['min_ad'] = min_ad
            param[f'SS{i+1}'][f'{leds[j]}']['max_od'] = max_od
            param[f'SS{i+1}'][f'{leds[j]}']['rms'] = rms
            param[f'SS{i+1}'][f'{leds[j]}']['r_sq'] = r_sq
         
    plt.subplots_adjust(left=0.083, bottom=0.074, right=0.964, top=0.914, wspace=0.188, hspace=0.252)
    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Amostras-{n}/Gráficos/Plot.png')
    plt.show()

    json_object = json.dumps(param, indent=len(param.keys()))

    with open(f"logs/od-curves/EVOLVER-{evolver}/Amostras-{n}/json/param.json", "w") as file:
        file.write(json_object)


def graficos_od_og():
    with open('Calibração Original/calibrations.json', "r") as file:
        raw_data = json.load(file)

    data = {
        'measuredData': raw_data[2]['measuredData'][0],
        'raw': raw_data[2]['raw'][1]['vialData'],
        'fits': raw_data[2]['fits'][2]['coefficients']
    }

    fig, ax = plt.subplots(4, 4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Fit sigmoide de calibração para OD_600 - ORIGINAL FynchBio")

    for i in range(16):
        x = [[i]*3 for i in data['measuredData']]
        linspace = np.linspace(0, max(data['measuredData']), 500)
        median = [np.median(data['raw'][i][k]) for k in range(len(data['measuredData']))]
        std = [np.std(data['raw'][i][k]) for k in range(len(data['measuredData']))]

        plot = sigmoid(linspace, *data['fits'][i])
        fit = sigmoid(np.array(data['measuredData']), *data['fits'][i])

        
        ax[i//4, (i%4)].plot(x, data['raw'][i], 'o', markersize=3.5, color='black', alpha=0.6)
        ax[i//4, (i%4)].plot(data['measuredData'], median, 'o', markersize=2, color='yellow')
        #ax[i//4, (i%4)].errorbar(data[j]['measuredData'], median, yerr=std, fmt='none', capsize=2, color='red')
        ax[i//4, (i%4)].plot(linspace, plot, markersize = 1.5)

        if i%4 == 0:
            ax[i//4, (i%4)].set_ylabel('Leitura AD (16 bits)', fontsize=9)

        if i//4 == 3:
            ax[i//4, (i%4)].set_xlabel('OD_600', fontsize=9)

        ax[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax[i//4, (i%4)].set(title=f'SS{i+1}')

         
    plt.subplots_adjust(left=0.083, bottom=0.074, right=0.964, top=0.914, wspace=0.288, hspace=0.46)
    plt.show()

    '''
    with open('Calibração Original/calibration_fynch.json', "r") as file:
        raw_data = json.load(file)
    
    fig, ax = plt.subplots(4, 4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Fit sigmoide de calibração para OD_600 - ORIGINAL FynchBio (Calibração)")

    for n in range(16):
        median = [np.median(raw_data['vialData'][n][i]) for i in range(len(raw_data['inputData']))]
        std = [np.std(raw_data['vialData'][n][i]) for i in range(len(raw_data['inputData']))]

        param, cov = curve_fit(sigmoid, raw_data['inputData'], median, p0=[62721, 62721, 0, -1], maxfev=1000000000, sigma=std)
        x = [[i]*3 for i in raw_data['inputData']]
        linspace = np.linspace(0, max(raw_data['inputData']), 500)

        plot = sigmoid(linspace, *param)
        fit = sigmoid(np.array(raw_data['inputData']), *param)

        ax[n//4, (n%4)].plot(x, raw_data['vialData'][n], 'o', markersize=3.5, color='black', alpha=0.6)
        ax[n//4, (n%4)].plot(raw_data['inputData'], median, 'o', markersize=2, color='yellow')
        #ax[i//4, (i%4)].errorbar(data[j]['measuredData'], median, yerr=std, fmt='none', capsize=2, color='red')
        ax[n//4, (n%4)].plot(linspace, plot, markersize = 1.5)

        if n%4 == 0:
            ax[n//4, (n%4)].set_ylabel('Leitura AD (16 bits)', fontsize=9)

        if i//4 == 3:
            ax[n//4, (n%4)].set_xlabel('OD_600', fontsize=9)

        ax[n//4, (n%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax[n//4, (n%4)].set(title=f'SS{n+1}')
    
    plt.subplots_adjust(left=0.083, bottom=0.074, right=0.964, top=0.914, wspace=0.288, hspace=0.46)
    plt.show()
    '''
    


# REPETIBILIDADE DE MEDIDAS SEM ALTERAÇÃO NENHUMA, SOMENTE RUÍDO
def data_repetibilidade(logs, active_ss):
    od_data = {}

    od_data['led'] = {
        'ad': [float(value) for value in graph_data(logs[0], 'organized_od')['led']],
        'int_rad': []
    }

    od_data['led']['int_rad'] = ad_od_led(od_data['led']['ad'])

    od_data['avg'] = {}
    od_data['max'] = {}
    od_data['min'] = {}
    od_data['dif'] = {}
    od_data['var'] = {}
    od_data['std'] = {}

    for ss in active_ss:
        od_data[f'SS{ss}'] = {
            'avg': [],
            'max': [],
            'min': [],
            'incerteza': [],
            'median': [],
            'std': []
        }

        for i in range(len(logs)):
            od_data[f'SS{ss}'][f'log{i}'] = []


    for n,log in enumerate(logs):
        od_raw_data = graph_data(log, 'organized_od')

        for ss in active_ss:
            od_data[f'SS{ss}'][f'log{n}'] = [float(value) for value in od_raw_data[f'SS{ss}']]
    
    for ss in active_ss:
        for point in range(len(od_data['led']['ad'])):
            point_aux = [od_data[f'SS{ss}'][f'log{i}'][point] for i in range(len(logs))]
            
            od_data[f'SS{ss}']['avg'] += [statistics.fmean(point_aux)]
            od_data[f'SS{ss}']['max'] += [max(point_aux)]
            od_data[f'SS{ss}']['min']+= [min(point_aux)]
            od_data[f'SS{ss}']['median'] += [np.median(point_aux)]
            od_data[f'SS{ss}']['std'] += [np.std(point_aux)]
            od_data[f'SS{ss}']['incerteza'] += [math.sqrt((np.std(point_aux) / math.sqrt(len(logs)))**2 + (1)**2)]

    return od_data


def graficos_repetibilidade(pts, evolver, active_ss):
    logs = logs_repetibilidade[f'{evolver}'][f'{pts}']
    ods = data_repetibilidade(logs, active_ss)

    figure, ax = plt.subplots(2,4)
    figure.set_figwidth(16)
    figure.set_figheight(8)

    figure.suptitle(f'Log de OD: Repetibilidade - eVOLVER {evolver}')

    for ss in active_ss:
        k = ss-1

        ax[k//4, (k%4)].plot(ods['led']['int_rad'], ods[f'SS{ss}']['max'], linestyle='--', color='black', alpha=0.7, lw=1)
        ax[k//4, (k%4)].plot(ods['led']['int_rad'], ods[f'SS{ss}']['min'], linestyle='--', color='black', alpha=0.7, lw=1)
        ax[k//4, (k%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        for i in range(len(logs)):
            ax[k//4, (k%4)].scatter(ods['led']['int_rad'], ods[f'SS{ss}'][f'log{i}'], s=10, alpha=1, label=f'Log {i+1}') # ({logs[i].split("/")[-1].split("_")[1]})')

        ax[k//4, (k%4)].legend(title="Teste de nº:", ncol=2, loc='best', fontsize='8')
        ax[k//4, (k%4)].set(title=f'SS{ss}', xlabel='Intensidade LED (mW/sr)', ylabel='Leitura AD do PT (16 bits)')

    plt.subplots_adjust(left=0.055, bottom=0.083, right=0.97, top=0.921, hspace=0.276)
    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Repetibilidade/Gráficos/{pts}pontos-PorSS.png')
    plt.show()

    #
    figure, ax = plt.subplots(2,4)
    figure.set_figwidth(16)
    figure.set_figheight(8)

    figure.suptitle(f'Log de OD: Repetibilidade, valores medianos - eVOLVER {evolver}')
    
    for ss in active_ss:
        k=ss-1 
        erro = [ods[f'SS{ss}']['std'],ods[f'SS{ss}']['std']]

        ax[k//4, (k%4)].plot(ods['led']['int_rad'], ods[f'SS{ss}']['median'], color='black', alpha=0.7, linestyle='--', lw=1, label='Média')
        ax[k//4, (k%4)].errorbar(ods['led']['int_rad'], ods[f'SS{ss}']['median'], xerr=None, yerr=erro, markeredgecolor='red', markerfacecolor='red', markersize=4,fmt='o', elinewidth=2, capsize=3, color='black', alpha=1, lw=1, label='Incerteza')
        ax[k//4, (k%4)].legend(loc='best')

        ax[k//4, (k%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax[k//4, (k%4)].set(title=f'SS{ss}', xlabel='Intensidade LED (mW/sr)', ylabel='Leitura AD do PT (16 bits)')

    plt.subplots_adjust(hspace=0.293)
    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Repetibilidade/Gráficos/{pts}pontos-Mediana-PorSS.png')
    plt.show()

    #
    figure = plt.figure()
    figure.set_figwidth(12)
    figure.set_figheight(7)
    
    for ss in active_ss:
        plt.plot(ods['led']['int_rad'], ods[f'SS{ss}']['incerteza'], label='SS{}'.format(ss))
    
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.title('Log de OD: Incerteza nas Smart Sleeves do eVOLVER {}'.format(evolver))
    plt.xlabel('Intensidade LED (mW/sr)')
    plt.ylabel('Leitura AD do PT (16 bits)')

    plt.legend(loc='best', title='Incerteza das SSs:')
    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Repetibilidade/Gráficos/{pts}pontos-Incertezas.png')
    plt.show()

    

# EFEITO DO USO DAS TAMPAS            
def graficos_tampas(logs, evolver, active_ss):
    raw_sem = graph_data(logs['sem'], 'organized_od')
    raw_com = graph_data(logs['com'], 'organized_od')

    sem = {
        'date': logs['sem'].split('/')[-1],
        'avg': [],
        'erro': [[],[]],
        'led': ad_od_led([float(value) for value in raw_sem['led']])
    }

    com = {
        'date': logs['com'].split('/')[-1],
        'avg': [],
        'erro': [[],[]],
        'led': ad_od_led([float(value) for value in raw_com['led']])
    }

    for ss in active_ss:
        sem[f'SS{ss}'] = [float(value) for value in raw_sem[f'SS{ss}']]
        com[f'SS{ss}'] = [float(value) for value in raw_com[f'SS{ss}']]

    for point in range(len(sem['led'])):
        sem['avg'] += [statistics.fmean([sem[f'SS{ss}'][point] for ss in active_ss])]
        sem['erro'][0] += [statistics.stdev([sem[f'SS{ss}'][point] for ss in active_ss])/math.sqrt(len(active_ss))]
    
    for point in range(len(com['led'])):
        com['avg'] += [statistics.fmean([com[f'SS{ss}'][point] for ss in active_ss])]
        com['erro'][0] += [statistics.stdev([com[f'SS{ss}'][point] for ss in active_ss])/math.sqrt(len(active_ss))]

    sem['erro'][1] = sem['erro'][0]    
    com['erro'][1] = com['erro'][0]
    
    #
    figure, axs = plt.subplots(1,2)
    figure.set_figwidth(15)
    figure.set_figheight(7)

    plt.suptitle('Log de OD: eVOLVER {}'.format(evolver))

    for ss in active_ss:
        axs[0].plot(sem['led'], sem[f'SS{ss}'], label=f'SS{ss}')
        axs[1].plot(com['led'], com[f'SS{ss}'], label=f'SS{ss}')

    axs[0].set(title='Sem Tampas - {}'.format(sem['date']))
    axs[1].set(title='Com Tampas - {}'.format(com['date']))
    
    for ax in axs.flat:
        ax.set(xlabel='Intensidade LED (mW/sr)', ylabel='Leitura AD do PT (16 bits)')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.legend()

    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Tampa/Gráficos/TodasSS.png')
    plt.show()

    #
    figure = plt.figure()
    figure.set_figwidth(12)
    figure.set_figheight(7)

    plt.title('Log de OD: Média das 8 Smart Sleeves - eVOLVER {}'.format(evolver))

    plt.errorbar(sem['led'], sem['avg'], xerr=None, yerr=sem['erro'], fmt='o', markersize=4, capsize=3, label='Sem tampa ({}/{} as {})\nIncerteza média: {:.0f}'.format(sem['date'].split('_')[1].split('-')[0], sem['date'].split('_')[1].split('-')[1], sem['date'].split('_')[2], statistics.fmean(sem['erro'][0])))
    plt.errorbar(com['led'], com['avg'], xerr=None, yerr=com['erro'], fmt='o', markersize=4, capsize=3, label='Com tampas ({}/{} as {})\nIncerteza média: {:.0f}'.format(com['date'].split('_')[1].split('-')[0], com['date'].split('_')[1].split('-')[1], com['date'].split('_')[2], statistics.fmean(com['erro'][0])))
    
    plt.xlabel('Intensidade LED (mW/sr)')
    plt.ylabel('Leitura AD do PT (16 bits)')
    plt.legend(loc='best')

    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Tampa/Gráficos/Média.png')
    plt.show()

    

# EFEITO DO VOLUME NO OD
def od_monitor_grafico(evolver, logs):
    ml = [7,8,9,10,11,21]
    od_data = []

    for k,log in enumerate(logs):
        od_data += [graph_data(log, 'organized_od')]

        for key in od_data[k]:
            for i in range(len(od_data[k][key])):
                od_data[k][key][i] = float(od_data[k][key][i])

            od_data[k][key] = od_data[k][key]

    #
    figure,ax = plt.subplots(2,3,sharey=True)
    figure.set_figwidth(16)
    figure.set_figheight(10)

    figure.suptitle(f'Medindo volume mínimo para leitura de OD_600, com agitação de 50% - eVOLVER {evolver}')

    for i in range(len(logs)):
        for j in range(8):
            ax[i//3, (i%3)].plot(od_data[i]['time'], od_data[i][f'SS{j+1}'], label=f'SS{j+1}')
            ax[i//3, (i%3)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax[i//3, (i%3)].set(title=f'{ml[i]} mL de líquido', xlabel='Tempo decorrido (s)', ylabel='Leitura AD do PT (16 bits)')
            ax[i//3, (i%3)].legend(fontsize="8",loc='best')
    
    plt.subplots_adjust(bottom=0.09, top=0.91, right=0.93, hspace=0.36)
    plt.savefig('logs/od-curves/EVOLVER-2/VolumeMin//Gráficos/PorVolume.png')
    plt.show()

    #
    figure,ax = plt.subplots(2,4, sharey=True)
    figure.set_figwidth(16)
    figure.set_figheight(10)

    figure.suptitle(f'Medindo volume mínimo para leitura de OD_600, com agitação de 50%, para cada SS - eVOLVER {evolver}')

    for i in range(8):
        for j in range(len(ml)):
            ax[i//4, (i%4)].plot(od_data[j]['time'], od_data[j][f'SS{i+1}'], label=f'{ml[j]} mL') #: incerteza ±{:.0f}'.format(ml[j], math.sqrt((np.std(od_data[j][f"SS{i+1}"])/len(logs[j]))**2 + (1)**2)))
            ax[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax[i//4, (i%4)].set(title=f'SS{i+1}', xlabel='Tempo decorrido (s)', ylabel='Leitura AD do PT (16 bits)')
            ax[i//4, (i%4)].legend(fontsize="8",loc='best')
    
    plt.subplots_adjust(bottom=0.08, top=0.9, left=0.07, right=0.97, hspace=0.3)
    plt.savefig('logs/od-curves/EVOLVER-2/VolumeMin/Gráficos/PorSS.png')
    plt.show()



if __name__ == "__main__":
    # ROTAÇÃO
    ''' - VIAL VAZIO
        * 100k
    graph_angles(1,1)
    graph_revesa(1,1)
    graph_rot(1,1)
    '''
    ''' - VIAL COM 20 mL DE ÁGUA, 20% DE AGITAÇÃO, 0.1|10 NAS BOMBAS
        * 100k
    graph_angles(2,1)
    graph_revesa(2,1)
    graph_rot(2,1)
        * 1M
    graph_angles(3,1)
    graph_revesa(3,1)
    graph_rot(3,1)
    '''
    
    #graph_pump(2,1)
    #graphs_rot_subs(1,2,1)
    #teste_influence_subs(2,1,2,1,[410,819,1228,1638,2048,2457,2866,3276,3686,4095])
    #graphs_rot_r(2,3,1)
    #influ_agita(1)
    

    # CALIBRAÇÃO
    ''' 
    graficos_od_og()

    graficos_od(1, 1,[1024,1556,2048,2580,3071,4095])
    graficos_od(2, 1,[1024,1556,2048,2580,3071,4095])

    graficos_od(1, 2,[1024,2048,3072,4095])
    graficos_od(2, 2,[1024,2048,3072])
    graficos_od(3, 2,[1024,2048,3072])
    '''

    # REPETIBILIDADE
    '''
    graficos_repetibilidade(10, 2, [1,2,3,4,5,6,7,8])
    graficos_repetibilidade(100, 2, [1,2,3,4,5,6,7,8])
    graficos_repetibilidade(100, 1, [1,2,3,4,5,6,7,8])
    '''

    #graficos_tampas(logs_tampas, 2, [1,2,3,4,5,6,7,8])
    #od_monitor_grafico(2, logs_vol)