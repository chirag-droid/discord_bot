from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from discord.mentions import AllowedMentions

from discord_bot.config import BotConfig

bot = Bot(
    command_prefix=commands.when_mentioned_or(BotConfig.prefix),
    description=BotConfig.description,
    activity=Game(BotConfig.activity, large_image_url=BotConfig.large_image),
    allowed_mentions=AllowedMentions(everyone=False),
    case_insensitive=True,
    strip_after_prefix=True,
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
