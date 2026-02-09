import os
from satmathbot.cogs import qotd
import logging

import discord
import discord.context_managers
import discord.ext
import discord.ext.commands
from discord.ext import commands
from dotenv import load_dotenv

logging.getLogger("root").setLevel(logging.INFO)

assert load_dotenv("./.env")  # make sure it loads
intents = discord.Intents.all() # FIX
TESTING_GUILD = discord.Object(1419067897652711486)

client = commands.Bot(
    intents=intents,
    command_prefix="!",  # command prefix doesn't really matter as this bot uses slash commands because they're cooler 😀
)

@client.event
async def on_ready() -> None:
    await qotd.setup(client)
    await client.tree.sync()  # TESTING ONLY
    logging.info("Bot is ready!!")


try:
    is_dev = bool(int(os.environ["DEV"]))
except KeyError:
    is_dev = False
logging.info(
    "We're in dev envirorment" if is_dev else "We're in production envirorment"
)

if is_dev:

    @client.tree.command(name="reload_and_sync")
    async def reload(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        logging.info("reloading bot")
        for cog in client.cogs.values():
            cog_to_reload = await client.remove_cog(cog.__cog_name__.lower(), guild=TESTING_GUILD)
            if cog_to_reload == None:
                raise ValueError(f"Cog: {cog.__cog_name__.lower()} not found ")
            await client.add_cog(
                cog_to_reload
            )
            

            logging.info(f"reloaded cog {cog.__cog_name__}")
        await interaction.followup.send("reloaded cogs")
        await client.tree.sync(guild=TESTING_GUILD)
        await interaction.followup.send("sunc")


@client.tree.error
async def on_command_error(interaction: discord.Interaction, error):
    if not interaction.response.is_done:
        await interaction.response.send_message(
            "An error occured, please try again later."
        )
    else:
        await interaction.followup.send("An error occured, please try again later.")
    logging.error("Error occured: ", exc_info=error)


client.run(
    os.environ["TOKEN"],
    log_level=os.environ.get("LOG_LEVEL", "INFO").upper()
    
)