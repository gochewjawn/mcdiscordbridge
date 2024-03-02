from ..bot import McDiscordBridgeBot
from discord.ext import commands


class OwnerCog(commands.Cog):
    def __init__(self, bot: McDiscordBridgeBot) -> None:
        self.bot = bot

    @commands.command(name="syncappcommands")
    @commands.is_owner()
    async def sync_application_commands(self, ctx: commands.Context) -> None:
        if gid := self.bot.config.debug_guild_id:
            debug_guild = self.bot.get_guild(gid) or await self.bot.fetch_guild(gid)
            self.bot.tree.copy_global_to(guild=debug_guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.message.reply("Synced!")


async def setup(bot: McDiscordBridgeBot) -> None:
    await bot.add_cog(OwnerCog(bot))
