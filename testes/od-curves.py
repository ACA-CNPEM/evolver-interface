import serial
import socket
import numpy as np
import time
import csv
import os


points = np.array([i*40.95 for i in range(101)])
commands = []

for p in points:
    line = "od_ledi,"
    for i in range(16):
        line += f"{p},"
    line += "_!"
    commands += [line]

acknoledgment = 'od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'
read_od = 'od_135l,0,_!'
read_temp = 'templ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'


# Log variables
id = 'log_' + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())
unit = socket.gethostname()
path = f'logs/od-curves/{unit}/{id}'

if not os.path.exists(path):
    os.makedirs(path)


# Serial communication variable
serial_channel = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)


# Function that sends messages to evolver and saves them to log
def send_messages(command, channel):
    channel.write(str.encode(command))
    time.sleep(1)

    input_string = ""
    received_time = time.time()
    
    while channel.in_waiting:
        input_bit = channel.read()
        input_string += input_bit.decode()

        if (input_string.rfind('end') != -1):
            #print(input_string)
            input_string = input_string.split(',')
            module = input_string[0]

            log_data = input_string[1:(len(input_string)-1)]
            log_data.insert(0, received_time)
            log_data.insert(1, module)

            with open(f'{path}/{module}_raw.csv', 'a') as log_file:
                log_writer = csv.writer(log_file, delimiter=',')
                log_writer.writerow(log_data)

            input_string = ""


# Initializing experiment
serial_channel.write(str.encode('stiri,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,_!'))
time.sleep(1)
serial_channel.write(str.encode('stira,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)

serial_channel.write(str.encode('tempi,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,_!'))
time.sleep(1)
serial_channel.write(str.encode('tempa,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)

serial_channel.write(str.encode('od_135i,10,_!'))
time.sleep(1)
serial_channel.write(str.encode('od_135a,10,_!'))
time.sleep(1)

serial_channel.reset_input_buffer()
print("GO!")

for command in commands:
    send_messages(command, serial_channel)
    serial_channel.write(str.encode(acknoledgment))
    time.sleep(5)
    
    for i in range(5):
        send_messages(read_od, serial_channel)


serial_channel.write(str.encode('od_ledi,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)
serial_channel.write(str.encode('od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
print("DONE!!!")