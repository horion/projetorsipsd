# esse codigo recebera as mensagem da fila e exibira na tela

import pika
import random
import graficoHistograma as grf

# Conectando ao servidor RabbitMQ
credencial = pika.PlainCredentials('luiz', '113211')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.56.103', 5672, 'filas', credencial))
channel = connection.channel()

# Criando uma fila, apesar de ter sido criado a fila no  programa send.py
# Temos que ter a certeza que a fila existe se nao a mensagem e perdida

channel.queue_declare(queue='HTTP',durable=True)
channel.queue_declare(queue='DNS',durable=True)
channel.queue_declare(queue='SSH',durable=True)
channel.queue_declare(queue='FTP',durable=True)
channel.queue_declare(queue='Unknown',durable=True)
channel.queue_declare(queue='All',durable=True)

contadorHTTP = 0
contadorDNS = 0
contadorSSH = 0
contadorFTP = 0
contadorDesconhecido = 0
contadorAll = 0

valorHTTP = 0
valorDNS = 0
valorSSH = 0
valorFTP = 0
valorDesconhecido = 0
valorAll = 0

listaHTTP = []
listaDNS = []
listaSSH = []
listaFTP = []
listaDesconhecida = []
listaAll = []

# Recebendo Mensagens da fila
# A biblioteca Pika faz a chamada da funcao callback sempre que recebe 
# uma mensagem.

rand = random.randint(1, 1000)


def callBackHTTP(ch, method, properties, body):
    print "[x] Mensagem HTTP recebida %r" % (body,)
    global contadorHTTP
    global valorHTTP
    contadorHTTP += 1
    listaHTTP.append(contadorHTTP)
    valorHTTP = sum(listaHTTP)


def callBackDNS(ch, method, properties, body):
    print "[x] Mensagem DNS recebida %r" % (body,)
    global contadorDNS
    global valorDNS
    contadorDNS += 1
    listaDNS.append(contadorDNS)
    valorDNS = sum(listaDNS)


def callBackSSH(ch, method, properties, body):
    print "[x] Mensagem SSH recebida %r" % (body,)
    global contadorSSH
    global valorSSH
    contadorSSH += 1
    listaSSH.append(contadorSSH)
    valorSSH = sum(listaSSH)


def callBackFTP(ch, method, properties, body):
    print "[x] Mensagem FTP recebida %r" % (body,)
    global contadorFTP
    contadorFTP += 1
    global valorFTP
    listaFTP.append(contadorFTP)
    valorFTP = sum(listaFTP)


def callBackUnknown(ch, method, properties, body):
    print "[x] Mensagem Unknown recebida %r" % (body,)
    global contadorDesconhecido
    contadorDesconhecido += 1
    global valorDesconhecido
    listaDesconhecida.append(contadorDesconhecido)
    valorDesconhecido = sum(listaDesconhecida)


def callBackAll(ch, method, properties, body):
    print "[x] Mensagem All recebida %r" % (body,)
    global contadorAll
    contadorAll += 1
    global valorAll
    listaAll.append(contadorAll)
    valorAll = sum(listaAll)



#grf.plotarGrafico(valorHTTP,valorDNS,valorSSH,valorFTP,valorDesconhecido,valorAll)





    # Informando ao Servidor RabbitMQ que a funcao callback deve receber
    # as mensagens da 'Fila_Mensagens'





channel.basic_consume(callBackHTTP, queue='HTTP', no_ack=True)
channel.basic_consume(callBackDNS, queue='DNS', no_ack=True)
channel.basic_consume(callBackSSH, queue='SSH', no_ack=True)
channel.basic_consume(callBackFTP, queue='FTP', no_ack=True)
channel.basic_consume(callBackUnknown, queue='Unknown', no_ack=True)
channel.basic_consume(callBackAll, queue='All', no_ack=True)

print '[*] Esperando Mensagens. Para sair pressione CTRL + C'

channel.start_consuming()
