import math

BETA = 3435

r = 0.3 # cm
d = math.sqrt(5.12*(1 - math.cos(math.pi * 3/4))) # cm
R = math.sqrt(r*r + d*d) # cm
AREA_2_STERADIAN = (r*r*R)/(2*(R - d))


def ad_stir(commands): # AD -> %
    return [100*value/98 for value in commands]


def stir_ad(commands): # % -> AD
    return [round(98*value/100) for value in commands]



def ad_temp(commands): # AD -> °C
    command_list = []

    for value in commands:
        voltage = 3.3*value/4095 # V
        resistance_factor = math.log(voltage/(3.3 - voltage)) * 1/BETA # 1/Kelvin
        command_list += [1/((1/298.15) + resistance_factor) - 273.15]

    return command_list


def temp_ad(commands): # °C -> AD
    command_list = []

    for value in commands:
        exponential_factor = -BETA * (1/(value + 273.15) - 1/298.15)
        value = 4095/(math.exp(exponential_factor) + 1)
        command_list += [round(value)]

    return command_list


def ad_od_led(commands): # AD -> mW/sr
    command_list = []

    for value in commands:
        current = 120 * value/4095 # mA
        command_list += [0.8125*current + 3.75]

    return command_list


def od_led_ad(commands): # mW/sr -> AD
    command_list = []

    for value in commands:
        current = (value - 3.75)/0.8125 # mA
        command_list += [round(4095*current/120)]

    return command_list


def ad_od_135(commands, led_commands): # AD -> [0,1]
    command_list = []
    led_commands = ad_od_led(led_commands)

    for (i,value) in enumerate(commands):
        current = (4095 - value)*3.3/409500 # mA
        irradiance = 0.5/5.5 * (current - 1) + 0.5 # mW/cm²
        #voltage = 3.3*value/4095 - 82*current # V
        command_list += [(irradiance*AREA_2_STERADIAN)/led_commands[i]]

    return command_list


def od_135_ad(commands, led_commands): # [0,1] -> AD
    command_list = []
    led_commands = ad_od_led(led_commands)

    for (i,value) in enumerate(commands):
        irradiance = (value * led_commands[i])/AREA_2_STERADIAN
        current = 5.5/0.5 * (irradiance - 0.5) + 1
        command_list += [round(4095 - current*409500/3.3)]

    return command_list


print(ad_od_135([2048],[4095]))
print(od_135_ad([0.035717642755589626],[4095]))

'''def input2commands(input_string):
    
        This funciton takes an input_string, with values set for the AD, and converts it into a list of command 
        values in real life units

        input (String): input_string e.g. 'tempi,4095,4095,4095,4095, ... ,4095,4095,4095,4095,end'
        output (float[]): list of commands from input e.g. [20,20,20,20, ..., 20,20,20,20] (°C)
    

    input_string = input_string.split(',')
    module = input_string[0][:-1]
    tag = input_string[0][-1]

    commands = [float(command) for command in input_string[1:(len(input_string)-1)]]

    if module == 'stir':
        converted = ad_stir(commands)

    elif module == 'temp':
        converted = ad_temp(commands)

    elif module == 'od_led':
        converted = ad_od_led(commands)

    elif module == 'od_135':
        #get od_led values
        converted = ad_od_135(commands) # led

    print(commands, module, converted)
    return converted



def commands2input(module, commands):
    
        This funciton takes a list of commands and converts it into a command_line with compatible AD values

        input (float[]): list of commands e.g. [8, ... ,50] (%)
        output (String): input_string with commands e.g. 'stiri,8 ... ,49,_!'
    

    if module == 'stir':
        converted = stir_ad(commands)
    
    elif module == 'temp':
        converted = temp_ad(commands)
    
    elif module == 'od_led':
        converted = od_led_ad(commands)

    elif module == 'od_135':
        converted = od_135_ad(commands, [4095])


    return converted


#input2commands('tempe,1200,2048,end')
input2commands('od_135i,4000,_!')
commands2input('od_135','i',[0.03559324257546879])
ad_od_135([2048],[4095])
#input2commands('od_lede,4090,2048,end')'''