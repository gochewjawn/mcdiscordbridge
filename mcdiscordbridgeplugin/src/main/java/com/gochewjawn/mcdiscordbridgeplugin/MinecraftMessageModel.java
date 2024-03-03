package com.gochewjawn.mcdiscordbridgeplugin;

public class MinecraftMessageModel {
    private String author;
    private String content;

    public MinecraftMessageModel(String author, String content) {
        this.author = author;
        this.content = content;
    }

    public String getAuthor() {
        return author;
    }

    public String getContent() {
        return content;
    }
}
