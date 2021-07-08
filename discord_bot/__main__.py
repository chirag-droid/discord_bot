from discord_bot.bot import bot
from discord_bot.config import BotConfig
from discord_bot.utils.extensions import walk_extensions

for ext in walk_extensions():
    bot.load_extension(ext)

bot.run(BotConfig.TOKEN)
