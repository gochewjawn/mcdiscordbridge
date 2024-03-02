from ..bot import McDiscordBridgeBot, McMessage
from aiokafka import AIOKafkaConsumer
from asyncio import Task, get_event_loop
from discord.ext import commands
from discord import Interaction, app_commands
from json import loads


class ConsumerCog(commands.Cog):
    def __init__(self, bot: McDiscordBridgeBot) -> None:
        self.bot = bot
        self.consumer = AIOKafkaConsumer(
            self.bot.config.kafka_consumer_topic,
            bootstrap_servers=self.bot.config.kafka_bootstrap_servers,
            value_deserializer=deserialize_minecraft_message,
        )
        self.consumer_task: Task | None = None

    async def cog_load(self) -> None:
        await self.consumer.start()
        self.consumer_task = get_event_loop().create_task(self.create_consumer_task())

    async def create_consumer_task(self) -> None:
        async for msg in self.consumer:
            await self.send_to_consumer_channels(msg.value)

    async def send_to_consumer_channels(self, msg: McMessage) -> None:
        for id in self.bot.database.consumer_channel_ids:
            chan = self.bot.get_channel(id) or await self.bot.fetch_channel(id)
            await chan.send(f"**{msg.author}**: {msg.content}")

    @app_commands.command(
        name="addconsumerchannel",
        description="Sets up a channel to receive messages from Minecraft",
    )
    async def add_consumer_channel(self, inter: Interaction) -> None:
        if inter.channel_id:
            cids = set(self.bot.database.consumer_channel_ids) | {inter.channel_id}
            self.bot.database.consumer_channel_ids = list(cids)
            await inter.response.send_message(
                "This channel will now receive messages from Minecraft! 😍"
            )
        else:
            await inter.response.send_message(
                f"Sorry, {inter.author.mention}. You sure you're in a channel?"
            )

    async def cog_unload(self) -> None:
        self.consumer_task and self.consumer_task.cancel()
        await self.consumer.stop()


def deserialize_minecraft_message(msg: bytes) -> McMessage:
    return McMessage(**loads(msg))


async def setup(bot: McDiscordBridgeBot) -> None:
    await bot.add_cog(ConsumerCog(bot))
