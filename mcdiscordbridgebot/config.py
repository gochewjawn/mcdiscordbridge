from dataclasses import dataclass
from dotenv import load_dotenv
from os import environ


@dataclass
class Config:
    kafka_bootstrap_servers: list[str]
    kafka_producer_topic: str  # Messages will be sent here from Discord.
    kafka_consumer_topic: str  # Messages sent here will be replicated to Discord.
    database_path: str  # Maintains which Discord channels are bridged to, bridged from.
    log_path: str
    discord_token: str
    debug_guild_id: int
    mc_server_ip: str  # Shows Minecraft server information as status.


def create_config_from_environment() -> Config:
    load_dotenv()
    return Config(
        kafka_bootstrap_servers=environ["KAFKA_BOOTSTRAP_SERVERS"].split(","),
        kafka_producer_topic=environ["KAFKA_PRODUCER_TOPIC"],
        kafka_consumer_topic=environ["KAFKA_CONSUMER_TOPIC"],
        database_path=environ.get("DATABASE_PATH", "data/db.json"),
        log_path=environ.get("LOG_PATH", "data/log.txt"),
        discord_token=environ["DISCORD_TOKEN"],
        debug_guild_id=int(environ.get("DEBUG_GUILD_ID", 0)),
        mc_server_ip=environ["MC_SERVER_IP"],
    )
