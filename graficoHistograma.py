__author__ = 'LUIZ'

import matplotlib.pyplot as plt




def plotarGrafico(contadorDNS, contadorHTTP,contadorSSH,contadorFTP,contadorUnknown,contadorAll ):

    eixoPacote = [1, 2, 3, 4, 5, 6]
    eixoContador = []

    if (contadorDNS >= 0):
        eixoContador.append(contadorDNS)
    if(contadorHTTP >= 0):
        eixoContador.append(contadorHTTP)
    if(contadorSSH >= 0):
        eixoContador.append(contadorSSH)
    if(contadorFTP >= 0):
        eixoContador.append(contadorFTP)
    if(contadorUnknown >= 0):
        eixoContador.append(contadorUnknown)
    if(contadorAll >= 0):
        eixoContador.append(contadorAll)

    plt.plot(eixoPacote,eixoContador)

    plt.title("Grafico de Pacotes")
    plt.xlabel("Eixo Pacotes")
    plt.ylabel("Eixo Contador")

    plt.show()



