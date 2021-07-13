import discord
from discord.ext import commands

from discord_bot.config import BotConfig


class Help(commands.Cog, name="Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context, arg=None):
        """
        List all commands from every Cog the bot has loaded.
        """
        if not arg:
            embed = discord.Embed(
                title="Help Commands",
                description="List of available commands:",
                color=0x42F56C,
            )
            for i in self.bot.cogs:
                cog = self.bot.get_cog(i)
                help_text = self.get_help_cog(cog)
                if help_text:
                    embed.add_field(
                        name=i.capitalize(),
                        value=f"```{self.get_help_cog(cog)}```",
                        inline=False,
                    )

        else:
            if arg.capitalize() in self.bot.cogs:
                help_text = self.get_help_cog(arg.capitalize())
            elif self.bot.get_command(arg.lower()):
                help_text = self.get_help(self.bot.get_command(arg.lower()))
            else:
                embed = discord.Embed(
                    title="Not found!",
                    description=f"Command/cog {arg} not found",
                    color=discord.Color.red(),
                )
                return await context.send(embed=embed)

            embed = discord.Embed(
                title=f"Help command for {arg}",
                description=f"```{help_text}```",
                color=0x42F56C,
            )

        return await context.send(embed=embed)

    def get_help_cog(self, cog: commands.Cog):
        if isinstance(cog, str):
            cog = self.bot.get_cog(cog)
        commands = cog.get_commands()
        return "\n".join([self.get_help(command) for command in commands])

    @staticmethod
    def get_help(command: commands.Command):
        prefix = BotConfig.prefix
        if not isinstance(prefix, str):
            prefix = prefix[0]
        return f"{prefix}{command.name} - {command.help}"


def setup(bot):
    bot.add_cog(Help(bot))
