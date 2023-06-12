import matplotlib.pyplot as plt
import csv

from utils import *
from organize_logs import graph_data, ss2channel

def organize_temp_curves_kapton(name):
    columns = ['time(s)']
    for i in range(16):
            columns += [f'SS{i+1}']

    data_k = {}
    data = {
        'setpoint': [],
    }

    for column in columns:
        data[column] = []
        data_k[column] = []

    with open(f'logs/temp-curves/EVOLVER-1/log_24-05-23_13:19:23/raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
    
    with open(f'logs/temp-curves/EVOLVER-1/log_25-05-23_09:09:41/raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data_k = [row for row in log_reader]
    
    raw_data = raw_data[1:]
    raw_data_k = raw_data_k[1:]

    inicial_time = float(raw_data[0][0])
    inicial_time_k = float(raw_data_k[0][0])

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
    
    for line in raw_data_k:
        if line[1][-1] != 'e':
            data_k['time(s)'] += [float(line[0]) - inicial_time_k]
            line = line[2:]  

            for i in range(16):
                data_k[f'SS{i+1}'] += [float(line[ss2channel[i]])]

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)
    
    for ss in [1,2]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com 1 volta')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/1_volta.png')
    plt.show()

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in [3,4]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com 2 voltas')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/2_voltas.png')
    plt.show()

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in [5,6]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com 3 voltas')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/3_voltas.png')
    plt.show()

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in [7,8]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com pouco mais de 6 voltas')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/6_voltas.png')
    plt.show()


def organize_temp_curves_realtime_kapton(name):
    columns = ['time(s)']
    for i in range(16):
            columns += [f'SS{i+1}']

    data_k = {}
    data = {}

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

    for line in raw_data:
        data['time(s)'] += [float(line[0]) - inicial_time]
        line = line[1:]  

        for i in range(16):
            data[f'SS{i+1}'] += [float(line[ss2channel[i]])]

    for line in raw_data_k:
        data_k['time(s)'] += [float(line[0]) - inicial_time_k]
        line = line[1:]  

        for i in range(16):
            data_k[f'SS{i+1}'] += [float(line[ss2channel[i]])]
    
    for key in data.keys():
        data[key] = data[key][:3550]
        data_k[key] = data_k[key][:3370]

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)
    
    for ss in [1,2]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com 1 volta')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/1_volta_resfriando.png')
    plt.show()

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in [3,4]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com 2 voltas')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/2_voltas_resfriando.png')
    plt.show()

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in [5,6]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com 3 voltas')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/3_voltas_resfriando.png')
    plt.show()

    figure = plt.figure()
    figure.set_figwidth(15)
    figure.set_figheight(10)

    for ss in [7,8]:
        plt.plot(data['time(s)'], ad_temp(data[f'SS{ss}']), label=f'SS{ss}', linestyle='--')
        plt.plot(data_k['time(s)'], ad_temp(data_k[f'SS{ss}']), label=f'SS{ss} w/ Kapton')

    plt.title(f'Log de Temp: sem Kapton e com pouco mais de 6 voltas')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    figure.legend()

    plt.savefig(f'logs/temp-curves/EVOLVER-1/Kapton/6_voltas_resfriando.png')
    plt.show()