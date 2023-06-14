import matplotlib.pyplot as plt
from organize_logs import graph_data
from utils import *

logs_od = ['logs/od-curves/EVOLVER-1/log_01-06-23_13:00:06','logs/od-curves/EVOLVER-1/log_01-06-23_13:20:16', 
        'logs/od-curves/EVOLVER-1/log_01-06-23_13:40:34', 'logs/od-curves/EVOLVER-1/log_01-06-23_14:01:05',
        'logs/od-curves/EVOLVER-1/log_01-06-23_14:21:46', 'logs/od-curves/EVOLVER-1/log_01-06-23_14:41:50',
        'logs/od-curves/EVOLVER-1/log_02-06-23_09:41:41', 'logs/od-curves/EVOLVER-1/log_02-06-23_10:02:48',
        'logs/od-curves/EVOLVER-1/log_02-06-23_10:24:45', 'logs/od-curves/EVOLVER-1/log_02-06-23_10:51:53', 
        'logs/od-curves/EVOLVER-1/log_02-06-23_11:23:06', 'logs/od-curves/EVOLVER-1/log_02-06-23_11:43:25',
        'logs/od-curves/EVOLVER-1/log_05-06-23_09:15:40', 'logs/od-curves/EVOLVER-1/log_05-06-23_09:40:32',
        'logs/od-curves/EVOLVER-1/log_05-06-23_10:01:54', 'logs/od-curves/EVOLVER-1/log_05-06-23_10:22:37', 
        'logs/od-curves/EVOLVER-1/log_05-06-23_10:48:00', 'logs/od-curves/EVOLVER-1/log_05-06-23_11:09:00']

logs_repetibilidade = ['logs/od-curves/EVOLVER-2/log_13-06-23_08:39:40', 
                       'logs/od-curves/EVOLVER-2/log_13-06-23_09:10:18', 
                       'logs/od-curves/EVOLVER-2/log_13-06-23_11:26:38',
                       'logs/od-curves/EVOLVER-2/log_13-06-23_12:28:03', 
                       'logs/od-curves/EVOLVER-2/log_14-06-23_09:01:19',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_09:20:53',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_09:32:05',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_09:36:53',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_09:50:28',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_09:54:22',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_10:02:54',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_10:55:03',
                       'logs/od-curves/EVOLVER-2/log_14-06-23_11:14:23']


