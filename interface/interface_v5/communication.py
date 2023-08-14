import multiprocessing as mp
import serial
import time
from constants import *


def leitura(canal, delay):
    time.sleep(delay)

    mensagem = canal.readline().decode('UTF-8')
    print(mensagem)


if __name__ == '__main__':
    leitura(evolver_canal, evolver_delay)


'''def reading(channel, delay, messages):
    while True:
        time.sleep(delay)
        messages += [(time.time(), channel.readline().decode('UTF-8'))]



class EvolverSerialCommunication:

    def __init__(self, channel):
        self.channel = channel
        self.messages = []
        self.queue = mp.Queue()

        self.reading_process = mp.Process(target=reading, args=[channel, 0.1, self.messages])
        

    def starting(self):
        self.reading_process.start()
        self.reading_process.join()

    def reading_commands(self):
        if (len(self.messages) > 0):
            return self.messages[-1]'''

    

    

        