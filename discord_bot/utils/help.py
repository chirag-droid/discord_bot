from itertools import repeat
from typing import Union

from discord.ext import commands

from discord_bot.config import BotConfig


def get_help(command: Union[commands.Command, commands.Group], subcommands=False):
    """
    A util function that walks through all commands recursivey and returns help str.
    """
    prefix = BotConfig.prefix
    if not isinstance(prefix, str):
        prefix = prefix[0]

    if subcommands and isinstance(command, commands.Group):
        command_list = [command, *command.walk_commands()]
        return "\n\n".join(map(get_help, command_list))

    aliases = command.aliases
    if len(aliases) > 0:
        aliases = f"Command aliases - {', '.join(aliases)}"
    else:
        aliases = ""

    help_text = f"{prefix}{command.qualified_name} - {command.help}\n{aliases}"
    if command.hidden:
        return f"||{help_text}||"
    return help_text


def get_help_cog(cog: commands.Cog, subcommands=False):
    """A util function to get help text for a cog"""
    commands = cog.get_commands()
    return map(get_help, commands, repeat(subcommands))
