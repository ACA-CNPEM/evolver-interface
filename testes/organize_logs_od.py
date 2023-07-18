import matplotlib.pyplot as plt
from organize_logs import graph_data
from utils import *
import statistics
from scipy.optimize import curve_fit
import json

logs_repetibilidade = [
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
]

logs_repetibilidade_100 = [
    [
        'logs/od-curves/EVOLVER-2/Repetibilidade/log_14-06-23_13:21:39',
        'logs/od-curves/EVOLVER-2/Repetibilidade/log_16-06-23_14:33:37',
        'logs/od-curves/EVOLVER-2/Repetibilidade/log_19-06-23_08:24:04'
    ],
    [
        'logs/od-curves/EVOLVER-1/Repetibilidade/log_16-06-23_14:37:47',
        'logs/od-curves/EVOLVER-1/Repetibilidade/log_19-06-23_08:24:59',
        'logs/od-curves/EVOLVER-1/Repetibilidade/log_19-06-23_09:16:49',
        'logs/od-curves/EVOLVER-1/Repetibilidade/log_20-06-23_11:16:05',
        'logs/od-curves/EVOLVER-1/Repetibilidade/log_20-06-23_11:42:40',
        'logs/od-curves/EVOLVER-1/Repetibilidade/log_20-06-23_13:17:10'
    ]
]

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


def data_od(n, evolver, led):
    with open('logs/od-curves/EVOLVER-{}/Amostras-{}/json/cal_od_{}.json'.format(evolver,n,led), "r") as file:
        data = json.load(file)
    
    return data


