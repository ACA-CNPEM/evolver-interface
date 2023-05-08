import os
import csv
import socket
import matplotlib.pyplot as plt
from utils import *

log_path = 'logs/EVOLVER-2/log_05-05-23_14:46:39'
ss2channel = [15,14,11,10,7,6,3,2,13,12,9,8,5,4,1,0]
pump2ss =[[39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40],[23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24],[7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]]



def organize_raw_logs(name):
    columns = [f'SS{i+1}' for i in range(16)]
    columns.insert(0, 'time(s)')

    with open(f'{name}/raw.csv', 'r') as log_file:
            log_reader = csv.reader(log_file, delimiter=',')
            raw_data = [row for row in log_reader]
        
    with open(f'{name}/organized.csv', 'a') as log_file:
        log_writer = csv.writer(log_file, delimiter=';')
        log_writer.writerow(columns)

        inicial_time = float(raw_data[0][0])

        for line in raw_data:
            ordered = [float(line[0]) - inicial_time]
            line = line[2:]

            ordered += [line[i] for i in ss2channel]
            log_writer.writerow(ordered)



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
    figure.legend()

    if not os.path.exists(f'{name}/graficos'):
        os.makedirs(f'{name}/graficos')

    plt.savefig(f'{name}/graficos/log_od.png')
    plt.show()



def graficos_temp(name, active_ss, delta_t):
    temp_raw_data = graph_data(name, 'organized')
    temp_data = {}

    for key in temp_raw_data.keys():
        temp_data[key] = []

    for point in range(len(temp_raw_data['SS1'])):
        if (point % delta_t == 0):
            for key in temp_data.keys():
                temp_data[key] += [float(temp_raw_data[key][point])]
            
            '''if len(setpoints) > 1:
                if (float(temp_raw_data['timestamp'][point]) >= float(setpoints[1][0])):
                    setpoint_data += [float(setpoints[1][1])]
                    setpoints.pop(0)
                else:
                    setpoint_data += [float(setpoints[0][1])]
            else:
                setpoint_data += [float(setpoints[0][1])]'''

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    #plt.plot(temp_data['time(s)'], ad_temp(setpoint_data), label='Setpoint', linestyle='--')
    for ss in active_ss:
        plt.plot(temp_data['time(s)'], ad_temp(temp_data[f'SS{ss}']), label=f'SS{ss}')
    
    date = name.split('_')[1:]
    date = '_'.join(date)
    plt.title(f'Log de temperatura: {date}')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'{name}/log_temp.png')
    plt.show()




if __name__ == "__main__":
    if not os.path.exists(log_path):
        print("LOG NOT FOUND!")
        
    else:
        if not os.path.exists(f'{log_path}/organized.csv'):
            organize_raw_logs(log_path)
        
        graficos_temp(log_path, [1,2,3,4,5,6,7,8], 10)