import serial
import time
from utils import *
import os 
import socket


id = 'log_' + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())
unit = socket.gethostname()
path = f'logs/temp-curves-realtime/{unit}/{id}'

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


ss2channel = [15,14,11,10,7,6,3,2,13,12,9,8,5,4,1,0]


# Function that sends messages to evolver and saves them to log
def send_messages(name, channel):
    channel.write(str.encode('templ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
    time.sleep(1)

    input_string = ""
    received_time = time.time()
    
    while channel.in_waiting:
        input_bit = channel.read()
        input_string += input_bit.decode()

        if (input_string.rfind('end') != -1):
            input_string = input_string.split(',')[1:-1]
            input_string.insert(0, received_time)
            
            with open(f'{name}/raw.csv', 'a') as log_file:
                log_writer = csv.writer(log_file, delimiter=',')
                log_writer.writerow(input_string)

            input_string = ""



# Initializing experiment
serial_channel.write(str.encode('stiri,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)

serial_channel.write(str.encode('stira,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)

serial_channel.write(str.encode('od_ledi,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)

serial_channel.write(str.encode('od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)

a = 4095
command_stirng = 'tempi,'

for j in range(16):
    command_stirng += f'{a},'

command_stirng += '_!'

serial_channel.write(str.encode(command_stirng))
time.sleep(1)
serial_channel.write(str.encode('tempa,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)

serial_channel.reset_input_buffer()
print("GO!")




while True:
    send_messages(path, serial_channel)
