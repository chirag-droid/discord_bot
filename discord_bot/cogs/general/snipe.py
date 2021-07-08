import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context


class Snipe(commands.Cog, name="General"):
    """Snipe last editted and deleted messages"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.last_message: "dict[str, Message]" = {}
        self.last_edit_message: "dict[str, dict[str, Message]]" = {}

    @commands.Cog.listener()
    async def on_message_delete(self, msg: Message):
        self.last_message[msg.channel.id] = msg

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        self.last_edit_message[before.channel.id] = {
            "before": before,
            "after": after,
        }

    @commands.command(name="snipe")
    async def snipe(self, ctx: Context):
        """A command to snipe deleted messages"""
        if not self.last_message.get(ctx.channel.id):
            await ctx.send("There is no message to snipe!")
            return

        message = self.last_message[ctx.channel.id]
        author = message.author
        content = message.content

        embed = discord.Embed(
            title=f"Message from {author}",
            description=content,
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="editsnipe")
    async def editsnipe(self, ctx: Context):
        """A command to snipe last editted messsages"""
        messages = self.last_edit_message.get(ctx.channel.id)

        if not messages:
            await ctx.send("There is no message to snipe")
            return

        before_msg = messages.get("before")
        after_msg = messages.get("after")
        author = before_msg.author
        before = before_msg.content
        after = after_msg.content

        embed = discord.Embed(
            title=f"Message from {author}",
            description=f"**Before**: {before}\n**After**: {after}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Snipe(bot))
