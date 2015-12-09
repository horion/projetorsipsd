package com.stratio.example.receber;

import java.io.IOException;
import org.apache.spark.streaming.*;
import org.apache.spark.SparkConf;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.*;

public class SparkStreaming {
	private SparkStreaming() {
	}

	public static JavaStreamingContext ssc;

	public static void main(String[] args) throws IOException {
		 Duration batchInterval = new Duration(2000);
			
		 ssc = new JavaStreamingContext("spark://192.168.1.115:7077", "CustomReceiver", batchInterval,System.getenv("SPARK_HOME"),
	            JavaStreamingContext.jarOfClass(SparkStreaming.class));
		
		JavaDStream<String> CSR = ssc.receiverStream(new CustomReceiver());
		//here is rabbitmq stream as spark streaming
		CSR.print();
		
		ssc.start();
		ssc.awaitTermination();
	}
}