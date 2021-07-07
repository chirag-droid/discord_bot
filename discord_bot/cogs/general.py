import time

import discord
from discord.ext import commands


class General(commands.Cog):
    """General bot commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_message = None

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket, and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        ping = f"""
            Pong! {round(self.bot.latency * 1000)}ms
            API: {round((end_time - start_time) * 1000)}ms"""

        ping = "\n".join([x.strip() for x in ping.split("\n")])

        await message.edit(content=ping)

    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        self.last_message = msg

    @commands.command(name="snipe")
    async def snipe(self, ctx: commands.Context):
        """A command to snipe deleted messages"""
        if not self.last_message:
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_message.author
        content = self.last_message.content

        embed = discord.Embed(
            title=f"Message from {author}",
            description=content,
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
