import serial
import time
import csv
import os

import yaml
from yaml.loader import SafeLoader

dia = 1
id = 'log_' + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())

if not os.path.exists(f'logs/{id}/raw'):
    os.makedirs(f'logs/{id}/raw')


with open('configuration.yaml') as configuration_file:
    config = yaml.load(configuration_file, Loader=SafeLoader)
    commands = config[f'dia{dia}']
    acknoledgment= config['acknoledgment']
    smart_sleeves = config['smart_sleeves']


serial_channel = serial.Serial(
    port = '/dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)


def send_messages(file_name, command, channel):
    channel.write(str.encode(command))
    time.sleep(1)
    input_string = ""

    while channel.in_waiting:
        input_bit = channel.read()
        input_string += input_bit.decode('utf-8')

        if (input_string.rfind('end') != -1):
            received_time = time.time()
            print(input_string)

            with open(f'logs/{id}/raw/{file_name}.csv', 'a') as log_file:
                input_string = input_string.split(',')
                module = input_string[0]
                
                log_data = input_string[1:(len(input_string)-1)]
                log_data.insert(0, received_time)
                log_data.insert(1, module)

                log_writer = csv.writer(log_file, delimiter=',')
                log_writer.writerow(log_data)

            input_string = ""


for module in commands.keys():
    send_messages(f'log_inicial', commands[module], serial_channel)

'''for module in commands.keys():
    print(acknoledgment[module])
    serial_channel.write(str.encode(acknoledgment[module]))'''


while True:
    try:
        send_messages(f'log_temp', commands['temp'], serial_channel)
        send_messages(f'log_od', commands['od_135'], serial_channel)
        time.sleep(10)

    except KeyboardInterrupt:

        columns = ['timestamp', 'module']
        for i in range(8):
            columns += [f'SS{i+1}']

        with open(f'logs/{id}/raw/log_inicial.csv', 'r') as log_file:
            log_reader = csv.reader(log_file, delimiter=',')
            raw_data = [row for row in log_reader]
        
        with open(f'logs/{id}/log_inicial.csv', 'a') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.write(columns)

            for line in raw_data:
                echo_string = line[2].split(',')

                module = echo_string[0][0:(len(echo_string[0]) - 1)]
                data = {
                        'Module': module, 
                        'Timestamp': line[0]
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
                        '''data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string})"
                        data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string})"
                        data[f'SS{i+1}'] = f"{broadcast_string[smart_sleeves[f'ss{i+1}']]} ({echo_string})"'''

                    else:
                        data[f'SS{i+1}'] = echo_string[smart_sleeves[f'ss{i+1}']]
                
            log_writer.writerow(data)
            
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