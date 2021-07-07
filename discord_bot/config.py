from os.path import exists
from typing import NamedTuple

from envyaml import EnvYAML

if not exists("config.yml"):
    config = EnvYAML("ex_config.yml")
else:
    config = EnvYAML("config.yml")


class BotConfig(NamedTuple):
    TOKEN = config["bot"].get("TOKEN")
    prefix = config["bot"].get("prefix", "a!")
    description = config["bot"].get("description", "Anime girls bot")
    activity = config["bot"].get("activity", "with anime girls")
    large_image = config["bot"].get("large_image", None)
