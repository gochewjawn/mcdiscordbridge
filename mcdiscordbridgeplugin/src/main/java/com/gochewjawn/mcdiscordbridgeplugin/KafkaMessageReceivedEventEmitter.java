package com.gochewjawn.mcdiscordbridgeplugin;

import java.time.Duration;

import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.bukkit.Bukkit;
import org.bukkit.scheduler.BukkitRunnable;

public class KafkaMessageReceivedEventEmitter extends BukkitRunnable {
    private final KafkaConsumer<String, String> kafkaConsumer;

    public KafkaMessageReceivedEventEmitter(final KafkaConsumer<String, String> kafkaConsumer) {
        this.kafkaConsumer = kafkaConsumer;
    }

    @Override
    public void run() {
        while (!isCancelled()) {
            ConsumerRecords<String, String> records = kafkaConsumer.poll(Duration.ofMillis(1000));
            for (ConsumerRecord<String, String> record : records) {
                Bukkit.getPluginManager().callEvent(new KafkaMessageReceivedEvent(record));
            }
        }
    }
}
