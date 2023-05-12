from constants import *
import time
import os

PATH_TO_LOGS = "logs/logs_temp"
date = time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())

#if not os.path.exists(folder_path):
#        os.makedirs(folder_path)

status_temp = [ "0" for i in range(16) ]
comando = "tempi," + ",".join(status_temp) + ",_!"
temp_broadcast = ''
while True:
    evolver_canal.write(str.encode(comando))
    time.sleep(1)

    temp_broadcast = evolver_canal.readline().decode('UTF-8')
    print(temp_broadcast)