import asyncio

import discord
from discord.ext import commands

from discord_bot.bot import Bot
from discord_bot.config import GuildConfig


class Suggest(commands.Cog):
    def __init__(self, bot: Bot):
        """A cog for suggestions and bug reporting."""
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx: commands.Context, *arg):
        """Use this command to suggest something."""
        if not arg:
            return await ctx.send("You had to send suggestion, not your dumb feelings.")

        arg = " ".join(arg)

        embed = discord.Embed()
        embed.title = f"Suggestion from {ctx.author}"
        embed.description = arg
        embed.color = discord.Color.green()

        await ctx.send(
            content="Is this suggestion ok? Reply with yes you have 30sec", embed=embed
        )

        def check(mes: discord.Message):
            return mes.author == ctx.author and mes.channel == ctx.channel

        try:
            suggestion = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send("Ok not sending your suggestion")

        if suggestion.content.lower() != "yes":
            return await ctx.send("Ok not sending your suggestion")

        channel = self.bot.get_channel(GuildConfig.suggestChannel)
        if not channel:
            return await ctx.send("Couldn't find the suggestion channel.")

        mes: discord.Message = await channel.send(embed=embed)
        await mes.add_reaction("👍")
        await mes.add_reaction("👎")
        await ctx.send("Suggestion sent. Thanks for your suggestion.")

    @commands.command()
    async def report(self, ctx: commands.Context, *arg):
        """Use this command to report a bug or an issue"""
        if not arg:
            return await ctx.send("You had to send report, not your dumb feelings.")

        arg = " ".join(arg)

        embed = discord.Embed()
        embed.title = f"Bug report/issue from {ctx.author}"
        embed.description = arg
        embed.color = discord.Color.green()

        await ctx.send(
            content="Is this issue ok? Reply with yes you have 30sec", embed=embed
        )

        def check(mes: discord.Message):
            return mes.author == ctx.author and mes.channel == ctx.channel

        try:
            suggestion = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send("Ok not sending your report")

        if suggestion.content.lower() != "yes":
            return await ctx.send("Ok not sending your report")

        channel = self.bot.get_channel(GuildConfig.reportingChannel)
        if not channel:
            return await ctx.send("Couldn't find the report channel.")

        await channel.send(embed=embed)
        await ctx.send("Suggestion sent. Thanks for your report.")


def setup(bot: Bot):
    bot.add_cog(Suggest(bot))
