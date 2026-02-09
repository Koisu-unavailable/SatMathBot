import discord
import discord.ext
from discord.ext import commands
import discord.ext.commands
import logging
from satmathbot.genmath.algebra import AlgebraGen

logger = logging.Logger("QotdCog")
logger.setLevel(logging.INFO)
class Qotd(commands.Cog):
    group = discord.app_commands.Group(name="qotd", description="Commands related to the question of the day")
    def __init__(self, bot: discord.ext.commands.Bot) -> None:
        self.bot = bot
        self.__cog_name__ = "qotd"
    @group.command(name="qotd", description="get the question of the day")
    async def qotd(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        algebraGen = AlgebraGen()
        problem_image = algebraGen.generate_problem()
        await interaction.followup.send("Solve for X: ", file=discord.File(problem_image, "latex.png"))
        return
    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Qotd(bot))
    logger.info("QOTD Cog has been loaded")
    