def graficos_od(n, evolver, leds):
    data = [data_od(n, evolver, led) for led in leds]

    fig, ax = plt.subplots(2, 4, sharey=True)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Fit sigmoide de calibração para OD_600 - eVOLVER{}".format(evolver))

    for i in range(8):
        for j in range(len(leds)):

            x = [[i]*5 for i in data[j]['measuredData']]
            linspace = np.linspace(0, max(data[j]['measuredData']), 500)
            median = [np.median(data[j]['raw'][i][k]) for k in range(len(data[j]['measuredData']))]

            ax[i//4, (i%4)].plot(x, data[j]['raw'][i], 'o', markersize=3.5, color='black', alpha=0.6)
            ax[i//4, (i%4)].plot(data[j]['measuredData'], median, 'o', markersize=2, color='yellow')
            #ax[i//4, (i%4)].errorbar(data[j]['measuredData'], median, yerr=std, fmt='none', capsize=2, color='red')
            ax[i//4, (i%4)].plot(linspace, sigmoid(linspace, *data[j]['fits'][i]), markersize = 1.5, label = f"{round(100*leds[j]/4095)}%")
            
            ax[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax[i//4, (i%4)].set(title=f'SS{i+1}', xlabel='OD600', ylabel='Leitura AD do sensor PT (16 bits)')
            ax[i//4, (i%4)].legend(title='LED emitindo:', loc='best', fontsize=8)
    
    plt.subplots_adjust(left=0.083, bottom=0.074, right=0.964, top=0.914, wspace=0.188, hspace=0.252)
    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Amostras-{n}/Gráficos/Plot.png')
    plt.show()
    

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


def graficos_od_2(evolver, active_ss):
    ods = data_od_2(active_ss)
    date = '30-06-23'
    
    #
    figure, axs = plt.subplots(2,4)
    figure.set_figwidth(16)
    figure.set_figheight(8)

    for i in range(8):
        for value in ods['od']:
            aux = [statistics.fmean(ods[f'SS{i+1}']['{:.2f}'.format(value)][j]) for j in range(ods['n'])]
            axs[i//4, (i%4)].plot(ods['led']['int_rad'], aux, label='{:.2f}'.format(value))
        
        axs[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        axs[i//4, (i%4)].set(title=f'SS{i+1} | {date}', xlabel='Intensidade LED (mW/sr)', ylabel='Leitura AD do PT (16 bits)')
        axs[i//4, (i%4)].legend(title='OD_600:', loc='best', fontsize="8")

    figure.suptitle(f'Log de OD - eVOLVER {evolver}\nTensão média medida no PT em função da intensidade de radiação emitida pelo LED\n')
    plt.subplots_adjust(left=0.074, bottom=0.086, right=0.94, top=0.88, wspace=0.212, hspace=0.31)

    plt.savefig(f'logs/od-curves/EVOLVER-2/Amostras/Gráficos/PTxLEDxOD-PorSS.png')
    plt.show()

    #
    coefficients = [[] for ss in active_ss]
    coef_cov = [[] for ss in active_ss]
    chisq = []
    vial_data = [[] for ss in active_ss]
    
    median = [[] for ss in active_ss]
    std = [[] for ss in active_ss]
    
    for ss in active_ss:
        '''figure, ax = plt.subplots(2,2)
        figure.set_figwidth(16)
        figure.set_figheight(8)

        figure.suptitle(f'Log de OD600 para SS{ss}, eVOLVER {evolver} | {date}\nFit sigmoide para medidas de OD_600, para diferentes emissões do LED')
        '''
        for i in range(4):
            vial_data[ss-1] += [[ods[f'SS{ss}']['{:.2f}'.format(j)][i] for j in ods['od']]]
            #vial_data[ss-1][i] += [ods['10mL'][f'SS{ss}']['{:.2f}'.format(j)][i] for j in ods['od']]

        aux_ods = [k for k in ods['od']]

        for k in ods['od']:
            aux_ods += [k]

        for i,vial in enumerate(vial_data[ss-1]):
            median[ss-1] += [[np.median(data) for data in vial]]
            median[ss-1][i] += [np.median(data) for data in vial]

            std[ss-1] += [[np.std(data) for data in vial]]
            std[ss-1][i] += [np.std(data) for data in vial]

            param, cov = curve_fit(sigmoid, aux_ods, median[ss-1][i], p0=[62721, 62721, 0, -1], maxfev=1000000000, sigma=std[ss-1][i], absolute_sigma=True)
            '''print(a)
            param = a[0]
            cov = a[1]'''
            coefficients[ss-1].append(np.array(param).tolist())
            coef_cov[ss-1].append(np.array(cov).tolist())

        linear_space = np.linspace(0, max(ods['od']), 500)

        '''
        for i,led in enumerate([25,50,75,100]):
            ax[i//2, (i%2)].plot(aux_ods, median[ss-1][i], 'o', markersize=3, color='black')
            ax[i//2, (i%2)].errorbar(aux_ods, median[ss-1][i], yerr=std[ss-1][i], fmt='none', capsize=2, color='red')
            ax[i//2, (i%2)].plot(linear_space, sigmoid(linear_space, *coefficients[ss-1][i]), markersize = 1.5, label = None)
            ax[i//2, (i%2)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

            ax[i//2, (i%2)].set(xlabel='OD_600',ylabel='Leitura AD do PT (16 bits)', title='Fit para LED emitindo {}%'.format(led))

        plt.subplots_adjust(left=0.1, bottom=0.09, right=0.94, top=0.88, wspace=0.24, hspace=0.275)
        plt.savefig(f'logs/od-curves/EVOLVER-2/Amostras/Gráficos/Fit-SS{ss}.png')
        plt.show()
        '''

    #
    fig, ax = plt.subplots(2,4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Fit sigmoide para OD_600 - eVOLVER{}\nLED em 100%".format(evolver, ods['led']['int_rad'][3]))

    for i in range(8):
        for k,v in enumerate([25,50,75,100]):
            calc_values = sigmoid(np.array(aux_ods), *coefficients[i][k])
            chi = ((calc_values - median[i][k])**2) / median[i][k]

            ax[i//4, (i%4)].plot(aux_ods, median[i][k], 'o', markersize=3, color='black')
            ax[i//4, (i%4)].errorbar(aux_ods, median[i][k], yerr=std[i][k], fmt='none', capsize=2, color='red')
            ax[i//4, (i%4)].plot(linear_space, sigmoid(linear_space, *coefficients[i][k]), markersize = 1.5, label = '{}% -> chisq: {:.1e}'.format(v,sum(chi)))
            ax[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        ax[i//4, (i%4)].set(xlabel='OD_600',ylabel='Leitura AD do PT (16 bits)', title='SS{}'.format(i+1))
        ax[i//4, (i%4)].legend(title='LED')

    plt.subplots_adjust(left=0.1, bottom=0.09, right=0.94, top=0.88, wspace=0.3, hspace=0.3)
    plt.savefig(f'logs/od-curves/EVOLVER-2/Amostras/Gráficos/FitLED100%-PorSS.png')
    plt.show()


def graficos_od_3(evolver, active_ss):
    ods = data_od_3(active_ss)
    date = '11-07-23'
    
    #
    figure, axs = plt.subplots(2,4, sharey=True)
    figure.set_figwidth(16)
    figure.set_figheight(8)

    for i in range(8):
        for value in ods['od']:
            aux = [statistics.fmean(ods[f'SS{i+1}']['{:.2f}'.format(value)][j]) for j in range(ods['n'])]
            axs[i//4, (i%4)].plot(ods['led']['int_rad'], aux, label='{:.2f}'.format(value))
        
        axs[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        axs[i//4, (i%4)].set(title=f'SS{i+1} | {date}', xlabel='Intensidade LED (mW/sr)', ylabel='Leitura AD do PT (16 bits)')
        axs[i//4, (i%4)].legend(title='OD_600:', loc='best', fontsize="8")

    figure.suptitle(f'Log de OD - eVOLVER {evolver}\nTensão média medida no PT em função da intensidade de radiação emitida pelo LED\n')
    plt.subplots_adjust(left=0.074, bottom=0.086, right=0.94, top=0.88, wspace=0.212, hspace=0.31)

    plt.savefig(f'logs/od-curves/EVOLVER-2/Amostras-2/Gráficos/PTxLEDxOD-PorSS.png')
    plt.show()

    #
    coefficients = [[] for ss in active_ss]
    coef_cov = [[] for ss in active_ss]
    vial_data = [[] for ss in active_ss]
    
    median = [[] for ss in active_ss]
    std = [[] for ss in active_ss]
    
    for ss in active_ss:
        '''figure, ax = plt.subplots(1,3)
        figure.set_figwidth(16)
        figure.set_figheight(8)

        figure.suptitle(f'Log de OD600 para SS{ss}, eVOLVER {evolver} | {date}\nFit sigmoide para medidas de OD_600, para diferentes emissões do LED')
        '''
        for i in range(ods['n']):
            vial_data[ss-1] += [[ods[f'SS{ss}']['{:.2f}'.format(j)][i] for j in ods['od']]]

        for i,vial in enumerate(vial_data[ss-1]):
            median[ss-1] += [[np.median(data) for data in vial]]

            std[ss-1] += [[np.std(data) for data in vial]]

            param, cov = curve_fit(sigmoid, ods['od'], median[ss-1][i], p0=[62721, 62721, 0, -1], maxfev=1000000000)
            coefficients[ss-1].append(np.array(param).tolist())
            coef_cov[ss-1].append(np.array(cov).tolist())

        linear_space = np.linspace(0, max(ods['od']), 500)
        
        '''for i,led in enumerate([25,50,75]):
            ax[i].plot(ods['od'], median[ss-1][i], 'o', markersize=3, color='black')
            ax[i].errorbar(ods['od'], median[ss-1][i], yerr=std[ss-1][i], fmt='none', capsize=2, color='red')
            ax[i].plot(linear_space, sigmoid(linear_space, *coefficients[ss-1][i]), markersize = 1.5, label = None)
            ax[i].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

            ax[i].set(xlabel='OD_600',ylabel='Leitura AD do PT (16 bits)', title='Fit para LED emitindo {}%'.format(led))

        plt.subplots_adjust(left=0.1, bottom=0.09, right=0.94, top=0.88, wspace=0.24, hspace=0.275)
        plt.savefig(f'logs/od-curves/EVOLVER-2/Amostras/Gráficos/Fit-SS{ss}.png')
        plt.show()'''
        

    #
    fig, ax = plt.subplots(2,4, sharey=True)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    plt.suptitle("Fit sigmoide para OD_600 - eVOLVER{}".format(evolver)) #, ods['led']['int_rad'][3]))

    for i in range(8): #[-1] = led em 100%
        for k,led in enumerate([25,50,75]):
            ax[i//4, (i%4)].plot(ods['od'], median[i][k], 'o', markersize=3, color='black')
            ax[i//4, (i%4)].errorbar(ods['od'], median[i][k], yerr=std[i][k], fmt='none', capsize=2, color='red')
            ax[i//4, (i%4)].plot(linear_space, sigmoid(linear_space, *coefficients[i][k]), markersize = 1.5, label = "{}%".format(led))
            ax[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        ax[i//4, (i%4)].set(xlabel='OD_600',ylabel='Leitura AD do PT (16 bits)', title='SS{}'.format(i+1))
        ax[i//4, (i%4)].legend(title="LED:")

    plt.subplots_adjust(left=0.1, bottom=0.09, right=0.94, top=0.88, wspace=0.3, hspace=0.3)
    plt.savefig(f'logs/od-curves/EVOLVER-2/Amostras-2/Gráficos/FitLED100%-PorSS.png')
    plt.show()

    for i in range(8):
        print(f'SS{i+1}')
        for l in range(ods['n']):
            print(coefficients[i][l])


def graficos_repetibilidade(logs, pts, evolver, active_ss):
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


def analise(logs_od, logs_rep, evolver, active_ss):
    ods = data_od_1(logs_od[0], active_ss)
    rep = data_repetibilidade(logs_rep, active_ss)
    
    '''
    for ss in active_ss:
        erro = [math.sqrt(rep['std'][f'SS{ss}'][i]/math.sqrt(len(logs_rep))**2 + (3.3/4095.0)**2) for i in range(len(rep['led']))]
        
        for k,par in enumerate([[5,4], [4,3], [3,2], [2,1], [1,0]]):
            var_v = [ods[f'SS{ss}']['v'][par[0]][v] - ods[f'SS{ss}']['v'][par[1]][v] for v in range(len(ods['led']['v']))]
            #var_v = [-1*v if v < 0 else v for v in var]
            status = [var_v[i] >= erro[i] for i in range(len(ods['led']['int_rad']))]
            
            figure = plt.figure()
            figure.set_figwidth(20)
            figure.set_figheight(10)

            plt.title(f'SS{ss}, eVOLVER {evolver}\nRegião em que consigo medir OD_600 entre {ods["od"][par[0]]} e {ods["od"][par[1]]} (em verde)')

            plt.plot(ods['led']['int_rad'], var_v, lw=2, label='Variação de Tensão para valores de OD no range')
            plt.plot(ods['led']['int_rad'], erro, lw=2, label='Incerteza da Medida')


            plt.fill_between(ods['led']['int_rad'], erro, var_v, where=status, facecolor='green', alpha=0.5, interpolate=True)

            plt.legend(title='Range de OD_600:')
            plt.xlabel('Intensidade LED (mW/sr)')
            plt.ylabel('Precisão')

            plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Amostras/Gráficos/Incertezas-SS{ss}-Range{k}.png')
            plt.show()

    
    for ss in active_ss:
        figure, axs = plt.subplots(2,2)
        figure.set_figwidth(20)
        figure.set_figheight(10)

        plt.subplots_adjust(left=0.08, bottom=0.07, right=0.97, top=0.93, wspace=0.15, hspace=0.23)

        figure.suptitle('SS{}, eVOLVER {}'.format(ss, evolver))
        for res in [[0.05, [0,0]], [0.08, [0,1]], [0.1, [1,0]], [0.2, [1,1]]]:
            
            erro = [math.sqrt(rep['std'][f'SS{ss}'][i]/math.sqrt(len(logs_rep))**2 + (3.3/4095.0)**2) for i in range(len(rep['led']))]
            axs[res[1][0],res[1][1]].plot(rep['led'], erro, label='Incerteza')

            for par in [[5,4], [4,3], [3,2], [2,1], [1,0]]:
                divisor = (ods['od'][par[1]] - ods['od'][par[0]]) / res[0]

                var = [(ods[f'SS{ss}']['v'][par[0]][v] - ods[f'SS{ss}']['v'][par[1]][v])/divisor for v in range(len(ods['led']['v']))]
                axs[res[1][0],res[1][1]].plot(ods['led']['int_rad'], var, label='{:.2f} a {:.2f}'.format(ods['od'][par[0]], ods['od'][par[1]]))

            axs[res[1][0],res[1][1]].set(title='Precisão: {}'.format(res[0]), xlabel='Intensidade LED (mW/sr)', ylabel='Tensão (V)')
            axs[res[1][0],res[1][1]].legend(title='Range de OD_600:')
        
        plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Incertezas/Incertezas-SS{ss}.png')
        plt.show()
    '''
    
                
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

    #
    fig, ax = plt.subplots(2,4)
    fig.set_figwidth(16)
    fig.set_figheight(8)

    fig.suptitle('Log de OD: Efeito do uso de tampa para as 8 Smart Sleeves - eVOLVER {}'.format(evolver))
    
    for i in range(8):
        ax[i//4, (i%4)].plot(sem['led'], sem[f'SS{ss}'], label=f'Sem')
        ax[i//4, (i%4)].plot(com['led'], com[f'SS{ss}'], label=f'Com')

        ax[i//4, (i%4)].set(title=f'SS{i+1}', xlabel='Intensidade LED (mW/sr)', ylabel='Leitura AD do PT (16 bits)')
        ax[i//4, (i%4)].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax[i//4, (i%4)].legend()

    plt.subplots_adjust(left=0.09, right=0.93, wspace=0.23, hspace=0.35)
    plt.savefig(f'logs/od-curves/EVOLVER-{evolver}/Tampa/Gráficos/PorSS.png')
    plt.show()

    
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
    #graficos_tampas(logs_tampas, 2, [1,2,3,4,5,6,7,8])
    
    graficos_od(1, 1,[1024,1556,2048,2580,3071,4095])
    graficos_od(1, 2,[1024,2048,3072,4095])
    graficos_od(2, 2,[1024,2048,3072])

    #graficos_repetibilidade(logs_repetibilidade, 10, 2, [1,2,3,4,5,6,7,8])
    #graficos_repetibilidade(logs_repetibilidade_100[0], 100, 2, [1,2,3,4,5,6,7,8])
    #graficos_repetibilidade(logs_repetibilidade_100[1], 100, 1, [1,2,3,4,5,6,7,8])
    
    #analise(logs_od, logs_repetibilidade_100[1], 1, [1,2,3,4,5,6,7,8])
    #od_monitor_grafico(2, logs_vol)