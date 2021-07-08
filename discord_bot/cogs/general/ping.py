import time

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from discord_bot import start_time
from discord_bot.utils.messages import formatDocstr


class Ping(commands.Cog, name="General"):
    """Get the bot's current latency and uptime."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket, and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        ping = f"""
            Gateway Latency: {round(self.bot.latency * 1000)}ms
            API Latency: {round((end_time - start_time) * 1000)}ms
        """

        embed = discord.Embed(
            title=":ping_pong: Pong!",
            description=formatDocstr(ping),
            color=discord.Color.green(),
        )

        await message.edit(embed=embed)

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        """Get the bot's uptime"""
        await ctx.send(f"I started {start_time.humanize()}")


def setup(bot: Bot):
    bot.add_cog(Ping(bot))
