import serial

evolver_canal = serial.Serial(
    port = '/dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

evolver_delay = 0.1

ss_ativas = [1,2,3,4,5,6,7,8]
liquidos_ativos = [0,1,2]

titulo = 'Qual Smart Sleeve gostaria de alterar?\n(use ESPAÇO para selecionar e ENTER para continuar) '

liquidos = { 0: "Líquido A", 1: "Líquido B", 2: "Líquido C"}

convert = {
    "channel2ss": [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1],
    "ss2channel": [-1,15,14,11,10,7,6,3,2],

    "pump2ss": [8,7,6,5,4,3,2,1,16,15,14,13,12,11,10,9],
    "ss2pump": [[-1,39,38,37,36,35,34,33,32,47,46,45,44,43,42,41,40],
                [-1,23,22,21,20,19,18,17,16,31,30,29,28,27,26,25,24],
                [-1,7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]],
}

status = {
    "stir": [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8], # [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #
    "temp": [4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095], # [16,15,8,7,14,13,6,5,12,11,4,3,10,9,2,1], #
    "od_135": 1000,
    "od_led": [4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095,4095], # [1600,1500,800,700,1400,1300,600,500,1200,1100,400,300,1000,900,200,100], #
    "pump": ['--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--',] # [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47] #
}