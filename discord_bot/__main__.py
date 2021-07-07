import os
import traceback

from discord_bot.bot import bot
from discord_bot.config import BotConfig

for cog in os.listdir("discord_bot/cogs"):
    if not cog.startswith("_") and cog.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{cog[:-3]}")
            print(f"loaded {cog} succesfully")
        except Exception:
            traceback.print_exc()

bot.run(BotConfig.TOKEN)
