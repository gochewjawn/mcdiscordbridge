package com.gochewjawn.mcdiscordbridgeplugin;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.plugin.Plugin;
import org.bukkit.scheduler.BukkitRunnable;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

public class KafkaMessageReceivedListener implements Listener {
    private final Plugin plugin;

    public KafkaMessageReceivedListener(final Plugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onKafkaMessageReceivedEvent(KafkaMessageReceivedEvent event) {
        ConsumerRecord<String, String> record = event.getRecord();
        MinecraftMessageModel msgModel;

        try {
            Gson gson = new Gson();
            msgModel = gson.fromJson(record.value(), MinecraftMessageModel.class);
        } catch (JsonSyntaxException error) {
            return;
        }

        String msg = String.format("[DISCORD] <{0}> {1}", msgModel.getAuthor(), msgModel.getContent());
        new BroadcastMessageTask(plugin, msg).runTask(plugin);
    }
}

class BroadcastMessageTask extends BukkitRunnable {
    private final Plugin plugin;
    private final String message;

    public BroadcastMessageTask(final Plugin plugin, final String message) {
        this.plugin = plugin;
        this.message = message;
    }

    @Override
    public void run() {
        plugin.getServer().broadcastMessage(message);
    }
}