def data_od(logs, active_ss):
    od_data = {
        'od': [2.0, 1.04, 0.75, 0.51, 0.22, 0.0],
        'led': {
            'ad': [],
            'v': [],
            'int_rad': []
        },
    }

    for ss in active_ss:
        od_data[f'SS{ss}'] = {
            'ad': [[] for value in od_data['od']],
            'v': [[] for value in od_data['od']],
            'i': [[] for value in od_data['od']]
        }
    

    # SS1 e 2
    od_raw_data_1 = graph_data(logs[0], 'organized_od')
    od_raw_data_2 = graph_data(logs[1], 'organized_od')
    od_raw_data_3 = graph_data(logs[2], 'organized_od')
    od_raw_data_4 = graph_data(logs[3], 'organized_od')
    od_raw_data_5 = graph_data(logs[4], 'organized_od')
    od_raw_data_6 = graph_data(logs[5], 'organized_od')

    n_point = len(od_raw_data_1['led'])

    for point in range(n_point):
        od_data['led']['ad'] += [float(od_raw_data_1['led'][point])]

        od_data['SS1']['ad'][0] += [float(od_raw_data_1['SS1'][point])]
        od_data['SS2']['ad'][1] += [float(od_raw_data_1['SS2'][point])]

        od_data['SS1']['ad'][1] += [float(od_raw_data_2['SS1'][point])]
        od_data['SS2']['ad'][0] += [float(od_raw_data_2['SS2'][point])]

        od_data['SS1']['ad'][2] += [float(od_raw_data_3['SS1'][point])]
        od_data['SS2']['ad'][3] += [float(od_raw_data_3['SS2'][point])]

        od_data['SS1']['ad'][3] += [float(od_raw_data_4['SS1'][point])]
        od_data['SS2']['ad'][2] += [float(od_raw_data_4['SS2'][point])]

        od_data['SS1']['ad'][4] += [float(od_raw_data_5['SS1'][point])]
        od_data['SS2']['ad'][5] += [float(od_raw_data_5['SS2'][point])]

        od_data['SS1']['ad'][5] += [float(od_raw_data_6['SS1'][point])]
        od_data['SS2']['ad'][4] += [float(od_raw_data_6['SS2'][point])]
        
    # SS3, 4 e 5
    od_raw_data_7 = graph_data(logs[6], 'organized_od')
    od_raw_data_8 = graph_data(logs[7], 'organized_od')
    od_raw_data_9 = graph_data(logs[8], 'organized_od')
    od_raw_data_10 = graph_data(logs[9], 'organized_od')
    od_raw_data_11 = graph_data(logs[10], 'organized_od')
    od_raw_data_12 = graph_data(logs[11], 'organized_od')

    for point in range(n_point):
        od_data['SS3']['ad'][0] += [float(od_raw_data_7['SS3'][point])]
        od_data['SS4']['ad'][1] += [float(od_raw_data_7['SS4'][point])]
        od_data['SS5']['ad'][2] += [float(od_raw_data_7['SS5'][point])]
    
        od_data['SS3']['ad'][2] += [float(od_raw_data_8['SS3'][point])]
        od_data['SS4']['ad'][0] += [float(od_raw_data_8['SS4'][point])]
        od_data['SS5']['ad'][1] += [float(od_raw_data_8['SS5'][point])]

        od_data['SS3']['ad'][1] += [float(od_raw_data_9['SS3'][point])]
        od_data['SS4']['ad'][2] += [float(od_raw_data_9['SS4'][point])]
        od_data['SS5']['ad'][0] += [float(od_raw_data_9['SS5'][point])]

        od_data['SS3']['ad'][3] += [float(od_raw_data_10['SS3'][point])]
        od_data['SS4']['ad'][4] += [float(od_raw_data_10['SS4'][point])]
        od_data['SS5']['ad'][5] += [float(od_raw_data_10['SS5'][point])]

        od_data['SS3']['ad'][4] += [float(od_raw_data_11['SS3'][point])]
        od_data['SS4']['ad'][5] += [float(od_raw_data_11['SS4'][point])]
        od_data['SS5']['ad'][3] += [float(od_raw_data_11['SS5'][point])]

        od_data['SS3']['ad'][5] += [float(od_raw_data_12['SS3'][point])]
        od_data['SS4']['ad'][3] += [float(od_raw_data_12['SS4'][point])]
        od_data['SS5']['ad'][4] += [float(od_raw_data_12['SS5'][point])]

    # SS6, 7 e 8
    od_raw_data_13 = graph_data(logs[12], 'organized_od')
    od_raw_data_14 = graph_data(logs[13], 'organized_od')
    od_raw_data_15 = graph_data(logs[14], 'organized_od')
    od_raw_data_16 = graph_data(logs[15], 'organized_od')
    od_raw_data_17 = graph_data(logs[16], 'organized_od')
    od_raw_data_18 = graph_data(logs[17], 'organized_od')

    for point in range(n_point):
        od_data['SS6']['ad'][0] += [float(od_raw_data_13['SS6'][point])]
        od_data['SS7']['ad'][1] += [float(od_raw_data_13['SS7'][point])]
        od_data['SS8']['ad'][2] += [float(od_raw_data_13['SS8'][point])]

        od_data['SS6']['ad'][1] += [float(od_raw_data_14['SS6'][point])]
        od_data['SS7']['ad'][2] += [float(od_raw_data_14['SS7'][point])]
        od_data['SS8']['ad'][0] += [float(od_raw_data_14['SS8'][point])]

        od_data['SS6']['ad'][2] += [float(od_raw_data_15['SS6'][point])]
        od_data['SS7']['ad'][0] += [float(od_raw_data_15['SS7'][point])]
        od_data['SS8']['ad'][1] += [float(od_raw_data_15['SS8'][point])]

        od_data['SS6']['ad'][3] += [float(od_raw_data_16['SS6'][point])]
        od_data['SS7']['ad'][4] += [float(od_raw_data_16['SS7'][point])]
        od_data['SS8']['ad'][5] += [float(od_raw_data_16['SS8'][point])]

        od_data['SS6']['ad'][4] += [float(od_raw_data_17['SS6'][point])]
        od_data['SS7']['ad'][5] += [float(od_raw_data_17['SS7'][point])]
        od_data['SS8']['ad'][3] += [float(od_raw_data_17['SS8'][point])]

        od_data['SS6']['ad'][5] += [float(od_raw_data_18['SS6'][point])]
        od_data['SS7']['ad'][3] += [float(od_raw_data_18['SS7'][point])]
        od_data['SS8']['ad'][4] += [float(od_raw_data_18['SS8'][point])]

    od_data['led']['int_rad'] = ad_od_led(od_data['led']['ad'])
    od_data['led']['v'] = [od_data['led']['ad'][i] * 3.3/4095 for i in range(n_point)]

    for ss in active_ss:
        for od in range(len(od_data['od'])):
            od_data[f'SS{ss}']['v'][od] = [od_data[f'SS{ss}']['ad'][od][i] * 3.3/65520 for i in range(n_point)]
            od_data[f'SS{ss}']['i'][od] = [(3.3 - od_data[f'SS{ss}']['v'][od][i])/100.082 for i in range(n_point)]

    return od_data


