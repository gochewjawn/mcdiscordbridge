from ..bot import McDiscordBridgeBot, McMessage
from aiokafka import AIOKafkaProducer
from discord.ext import commands
from discord import Interaction, Message as DiscordMessage, app_commands
from json import dumps
from logging import getLogger

_logger = getLogger(__name__)


class ProducerCog(commands.Cog):
    def __init__(self, bot: McDiscordBridgeBot) -> None:
        self.bot = bot
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bot.config.kafka_bootstrap_servers,
            value_serializer=serialize_minecraft_message,
        )

    async def cog_load(self) -> None:
        await self.producer.start()

    async def cog_unload(self) -> None:
        await self.producer.stop()

    @app_commands.command(
        name="addproducerchannel",
        description="Sets up a channel to send messages to Minecraft",
    )
    async def add_producer_channel(self, inter: Interaction) -> None:
        if inter.channel_id:
            cids = set(self.bot.database.producer_channel_ids) | {inter.channel_id}
            self.bot.database.producer_channel_ids = list(cids)
            await inter.response.send_message(
                "This channel will now send messages to Minecraft! 😍"
            )
        else:
            await inter.response.send_message(
                f"Sorry, {inter.author.mention}. You sure you're in a channel?"
            )

    @commands.Cog.listener()
    async def on_message(self, msg: DiscordMessage) -> None:
        checks = (
            not msg.author.bot,
            msg.channel.id in self.bot.database.producer_channel_ids,
        )
        if all(checks):
            mc_msg = McMessage(author=msg.author.name, content=msg.content)
            _logger.info("Submitting Minecraft message to Kafka: %s", mc_msg)
            await self.producer.send_and_wait(
                self.bot.config.kafka_producer_topic,
                value=mc_msg,
            )


def serialize_minecraft_message(msg: McMessage) -> bytes:
    return dumps(msg.__dict__).encode()


async def setup(bot: McDiscordBridgeBot) -> None:
    await bot.add_cog(ProducerCog(bot))
