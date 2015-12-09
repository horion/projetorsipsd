# -*- coding: cp1252 -*-
import os, time
import socket
import socketerror
import pcap, dpkt, re
import threading, Queue
from Captura import *
from LogDeErros import *
import sys

class Coletor(threading.Thread):
	def __init__(self):
		super(Coletor, self).__init__()
		self.stoprequest = threading.Event()
		self.capt = Captura()
		self.capt.nomedocoletor("aluizio") #Para cada máquina virtual esse nome deve mudar

	def run(self):
		while True:
			try:
				if not self.stoprequest.isSet():
					self.capt.captura()
			except (KeyboardInterrupt, SystemExit):
				coletor.stoprequest.set()
				log.setErro(sys.exc_info()[1],nomecoletor)
				print "Um erro ocorreu!"
				os._exit(0)


	def stop(self):
		if not self.stoprequest.isSet():
			self.stoprequest.set()
			self.capt.status("stop")


	def resume(self):
		if self.stoprequest.isSet():
			self.stoprequest.clear()
			self.capt.status("resume")
			print self.stoprequest.isSet()
			print self.capt.stats

	def teste(self):
		if self.stoprequest.isSet():
			self.capt.status("teste")
			self.capt.capturateste()

		else:
			self.capt.status("stop")
			self.capt.status("teste")
			self.capt.capturateste()
		

def main():
	nomecoletor = "aluizio" #Para cada máquina virtual esse nome deve mudar
	log = LogDeErros()
	try:	
		coletor = Coletor()
		serverPort = 12000
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		clientSocket.settimeout(3)
		errorSocket = socketerror.socketError(socket.AF_INET,socket.SOCK_DGRAM)
		errorSocket.setErrorProb(0.1)
		errorSocket.settimeout(1)

		serverAddress = ""
		serverName = '<broadcast>'
		message= ""

		while True:
			message = "adicionar"
			clientSocket.sendto(message,(serverName, serverPort))
			message = nomecoletor
			clientSocket.sendto(message,(serverName, serverPort))
			try:
				returnMessage, serverAddress = clientSocket.recvfrom(2048) #Aguarda receber de retorno
				if returnMessage.upper() == "ADICIONADO":
					print "O coletor foi adicionado\n"
					break
			except socket.timeout:
				print "Sem resposta, enviando nova solicitação."			

		#coletor.start()
		while True:
			print "Aguandando ordens do Monitor\n"
			clientSocket.settimeout(None)
			returnMessage, serverAddress = clientSocket.recvfrom(2048)
			print returnMessage
			if returnMessage.upper() == "COLETAR":
				if coletor.stoprequest.isSet():
					coletor.resume()
				else:
					coletor.start()
			if returnMessage.upper() == "COLETARTESTE":
				coletor.teste()
			if returnMessage.upper() == "PARAR":
				coletor.stop()
				print coletor.isAlive()
			if returnMessage.upper() == "LOG":
	########################################## Transferência Confiável - Client ###########################################	
				numero_do_pacote = 0
				errorSocket.connect((serverAddress))
				nome_do_arquivo, serverAddress = clientSocket.recvfrom(2048) # recebe nome do arquivo de log que deve enviar
				nome_do_arquivo = open(nome_do_arquivo,'r+b') # abre o Arquivo
				lendo_arquivo = nome_do_arquivo.read(40) # lê um pedaço do arquivo e salva numa variável
				while lendo_arquivo: # loop enquanto ainda estiver lendo o arquivo
					receber = '' # inicializando valor padrão
					while (receber != 'ACK'): # loop enquanto não recebe ack
						enviar = lendo_arquivo+"&"+str(numero_do_pacote) # pedaço do arquivo + sequencia do pacote
						errorSocket.sendWithError(enviar) # envia a variável com chance de erro
						print "enviou pedaço do arquivo"
						try:
							print "esperando receber ack"
							msg = errorSocket.recvWithError(1024) # espera 5s para receber ack, se estourar entra no except
							print msg
							dados = msg.split('&') # separa o ack e o número de sequência
							receber = dados[0] # carrega o ack para disparar loop
							if (str(numero_do_pacote) == dados[1]):
								lendo_arquivo = nome_do_arquivo.read(40) # lê próxima parte do arquivo
								numero_do_pacote += 1 # incrementa o número de sequência do pacote
						except (socket.timeout): # tempo de resposta estourou
							print "estourou o tempo"
							break
				nome_do_arquivo.close() # fechando arquivo
				print "fechou o arquivo"
				while True:
					errorSocket.sendWithError("fim&*") # envia pacote final
					try:
						msg = errorSocket.recvWithError(1024) # espera 5s para receber ack, se estourar entra no except
						break
					except socket.timeout: # tempo de resposta estourou
						print "estourou o tempo"
				print "Enviou o fim"
	##################################### ########################################### ######################################	

		clientSocket.close()

	except (KeyboardInterrupt, SystemExit):
		coletor.stoprequest.set()
		log.setErro(sys.exc_info()[1],nomecoletor)
		print "Um erro ocorreu!"
		os._exit(0)

if __name__ == '__main__':
	main()