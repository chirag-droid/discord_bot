import discord
from discord.ext import commands

from discord_bot.bot import Bot
from discord_bot.config import BotConfig
from discord_bot.utils.help import get_help, get_help_cog


class Help(commands.Cog, name="Help"):
    """Get info on a available commands, cogs"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context, *arg):
        """
        List all commands from every Cog the bot has loaded.
        """
        prefix = BotConfig.prefix
        if not isinstance(prefix, str):
            prefix = prefix[0]

        embed = discord.Embed()
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        footer = f"For more information about a command run {prefix}help <command>"
        embed.set_footer(text=footer)
        color = 0x42F56C

        if not arg:
            title = "Help Commands"
            description = "List of available commands."

            for i in self.bot.cogs:
                cog = self.bot.get_cog(i)
                help = "".join(get_help_cog(cog))
                if not help:
                    continue
                embed.add_field(
                    name=f"{i.capitalize()}",
                    value=f"```{help}```",
                    inline=False,
                )

        else:
            arg = " ".join(arg)
            if arg.capitalize() in self.bot.cogs:
                cog = self.bot.get_cog(arg.capitalize())
                title = f"Help for category {arg.capitalize()}"
                help = "".join(get_help_cog(cog, subcommands=True, show_hidden=True))
                description = f"```{help}```"

            elif self.bot.get_command(arg.lower()):
                command = self.bot.get_command(arg.lower())
                title = f"Help for command {arg.lower()}"
                description = (
                    f"```{get_help(command, subcommands=True, show_hidden=True)}```"
                )

            else:
                title = "Not found!"
                description = f"Command/cog {arg} not found"
                color = discord.Color.red()

        if color:
            embed.color = color
        embed.title = title
        embed.description = description
        return await context.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Help(bot))
