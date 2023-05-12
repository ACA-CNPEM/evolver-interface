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

def envia_string(message):
    comm.write(str.encode(message))
    time.sleep(1)

def recebe_string():
    message = comm.readline().decode()

    while (comm.inWaiting() != 0):
        message += comm.read().decode()

    return message