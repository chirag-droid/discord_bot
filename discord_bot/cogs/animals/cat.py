import io

import discord
import requests
from discord.ext import commands
from requests.exceptions import HTTPError
from requests.utils import requote_uri

from discord_bot.bot import Bot


class Cat(commands.Cog, name="Cat"):
    """Get random cat, gif or make a cat say something"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.base_api = "https://cataas.com"

    def generate_embed(self, ctx: commands.Context, url=None):
        embed = discord.Embed()
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.color = 0xFF0090

        if not url:
            return embed

        r = requests.get(url)
        if r.status_code != 200:
            return HTTPError
        r = r.json()

        embed.set_image(url=self.base_api + r.get("url"))
        return embed

    @commands.group(name="cat", aliases=["meow", "randomcat", "cats"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cat(self, ctx: commands.Context):
        """Sends a random cat"""
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                embed = self.generate_embed(ctx, f"{self.base_api}/cat?json=true")
                if isinstance(embed, HTTPError):
                    return await ctx.reply("An http error occured")
                embed.title = "Random Cat"
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
            embed = self.generate_embed(
                ctx, f"{self.base_api}/cat/says/{text}?json=true"
            )
            if isinstance(embed, HTTPError):
                return await ctx.reply("An http error occured")
            embed.title = f"Cat saying {arg}"
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

            embed = self.generate_embed(ctx)
            embed.title = "Cat gif"
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
            embed = self.generate_embed(ctx)
            embed.title = "Random cat fact"
            embed.description = r.get("fact")
            await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Cat(bot))
