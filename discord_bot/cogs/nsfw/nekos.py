import discord
import nekos
from discord.ext import commands

from discord_bot.bot import Bot


class Nekos(commands.Cog, name="Nsfw"):
    """NSFW commands to neko pics. And other fun commands."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def generate_embed(self, ctx: commands.Context, target: str) -> discord.Embed:
        target = target.lower()
        embed = discord.Embed()
        if target == "neko":
            embed.title = "Neko"
        else:
            embed.title = f"Neko {target}"
        try:
            embed.set_image(url=nekos.img(target))
            embed.color = 0xFF0090
        except nekos.errors.InvalidArgument as e:
            embed.title = "Invalid Arguments"
            embed.description = e.args[0]
            embed.color = discord.Color.red()

        embed.set_footer(text=f"Requested by {ctx.author}")
        return embed

    @commands.command(name="avatar")
    async def avatar(self, ctx: commands.Context):
        """Sends a discord avatar"""
        async with ctx.typing():
            await ctx.send(embed=self.generate_embed(ctx, "avatar"))

    @commands.command(name="neko")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def neko(self, ctx: commands.Context, target: str = "neko"):
        """Sends cute anime girls pic"""
        target = target.lower()
        if ctx.guild and not ctx.channel.is_nsfw() and target != "neko":
            raise commands.NSFWChannelRequired(channel=ctx.channel)
        async with ctx.typing():
            await ctx.send(embed=self.generate_embed(ctx, target))

    @commands.command(name="boobs", aliases=["tits", "tit", "boob"], hidden=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def boobs(self, ctx: commands.Context):
        """Sends boobs pics. What else do u expect?"""
        async with ctx.typing():
            await ctx.send(embed=self.generate_embed(ctx, "boobs"))

    @commands.command(name="pussy", hidden=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pussy(self, ctx: commands.Context):
        """Sends pussy pics. What else do you expect?"""
        async with ctx.typing():
            await ctx.send(embed=self.generate_embed(ctx, "pussy"))

    @commands.command(name="blowjob", aliases=["bj", "blow"], hidden=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blowjob(self, ctx: commands.Context):
        """Sends blowjob pics and gifs."""
        async with ctx.typing():
            await ctx.send(embed=self.generate_embed(ctx, "blowjob"))

    @commands.command(name="cum", aliases=["cum_jpg"], hidden=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cum(self, ctx: commands.Context):
        """Sends cum pics and gif."""
        async with ctx.typing():
            await ctx.send(embed=self.generate_embed(ctx, "cum"))

    @commands.command(name="anal", hidden=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def anal(self, ctx: commands.Context):
        """Do you actually need a help explaining that?"""
        async with ctx.typing():
            await ctx.send(embed=self.generate_embed(ctx, "anal"))


def setup(bot: Bot):
    bot.add_cog(Nekos(bot))
