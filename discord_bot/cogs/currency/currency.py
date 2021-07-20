from typing import Union
import discord
from discord.ext import commands
from discord_bot.bot import Bot
from discord_bot.utils.cache import AsyncCache
from pymongo.collection import Collection
from discord_bot.utils.messages import formatDocstr

async_cache = AsyncCache(max_size=256)


class Currency(commands.Cog):
    """A currency cog with commands like balance, share etc."""
    def __init__(self, bot: Bot):
        self.bot = bot
        self.collection: Collection = self.bot.mongoClient.users.currency

    @async_cache(arg_offset=1)
    async def get_data(self, id):
        data = await self.collection.find_one({"_id": id})
        data.pop('_id')
        if not data:
            await self.collection.insert_one({'_id': id, 'wallet': 0, 'bank': 1000})
            data = {'wallet': 0, 'bank': 1000}
        return data

    async def update_data(self, id: int, data: dict[str, Union[str, int]]):
        await self.collection.update_many({'_id': id}, {'$set': data})
        async_cache._cache[(id,)].update(data)

    @commands.command(aliases=['balance', 'wallet', 'bank', 'amount'])
    async def bal(self, ctx: commands.Context):
        """A currency command to know ou current balance."""
        data = await self.get_data(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author}'s balance"
        description = f"""
            **Wallet** - {data.get('wallet')}
            **Bank** - {data.get('bank')}
        """
        embed.description = formatDocstr(description)
        embed.color = discord.Color.random()

        await ctx.send(embed=embed)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx: commands.Context, amount: str = None):
        """Deposit your money from your wallet to bank"""
        if not amount.isnumeric():
            return await ctx.send("You had to enter a number not your dumb feelings.")
        amount = int(amount)

        data = await self.get_data(ctx.author.id)
        wallet = data.get('wallet')
        bank = data.get('bank')

        if amount <= 0:
            return await ctx.send("You can't deposit negative or zero amount.")
        if wallet < amount:
            return await ctx.send("Come back when you have that much money, kiddo")

        wallet -= amount
        bank += amount
        await self.update_data(ctx.author.id, {'wallet': wallet, 'bank': bank})

        await ctx.send(f"Success. Deposited {amount}, now you have {wallet} in wallet")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx: commands.Context, amount: str = None):
        """Withdraw money from your bank to wallet"""
        if not amount.isnumeric():
            return await ctx.send("You had to enter a number not your dumb feelings.")
        amount = int(amount)

        data = await self.get_data(ctx.author.id)
        wallet = data.get('wallet')
        bank = data.get('bank')

        if amount <= 0:
            return await ctx.send("You can't withdraw negative or zero amount.")
        if bank < amount:
            return await ctx.send("Come back when you have that much money, kiddo")

        wallet += amount
        bank -= amount
        await self.update_data(ctx.author.id, {'wallet': wallet, 'bank': bank})

        await ctx.send(f"Success. Withdrawed {amount}, now you have {bank} in bank")


def setup(bot: Bot):
    bot.add_cog(Currency(bot))
