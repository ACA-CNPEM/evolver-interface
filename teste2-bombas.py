import serial
import time

comm = serial.Serial(
    port = '/dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

pump_a = [39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40]
pump_b = [23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24]
pump_c = [7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]

string = 'pumpi,'
parar = string

for i in pump_c:
    parar += '0,'
    if (i <= 7):
        string += '3|4,'
    else:
        string += '0,'

for i in pump_b:
    parar += '0,'
    if (i <= 23):
        string += '1|6,'
    else:
        string += '0,'

for i in pump_a:
    parar += '0,'
    if (i <= 39):
        string += '1|6,'
    else:
        string += '0,'

string += '_!'
parar += '_!'
continuing = 'pumpi,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,_!'
acknowledge = 'pumpa,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,_!'

print(string)
print(parar)
print(continuing)
print(acknowledge)


def envia_string(message):
    comm.write(str.encode(message))
    time.sleep(1)

print(string)
envia_string(string)

time.sleep(5)

print(acknowledge)
envia_string(acknowledge)

while True:
    try:
        pararr = input("Quer parar? ")

        if (pararr):
            print(parar)
            envia_string(parar)

            print(acknowledge)
            envia_string(acknowledge)
    
    except KeyboardInterrupt:
        envia_string(parar)
        envia_string(acknowledge)
