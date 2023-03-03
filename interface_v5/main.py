from pick import pick

print("\n ****** Inicializando a interface! ******\n")

parametros = ['Agitação', 'Temperatura', 'Turbidez', 'Fluxo de fluidos', 'SAIR']
parametro_selecionado = pick(parametros, 'Selecione o parâmetro que deseja alterar: ', indicator='>>')

if (parametro_selecionado[1] == 0):
    print("Agitação")











print("\n ****** Encerrando a iteração. Volte logo! ******\n")