def data_repetibilidade(logs, active_ss):
    od_data = {}
    od_data['led'] = ad_od_led([float(value) for value in graph_data(logs[0], 'organized_od')['led']])
    od_data['avg'] = {}
    od_data['max'] = {}
    od_data['min'] = {}
    od_data['dif'] = {}

    for ss in active_ss:
        od_data[f'SS{ss}'] = [[] for i in range(len(logs))]
        od_data['avg'][f'SS{ss}'] = []
        od_data['max'][f'SS{ss}'] = []
        od_data['min'][f'SS{ss}'] = []
        od_data['dif'][f'SS{ss}'] = []

    for n,log in enumerate(logs):
        od_raw_data = graph_data(log, 'organized_od')

        for ss in active_ss:
            od_data[f'SS{ss}'][n] = [3.3*float(value)/65520 for value in od_raw_data[f'SS{ss}']]
    
    for ss in active_ss:
        for point in range(len(od_data[f'SS{ss}'][0])):
            point_aux = [od_data[f'SS{ss}'][i][point] for i in range(len(logs))]
            
            od_data['avg'][f'SS{ss}'] += [sum(point_aux)/len(logs)]
            od_data['max'][f'SS{ss}'] += [max(point_aux)]
            od_data['min'][f'SS{ss}'] += [min(point_aux)]
            od_data['dif'][f'SS{ss}'] += [od_data['max'][f'SS{ss}'][point] - od_data['min'][f'SS{ss}'][point]]

    return od_data

            

