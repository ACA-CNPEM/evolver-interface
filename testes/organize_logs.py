import os
import csv
import matplotlib.pyplot as plt
from utils import *



log_path = 'testes/logs/temp-curves/EVOLVER-1/log_16-05-23_11:42:39'
ss2channel = [15,14,11,10,7,6,3,2,13,12,9,8,5,4,1,0]
pump2ss =[[39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40],[23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24],[7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]]



def organize_extended_logs(name):
    os.makedirs(f'{name}/csv')

    columns = ['timestamp', 'module']
    for i in range(16):
            columns += [f'SS{i+1}']

    with open(f'{name}/csv/log_inicial.csv', 'a') as log_file:
        log_writer = csv.writer(log_file, delimiter=';')
        log_writer.writerow(columns)

    with open(f'{name}/raw/log_inicial.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    for line in raw_data:
        module = line[1]
        timestamp = line[0]
        raw_commands = line[2:]

        if module == 'pumpe':
            ordered = [f'{raw_commands[pump2ss[0][i]]}-{raw_commands[pump2ss[1][i]]}-{raw_commands[pump2ss[2][i]]}' for i in range(16)]
        else:
            ordered = [raw_commands[i] for i in ss2channel] if module[:-1] != 'od_135' else raw_commands
            
        ordered.insert(0, timestamp)
        ordered.insert(1, module)

        with open(f'{name}/csv/log_inicial.csv', 'a') as log_file:
             log_writer = csv.writer(log_file, delimiter=';')
             log_writer.writerow(ordered)

    columns.pop(1)
    columns.insert(1, 'time(s)')

    for log_type in ['log_od','log_temp']:
        with open(f'{name}/raw/{log_type}.csv', 'r') as log_file:
            log_reader = csv.reader(log_file, delimiter=',')
            raw_data = [row for row in log_reader]
        
        with open(f'{name}/csv/{log_type}.csv', 'a') as log_file:
            log_writer = csv.writer(log_file, delimiter=';')
            log_writer.writerow(columns)

            inicial_time = float(raw_data[0][0])

            for line in raw_data:
                ordered = [line[0], float(line[0]) - inicial_time]
                line = line[2:]

                ordered += [line[i] for i in ss2channel]
                log_writer.writerow(ordered)


def organize_od_curves(name):
    columns = ['led']
    for i in range(16):
            columns += [f'SS{i+1}']

    with open(f'{name}/od_lede_raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_led = [row for row in log_reader]
    
    led = []

    for data in raw_led:
        led += [float(data[2])]

    with open(f'{name}/od_135b_raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_od = [row for row in log_reader]
    
    with open(f'{name}/tempb_raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_temp = [row for row in log_reader]
        
    od_data = []
    temp_data = []

    sum = [0 for i in range(16)]
    temp_sum = [0 for i in range(16)]

    p = 0
    for k,line in enumerate(raw_od):
            line = line[2:]
            temp_line = raw_temp[k][2:]
                
            if(p < 4):
                sum = [sum[i]+float(line[ss2channel[i]]) for i in range(16)]
                temp_sum = [temp_sum[i]+float(temp_line[ss2channel[i]]) for i in range(16)]
                p += 1
                
            else:
                sum = [sum[i]+float(line[ss2channel[i]]) for i in range(16)]
                temp_sum = [temp_sum[i]+float(temp_line[ss2channel[i]]) for i in range(16)]

                od_data += [[sum[i]/5 for i in range(16)]]
                temp_data += [[temp_sum[i]/5 for i in range(16)]]

                sum = [0 for i in range(16)]
                temp_sum = [0 for i in range(16)]
                p = 0


    with open(f'{name}/organized_od.csv', 'a') as log_file:
        log_writer = csv.writer(log_file, delimiter=';')
        log_writer.writerow(columns)

        for i in range(len(led)):
            line = [led[i]]

            for j in range(16):
                line += [od_data[i][j]]

            log_writer.writerow(line)
    
    with open(f'{name}/organized_temp.csv', 'a') as log_file:
        log_writer = csv.writer(log_file, delimiter=';')
        log_writer.writerow(columns)


        for i in range(len(led)):
            line = [led[i]]

            for j in range(16):
                line += [temp_data[i][j]]

            log_writer.writerow(line)


def organize_temp_curves(name):
    columns = ['time(s)']
    for i in range(16):
            columns += [f'SS{i+1}']

    data = {
        'setpoint': [],
    }
    for column in columns:
        data[column] = []

    with open(f'{name}/raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    
    raw_data = raw_data[1:]
    inicial_time = float(raw_data[0][0])
    setpoint = 2050

    for line in raw_data:
        if line[1][-1] == 'e':
            setpoint = float(line[2])

        else:
            data['time(s)'] += [float(line[0]) - inicial_time]
            line = line[2:]  
            data['setpoint'] += [setpoint]

            for i in range(16):
                data[f'SS{i+1}'] += [float(line[ss2channel[i]])]
    
    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    plt.plot(data['time(s)'], ad_temp(data['setpoint']), label='Setpoint', linestyle='--')

    for ss in range(8):
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss+1}']), label=f'SS{ss+1}')
   

    plt.title(f'Log de Temp')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'{name}/log_temp.png')
    plt.show()


def organize_interface_tests(name):
    columns = ['time(s)']
    for i in range(16):
            columns += [f'SS{i+1}']

    type = name.split('/')[-2]
    os.makedirs(f'{name}/csv')

    with open(f'{name}/{type}.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    if type == 'od-1':
        columns.insert(1, 'stir')
        led = 0
        stir = 0

        for line in raw_data:
            module = line[1][:-1]

            if module == 'od_led':
                inicial_time = float(line[0])
                led = int(line[3])

                with open(f'{name}/csv/{led}.csv', 'a') as log_file:
                    log_writer = csv.writer(log_file, delimiter=';')
                    log_writer.writerow(columns)
            
            else:
                if module == 'stir':
                    stir = int(line[2])
                
                else:
                    organized = [float(line[0]) - inicial_time, stir]
                    line = line[2:]

                    for i in range(16):
                        organized += [float(line[ss2channel[i]])]
                    
                    with open(f'{name}/csv/{led}.csv', 'a') as log_file:
                        log_writer = csv.writer(log_file, delimiter=';')
                        log_writer.writerow(organized)
    
    elif type == 'od-2':
        print('a')

                
def graph_data(name, log_type):
    graph_data = {}

    with open(f'{name}/{log_type}.csv', 'r') as log_file:
            log_reader = csv.DictReader(log_file, delimiter=';')

            for header in log_reader.fieldnames:
                graph_data[header] = []

            for row in log_reader:
                for key in log_reader.fieldnames:
                    graph_data[key] += [row[key]]
    
    return graph_data


def graficos_interference_stir_od(name, active_ss, delta_t):
    for ad in [1024, 2048, 3072, 4095]:
        raw_data = graph_data(name, f'csv/{ad}')
        data = {}

        for key in raw_data.keys():
            data[key] = []
        
        for point in range(len(raw_data['time(s)'])):
            if (point % delta_t == 0):
                for key in data.keys():
                    data[key] += [float(raw_data[key][point])]
        
        figure, ax1 = plt.subplots()
        figure.set_figwidth(15)
        figure.set_figheight(10)
        
        ax1.set_xlabel('Time(s)')
        ax1.set_ylabel('OD (AD)')

        for ss in active_ss:
            ax1.plot(data['time(s)'], data[f'SS{ss}'], label=f'SS{ss}')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Agitação (%)')
        ax2.plot(data['time(s)'], ad_stir(data['stir']), linestyle='--')

        date = name.split('_')[1:]
        date = '_'.join(date)
        plt.title(f'Log de OD com Agitação para LED emitindo {ad_od_led([ad])[0]} mW/sr ({ad} AD) - {date}')
        figure.legend()

        if not os.path.exists(f'{name}/graficos'):
            os.makedirs(f'{name}/graficos')

        plt.savefig(f'{name}/graficos/{ad}.png')


def graficos_od(name, active_ss, delta_t):
    od_raw_data = graph_data(name, 'csv/log_od')
    od_data = {}

    for key in od_raw_data.keys():
        od_data[key] = []

    for point in range(len(od_raw_data['timestamp'])):
        if (point % delta_t == 0):
            for key in od_data.keys():
                od_data[key] += [float(od_raw_data[key][point])]

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in active_ss:
        plt.plot(od_data['time(s)'], od_data[f'SS{ss}'], label=f'SS{ss}')
   
    date = name.split('_')[1:]
    date = '_'.join(date)
    plt.title(f'Log de OD: {date}')

    plt.xlabel('Tempo (s)')
    plt.ylabel('OD (u.a.)')
    figure.legend()

    if not os.path.exists(f'{name}/graficos'):
        os.makedirs(f'{name}/graficos')

    plt.savefig(f'{name}/graficos/log_od.png')
    plt.show()


def graficos_od_curves(name, active_ss, delta_t):
    od_raw_data = graph_data(name, 'organized_od')
    od_data = {}
    t_data = {}

    avg_data = []
    avg_t_data = []
    avg_ss = [f'SS{ss}' for ss in active_ss]
    

    for key in od_raw_data.keys():
        od_data[key] = []
        t_data[key] = []

    for point in range(len(od_raw_data['led'])):
        if (point % delta_t == 0):
            sum1 = 0
            sum2 = 0

            for key in od_data.keys():
                od_data[key] += [float(od_raw_data[key][point])]
                t_data[key] += [(65520.0 - float(od_raw_data[key][point])) / (65520.0 - float(od_raw_data[key][-1])) if float(od_raw_data[key][-1]) != 65520.0 else 0]
                
                if key in avg_ss:
                    sum1 += float(od_raw_data[key][point])
                    sum2 += (65520.0 - float(od_raw_data[key][point])) / (65520.0 - float(od_raw_data[key][-1])) if float(od_raw_data[key][-1]) != 65520.0 else 0

            avg_data += [sum1/len(avg_ss)]
            avg_t_data += [sum2/len(avg_ss)]
    
    for i in range(len(od_data['led'])):
        od_data['led'][i] /= 4095
            
    if not os.path.exists(f'{name}/average_curve.csv'):
        with open(f'{name}/average_curve.csv', 'a') as log_file:
            log_writer = csv.writer(log_file, delimiter=';')
            log_writer.writerow(od_data['led'])
            log_writer.writerow(avg_data)
            log_writer.writerow(avg_t_data)

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    plt.plot(od_data['led'], avg_data, label=f'Média', linestyle='--')
    for ss in active_ss:
        plt.plot(od_data['led'], od_data[f'SS{ss}'], label=f'SS{ss}')
   
    date = name.split('_')[1:]
    date = '_'.join(date)
    plt.title(f'Log de OD: {date}')

    plt.xlabel('LED (% PWM)')
    plt.ylabel('PT (AD)')
    figure.legend()

    plt.savefig(f'{name}/log_od.png')
    plt.show()

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    plt.plot(od_data['led'], avg_t_data, label=f'Média', linestyle='--')
    for ss in active_ss:
        plt.plot(od_data['led'], t_data[f'SS{ss}'], label=f'SS{ss}') 

    plt.title(f'Log da transmissão de OD: {date}')
    plt.xlabel('LED (% PWM)')
    plt.ylabel('1 - PT/63730')
    figure.legend()

    plt.savefig(f'{name}/log_od_t.png')
    plt.show()


def graficos_od_curves_t(name, active_ss, delta_t):
    od_raw_data = graph_data(name, 'organized_od')
    od_data = {}
    t_data = {}
    d_data = []

    for key in od_raw_data.keys():
        od_data[key] = []
        t_data[key] = []

    for point in range(len(od_raw_data['led'])):
        if (point % delta_t == 0):
            sum = 0

            for key in od_data.keys():
                od_data[key] += [float(od_raw_data[key][point])]
                t_data[key] += [1-float(od_raw_data[key][point]) / 60000.0]
                
                if key in ['SS1','SS2','SS3','SS4','SS5','SS6','SS7','SS8']:
                    sum += 1-float(od_raw_data[key][point]) / 60000.0
            
            d_data += [sum/8]


    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    plt.plot(od_data['led'], d_data, label=f'Avg', linestyle='--')
    for ss in active_ss:
        plt.plot(od_data['led'], t_data[f'SS{ss}'], label=f'SS{ss}')
   
    date = name.split('_')[1:]
    date = '_'.join(date)
    plt.title(f'Log de transmissão de OD: {date}')

    plt.xlabel('LED (AD)')
    plt.ylabel('1 - PT/65520')
    figure.legend()

    plt.savefig(f'{name}/log_od_t.png')
    plt.show()


def graficos_temp(name, active_ss, delta_t):
    setpoint_raw_data = graph_data(name, 'csv/log_inicial')
    setpoint_data = []
    setpoints = []

    i = 0
    for module in setpoint_raw_data['module']:
        if module == 'tempe':
            point_index = setpoint_raw_data['module'].index(module, i, len(setpoint_raw_data['module']))
            i = point_index + 1
            setpoints += [[setpoint_raw_data['timestamp'][point_index], setpoint_raw_data['SS1'][point_index]]]
    
    temp_raw_data = graph_data(name, 'csv/log_temp')
    temp_data = {}

    for key in temp_raw_data.keys():
        temp_data[key] = []

    for point in range(len(temp_raw_data['timestamp'])):
        if (point % delta_t == 0):
            for key in temp_data.keys():
                temp_data[key] += [float(temp_raw_data[key][point])]
            
            if len(setpoints) > 1:
                if (float(temp_raw_data['timestamp'][point]) >= float(setpoints[1][0])):
                    setpoint_data += [float(setpoints[1][1])]
                    setpoints.pop(0)
                else:
                    setpoint_data += [float(setpoints[0][1])]
            else:
                setpoint_data += [float(setpoints[0][1])]

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    plt.plot(temp_data['time(s)'], ad_temp(setpoint_data), label='Setpoint', linestyle='--')
    for ss in active_ss:
        plt.plot(temp_data['time(s)'], ad_temp(temp_data[f'SS{ss}']), label=f'SS{ss}')
    
    date = name.split('_')[1:]
    date = '_'.join(date)
    plt.title(f'Log de temperatura: {date}')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()
    
    if not os.path.exists(f'{name}/graficos'):
        os.makedirs(f'{name}/graficos')

    plt.savefig(f'{name}/graficos/log_temp.png')
    plt.show()


def graficos_od_temp_curves(name, active_ss, delta_t):
    temp_raw_data = graph_data(name, 'organized_temp')
    temp_data = {}

    for key in temp_raw_data.keys():
        temp_data[key] = []
    
    od_raw_data = graph_data(name, 'organized_od')
    od_data = {}

    for key in od_raw_data.keys():
        od_data[key] = []

    for point in range(len(od_raw_data['led'])):
        if (point % delta_t == 0):
            for key in od_data.keys():
                od_data[key] += [float(od_raw_data[key][point])]
                temp_data[key] += [float(temp_raw_data[key][point])]

    for ss in active_ss:
        figure, ax1 = plt.subplots()
        figure.set_figwidth(15)
        figure.set_figheight(10)
    
        ax1.plot(od_data['led'], od_data[f'SS{ss}'], label=f'OD', color='b')
        ax1.set_xlabel('LED (AD)')
        ax1.set_ylabel('PT (AD)')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Temperatura (°C)')
        ax2.plot(temp_data['led'], ad_temp(temp_data[f'SS{ss}']), label=f'Temp', color='r')
   
        date = name.split('_')[1:]
        date = '_'.join(date)
        plt.title(f'Log de OD com temperatura: SS{ss} - {date}')
        figure.legend()

        if not os.path.exists(f'{name}/od_temp'):
            os.makedirs(f'{name}/od_temp')

        plt.savefig(f'{name}/od_temp/SS{ss}.png')


def plot_od_curves(name):
    with open(f'{name}/organized_od.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=';')
        raw_data = [row for row in log_reader]

        for row in raw_data[1:]:
            x_data = []
            y_data = []

            for i,item in enumerate(row):
                item = int(float(item))

                if i%2 == 0:
                    x_data += [item]
                else:
                    y_data += [item]
            
            x += [x_data]
            y += [y_data]

    x_data = []
    y_data = []

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)
    
    for i in range(8):
        x_data = [x_line[i] for x_line in x]
        y_data = [y_line[i] for y_line in y]
        plt.plot(x_data, y_data, label=f'SS{i+1}')

    plt.title(f"{name.split('/')[1]}")
    plt.xlabel('LED emission (AD)')
    plt.ylabel('PT detector (AD)')
    figure.legend()

    plt.savefig(f'{name}/all.png')
    plt.show()

    if not os.path.exists(f'{name}/SSs'):
        os.makedirs(f'{log_path}/SSs')

    for i in range(8):
        figure = plt.figure()
        figure.set_figwidth(15)
        figure.set_figheight(10)

        x_data = [x_line[i] for x_line in x]
        y_data = [y_line[i] for y_line in y]

        plt.plot(x_data, y_data)
        plt.title(f"SS{i+1}")
        plt.xlabel('LED emission (AD)')
        plt.ylabel('PT detector (AD)')

        plt.savefig(f'{name}/SSs/SS{i}.png')
        plt.show()


def graficos_od_stir(name, active_ss, delta_t):
    stir_raw_data = graph_data(name, 'csv/log_inicial')
    stir_data = []
    stir_values = []

    i = 0
    for module in stir_raw_data['module']:
        if module == 'stire':
            point_index = stir_raw_data['module'].index(module, i, len(stir_raw_data['module']))
            i = point_index + 1
            stir_values += [[stir_raw_data['timestamp'][point_index], stir_raw_data['SS1'][point_index]]]
    
    od_raw_data = graph_data(name, 'csv/log_od')
    od_data = {}

    for key in od_raw_data.keys():
        od_data[key] = []

    for point in range(len(od_raw_data['timestamp'])):
        if (point % delta_t == 0):
            for key in od_data.keys():
                od_data[key] += [float(od_raw_data[key][point])]
            
            if len(stir_values) > 1:
                if (float(od_raw_data['timestamp'][point]) >= float(stir_values[1][0])):
                    stir_data += [float(stir_values[1][1])]
                    stir_values.pop(0)
                else:
                    stir_data += [float(stir_values[0][1])]
            else:
                stir_data += [float(stir_values[0][1])]

    figure, ax1 = plt.subplots()
    figure.set_figwidth(15)
    figure.set_figheight(10)
    
    ax1.plot(od_data['time(s)'], stir_data, label=f'Taxa de agitação', linestyle='--', color='b')
    ax1.set_xlabel('Tempo (s)')
    ax1.set_ylabel('Agitação (%)')

    ax2 = ax1.twinx()
    ax2.set_ylabel('OD (u.a.)')

    for ss in active_ss:
        ax2.plot(od_data['time(s)'], od_data[f'SS{ss}'], label=f'SS{ss}')
   
    date = name.split('_')[1:]
    date = '_'.join(date)
    plt.title(f'Log de OD com agitação: {date}')
    figure.legend()

    if not os.path.exists(f'{name}/graficos'):
        os.makedirs(f'{name}/graficos')

    plt.savefig(f'{name}/graficos/log_od_stir.png')
    plt.show()


def graficos_od_temp(name, active_ss, delta_t):
    temp_raw_data = graph_data(name, 'csv/log_temp')
    temp_data = {}

    for key in temp_raw_data.keys():
        temp_data[key] = []
    
    od_raw_data = graph_data(name, 'csv/log_od')
    od_data = {}

    for key in od_raw_data.keys():
        od_data[key] = []

    for point in range(len(od_raw_data['timestamp'])):
        if (point % delta_t == 0):
            for key in od_data.keys():
                od_data[key] += [float(od_raw_data[key][point])]
                temp_data[key] += [float(temp_raw_data[key][point])]

    for ss in active_ss:
        figure, ax1 = plt.subplots()
        figure.set_figwidth(15)
        figure.set_figheight(10)
    
        ax1.plot(od_data['time(s)'], od_data[f'SS{ss}'], label=f'OD', color='b')
        ax1.set_xlabel('Tempo (s)')
        ax1.set_ylabel('OD (u.a.)')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Temperatura (°C)')
        ax2.plot(temp_data['time(s)'], ad_temp(temp_data[f'SS{ss}']), label=f'Temp', color='r')
   
        date = name.split('_')[1:]
        date = '_'.join(date)
        plt.title(f'Log de OD com temperatura: SS{ss} - {date}')
        figure.legend()

        if not os.path.exists(f'{name}/graficos/od_temp'):
            os.makedirs(f'{name}/graficos/od_temp')

        plt.savefig(f'{name}/graficos/od_temp/SS{ss}.png')



if __name__ == "__main__":
    log_path = '/'.join(log_path.split('/')[1:])

    if not os.path.exists(log_path):
        print("LOG NOT FOUND!")

    else:
        type = log_path.split('/')[1]
        
        if type == 'od-curves':
            if not os.path.exists(f'{log_path}/organized_od.csv'):
                organize_od_curves(log_path)

            graficos_od_curves(log_path, [1,2,3,4,5,6,7,8], 1)
            graficos_od_temp_curves(log_path, [1,2,3,4,5,6,7,8], 1)
        
        if type == 'temp-curves':
            organize_temp_curves(log_path)

            #graficos_od_curves(log_path, [1,2,3,4,5,6,7,8], 1)
            #plot_od_curves(log_path)

        if type == 'periodo-extendido':
            if not os.path.exists(f'{log_path}/csv'):
                organize_extended_logs(log_path)

            graficos_od(log_path, [1,2,3,4,5,6,7,8], 10)
            graficos_temp(log_path, [1,2,3,4,5,6,7,8], 10)
            graficos_od_stir(log_path, [1,2,3,4,5,6,7,8], 10)
            graficos_od_temp(log_path, [1,2,3,4,5,6,7,8], 10)
        
        if type == 'interference-tests':
            if not os.path.exists(f'{log_path}/csv'):
                organize_interface_tests(log_path)
            
            type = log_path.split('/')[3]

            if type == 'od-1':
                graficos_interference_stir_od(log_path,[1,2,3,4,5,6,7,8],1)
