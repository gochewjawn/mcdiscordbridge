package com.gochewjawn.mcdiscordbridgeplugin;

import java.util.Arrays;
import java.util.Properties;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitRunnable;

public class App extends JavaPlugin {
    private KafkaProducer<String, String> kafkaProducer;
    private KafkaConsumer<String, String> kafkaConsumer;
    private BukkitRunnable kafkaConsumerTask;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        kafkaProducer = createKafkaProducer();
        kafkaConsumer = createKafkaConsumer();
        kafkaConsumerTask = new KafkaMessageReceivedEventEmitter(kafkaConsumer, getConfig());
        kafkaConsumerTask.runTaskAsynchronously(this);
        getServer().getPluginManager().registerEvents(new KafkaMessageReceivedListener(this), this);
        getServer().getPluginManager().registerEvents(new MinecraftMessageExporter(kafkaProducer, getConfig()), this);
    }

    @Override
    public void onDisable() {
        kafkaConsumerTask.cancel();
    }

    private KafkaProducer<String, String> createKafkaProducer() {
        Properties props = new Properties();
        props.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, getConfig().getString("kafka-bootstrap-servers"));
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return new KafkaProducer<>(props);
    }

    private KafkaConsumer<String, String> createKafkaConsumer() {
        Properties props = new Properties();
        props.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, getConfig().getString("kafka-bootstrap-servers"));
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.setProperty(ConsumerConfig.GROUP_ID_CONFIG, "minecraft-group");
        props.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        return new KafkaConsumer<>(props);
    }
}
