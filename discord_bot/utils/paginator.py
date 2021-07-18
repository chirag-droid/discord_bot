import asyncio

import discord
from discord.ext import commands

from discord_bot.bot import Bot


class Paginator:
    def __init__(
        self,
        ctx: commands.Context,
        embed: discord.Embed,
        embeds: list[discord.Embed] = [],
        timeout=10,
    ):
        self.ctx = ctx
        self.bot: Bot = ctx.bot
        self.timeout = timeout
        self.embed = embed
        self.embeds = embeds

    def make_embeds(self):
        if len(self.embeds) != 0:
            return self.embeds

        base_embed = self.embed.copy()
        base_embed._fields = []
        fields = self.embed._fields.copy()

        for i in range((len(fields) // 3) + 1):
            start = i * 3
            base_embed._fields = [*fields[start:start + 3]]
            self.embeds.append(base_embed.copy())

    async def run(self):
        self.make_embeds()
        await self.loop()

    async def loop(self):
        current = 0
        mes: discord.Message = await self.ctx.send(embed=self.embeds[current])
        await mes.add_reaction("⬅️")
        await mes.add_reaction("➡️")

        def check(r: discord.Reaction, u: discord.User):
            return u == self.ctx.author and str(r.emoji) in "⬅️ ➡️"

        while True:
            try:
                reaction, _user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=self.timeout
                )

                if str(reaction.emoji) == "⬅️":
                    current -= 1
                elif str(reaction.emoji) == "➡️":
                    current += 1

                if current == len(self.embeds):
                    current = 0
                elif current < 0:
                    current = len(self.embeds) - 1

                await mes.edit(embed=self.embeds[current])

            except asyncio.TimeoutError:
                break
