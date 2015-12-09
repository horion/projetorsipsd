package com.stratio.example.receber;

import java.io.IOException;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;
import org.apache.spark.storage.StorageLevel;
import org.apache.spark.streaming.receiver.Receiver;


public class CustomReceiver extends Receiver<String> {

	private final static String QUEUE_NAME_ALL = "All";
	private final static String QUEUE_NAME_FTP = "FTP";
	private final static String QUEUE_NAME_DNS = "DNS";
	private final static String QUEUE_NAME_HTTP = "HTTP";
	private final static String QUEUE_NAME_UNKNOWN = "Unknown";
	private final static String QUEUE_NAME_SSH = "SSH";


	private ConnectionFactory factory;
	QueueingConsumer consumer;

	
	
	private String hostname = "192.168.56.103";// define hostname for rabbitmq reciver
	private int portNumber = 5672;
	private String virtualHost = "filas";
	private String username = "luiz";
	private String password = "113211";
	
	Connection connection;
	Channel channel;

	public CustomReceiver() {
		super(StorageLevel.MEMORY_AND_DISK_2());

	}

	@Override
	public void onStart() {
		new Thread()  {
			@Override public void run() {
				receive();
			}
		}.start();
	}

	protected void receive(){
		try{
			factory = new ConnectionFactory();
			factory.setHost(hostname);
			factory.setPort(portNumber);
			factory.setVirtualHost(virtualHost);
			factory.setUsername(username);
			factory.setPassword(password);
			
			connection = factory.newConnection();
			channel = connection.createChannel();
			
			channel.queueDeclare(QUEUE_NAME_ALL, true, false, false, null);
			channel.queueDeclare(QUEUE_NAME_DNS, true, false, false, null);
			channel.queueDeclare(QUEUE_NAME_FTP, true, false, false, null);
			channel.queueDeclare(QUEUE_NAME_HTTP, true, false, false, null);
			channel.queueDeclare(QUEUE_NAME_UNKNOWN, true, false, false, null);
			channel.queueDeclare(QUEUE_NAME_SSH, true, false, false, null);
			
			consumer = new QueueingConsumer(channel);


			channel.basicConsume(QUEUE_NAME_ALL, true, consumer);
			channel.basicConsume(QUEUE_NAME_DNS, true, consumer);
			channel.basicConsume(QUEUE_NAME_FTP, true, consumer);
			channel.basicConsume(QUEUE_NAME_HTTP, true, consumer);
			channel.basicConsume(QUEUE_NAME_UNKNOWN, true, consumer);
			channel.basicConsume(QUEUE_NAME_SSH, true, consumer);
			
			enviar enviarClassificacao = new enviar();
			
			while (!Thread.currentThread().isInterrupted()) {
				
				QueueingConsumer.Delivery delivery = consumer.nextDelivery();
				
				String message = new String(delivery.getBody());
				try{
					
					enviarClassificacao.enviarTupla(message);
				}catch (Exception e){
					System.out.println("ERRO AO ENVIAR MENSAGEM");
				}
				
				store(message);
				


			}
		}catch (Exception e){
			System.out.println("DEU PAU");
		}
	}

	@Override
	public void onStop() {

	}

}
