from .config import Config
from .database import Database
from dataclasses import dataclass
from discord.ext import commands
from discord import  Intents
from logging import getLogger

_logger = getLogger(__name__)


class McDiscordBridgeBot(commands.Bot):
    def __init__(self, config: Config, database: Database) -> None:
        super().__init__("!", intents=create_intents())
        self.config = config
        self.database = database

    async def on_ready(self) -> None:
        await self.load_extension("mcdiscordbridgebot.cogs.ownercog")
        await self.load_extension("mcdiscordbridgebot.cogs.consumercog")
        await self.load_extension("mcdiscordbridgebot.cogs.producercog")
        await self.load_extension("mcdiscordbridgebot.cogs.statuscog")
        _logger.info("Loaded extensions")


@dataclass
class McMessage:
    author: str
    content: str


def create_intents() -> Intents:
    intents = Intents.default()
    intents.message_content = True
    return intents
