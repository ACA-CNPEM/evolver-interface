import serial
import time
import csv
import os
import yaml
from yaml.loader import SafeLoader


# Log variables
dia = 3
id = 'log_' + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())

if not os.path.exists(f'logs/{dia}/{id}/raw'):
    os.makedirs(f'logs/{dia}/{id}/raw')


# Configuration variables
with open('configuration.yaml') as configuration_file:
    config = yaml.load(configuration_file, Loader=SafeLoader)
    commands = config[f'dia{dia}']
    acknoledgment= config['acknoledgment']
    smart_sleeves = config['smart_sleeves']


# Serial communication variable
serial_channel = serial.Serial(
    port = '/dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)


'''# Function that organizes raw logs
def organize_logs(name):
    columns = ['timestamp', 'module']
    for i in range(8):
            columns += [f'SS{i+1}']

    with open(f'logs/{name}/raw/log_inicial.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
        
    with open(f'logs/{name}/log_inicial.csv', 'a') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.write(columns)

        for line in raw_data:
            echo_string = line[2].split(',')

            module = echo_string[0][0:(len(echo_string[0]) - 1)]
            data = {
                'module': module, 
                'timestamp': line[0],
            }
                
            echo_string = echo_string[1:(len(echo_string) - 1)]
                
            if module in ['temp','od_135']:
                broadcast_string = line[3].split(',')
                broadcast_string = broadcast_string[1:(len(broadcast_string) - 1)]

            for i in range(8):
                if module == 'temp':
                    data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string[smart_sleeves[f'ss{i+1}']]})"

                elif module == 'od_135':
                    data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string})"

                elif module == 'pump':
                    print('pump')
                    #data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string})"
                    #data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string})"
                    #data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string})"

                else:
                    data[f'SS{i+1}'] = echo_string[smart_sleeves[f'ss{i+1}']]
                
        log_writer.writerow(data)
'''

# Function that sends messages to evolver and saves them to log
def send_messages(file_name, command, channel):
    channel.write(str.encode(command))
    time.sleep(1)

    input_string = ""
    received_time = time.time()
    
    while channel.in_waiting:
        input_bit = channel.read()
        input_string += input_bit.decode()

        if (input_string.rfind('end') != -1):
            print(input_string)

            with open(f'logs/{dia}/{id}/raw/{file_name}.csv', 'a') as log_file:
                input_string = input_string.split(',')
                module = input_string[0]
                
                log_data = input_string[1:(len(input_string)-1)]
                log_data.insert(0, received_time)
                log_data.insert(1, module)

                log_writer = csv.writer(log_file, delimiter=',')
                log_writer.writerow(log_data)

            input_string = ""


# Initializing experiment
for module in commands.keys():
    command_line = commands[module]['status1'] if type(commands[module]) == dict else commands[module]
    send_messages(f'log_inicial', command_line, serial_channel)

with open(f'logs/{dia}/{id}/raw/log_inicial.csv', 'r') as log_file:
    log_reader = csv.reader(log_file, delimiter=',')
    raw_data = [row for row in log_reader]

with open(f'logs/{dia}/{id}/raw/log_temp.csv', 'a') as log_file:
    log_writer = csv.writer(log_file, delimiter=',')
    log_writer.writerow(raw_data[1])
    log_writer.writerow(raw_data[2])

with open(f'logs/{dia}/{id}/raw/log_od.csv', 'a') as log_file:
    log_writer = csv.writer(log_file, delimiter=',')
    log_writer.writerow(raw_data[4])


# Acknowledging commands
'''for module in commands.keys():
    print(acknoledgment[module])
    serial_channel.write(str.encode(acknoledgment[module]))'''


cycle = 0
temp_command = commands['temp'] if type(commands['temp']) != dict else commands['temp']['status1']

# Experiment loop
while True:
    if dia == 3:
        if cycle == 720: # 10h - 12h
            temp_command = commands['temp']['status2']

            send_messages(f'log_inicial', commands['stir']['status2'], serial_channel)
            send_messages(f'log_inicial', temp_command, serial_channel)

            #serial_channel.write(str.encode(acknoledgment['stir']))
            #serial_channel.write(str.encode(acknoledgment['temp']))

        elif cycle == 1440: # 12h - 14h
            temp_command = commands['temp']['status3']

            send_messages(f'log_inicial', commands['stir']['status1'], serial_channel)
            send_messages(f'log_inicial', temp_command, serial_channel)
            send_messages(f'log_inicial', commands['pump']['status2'], serial_channel)

            #serial_channel.write(str.encode(acknoledgment['stir']))
            #serial_channel.write(str.encode(acknoledgment['temp']))
            #serial_channel.write(str.encode(acknoledgment['pump']))

        elif cycle == 2160: # 14h - 16h
            temp_command = commands['temp']['status1']

            send_messages(f'log_inicial', commands['stir']['status2'], serial_channel)
            send_messages(f'log_inicial', temp_command, serial_channel)

            #serial_channel.write(str.encode(acknoledgment['stir']))
            #serial_channel.write(str.encode(acknoledgment['temp']))
        
    elif dia == 4:
        if cycle == 1440:
            send_messages(f'log_inicial', commands['pump']['status2'], serial_channel)
            #serial_channel.write(str.encode(acknoledgment['pump']))

    send_messages(f'log_temp', temp_command, serial_channel)
    send_messages(f'log_od', commands['od_135'], serial_channel)

    time.sleep(1)
    cycle += 1

    if cycle >= 2880: # 8h funcionando, fim do experimento
        #organize_logs(f"{dia}/{id}")
        break





        







#'pumpi,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,_!')
'''def send_stir():
    i = 0
    while True:
        si.serial_event(f'stiri,{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},_!')
        i += 1

def send_od_led():
    i = 0
    while True:
        si.serial_event(f'od_ledi,{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},_!')
        i += 1

prc = mp.Process(target=send_stir, args=[])
prc2 = mp.Process(target=send_od_led, args=[])

prc.start()
prc2.start()

si.serial_event('stiri,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!')
si.serial_event('stiri,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!')
si.serial_event('od_ledi,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!')'''











'''def send_command():
    global modules, communication, serial_channel
    string_command = ""

    for module in modules.keys():
        string_command = f"{module}i,"

        for i in modules[module]:
            string_command += f"{i},"
        
        string_command += communication['outgoing_end']
    
        print(string_command)
    #serial_channel.write(str.encode(string_command))

send_command()'''