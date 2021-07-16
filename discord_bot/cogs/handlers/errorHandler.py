import discord
from discord.ext import commands

from discord_bot.bot import Bot
from discord_bot.utils.messages import formatDocstr


class errorHandler(commands.Cog):
    """
    Error Handler cog that handles bot errors globally
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """
        Triggered when a valid command catches an error
        """

        if isinstance(error, commands.CommandNotFound):
            title = "Command not found"
            description = f"""
                No command {ctx.invoked_with} found.
                Please try again.
            """

        elif isinstance(error, commands.CommandOnCooldown):
            title = "You are on cooldown"
            description = f"""
                Please try again in {int(error.retry_after)} seconds
            """

        elif isinstance(error, commands.MissingPermissions):
            title = "Missing Permissions"
            description = """
                You are missing the required
                permissions to run this command!
            """

        elif isinstance(error, commands.UserInputError):
            title = "Input error"
            description = """
                Something about your input was wrong,
                please check your input and try again!
            """

        elif isinstance(error, commands.NSFWChannelRequired):
            title = "What are u doing?"
            description = """
                You are trying  to run a nsfw command.
                NSFW commands can only be ran in NSFW channels.
            """

        elif isinstance(error, commands.NotOwner):
            title = "Not Owner"
            description = """
                Are you trying to break me by running a owner only command?
                Sucks to be you.
            """

        elif isinstance(error, commands.CheckFailure):
            title = "Check Failure"
            description = """
                You can't run this command because certain checks failed.
            """

        else:
            title = "Unhandled error"
            description = f"""
                An Unhandled exception occured,
                if this happens frequently please report to bot devs.\n{error}
            """

        await ctx.reply(
            embed=discord.Embed(
                title=title,
                description=formatDocstr(description),
                color=discord.Color.red(),
            ),
            mention_author=True,
        )


def setup(bot: Bot):
    bot.add_cog(errorHandler(bot))
