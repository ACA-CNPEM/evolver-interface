import serial
import time

# Serial communication variable
serial_channel = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

serial_channel.write(str.encode('stiri,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)
serial_channel.write(str.encode('stira,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))

serial_channel.write(str.encode('tempi,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,_!'))
time.sleep(1)
serial_channel.write(str.encode('tempa,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))

serial_channel.write(str.encode('od_ledi,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))
time.sleep(1)
serial_channel.write(str.encode('od_leda,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,_!'))