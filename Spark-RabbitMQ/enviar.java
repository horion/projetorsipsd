package com.stratio.example.receber;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Random;

import javax.net.ssl.HttpsURLConnection;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

public class enviar {

	private final static String QUEUE_RATO = "Rato";
	private final static String QUEUE_ELEFANTE = "Elefante";
	private final static String QUEUE_TARTARUGA = "Tartaruga";
	private final static String QUEUE_LIBELULA = "Libelula";
	private final static String QUEUE_CARAMUJO = "Caramujo";
	private final static String QUEUE_GUEPARDO = "Guepardo";
	
	private final static Long ZERO_LONG = 0L;

	final Long PARAMETRO_TAMANHO = 152L;
	final Long PARAMETRO_DURACAO = 720L;
	final Long PARAMETRO_TAXA = 101L;

	private String tipo = new String();
	private String duracao = new String();
	private String tamanho = new String();
	private String taxa = new String();

	private String hostname = "192.168.56.102";
	private int portNumber = 5672;
	private String virtualHost = "classificadas";
	private String username = "luiz";
	private String password = "113211";
	
	
	String tamanhoClassificado;
	String duracaoClassificado;
	String taxaClassificado;
	
	private static File arquivo = new File("/home/mininet/aluizio/rsi-psd/sequence.txt");
	Long sequence = new Long(0);

	public void enviarTupla(String message) throws java.io.IOException {

		System.out.println("###### INICIANDO ######");
		System.out.println("###### CRIANDO CONEXÃO ######");

		ConnectionFactory factory = new ConnectionFactory();
		factory.setHost(hostname);
		factory.setPort(portNumber);
		factory.setVirtualHost(virtualHost);
		factory.setUsername(username);
		factory.setPassword(password);

		System.out.println("###### DECLARANDO FILAS ######");

		Connection connection = factory.newConnection();
		Channel channel = connection.createChannel();
		channel.queueDeclare(QUEUE_RATO, true, false, false, null);
		channel.queueDeclare(QUEUE_ELEFANTE, true, false, false, null);
		channel.queueDeclare(QUEUE_TARTARUGA, true, false, false, null);
		channel.queueDeclare(QUEUE_LIBELULA, true, false, false, null);
		channel.queueDeclare(QUEUE_CARAMUJO, true, false, false, null);
		channel.queueDeclare(QUEUE_GUEPARDO, true, false, false, null);
		
		try {
			classificarFilasParaEnvio(message,channel);
		} catch (Exception e) {
			System.out.println("MENSAGEM NÃO ENVIADA");
		}

		channel.close();
		connection.close();
	}

	public void classificarFilasParaEnvio(String message, Channel channel) throws Exception  {

		while (!Thread.currentThread().isInterrupted()) {
			String[] parts = message.split(",");
			tipo = parts[1];
			tamanho = parts[2];
			duracao = parts[3];
			taxa = parts[4];

			tipo = tipo.replace("(", "");
			taxa = taxa.replace(")", "");
			
			
			Double tamanhoLong = Double.parseDouble(tamanho);
			Double duracaoLong = Double.parseDouble(duracao);
			Double taxaLong = Double.parseDouble(taxa);
			

			if (tamanho.equalsIgnoreCase(QUEUE_ELEFANTE)) {
				setTamanhoClassificado(QUEUE_ELEFANTE);
			} else {
				setTamanhoClassificado(QUEUE_RATO);
			}

			if (duracao.equalsIgnoreCase(QUEUE_TARTARUGA)) {
				setDuracaoClassificado(QUEUE_TARTARUGA);
			} else {
				setDuracaoClassificado(QUEUE_LIBELULA);
			}
			if (taxa.equalsIgnoreCase(QUEUE_GUEPARDO)) {
				setTaxaClassificado(QUEUE_GUEPARDO);
			} else {
				setTaxaClassificado(QUEUE_CARAMUJO);
			}
			
			
			montarMensagemClassificadaParaEnvio(tipo,tamanhoClassificado,duracaoClassificado,taxaClassificado,channel);

		}
		
		
		

	}
	public  void montarMensagemClassificadaParaEnvio(String tipo,String tamanho,String duracao ,String taxa, Channel channel) throws IOException{
		sequence = obterSequence(sequence);
		HashMap<String, String> novaMensagem = new LinkedHashMap<String, String>();
		
		novaMensagem.put("id", sequence.toString());
		novaMensagem.put("protocolo", tipo);
		novaMensagem.put("tamanho", tamanho);
		novaMensagem.put("duracao",duracao);
		novaMensagem.put("taxa",taxa);
		
		System.out.println(novaMensagem.toString());
		
		if (tamanho.equalsIgnoreCase(QUEUE_ELEFANTE)) {
			System.out.println("ENVIAR PARA FILA ELEFANTE");
			channel.basicPublish("", QUEUE_ELEFANTE, null, novaMensagem.toString().getBytes());
		} else {
			System.out.println("ENVIAR PARA FILA RATO");
			channel.basicPublish("", QUEUE_RATO, null, novaMensagem.toString().getBytes());
		}

		if (duracao.equalsIgnoreCase(QUEUE_TARTARUGA)) {
			System.out.println("ENVIAR FILA TARTARUGA");
			channel.basicPublish("", QUEUE_TARTARUGA, null, novaMensagem.toString().getBytes());
		} else {
			System.out.println("ENVIAR FILA LIBELULA");
			channel.basicPublish("", QUEUE_LIBELULA, null, novaMensagem.toString().getBytes());
		}
		if (taxa.equalsIgnoreCase(QUEUE_GUEPARDO)) {
			System.out.println("ENVIAR FILA GUEPARDO");
			channel.basicPublish("", QUEUE_GUEPARDO, null, novaMensagem.toString().getBytes());
		} else {
			System.out.println("ENVIAR FILA CARAMUJO");
			channel.basicPublish("", QUEUE_CARAMUJO, null, novaMensagem.toString().getBytes());
		}
		visualizarInfo(tipo.toLowerCase(),tamanho.toLowerCase(),duracao.toLowerCase(),taxa.toLowerCase());
		
		
	}
	
