import math

BETA = 3435

def stir_ad(commands): # %
    return [value/98 for value in commands]

def temp_ad(commands): # °C
    return [1/((math.log(value/(4095 - value)) * 1/BETA) + 1/298.15) - 273.15 for value in commands]

def led_ad(commands): # %
    return [1 - value/4095 for value in commands]

def od_ad(commands):
    print(commands)


def input_conversion(input_string):
    input_string = input_string.split(',')
    commands = [float(command) for command in input_string[1:(len(input_string)-1)]]
    module = input_string[0][:(len(input_string[0])-1)]

    if module == 'stir':
        converted = stir_ad(commands)

    elif module == 'temp':
        converted = temp_ad(commands)

    elif module == 'od_led':
        converted = led_ad(commands)

    elif module == 'od_135':
        print(module)

    elif module == 'pump':
        print(module)

    print(commands, module, converted)
    return converted


input_conversion('tempe,1200,2048,end')
input_conversion('stire,8,50,end')
input_conversion('od_lede,4090,2048,end')