# esse codigo recebera as mensagem da fila e exibira na tela

import pika

# Conectando ao servidor RabbitMQ
credencial = pika.PlainCredentials('luiz','113211')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.56.102',5672,'filas',credencial))
channel = connection.channel()

# Criando uma fila, apesar de ter sido criado a fila no  programa send.py
# Temos que ter a certeza que a fila existe se nao a mensagem e perdida

channel.queue_declare(queue='HTTP')
channel.queue_declare(queue='DNS')
channel.queue_declare(queue='SSH')
channel.queue_declare(queue='FTP')
channel.queue_declare(queue='Unknown')
channel.queue_declare(queue='All')

contadorHTTP= 0
contadorDNS = 0
contadorSSH = 0
contadorFTP = 0
contadorDesconhecido = 0
contadorAll = 0

# Recebendo Mensagens da fila
# A biblioteca Pika faz a chamada da funcao callback sempre que recebe 
# uma mensagem.


def callBackHTTP(ch, method, properties, body):
	print "[x] Mensagem HTTP recebida %r" %(body,)
	global contadorHTTP
	contadorHTTP += 1
	print contadorHTTP
	
def callBackDNS(ch,method,properties,body):
	print "[x] Mensagem DNS recebida %r" %(body,)
	global contadorDNS
	contadorDNS += 1
	print contadorDNS
def callBackSSH(ch,method,properties,body):
	print "[x] Mensagem SSH recebida %r" %(body,)
	global contadorSSH
	contadorSSH += 1
	print contadorSSH
def callBackFTP(ch,method,properties,body):
	print "[x] Mensagem FTP recebida %r" %(body,)
	global contadorFTP
	contadorFTP += 1
	print contadorFTP
def callBackUnknown(ch,method,properties,body):
	print "[x] Mensagem Unknown recebida %r" %(body,)
	global contadorDesconhecido
	contadorDesconhecido += 1 
	print contadorDesconhecido
def callBackAll(ch,method,properties,body):
	print "[x] Mensagem All recebida %r" %(body,)
	global contadorAll
	contadorAll += 1
	print contadorAll
	
# Informando ao Servidor RabbitMQ que a funcao callback deve receber
# as mensagens da 'Fila_Mensagens'

if tupla.contains("http") > 0:
	channel.basic_consume(callBackHTTP, queue='HTTP', no_ack=True)
channel.basic_consume(callBackDNS, queue='DNS', no_ack=True)
channel.basic_consume(callBackSSH, queue='SSH', no_ack=True)
channel.basic_consume(callBackFTP, queue='FTP', no_ack=True)
channel.basic_consume(callBackUnknown, queue='Unknown', no_ack=True)
channel.basic_consume(callBackAll, queue='All', no_ack=True)


print '[*] Esperando Mensagens. Para sair pressione CTRL + C'
channel.start_consuming()
 
