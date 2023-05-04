'''
    Esse script envia o comando para cada SS, de 1 a 8, para ligar seu stir em
    50 (~51%) durante 5s e depois voltar para o estado inicial de 8 (~8%).
'''

import serial
import time

serial_channel = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

def send_messages(command, channel):
    channel.write(str.encode(command))
    time.sleep(1)

    input_string = ""
   
    while channel.in_waiting:
        input_bit = channel.read()
        input_string += input_bit.decode()

        if (input_string.rfind('end') != -1):
            print(input_string)
            break


acknoledgment = 'stira,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,_!'

send_messages('stiri,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,80,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,8,8,8,8,8,8,8,8,8,8,8,8,80,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,8,8,8,8,8,8,8,8,8,80,8,8,8,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,8,8,8,8,8,8,8,8,80,8,8,8,8,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,8,8,8,8,8,80,8,8,8,8,8,8,8,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,8,8,8,8,80,8,8,8,8,8,8,8,8,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,8,80,8,8,8,8,8,8,8,8,8,8,8,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,80,8,8,8,8,8,8,8,8,8,8,8,8,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
time.sleep(5)

send_messages('stiri,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,_!', serial_channel)
serial_channel.write(str.encode(acknoledgment))
