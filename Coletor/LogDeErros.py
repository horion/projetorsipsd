from datetime import datetime
import os.path

class LogDeErros():
        nome_arq = "logs_aluizio.txt"
	def setErro(self,msg,coletor):
		data = datetime.now()
		self.nome_arq = "logs_"+coletor+".txt"
		arquivo = open(self.nome_arq,"a+")
		arquivo.write(str(data)+" - "+str(msg)+"\n")
		arquivo.close

	def getLog(self):
		if os.path.isfile(self.nome_arq):
			arquivo = open(self.nome_arq,"r")
			msg = arquivo.read()
			arquivo.close
			return msg
		else:
			return "arquivo nao encontrado"