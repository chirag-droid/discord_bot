from itertools import repeat
from typing import Union

from discord.ext import commands

from discord_bot.config import BotConfig


def get_help(
    command: Union[commands.Command, commands.Group],
    subcommands=False,
    show_hidden=False,
):
    """
    A util function that walks through all commands recursivey and returns help str.
    """
    if not show_hidden and command.hidden:
        return ""

    prefix = BotConfig.prefix
    if not isinstance(prefix, str):
        prefix = prefix[0]

    help_text = f"{prefix}{command.qualified_name} - {command.help}"

    aliases = command.aliases
    if len(aliases) > 0:
        help_text += f"\nCommand aliases - {', '.join(aliases)}\n"

    if isinstance(command, commands.Group):
        if subcommands:
            command_list = [command, *command.walk_commands()]
            return "\n\n".join(map(get_help, command_list))
        subcommand_names = ", ".join([x.name for x in command.walk_commands()])
        help_text += f"Command Subcommands - {subcommand_names}"

    return help_text


def get_help_cog(cog: commands.Cog, subcommands=False, show_hidden=False):
    """A util function to get help text for a cog"""
    commands = cog.get_commands()
    return map(get_help, commands, repeat(subcommands), repeat(show_hidden))
