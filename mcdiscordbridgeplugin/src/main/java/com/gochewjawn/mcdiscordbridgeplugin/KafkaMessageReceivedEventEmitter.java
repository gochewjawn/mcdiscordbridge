package com.gochewjawn.mcdiscordbridgeplugin;

import java.time.Duration;
import java.util.Arrays;

import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.bukkit.Bukkit;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.scheduler.BukkitRunnable;

public class KafkaMessageReceivedEventEmitter extends BukkitRunnable {
    private final KafkaConsumer<String, String> kafkaConsumer;
    private final FileConfiguration config;

    public KafkaMessageReceivedEventEmitter(
            final KafkaConsumer<String, String> kafkaConsumer,
            final FileConfiguration config) {
        this.kafkaConsumer = kafkaConsumer;
        this.config = config;
    }

    @Override
    public void run() {
        kafkaConsumer.subscribe(Arrays.asList(config.getString("kafka-consumer-topic")));
        while (!isCancelled()) {
            ConsumerRecords<String, String> records = kafkaConsumer.poll(Duration.ofMillis(1000));
            for (ConsumerRecord<String, String> record : records) {
                Bukkit.getPluginManager().callEvent(new KafkaMessageReceivedEvent(record));
            }
        }
    }
}
