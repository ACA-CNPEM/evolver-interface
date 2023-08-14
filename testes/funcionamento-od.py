import serial
import time

ss2channel = [15,14,11,10,7,6,3,2,13,12,9,8,5,4,1,0]

channel = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

ss = 0

command = 'od_ledi,'

for i in range(16):
    if(ss2channel.index(i) + 1 == ss):
        command += '4095,'
    else:
        command += '0,'
command += '_!'

channel.write(str.encode(command))
time.sleep(1)
channel.write(str.encode('od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(5)

input_string = ""
while channel.in_waiting:
    input_bit = channel.read()
    input_string += input_bit.decode()

    if (input_string.rfind('end') != -1):
        input_string = input_string.split(',')[1:-1]

        for i in range(8):
            print(f'SS{i+1}: {input_string[ss2channel[i]]}')
        
        input_string = ""

print()
message = str.encode('od_135l,0,_!')
channel.write(message)
time.sleep(20)

input_string = ""
    
while channel.in_waiting:
    input_bit = channel.read()
    input_string += input_bit.decode()

    if (input_string.rfind('end') != -1):
        input_string = input_string.split(',')[1:-1]

        for i in range(8):
            print(f'SS{i+1}: {input_string[ss2channel[i]]}')
        
        input_string = ""