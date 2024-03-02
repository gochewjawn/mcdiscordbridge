package com.gochewjawn.mcdiscordbridgeplugin;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.bukkit.event.Event;
import org.bukkit.event.HandlerList;

public class KafkaMessageReceivedEvent extends Event {
    private static final HandlerList HANDLERS = new HandlerList();
    private final ConsumerRecord<String, String> record;

    public KafkaMessageReceivedEvent(final ConsumerRecord<String, String> record) {
        super(true);
        this.record = record;
    }

    public static HandlerList getHandlerList() {
        return HANDLERS;
    }

    @Override
    public HandlerList getHandlers() {
        return HANDLERS;
    }

    public ConsumerRecord<String, String> getRecord() {
        return record;
    }
}
