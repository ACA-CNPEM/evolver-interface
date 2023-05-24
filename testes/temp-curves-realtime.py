import serial
import time
from utils import *


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
def send_messages(channel):
    channel.write(str.encode('templ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
    time.sleep(1)

    input_string = ""
    
    while channel.in_waiting:
        input_bit = channel.read()
        input_string += input_bit.decode()

        if (input_string.rfind('end') != -1):
            input_string = input_string.split(',')[1:-1]
            temp = [float(input_string[ss2channel[i]]) for i in range(8)]

            print(f'SS{8}: {temp[7]} --> {ad_temp(temp)[7]}')

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
    send_messages(serial_channel)
    print()
