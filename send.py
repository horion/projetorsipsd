# Codigo que mostra um exemplo de como enviar uma unica mensagem para a fila

import pika


# Estabelecendo uma conexao com o servidor RabbitMQ na maquina local - localhost
# para se conectar em uma maquina diferente temos que especificar o endereco IP
credencial = pika.PlainCredentials('luiz','113211')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.56.102',5672,'filas',credencial))

channel = connection.channel()

# Criando uma fila para qual a mensagem sera entregue,
# sera nomeada 'Fila_Mensagens'

channel.queue_declare(queue = 'HTTP')
channel.queue_declare(queue = 'DNS')
channel.queue_declare(queue = 'SSH')
channel.queue_declare(queue = 'FTP')
channel.queue_declare(queue = 'Unknown')
channel.queue_declare(queue = 'All')

channel.basic_publish(exchange='',routing_key='HTTP',body='Testando fila distribuida HTTP')
channel.basic_publish(exchange='',routing_key='DNS',body='Testando fila Distribuida DNS')
channel.basic_publish(exchange='',routing_key='SSH',body='Testando fila Distribuida SSH')
channel.basic_publish(exchange='',routing_key='FTP',body='Testando fila Distribuida FTP')
channel.basic_publish(exchange='',routing_key='Unknown',body='Testando fila Distribuida Desconhecida')
channel.basic_publish(exchange='',routing_key='All',body='Testando fila Distribuida Todos')


print "[x] Mensagem Enviada!"

connection.close()
