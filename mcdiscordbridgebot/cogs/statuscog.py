from ..bot import McDiscordBridgeBot
from discord.ext import commands, tasks
from discord import Game
from logging import getLogger
from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse

import discord

_logger = getLogger(__name__)


class StatusCog(commands.Cog):
    def __init__(self, bot: McDiscordBridgeBot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        self.query_server_task.start()

    async def cog_unload(self) -> None:
        self.query_server_task.cancel()

    @tasks.loop(minutes=1)
    async def query_server_task(self) -> None:
        _logger.info("Querying Minecraft server status")
        server = JavaServer.lookup(self.bot.config.mc_server_ip)
        status = server.status()
        await self.bot.change_presence(activity=self.create_activity_presence(status))

    def create_activity_presence(self, status: JavaStatusResponse) -> Game:
        return discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{status.players.online} / {status.players.max} players",
        )


async def setup(bot: McDiscordBridgeBot) -> None:
    await bot.add_cog(StatusCog(bot))
