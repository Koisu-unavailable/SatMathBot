import discord
import discord.ext
from discord.ext import commands
import discord.ext.commands
import logging


logger = logging.Logger("QotdCog")
logger.setLevel(logging.INFO)
class Qotd(commands.Cog):
    group = discord.app_commands.Group(name="qotd", description="Commands related to the question of the day")
    def __init__(self, bot: discord.ext.commands.Bot) -> None:
        self.bot = bot
    @group.command(name="qotd", description="get the question of the day")
    async def qotd(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World")
        return
    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Qotd(bot))
    print("QOTD Cog has been loaded")
    logger.info("QOTD Cog has been loaded")
    