import discord
import requests
from discord.ext import commands

from discord_bot.bot import Bot


class Dog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.base_url = "https://dog.ceo/api"
        self.fact_url = "https://dog-facts-api.herokuapp.com/api/v1"

    @commands.group(name="dog", aliases=["dogs"])
    async def dog(self, ctx: commands.Context):
        """Sends a random dog pic"""
        if ctx.invoked_subcommand is not None:
            return

        async with ctx.typing():
            embed = discord.Embed()
            embed.title = "Random Dog Pic"
            embed.color = discord.Color.blue()
            embed.set_footer(text=f"Requested by {ctx.author}")

            r = requests.get(f"{self.base_url}/breeds/image/random")
            if r.status_code != 200:
                await ctx.reply("An http error occured while processing your request")
            r = r.json()
            url = r.get("message")

            embed.set_image(url=url)
            await ctx.send(embed=embed)

    @dog.command(name="fact", aliases=["facts"])
    async def fact(self, ctx: commands.Context):
        """Get a random dog fact"""
        async with ctx.typing():
            embed = discord.Embed()
            embed.title = "Random Dog Fact"
            embed.color = discord.Color.blue()
            embed.set_footer(text=f"Requested by {ctx.author}")

            r = requests.get(f"{self.fact_url}/resources/dogs?number=1")
            if r.status_code != 200:
                await ctx.reply("An http error occured while processing your request")
            facts = r.json()
            embed.description = facts[0].get("fact")
            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Dog(bot))