	private void visualizarInfo(String tipoView, String tamanhoView,
			String duracaoView, String taxaview) throws IOException {
		String url = "http://psd-acplanner.rhcloud.com/ProjetoPadrao/resources/send?size="+tamanhoView+"&time="+taxaview+"&rate="+duracaoView+"&group=2&protocol="+tipoView+"";
		URL obj = new URL(null, url, new sun.net.www.protocol.https.Handler());
		HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();

		// add reuqest header
		con.setRequestMethod("POST");
		con.setRequestProperty("User-Agent", "Mozilla/5.0");
		con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

		// Send post request

		int responseCode = con.getResponseCode();
		System.out.println("\nSending 'POST' request to URL : " + url);
		System.out.println("Response Code : " + responseCode);

		BufferedReader in = new BufferedReader(new InputStreamReader(
				con.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();

		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();

		// print result
		System.out.println(response.toString());
		
	}
	public void persistirUltimaSequence(Long lastSequence) throws IOException{
		arquivo = new File("/home/mininet/aluizio/rsi-psd/sequence.txt");
		arquivo.createNewFile();
		FileWriter writer = new FileWriter(arquivo);
		BufferedWriter bw = new BufferedWriter(writer);
		bw.write(lastSequence.toString());
		bw.close();
		writer.close();
	}
	public Long obterSequence(Long sequence) throws IOException{
		if(arquivo.exists()){
			FileReader reader = new FileReader("/home/mininet/aluizio/rsi-psd/sequence.txt");
			BufferedReader leitor = new BufferedReader(reader);
			String linha = null;
			linha = leitor.readLine();
			
			sequence = Long.parseLong(linha);
			sequence = ++sequence;
			persistirUltimaSequence(sequence);
			
			leitor.close();
		}else{
			sequence = ++sequence;
			persistirUltimaSequence(sequence);
		}
		
		return sequence;
	}
	
	public Long getSequence() {
		return sequence;
	}

	public  void setSequence(Long sequence) {
		this.sequence = sequence;
	}
	
	public  String getTamanhoClassificado() {
		return tamanhoClassificado;
	}

	public  void setTamanhoClassificado(String tamanhoClassificado) {
		this.tamanhoClassificado = tamanhoClassificado;
	}

	public  String getDuracaoClassificado() {
		return duracaoClassificado;
	}

	public  void setDuracaoClassificado(String duracaoClassificado) {
		this.duracaoClassificado = duracaoClassificado;
	}

	public  String getTaxaClassificado() {
		return taxaClassificado;
	}

	public  void setTaxaClassificado(String taxaClassificado) {
		this.taxaClassificado = taxaClassificado;
	}
	
}
