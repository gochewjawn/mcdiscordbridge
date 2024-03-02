FROM python:3.12.2-slim-bullseye

WORKDIR /app

COPY requirements.txt .
COPY mcdiscordbridgebot/ mcdiscordbridgebot/

RUN [ "pip", "install", "--no-cache-dir", "-r", "requirements.txt" ]

LABEL maintainer="gochewjawn <gochewjawn@outlook.com>"
LABEL version="1.0.0"
LABEL description="Minecraft, Discord messaging bridge bot"

CMD [ "python", "-m", "mcdiscordbridgebot" ]
