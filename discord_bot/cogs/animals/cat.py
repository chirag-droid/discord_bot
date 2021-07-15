import io

import discord
import requests
from discord.ext import commands
from requests.utils import requote_uri


class Cat(commands.Cog, name="Cat"):
    """Get random cat, gif or make a cat say something"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_api = "https://cataas.com"

    @commands.group(name="cat", aliases=["meow", "randomcat", "cats"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cat(self, ctx: commands.Context):
        """Sends a random cat"""
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                r = requests.get(f"{self.base_api}/cat?json=true").json()
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
            r = requests.get(f"{self.base_api}/cat/says/{text}?json=true").json()
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
                await ctx.reply("An error occured when sending gif.")

            gif = io.BytesIO(r.content)
            file = discord.File(gif, "cat.gif")

            embed = discord.Embed(title="Random cat gif", color=0xFF0090)
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.set_image(url="attachment://cat.gif")
            embed.video = self.base_api + r.get("url")

            await ctx.reply(embed=embed, file=file)


def setup(bot: commands.Bot):
    bot.add_cog(Cat(bot))