def graficos_od(logs, active_ss):
    ods = data_od(logs, active_ss)

    for ss in active_ss:
        if ss in[1,2]:
            date = '01-06-23'
        elif ss in [3,4,5]:
            date = '02-06-23'
        else:
            date = '05-06-23'
        
        # 
        figure = plt.figure()
        figure.set_figwidth(12)
        figure.set_figheight(7)

        for i,value in enumerate(ods['od']):
            plt.plot(ods['led']['int_rad'], ods[f'SS{ss}']['v'][i], label=f'{value}')

        plt.title(f'Log de OD - SS{ss} | {date}\nTensão medida no PT em função da intensidade de radiação emitida pelo LED\n')
        plt.xlabel('Intensidade LED (mW/sr)')
        plt.ylabel('Tensão PT (V)')
        plt.legend(title='OD_600:')

        plt.savefig(f'logs/od-curves/EVOLVER-1/Amostras/SS{ss}-ODxLED.png')
        plt.show()


        '''
        #
        figure, axs = plt.subplots(1,2)
        figure.set_figwidth(12)
        figure.set_figheight(7)
        figure.suptitle(f'Log de OD600 - SS{ss} | {date}\n')

        axs[0].plot(ods['led']['int_rad'], ods[f'SS{ss}']['v'][5], label='OD_600 = 0')
       
        for i,value in enumerate(ods['od'][:-1]):
            axs[1].plot(ods[f'SS{ss}']['v'][5], ods[f'SS{ss}']['v'][i], label=f'{value}')
 
        axs[0].set(xlabel='Intensidade LED (mW/sr)', ylabel='Tensão PT, OD = 0 (V)', title='Tensão medida no PT com OD600 = 0\nem função da intensidade de radiação emitida pelo LED\n')
        axs[1].set(xlabel='Tensão PT, OD = 0 (V)', ylabel='Tensão PT(V)', title='Tensão medida no PT em função\n da tensão medida no PT quando OD = 0\n')

        axs[0].legend()
        axs[1].legend(title='OD_600:')

        plt.savefig(f'logs/od-curves/EVOLVER-1/Amostras/SS{ss}-ODxOD0.png')
        plt.show()
        '''


        '''
        #
        figure, axs = plt.subplots(2,2)
        figure.set_figwidth(12)
        figure.set_figheight(7)

        figure.suptitle(f'Log de OD600 para SS{ss} | {date}\nTransmitância e Absorbância')

        led = round(100*ods['led']['ad'][25]/4095)
        t = [ods[f'SS{ss}']['ad'][i][25]/ods[f'SS{ss}']['ad'][5][25] for i in range(len(ods['od']))]
        a = [-math.log10(t[i]) for i in range(len(ods['od']))]
        axs[0,0].plot(ods['od'], t, label='Transmitância')
        axs[0,0].plot(ods['od'], a, label='Absorbância')
        axs[0,0].set(title='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][25]))


        led = round(100*ods['led']['ad'][50]/4095)
        t = [ods[f'SS{ss}']['ad'][i][50]/ods[f'SS{ss}']['ad'][5][50] for i in range(len(ods['od']))]
        a = [-math.log10(t[i]) for i in range(len(ods['od']))]
        axs[0,1].plot(ods['od'], t, label='Transmitância')
        axs[0,1].plot(ods['od'], a, label='Absorbância')
        axs[0,1].set(title='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][50]))

        led = round(100*ods['led']['ad'][75]/4095)
        t = [ods[f'SS{ss}']['ad'][i][75]/ods[f'SS{ss}']['ad'][5][75] for i in range(len(ods['od']))]
        a = [-math.log10(t[i]) for i in range(len(ods['od']))]
        axs[1,0].plot(ods['od'], t, label='Transmitância')
        axs[1,0].plot(ods['od'], a, label='Absorbância')
        axs[1,0].set(title='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][75]))

        led = round(100*ods['led']['ad'][100]/4095)
        t = [ods[f'SS{ss}']['ad'][i][100]/ods[f'SS{ss}']['ad'][5][100] for i in range(len(ods['od']))]
        a = [-math.log10(t[i]) for i in range(len(ods['od']))]
        axs[1,1].plot(ods['od'], t, label='Transmitância')
        axs[1,1].plot(ods['od'], a, label='Absorbância')
        axs[1,1].set(title='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][100]))

        for ax in axs.flat:
            ax.set(xlabel='OD_600', ylabel='u.a.')
            ax.legend()

        plt.savefig(f'logs/od-curves/EVOLVER-1/Amostras/SS{ss}-ODxTeA.png')
        plt.show()
        '''

        
        #
        figure, axs = plt.subplots(2,2)
        figure.set_figwidth(12)
        figure.set_figheight(7)

        figure.suptitle(f'Log de OD600 para SS{ss} | {date}\nTensão medida em função de OD_600')

        led = round(100*ods['led']['ad'][25]/4095)
        x = [ods[f'SS{ss}']['v'][i][25] for i in range(len(ods['od']))]
        axs[0,0].scatter(ods['od'], x)
        axs[0,0].plot(ods['od'], x, label='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][25]))

        led = round(100*ods['led']['ad'][50]/4095)
        x = [ods[f'SS{ss}']['v'][i][50] for i in range(len(ods['od']))]
        axs[0,1].scatter(ods['od'], x, color='orange')
        axs[0,1].plot(ods['od'], x, label='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][50]), color='orange')

        led = round(100*ods['led']['ad'][75]/4095)
        x = [ods[f'SS{ss}']['v'][i][75] for i in range(len(ods['od']))]
        axs[1,0].scatter(ods['od'], x, color='green')
        axs[1,0].plot(ods['od'], x, label='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][75]), color='green')

        led = round(100*ods['led']['ad'][100]/4095)
        x = [ods[f'SS{ss}']['v'][i][100] for i in range(len(ods['od']))]
        axs[1,1].scatter(ods['od'], x, color='red')
        axs[1,1].plot(ods['od'], x, label='LED {}% = {:.1f} mW/sr'.format(led, ods['led']['int_rad'][100]), color='red')

        for ax in axs.flat:
            ax.set(xlabel='OD_600', ylabel='Tensão PT (V)')
            ax.legend()

        plt.savefig(f'logs/od-curves/EVOLVER-1/Amostras/SS{ss}-ODxV.png')
        plt.show()


def graficos_repetibilidade(logs, active_ss):
    ods = data_repetibilidade(logs, active_ss)

    for ss in active_ss:
        figure = plt.figure()
        figure.set_figwidth(12)
        figure.set_figheight(7)

        plt.plot(ods['led'], ods['avg'][f'SS{ss}'], color='black', alpha=0.5)
        plt.plot(ods['led'], ods['max'][f'SS{ss}'], color='black', linestyle='--', alpha=0.5)
        plt.plot(ods['led'], ods['min'][f'SS{ss}'], color='black', linestyle='--', alpha=0.5)

        for i in range(len(logs)):
            plt.scatter(ods['led'], ods[f'SS{ss}'][i], label=f'nº{i+1} ({logs[i].split("/")[-1].split("_")[1]})')
            #plt.errorbar(ods['led'], ods[f'SS{ss}'][i], xerr=, yerr=)
        
        plt.legend(title="Teste de nº:")
        plt.title(f'Log de OD: Repetibilidade da SS{ss}')

        plt.xlabel('Intensidade LED (mW/sr)')
        plt.ylabel('Tensão PT (V)')
        
        plt.savefig(f'logs/od-curves/EVOLVER-2/Repetibilidade/SS{ss}.png')
        plt.show()


if __name__ == "__main__":
    #graficos_od(logs_od, [1,2,3,4,5,6,7,8])
    graficos_repetibilidade(logs_repetibilidade, [1,2,3,4,5,6,7,8])