from constants import *

def leitura_input(pergunta):
    try:
        resposta = int(input(pergunta))
    except ValueError:
        resposta = 0
    return resposta


def leitura_pump_input(pergunta):
    resposta = input(pergunta)

    if (resposta.find('|') >= 0):
        resposta_copia = resposta.split('|')

        if(len(resposta_copia) > 2):
            resposta = '--'
        else:
            try:
                resposta_copia[0] = int(resposta_copia[0])
                resposta_copia[1] = int(resposta_copia[1])
                resposta = f'{resposta_copia[0]}|{resposta_copia[1]}'
            except:
                resposta = '--'
    else:
        try:
            resposta = int(resposta)
        except ValueError:
            resposta = '--'
    
    return resposta


def envia_comando(comando):
    canal.write(str.encode(comando))