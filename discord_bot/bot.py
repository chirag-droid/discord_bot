import platform
import traceback

import discord
from discord.ext import commands

import discord_bot


class Bot(commands.Bot):
    def __init__(self, *args, mongoClient, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongoClient = mongoClient

    async def login(self, *args, **kwargs):
        await self.ping_mongodb()
        return await super().login(*args, **kwargs)

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(f"Start time: {discord_bot.start_time}")
        print(f"Running bot version {discord_bot.__version__}")
        print(f"Discord.py API version: {discord.__version__}")
        print(f"Python Version {platform.python_version()}")
        print("----------------------")

    def add_cog(self, cog: commands.Cog):
        super().add_cog(cog)
        print(f"Succesfully Loaded cog: {cog.qualified_name}")

    async def ping_mongodb(self):
        print("\nEstablishing connection to mongoDb...")

        try:
            await self.mongoClient.server_info()
            print("Connection to mongodb was succesful\n")
        except Exception:
            print("Coudn't connect to mongodb")
            traceback.print_exc()

    async def close(self):
        print("Closing mongoDb session.")
        self.mongoClient.close()
        return await super().close()
