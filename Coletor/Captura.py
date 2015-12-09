# -*- coding: cp1252 -*-
import time
import pcap, dpkt, re
from os import system
from LogDeErros import *
import sys
from Producer import *
from threading import *

class Captura():
	"""Classe que ira capturar pacotes"""
	def __init__(self):
		self.stats = "resume"
		self.log = LogDeErros()
		self.nomecoletor = ""
		self.contaSemIP = 0
		self.contaUDP = 0
		self.contaTCP = 0
		self.contaPacote=0
		self.fluxo={}
		self.timer={}
		self.time=5
		self.producer = Produtor()


	def nomedocoletor(self,nome):
		self.nomecoletor = nome

	def status(self, arg):
		self.stats = arg
		print "Mudou status de captura para:", arg

	def assinar(self):
		file = open('l7-pat/dns.pat').readlines()
		expr = file[0]
		dns = re.compile(expr)
		file = open('l7-pat/ftp.pat').readlines()
		expr = file[0]
		ftp = re.compile(expr)
		file = open('l7-pat/http.pat').readlines()
		expr = file[0]
		http = re.compile(expr)
		file = open('l7-pat/ssh.pat').readlines()
		expr = file[0]
		ssh = re.compile(expr)
		file = open('l7-pat/bittorrent.pat').readlines()
		expr = file[0]
		bittorrent = re.compile(expr)
		file = open('l7-pat/dhcp.pat').readlines()
		expr = file[0]
		dhcp = re.compile(expr)
		file = open('l7-pat/ssdp.pat').readlines()
		expr = file[0]
		ssdp = re.compile(expr)
		file = open('l7-pat/ssl.pat').readlines()
		expr = file[0]
		ssl = re.compile(expr)

		assinaturas = {"dns":dns,"ftp":ftp,"http":http,"ssh":ssh,"bittorrent":bittorrent,"dhcp":dhcp,"ssdp":ssdp,"ssl":ssl}
		return assinaturas

	def capturateste(self):
		try:
			for ts, pkt in pcap.pcap("test-capture.pcap"):
				if self.stats == "teste":
					eth = dpkt.ethernet.Ethernet(pkt)
					ip = eth.data
					if isinstance(ip,dpkt.ip.IP):
						ipsrc = ip.src
						ipdst = ip.dst
						protocolo = ip.p
						transp = ip.data
						if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
							if isinstance(ip.data,dpkt.tcp.TCP):
								self.contaTCP += 1
							elif isinstance(ip.data,dpkt.udp.UDP):
								self.contaUDP += 1
							portsrc = transp.dport
							portdest = transp.sport
							key=str(ipsrc)+str(portsrc)+str(ipdst)+str(portdest)+str(protocolo)
							if not key in self.fluxo:
								self.fluxo[key] = [(ts,ip)]
								self.conta_timeout_fluxo(key)
							else:
								self.fluxo[key].append((ts,ip))
								self.conta_timeout_fluxo(key)		
					else:
						self.contaSemIP += 1
						print "Pacote sem IP"
				if self.stats == "resume":
					self.captura()
				if self.stats == "":
					print "Coletor suspenso"
					system("clear")
			self.status("stop")
		except (KeyboardInterrupt, SystemExit):
			self.log.setErro(sys.exc_info()[1],self.nomecoletor)
			print "Erro ao fazer captura de teste."
			self.status("stop")
			os._exit(0)

	def captura(self):
		try:
			for ts, pkt in pcap.pcap():
				if self.stats == "resume":
					eth = dpkt.ethernet.Ethernet(pkt)
					ip = eth.data
					if isinstance(ip,dpkt.ip.IP):
						ipsrc = ip.src
						ipdst = ip.dst
						protocolo = ip.p
						transp = ip.data
						if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
							if isinstance(ip.data,dpkt.tcp.TCP):
								self.contaTCP += 1
							elif isinstance(ip.data,dpkt.udp.UDP):
								self.contaUDP += 1
							portsrc = transp.dport
							portdest = transp.sport
							key=str(ipsrc)+str(portsrc)+str(ipdst)+str(portdest)+str(protocolo)
							if not key in self.fluxo:
								self.fluxo[key] = [(ts,ip)]
								self.conta_timeout_fluxo(key)
							else:
								self.fluxo[key].append((ts,ip))
								self.conta_timeout_fluxo(key)
							print key		
					else:
						self.contaSemIP += 1
						print "Pacote sem IP"

				if self.stats == "teste":

					self.capturateste()

				if self.stats == "stop":
					for i in self.timer:
						self.timer[i].cancel()
					print "Coletor suspenso"
					break
		except (KeyboardInterrupt, SystemExit):
			self.log.setErro(sys.exc_info()[1],self.nomecoletor)
			print "Erro ao fazer captura."
			os._exit(0)

	def classifica_fluxo(self, fluxo): # recebe uma lista no formato: [(ts,pkt),(ts,pkt)]
		self.protocols = self.assinar()
		achou=False
		for item in fluxo:
			app = item[1].data.data.lower()
			for p in self.protocols.items():
				if p[1].search(app):
					achou = True
					protocolo = p[0]
			if achou:
				return protocolo
			else:
				return "nenhum"

	def calcula_tempo_fluxo(self, fluxo): # recebe uma lista no formato: [(ts,pkt),(ts,pkt)]
		tempo_inicial = fluxo[0][0]
		tempo_final = fluxo[-1][0]
		duracao = tempo_final - tempo_inicial
		return duracao

	def calcula_tamanho_fluxo(self, fluxo): # recebe uma lista no formato: [(ts,pkt),(ts,pkt)]
		tamanho=0
		for pacote in fluxo:
			tamanho+=pacote[1].len
			return tamanho

	def conta_timeout_fluxo(self, key): # recebe uma string que é key de um fluxo em um dicionário
		if key in self.timer:
			self.timer[key].cancel()
		self.timer[key] = Timer(self.time,self.finaliza_fluxo,args=[key])
		self.timer[key].start()
			

	def finaliza_fluxo(self, key): # recebe uma string que é key de um fluxo em um dicionário
		self.cria_tupla(self.fluxo[key])
		del(self.fluxo[key])


	def cria_tupla (self, fluxo):
		protocolo =  self.classifica_fluxo(fluxo)
		tempo = self.calcula_tempo_fluxo(fluxo)
		tempo = tempo * 0.001
		tamanho = self.calcula_tamanho_fluxo(fluxo)
		tamanho = tamanho / 1024.0
		if tempo > 0 and tamanho > 0:
			taxa = tamanho / tempo
			tupla = (protocolo,"%.6f" % tamanho,"%.6f" % tempo,"%.6f" % taxa)
			print "Tupla gerada:", tupla
			#self.enviarTupla(tupla)

	def enviarTupla(self,tupla):
            credencial = pika.PlainCredentials('luiz', '113211')
            connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.56.103', 5672, 'filas', credencial))

            channel = connection.channel()



       	    channel.queue_declare(queue='HTTP')
            channel.queue_declare(queue='DNS')
            channel.queue_declare(queue='SSH')
            channel.queue_declare(queue='FTP')
            channel.queue_declare(queue='Unknown')
            channel.queue_declare(queue='All')

            if('http' in tupla or 'HTTP' in tupla):
            	channel.basic_publish(exchange='', routing_key='HTTP', body=str(tupla))
            elif('dns' in tupla or 'DNS' in tupla):
            	channel.basic_publish(exchange='', routing_key='DNS', body=str(tupla))
            elif('ssh' in tupla or 'SSH' in tupla):
            	channel.basic_publish(exchange='', routing_key='SSH', body=str(tupla))
            elif('ftp' in tupla or 'FTP' in tupla):
            	channel.basic_publish(exchange='', routing_key='FTP', body=str(tupla))
            elif(('dns' in tupla or 'DNS' in tupla) or ('http' in tupla or 'HTTP' in tupla) or ('ssh' in tupla or 'SSH' in tupla) or ('ftp' in tupla or 'FTP' in tupla)):
            	channel.basic_publish(exchange='', routing_key='All', body=str(tupla))
            else:
            	channel.basic_publish(exchange='', routing_key='Unknown', body=str(tupla))
            	channel.basic_publish(exchange='', routing_key='All', body=str(tupla))


            print "[x] Mensagem Enviada!"
