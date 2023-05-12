import multiprocessing as mp
import serial
import time


class SerialInterface:
    def __init__(self, serial_configuration):

        self.port = serial_configuration['port']
        self.baudrate = serial_configuration['baudrate']
        self.timeout = serial_configuration['timeout']
        self.delay = serial_configuration['delay']
        self.incoming_end = serial_configuration['incoming_end']
        
        self.serial_channel = serial.Serial(
            port = self.port,
            baudrate = self.baudrate,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = self.timeout
        )
        self.start_time = time.time()
    
        self.received = mp.Queue()
        self.sent = mp.Queue()

        self.to_send = mp.Queue()


    def close_serial(self):
        self.serial_channel.close()


    def add_command(self, message):
        self.to_send.put(message)


    def serial_event(self):
        while True:
            if not self.to_send.empty():
                message = self.to_send.get()
                message = str.encode(message)

                self.serial_channel.write(message)
                self.sent.put([time.time(), message])
                time.sleep(0.5)
            
            input_string = ""

            while self.serial_channel.in_waiting:
                input_bit = self.serial_channel.read()
                input_string += input_bit.decode('utf-8')

                if (input_string.rfind(self.incoming_end) != -1):
                    print(input_string)
                    self.received.put([time.time(), input_string])
                    input_string = ""


























'''def reading_input(channel):
    serial_input = ""

    while channel.in_waiting:
        input_bit = channel.read()
        serial_input += input_bit

        if (input_bit == 'd' and serial_input.rfind('n') == len(serial_input - 1)): # end
            print(serial_input)
            
interface.analyze_input(serial_input)

                if (interface.get_address_found()):
                    print(serial_input)
                    interface.set_address_found(False)
                    break

class SerialInterface:
    def __init__(self, start_mark, end_mark, frame):
        self._start_mark = start_mark
        self._end_mark = end_mark
        self._frame = frame
        self._address_found = False
        self._message_log = mp.Queue()

    def get_start(self):
        return self._start_mark
    
    def get_end(self):
        return self._end_mark
    
    def get_frame(self):
        return self._frame
    
    def get_address_found(self):
        return self._address_found
    
    def set_address_found(self, status):
        self._address_found = status

    def add_to_log(self, command_line):
        self._message_log.put([time.time(), command_line])
    

    def reading_input(self, channel):
        serial_input = ""

        while channel.in_waiting:
            input_bit = channel.read()
            serial_input += input_bit

            if (input_bit == 'd' and serial_input.rfind('n') == len(serial_input - 1)): # end
                interface.analyze_input(serial_input)

                if (interface.get_address_found()):
                    print(serial_input)
                    interface.set_address_found(False)
                    break

    def analyze_input(self, input_string):
        # selecting only the desired command, that corresponds with the start mark
        start_index = input_string.rfind(self.get_start())
        end_index = input_string.rfind(self.get_end())

        if (start_index != -1 and end_index != -1):
            input_string = input_string[start_index:(end_index + len(self.get_end()))]
            print(input_string)

            # since the serial channel is cleared from time to time, there might be extra start and end marks
            # therefore we should repeat the previous step
            start_index = input_string.rfind(self.get_start())
            end_index = input_string.rfind(self.get_end())
            input_string = input_string[start_index:(end_index + len(self.get_end()))]

            # now we must check the number of commands sent, to be sure its a valid command line
            command_list = input_string.split(',')
            command_list = command_list[1:(len(command_list) - 1)]
            
            if (len(command_list) == self.get_frame()):
                self.set_address_found(True)
                self.add_to_log(command_list)
                print(command_list)




def serial_monitoring(interface):
    serial_input = ""

    while serial_comm.in_waiting:
        input_bit = serial_comm.read().decode()
        serial_input += input_bit

        if (serial_input.rfind('end') != -1): # end
            interface.analyze_input(serial_input)
            
            if (interface.get_address_found()):
                interface.set_address_found(False)
                break
                #serial_input = '''''