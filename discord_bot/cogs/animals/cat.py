import io

import discord
import requests
from discord.ext import commands
from requests.utils import requote_uri

from discord_bot.bot import Bot


class Cat(commands.Cog, name="Cat"):
    """Get random cat, gif or make a cat say something"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.base_api = "https://cataas.com"

    @commands.group(name="cat", aliases=["meow", "randomcat", "cats"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cat(self, ctx: commands.Context):
        """Sends a random cat"""
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                r = requests.get(f"{self.base_api}/cat?json=true")
                if r.status_code != 200:
                    return ctx.reply("An http error occured")
                r = r.json()
                embed = discord.Embed(title="Random Cat", color=0xFF0090)
                embed.set_image(url=self.base_api + r.get("url"))
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.reply(embed=embed)

    @cat.command(name="say", aliases=["says"])
    async def say(self, ctx: commands.Context, *arg):
        """Make a cat say something"""
        async with ctx.typing():
            if arg:
                arg = " ".join(arg)
            else:
                arg = "say something"
            text = requote_uri(arg)
            r = requests.get(f"{self.base_api}/cat/says/{text}?json=true")
            if r.status_code != 200:
                return ctx.reply("An http error occured")
            r = r.json()
            embed = discord.Embed(title=f"Cat saying {arg}", color=0xFF0090)
            embed.set_image(url=self.base_api + r.get("url"))
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.reply(embed=embed)

    @cat.command(name="gif", aliases=["vid", "video"])
    async def gif(self, ctx: commands.Context):
        """Sends a random cat gif"""
        async with ctx.typing():
            r = requests.get(f"{self.base_api}/cat/gif")
            if r.status_code != 200:
                return await ctx.reply("An error occured when sending gif.")

            gif = io.BytesIO(r.content)
            file = discord.File(gif, "cat.gif")

            embed = discord.Embed(title="Random cat gif", color=0xFF0090)
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.set_image(url="attachment://cat.gif")

            await ctx.reply(embed=embed, file=file)

    @cat.command(name="fact", aliases=["facts"])
    async def fact(self, ctx: commands.Context):
        """Get a random cat fact"""
        async with ctx.typing():
            r = requests.get("https://catfact.ninja/fact")
            if r.status_code != 200:
                return await ctx.reply("An http error occured")
            r = r.json()
            embed = discord.Embed(title="Random cat fact", color=0xFF0090)
            embed.description = r.get("fact")
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Cat(bot))
