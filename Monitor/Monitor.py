# -*- coding: cp1252 -*-
from socket import *
import socketerror
import threading
import Queue
import os
import sys

class Monitor(threading.Thread):
	def __init__(self):
		super(Monitor, self).__init__()
		self.serverPort = 12000 # Porta que o servidor vai monitorar
		self.serverSocket = socket(AF_INET, SOCK_DGRAM) #Cria o Socket UDP (SOCK_DGRAM) para rede IPv4 (AF_INET)
		self.listadecoletores=[]
		self.stoprequest = threading.Event()
		self.logrequest = threading.Event()

		self.sequencia = 0

	def run(self):
		self.serverSocket.bind(('', self.serverPort)) #Associa o Socket criado com a porta desejada

		while not self.stoprequest.isSet():
			if self.logrequest.isSet():
				pass
			else:
				message, clientAddress = self.serverSocket.recvfrom(2048) #Aguarda receber dados do socket
				nome, clientAddress = self.serverSocket.recvfrom(2048) #Aguarda receber dados do socket
				if message.upper() == "ADICIONAR":
					if not clientAddress in self.listadecoletores:
						self.listadecoletores.append((nome, clientAddress))
						print "Novo coletor adicionado. Seu nome e endereço é:",(nome,clientAddress[0])
					else:
						print "O coletor já estava adicionado."
					returnMessage = "adicionado"
					self.serverSocket.sendto(returnMessage, clientAddress)

				print("\nMonitor ON. Digite o numero correspondente as opções:")
				print("\n1-Retomar coleta de pacotes\n2-Parar coleta de pacotes\n3-Baixar log de erros\n4-SAIR\n\n")

		self.serverSocket.close()

	def stop(self):
		self.stoprequest.set()

	def resume(self):
		self.stoprequest.clear()

	def coletar(self, clientAddress):
		message = "coletar"
		self.serverSocket.sendto(message, clientAddress)

	def coletarteste(self, clientAddress):
		message = "coletarteste"
		self.serverSocket.sendto(message, clientAddress)

	def suspender(self, clientAddress):
		message = "parar"
		self.serverSocket.sendto(message, clientAddress)
		print "suspendeu"

	def log(self, n, clientAddress):

########################################## Transferência Confiável - Servidor ###########################################	
		self.logrequest.set()
		self.sequencia = 0
		message = "log"
		self.serverSocket.sendto(message, clientAddress) # envia ordem de baixar o log
		nome_do_arquivo = "logs_"+self.listadecoletores[n-1][0]+".txt" # nome do arquivo de log
		self.serverSocket.sendto(nome_do_arquivo, clientAddress) # envia nome do arquivo de log que deve ser baixado
		arquivo = open(nome_do_arquivo,'w+b') # cria ou abre arquivo para salvar conteudo que será baixado
		print "Criando arquivo"
		while True: # loop infinito
			try:
				ack = 'ACK' # inicia variável ack
				message, clientAddress = self.serverSocket.recvfrom(1024) # recebe pacote com dados e número de sequência
				print "recebeu pedaço do arquivo"
				dados = message.split('&') # separa o pacote e o número de sequência
				pacote = dados[0]
				numero_do_pacote = dados[1]
				print numero_do_pacote
				print self.sequencia
				if pacote == 'fim' and numero_do_pacote == '*': # se for o pacote final sai do loop
					self.serverSocket.sendto('ACK&fim', clientAddress)
					print "Recebeu pacote final"
					break
				else:
					if (int(numero_do_pacote) == self.sequencia): # se não for o pacote final e os números de sequência forem iguais
						print "recebeu pacote ", numero_do_pacote
						print pacote
						arquivo.write(pacote) # escreve o conteudo do pacote no arquivo
						enviar = ack+"&"+str(self.sequencia) # carrega o ack e a sequência
						print enviar
						self.serverSocket.sendto(enviar, clientAddress) # envia o ack do pacote n 
						print "enviou ack ", numero_do_pacote
						self.sequencia += 1 # incrementa a sequência
					elif (int(numero_do_pacote) == (self.sequencia-1)): # se receber o pacote anterior duplicado por conta de timeout
						print "Recebeu pacote duplicado"
						enviar = ack+"&"+str(self.sequencia-1) # carrega o ack do pacote anterior
						self.serverSocket.sendto(enviar, clientAddress) # envia o ack do pacote anterior
						print "Enviou ack do pacote anterior"
			except (KeyboardInterrupt, SystemExit):
				break
		arquivo.close()
		print "fim do download do arquivo"
		self.logrequest.clear()
##################################### ########################################### ######################################	

	def listarcoletores(self):
		n = 1
		print "Coletores ativos:"
		for i in self.listadecoletores:
			print str(n)+'-'+i[0]
			n = n + 1

	def retornaip(self, n):
		ip = self.listadecoletores[n-1][1]
		return ip


def main():
	try:
		monitor = Monitor()
		monitor.start()
		print("\nMonitor ON. Digite o numero correspondente as opções:")

		#######  Menu de Principal  #######
		while 1:
			opcao=raw_input("\n1-Retomar coleta de pacotes\n2-Parar coleta de pacotes\n3-Baixar log de erros\n4-SAIR\n\n")

			#######  Menu de Captura  #######
			if opcao == "1":
				print("\nMenu de captura. Digite o numero correspondente as opções:")
				opcao=raw_input("\n1-Reiniciar captura na rede\n2-Iniciar captura de teste\n\n")
				if opcao == "1":
					if not monitor.listadecoletores:
						print "\nNenhum coletor na rede."
					else:
						print "\nIniciada uma coleta de pacotes..."
						monitor.listarcoletores()
						n = input("Digite o número correspondente ao coletor desejado\n")
						ip = monitor.retornaip(n)
						monitor.coletar(ip)

				elif opcao == "2":
					print "\nIniciada uma coleta de pacotes..."
					monitor.listarcoletores()
					n = input("Digite o número correspondente ao coletor desejado\n")
					ip = monitor.retornaip(n)

					monitor.coletarteste(ip)
				else:
					print "Opção inválida"

			#######  Menu de Suspensão  #######
			elif opcao == "2":
				if not monitor.listadecoletores:
					print "\nNenhum coletor na rede."
				else:
					print "\nParando coleta de Pacotes"
					monitor.listarcoletores()
					n = input("Digite o número correspondente ao coletor desejado\n")
					ip = monitor.retornaip(n)

					monitor.suspender(ip)

			#######  Menu de Logs  #######
			elif opcao == "3":
				if not monitor.listadecoletores:
					print "\nNenhum coletor na rede."
				else:
					print "Em breve"
					print "\nBaixando log..."
					monitor.listarcoletores()
					n = input("Digite o número correspondente ao coletor desejado\n")
					ip = monitor.retornaip(n)
					monitor.log(n,ip)
			#######  SAIR  #######
			elif opcao == "4":
				monitor.stop()
				os._exit(0)
			else:
				print "Opção inválida"

	except:
		print sys.exc_info()[1]
		monitor.stop()
		os._exit(0)
		
if __name__ == '__main__':
	main()