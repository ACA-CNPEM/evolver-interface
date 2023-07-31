import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt


##### AUXILIARY VARIBALES #####
BETA = 3435

r = 0.3 # cm
d = math.sqrt(5.12*(1 - math.cos(math.pi * 3/4))) # cm
R = math.sqrt(r*r + d*d) # cm
AREA_2_STERADIAN = (r*r*R)/(2*(R - d))


def sigmoid(x, a, b, c, d):
    return a + (b - a)/(1 + (10**((c-x)*d)))


def d_sigmoid(x, a, b, c, d):
    return (np.log(10)*(b-a)*d*10**(d*(c-x)))/(1+10**(d*(c-x)))**2


def ad_od135(x, a, b, c, d):

    if type(x) != list:
        ad = np.clip(np.array([x]), math.ceil(a), math.floor(b))
    elif type(x) != np.ndarray:
        ad = np.clip(np.array(x), math.ceil(a), math.floor(b))
    else:
        ad = np.clip(x, math.ceil(a), math.floor(b))
            
    return c - np.log10((b-a)/(ad-a) - 1)/d


def ad_stir(commands): # AD -> %
    commands = np.clip(np.array(commands), 0, 98)
    return [100*value/98 for value in commands]


def stir_ad(commands): # % -> AD
    commands = np.clip(np.array(commands), 0, 100)
    return [round(98*value/100) for value in commands]


def ad_temp(commands): # AD -> °C
    command_list = []

    # limitando entre cerca de 15°C a 60°C
    commands = np.clip(np.array(commands), 940, 2450)

    for value in commands:
        voltage = 3.3*value/4095 # V
        resistance_factor = math.log(voltage/(3.3 - voltage)) * 1/BETA # 1/Kelvin
        command_list += [1/((1/298.15) + resistance_factor) - 273.15]

    return command_list


def temp_ad(commands): # °C -> AD
    command_list = []

    # limitando entre cerca de 15°C a 60°C
    commands = np.clip(np.array(commands), 15, 60)

    for value in commands:
        exponential_factor = -BETA * (1/(value + 273.15) - 1/298.15)
        value = 4095/(math.exp(exponential_factor) + 1)
        command_list += [round(value)]

    return command_list


def ad_od_led(commands): # AD -> mW/sr
    command_list = []

    # limitando entre completamente desligado ou ligado
    commands = np.clip(np.array(commands), 0, 4095)

    for value in commands:
        current = 50 * value/4095 # mA
        command_list += [0.8125*current + 3.75]

    return command_list


def od_led_ad(commands): # mW/sr -> AD
    command_list = []

    # limitando entre completamente desligado ou ligado
    commands = np.clip(np.array(commands), 3.75, 101.25)

    for value in commands:
        current = (value - 3.75)/0.8125 # mA
        command_list += [round(4095*current/50)]

    return command_list




if __name__ == "__main__":
    '''ad = [i for i in range(4096)]
    ad_ = [i for i in range(100)]

    temp = ad_temp(ad)
    led = ad_od_led(ad)
    stir = ad_stir(ad_)

    a,b,c = np.polyfit(ad[940:2450], temp[940:2450] ,2)
    fit = [a*i*i + b*i + c for i in ad]

    plt.plot(ad, temp, color='y')
    plt.plot(ad[940:2450], fit [940:2450], linestyle='--', label='y = ' + '{:.2f}'.format(c) + ' + {:.2f}'.format(b) + 'x + {:.2f}'.format(c) + 'x²')

    plt.title('Curva de conversão: AD para °C')
    plt.legend()

    plt.xlabel('Leitura AD')
    plt.ylabel('Temperatura (°C)')
    plt.show()

    a,b = np.polyfit(ad,led,1)
    fit = [a*i + b for i in ad]
    plt.plot(ad, led, color='y')
    plt.plot(ad, fit, linestyle='--', label='y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x')

    plt.title('Curva de conversão: AD para mW/sr')
    plt.legend()

    plt.xlabel('Leitura AD')
    plt.ylabel('Intensidade Radiante (mW/sr)')
    plt.show()

    a,b = np.polyfit(ad_, stir ,1)
    fit = [a*i + b for i in ad_]
    
    plt.plot(ad_, stir, color='y')
    plt.plot(ad_, fit, linestyle='--', label='y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x')

    plt.title('Curva de conversão: AD para %')
    plt.legend()

    plt.xlabel('Leitura AD')
    plt.ylabel('Rotação relativa (%)')
    plt.show()

    led = [4095 for i in calibration['max']]
    a,b = np.polyfit(calibration['max'], ad_od_135(calibration['max'], led), 1)
    fit = [a*i + b for i in calibration['max']]

    plt.plot(calibration['max'], ad_od_135(calibration['max'], led),color='y')
    plt.plot(calibration['max'], fit, linestyle='--', label='y = ' + '{:.2f}e-6'.format(b*1000000) + ' + {:.2f}'.format(a*1000000) + 'e-6 x')
    
    plt.title('Curva de conversão: AD para coeficiente de transmissão')
    plt.legend()

    plt.xlabel('Leitura AD')
    plt.ylabel('Transmissão (adimensional)')
    plt.show()'''