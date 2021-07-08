import discord
import nekos
from discord.ext import commands
from discord.ext.commands import Bot


class Nekos(commands.Cog, name="NSFW"):
    """NSFW commands to get hot and sexy pics"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="neko")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.is_nsfw()
    async def neko(self, ctx: commands.Context, target: str = "neko"):
        """Sends cute anime girls pic"""
        async with ctx.typing():
            try:
                await ctx.reply(nekos.img(target=target))
            except nekos.errors.InvalidArgument as e:
                title = "Invalid Arguments"
                description = e.args[0]
                await ctx.reply(
                    embed=discord.Embed(
                        title=title, description=description, color=discord.Color.red()
                    ),
                    mention_author=True,
                )


def setup(bot: Bot):
    bot.add_cog(Nekos(bot))
