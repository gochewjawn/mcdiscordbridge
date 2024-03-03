package com.gochewjawn.mcdiscordbridgeplugin;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;

import com.google.gson.Gson;

public class MinecraftMessageExporter implements Listener {
    private final KafkaProducer<String, String> kafkaProducer;
    private final FileConfiguration config;

    public MinecraftMessageExporter(
            final KafkaProducer<String, String> kafkaProducer,
            final FileConfiguration config) {
        this.kafkaProducer = kafkaProducer;
        this.config = config;
    }

    @EventHandler
    public void onPlayerChat(AsyncPlayerChatEvent event) {
        Player player = event.getPlayer();
        String message = event.getMessage();
        kafkaProducer.send(createProducerRecord(player, message));
    }

    private ProducerRecord<String, String> createProducerRecord(Player player, String message) {
        MinecraftMessageModel valueObject = new MinecraftMessageModel(player.getName(), message);
        return new ProducerRecord<String, String>(this.config.getString("kafka-producer-topic"),
                new Gson().toJson(valueObject));
    }
}
