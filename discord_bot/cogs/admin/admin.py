from discord.ext import commands

from discord_bot.bot import Bot


class Admin(commands.Cog):
    """Admin commands that only bot owner can run"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="shutdown", hidden=True)
    @commands.is_owner()
    async def shutdow(self, ctx: commands.Context):
        """Closes all connections and shuts down the bot"""
        await ctx.send("Shutting down the bot...")
        await self.bot.close()

    @commands.group(name="extension", aliases=["ext"], hidden=True)
    @commands.is_owner()
    async def ext(self, ctx: commands.Context):
        """A command to load, reload, unload extensions."""
        if ctx.invoked_subcommand is None:
            await ctx.reply("This command requires a subcommand to be passed")

    @ext.command(name="load", aliases=["l"])
    async def load(self, ctx: commands.Context, arg: str):
        """A command to load extensions."""
        try:
            self.bot.load_extension(f"discord_bot.cogs.{arg}")
            await ctx.reply(f"Successfully loaded extension {arg}")
        except Exception as e:
            await ctx.reply(f"Failed to load ext {arg}\n{e}")

    @ext.command(name="unload", aliases=["u"])
    async def unload(self, ctx: commands.Context, arg: str):
        """A command to unload extensions"""
        try:
            self.bot.unload_extension(f"discord_bot.cogs.{arg}")
            await ctx.reply(f"Successfully unloaded extension {arg}")
        except Exception as e:
            await ctx.reply(f"Failed to unload ext {arg}\n{e}")

    @ext.command(name="reload", aliases=["r"])
    async def reload(self, ctx: commands.Context, arg: str):
        """A command to reload extensions."""
        try:
            self.bot.reload_extension(f"discord_bot.cogs.{arg}")
            await ctx.reply(f"Successfully reloaded extension {arg}")
        except Exception as e:
            await ctx.reply(f"Failed to reload ext {arg}\n{e}")


def setup(bot: Bot):
    bot.add_cog(Admin(bot))
