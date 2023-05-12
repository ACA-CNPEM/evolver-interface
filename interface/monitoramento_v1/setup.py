import multiprocessing as mp
import serial
import time

import yaml
from yaml.loader import SafeLoader

from communication import SerialInterface


'''with open('configuration.yaml') as configuration_file:
    config = yaml.load(configuration_file, Loader=SafeLoader)
    smart_sleeves = config['smart_sleeves']
    liquids = config['liquids']
    modules = config['modules']


serial_channel = serial.Serial(
    port = '/dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)
start_time = time.time()'''

starter = 'tempi,'
for i in range(16):
    starter += '2048,'
starter += '_!'
print(starter)