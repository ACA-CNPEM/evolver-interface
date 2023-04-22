import os
import csv
import matplotlib.pyplot as plt


log_path = 'logs/1/log_14-04-23_08:49:48'
ss2channel = [15,14,11,10,7,6,3,2,13,12,9,8,5,4,1,0]
pump2ss =[[39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40],[23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24],[7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]]

def organize_raw_logs(name):
    if not os.path.exists(f'{name}/csv'):
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




def graph_data(name, log_type):
    graph_data = {}

    with open(f'{name}/csv/log_{log_type}.csv', 'r') as log_file:
            log_reader = csv.DictReader(log_file, delimiter=';')

            for header in log_reader.fieldnames:
                graph_data[header] = []

            for row in log_reader:
                for key in log_reader.fieldnames:
                    graph_data[key] += [row[key]]
    
    return graph_data



def graficos_od(name, active_ss, delta_t):
    od_raw_data = graph_data(name, 'od')
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
    plt.legend()

    if not os.path.exists(f'{name}/graficos'):
        os.makedirs(f'{name}/graficos')

    plt.savefig(f'{name}/graficos/log_od.png')
    plt.show()



def graficos_temp(name, active_ss, delta_t):
    temp_raw_data = graph_data(name, 'temp')
    temp_data = {}

    for key in temp_raw_data.keys():
        temp_data[key] = []

    for point in range(len(temp_raw_data['timestamp'])):
        if (point % delta_t == 0):
            for key in temp_data.keys():
                temp_data[key] += [float(temp_raw_data[key][point])]

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in active_ss:
        plt.plot(temp_data['time(s)'], temp_data[f'SS{ss}'], label=f'SS{ss}')
    
    date = name.split('_')[1:]
    date = '_'.join(date)
    plt.title(f'Log de temperatura: {date}')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (u.a.)')
    plt.legend()
    
    if not os.path.exists(f'{name}/graficos'):
        os.makedirs(f'{name}/graficos')

    plt.savefig(f'{name}/graficos/log_temp.png')
    plt.show()
    


#organize_raw_logs(log_path)
graficos_od(log_path, [1,2,3,4,5,6,7,8], 10)
graficos_temp(log_path, [1,2,3,4,5,6,7,8], 10)