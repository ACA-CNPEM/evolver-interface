import math

BETA = 3435

def ad_stir(commands): # AD -> %
    return [100*value/98 for value in commands]


def stir_ad(commands): # % -> AD
    command_line = ""
    
    for value in commands:
        command_line += f"{round(98*value/100)},"
        
    return command_line



def ad_temp(commands): # AD -> °C
    command_list = []

    for value in commands:
        voltage = 3.3*value/4095
        resistance_factor = math.log(voltage/(3.3 - voltage)) * 1/BETA
        command_list += [1/((1/298.15) + resistance_factor) - 273.15]

    return command_list

def temp_ad(commands): # °C -> AD
    command_line = ""

    for value in commands:
        exponential_factor = -BETA * (1/(value + 273.15) - 1/298.15)
        value = 4095/(math.exp(exponential_factor) + 1)
        command_line += f"{round(value)},"

    return command_line


def ad_od_led(commands): # AD -> mW/sr
    command_list = []

    for value in commands:
        current = 0.12 * value/4095
        command_list += [0.8125*current + 3.75]

    return command_list


def od_led_ad(commands): # mW/sr -> AD
    command_line = ""

    for value in commands:
        current = (value - 3.75)/0.8125
        command_line += f"{round(4095*current/0.12)},"

    return command_line


def ad_od_135(commands): # 
    command_list = []

    #for value in commands:
        

    return command_list



def input2commands(input_string):
    '''
        This funciton takes an input_string, with values set for the AD, and converts it into a list of command 
        values in real life units

        input (String): input_string e.g. 'tempi,4095,4095,4095,4095, ... ,4095,4095,4095,4095,_!'
        output (float[]): list of commands from input e.g. [20,20,20,20, ..., 20,20,20,20] (°C)
    '''

    input_string = input_string.split(',')
    commands = [float(command) for command in input_string[1:(len(input_string)-1)]]
    module = input_string[0][:(len(input_string[0])-1)]

    if module == 'stir':
        converted = ad_stir(commands)

    elif module == 'temp':
        converted = ad_temp(commands)

    elif module == 'od_led':
        converted = ad_od_led(commands)

    print(commands, module, converted)
    return converted



def commands2input(module, tag, commands):
    '''
        This funciton takes a list of commands and converts it into a command_line with compatible AD values

        input (float[]): list of commands e.g. [8, ... ,50] (%)
        output (String): input_string with commands e.g. 'stiri,8 ... ,49,_!'
    '''
    input_string = module + tag + ","

    if module == 'stir':
        input_string += stir_ad(commands)
    
    elif module == 'temp':
        input_string += temp_ad(commands)
    
    elif module == 'od_led':
        input_string += od_led_ad(commands)

    input_string += "_!"

    print(input_string)
    return input_string


#input2commands('tempe,1200,2048,end')
input2commands('od_ledi,4095,_!')
commands2input('od_led','i',[3.8475])
#input2commands('od_lede,4090,2048,end')