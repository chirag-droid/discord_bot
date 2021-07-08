import discord
from discord.ext import commands


class errorHandler(commands.Cog):
    """
    Error Handler cog that handles bot errors globally
    """

    def __init__(self, bot: commands.Bot):
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

        else:
            title = "Unhandled error"
            description = f"""
                An Unhandled exception occured,
                if this happens frequently please report to bot devs.\n{error}
            """

        if title and description:
            await ctx.reply(
                embed=discord.Embed(
                    title=title, description=description, color=discord.Color.red()
                ),
                mention_author=True,
            )


def setup(bot: commands.Bot):
    bot.add_cog(errorHandler(bot))
