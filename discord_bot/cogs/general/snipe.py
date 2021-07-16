import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands.context import Context

from discord_bot.bot import Bot
from discord_bot.utils.messages import formatDocstr


class Snipe(commands.Cog, name="Snipe"):
    """Snipe last editted and deleted messages"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.last_mes: "dict[str, dict[str, str]]" = {}
        self.edit_mes: "dict[str, dict[str, str]]" = {}

    @commands.Cog.listener()
    async def on_message_delete(self, msg: Message):
        if msg.author.bot:
            return
        self.last_mes[msg.channel.id] = {"author": msg.author, "content": msg.content}

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if before.author.bot:
            return
        self.edit_mes[before.channel.id] = {
            "author": before.author,
            "before": before.content,
            "after": after.content,
        }

    @commands.command(name="snipe")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def snipe(self, ctx: Context):
        """A command to snipe deleted messages"""
        if not self.last_mes.get(ctx.channel.id):
            await ctx.send("There is no message to snipe!")
            return

        mes = self.last_mes.get(ctx.channel.id)
        title = f"Message from {mes['author']}"
        description = mes["content"]

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="editsnipe")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def editsnipe(self, ctx: Context):
        """A command to snipe last editted messsages"""
        if not self.edit_mes.get(ctx.channel.id):
            await ctx.send("There is no message to snipe")
            return

        mes = self.edit_mes.get(ctx.channel.id)
        title = f"Message from {mes['author']}"
        description = f"""
            **Before**: {mes['before']}
            **After**: {mes['after']}
        """

        embed = discord.Embed(
            title=title,
            description=formatDocstr(description),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Snipe(bot))
