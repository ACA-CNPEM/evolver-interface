from communication import *

stir_si = SerialInterface('stir', 'end', 16)
temp_si = SerialInterface('tmep', 'end', 16)

stir_serial = mp.Process(target=serial_monitoring, args=[stir_si])
temp_serial = mp.Process(target=serial_monitoring, args=[temp_si])

stir_serial.start()
#temp_serial.start()

#stir_serial.join()
#temp_serial.join()'''