import serial
import time

pump2ss =[[39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40],[23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24],[7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]]

# Serial communication variable
serial_channel = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)


command_stirng = 'pumpi,30,30,30,30,30,30,30,30,--,--,--,--,--,--,--,--,0,0,0,0,0,0,0,0,--,--,--,--,--,--,--,--,0,0,0,0,0,0,0,0,--,--,--,--,--,--,--,--,_!'


serial_channel.write(str.encode(command_stirng))
time.sleep(1)

serial_channel.write(str.encode('pumpa,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,_!'))
