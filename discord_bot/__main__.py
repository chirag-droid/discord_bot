import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

from discord_bot.bot import Bot
from discord_bot.config import BotConfig
from discord_bot.utils.extensions import walk_extensions

bot = Bot(
    mongoClient=AsyncIOMotorClient(BotConfig.mongodb),
    command_prefix=commands.when_mentioned_or(*BotConfig.prefix),
    description=BotConfig.description,
    activity=discord.Game(BotConfig.activity, large_image_url=BotConfig.large_image),
    allowed_mentions=discord.AllowedMentions(everyone=False),
    case_insensitive=True,
    strip_after_prefix=True,
    help_command=None,
)

for ext in walk_extensions():
    bot.load_extension(ext)

bot.run(BotConfig.TOKEN)
