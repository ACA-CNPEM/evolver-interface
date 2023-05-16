import serial
import time
import csv
import os
import yaml
from yaml.loader import SafeLoader
import socket

# Log variables
type = 'od-1'
id = 'log_' + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())
unit = socket.gethostname()
path = f'logs/interference-tests/{unit}/{type}/{id}'

if not os.path.exists(path):
    os.makedirs(path)


# Configuration variables
with open('configuration.yaml') as configuration_file:
    config = yaml.load(configuration_file, Loader=SafeLoader)
    commands = config['interference-tests'][type]
    acknoledgment= config['acknoledgment']



# Serial communication variable
serial_channel = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

def creates_command(module, command_list):
    command_string = f'{module}i,'

    for command in command_list:
        command_string += f'{command},'

    return command_string + '_!'


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
            input_string = input_string.split(',')
            module = input_string[0]

            log_data = input_string[1:(len(input_string)-1)]
            log_data.insert(0, received_time)
            log_data.insert(1, module)

            with open(f'{path}/{file_name}.csv', 'a') as log_file:
                log_writer = csv.writer(log_file, delimiter=',')
                log_writer.writerow(log_data)

            input_string = ""


if type == 'od-1':
    for module in ['temp','od_135','pump']:
        
        serial_channel.write(str.encode(creates_command(module, commands[module])))
        time.sleep(1)
        serial_channel.write(str.encode(acknoledgment[module]))
        time.sleep(1)
        serial_channel.reset_input_buffer()
        
    for od_command in commands['od_led']:
        od_command_string = creates_command('od_led', od_command)
        send_messages(type, od_command_string, serial_channel)
        serial_channel.write(str.encode(acknoledgment['od_led']))

        time.sleep(5)

        for stir_command in commands['stir']:
            command_string = creates_command('stir', stir_command)
            send_messages(type, command_string, serial_channel)
            serial_channel.write(str.encode(acknoledgment['stir']))

            for i in range(10):
                send_messages(type, 'od_135l,0,_!', serial_channel)
        
        send_messages(type, 'templ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!', serial_channel)

if type == 'od-2':
    for module in ['stir','od_135','pump']:
        
        serial_channel.write(str.encode(creates_command(module, commands[module])))
        time.sleep(1)
        serial_channel.write(str.encode(acknoledgment[module]))
        time.sleep(1)
        serial_channel.reset_input_buffer()
    
    for temp_command in commands['temp']:
        temp_command_string = creates_command('temp', temp_command)
        send_messages(type, temp_command_string, serial_channel)
        serial_channel.write(str.encode(acknoledgment['temp']))

        time.sleep(5)

        for od_command in commands['od_led']:
            command_string = creates_command('od_led', od_command)
            send_messages(type, command_string, serial_channel)
            serial_channel.write(str.encode(acknoledgment['od_led']))

            for i in range(10):
                send_messages(type, 'od_135l,0,_!', serial_channel)
                send_messages(type, 'templ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!', serial_channel)

if type == 'temp-1':
    for module in ['od_led','od_135','pump']:
        
        serial_channel.write(str.encode(creates_command(module, commands[module])))
        time.sleep(1)
        serial_channel.write(str.encode(acknoledgment[module]))
        time.sleep(1)
        serial_channel.reset_input_buffer()
    
    for temp_command in commands['temp']:
        temp_command_string = creates_command('temp', temp_command)
        send_messages(type, temp_command_string, serial_channel)
        serial_channel.write(str.encode(acknoledgment['temp']))

        time.sleep(5)

        for stir_command in commands['stir']:
            command_string = creates_command('stir', stir_command)
            send_messages(type, command_string, serial_channel)
            serial_channel.write(str.encode(acknoledgment['stir']))

            for i in range(10):
                send_messages(type, 'templ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!', serial_channel)


if type == 'temp-2':
    for module in ['stir','od_led','od_135','pump']:
        
        serial_channel.write(str.encode(creates_command(module, commands[module])))
        time.sleep(1)
        serial_channel.write(str.encode(acknoledgment[module]))
        time.sleep(1)
        serial_channel.reset_input_buffer()
    
    for temp_command in commands['temp']:
        temp_command_string = creates_command('temp', temp_command)
        send_messages(type, temp_command_string, serial_channel)
        serial_channel.write(str.encode(acknoledgment['temp']))

        for i in range(20):
            send_messages(type, 'od_135l,0,_!', serial_channel)
            send_messages(type, 'templ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!', serial_channel)

'''
for i in ['2450', '2148', '1846', '1544', '1242', '940']:
    a = []
    for j in range(16):
        a += [i]
    print(a)
'''
            