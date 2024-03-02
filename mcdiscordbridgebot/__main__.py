from .bot import McDiscordBridgeBot
from .database import load_database
from .config import create_config_from_environment
from discord.utils import setup_logging
from logging import FileHandler, INFO

if __name__ == "__main__":
    config = create_config_from_environment()
    setup_logging(handler=FileHandler(config.log_path), level=INFO)
    with load_database(config.database_path) as db:
        bot = McDiscordBridgeBot(config, db)
        bot.run(config.discord_token)
