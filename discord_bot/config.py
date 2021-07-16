import os
import re
from os.path import exists
from typing import NamedTuple

import yaml


def _constructor_env_variables(loader, node):
    pattern = re.compile(r".*?\${(\w+)}.*?")
    value = loader.construct_scalar(node)
    match = pattern.findall(value)
    if match:
        full_value = value
        for g in match:
            full_value = full_value.replace(f"${{{g}}}", os.environ.get(g, g))
        return full_value
    return value


def _construct_yaml_tuple(self, node):
    seq = self.construct_sequence(node)
    return tuple(seq)


yaml.SafeLoader.add_constructor("tag:yaml.org,2002:python/tuple", _construct_yaml_tuple)
yaml.SafeLoader.add_constructor("!ENV", _constructor_env_variables)

if not exists("config.yml"):
    with open("ex_config.yml") as f:
        config = yaml.safe_load(f)
else:
    with open("config.yml") as f:
        config = yaml.safe_load(f)


class BotConfig(NamedTuple):
    TOKEN = config["bot"].get("TOKEN")
    prefix = config["bot"].get("prefix", ("a!", "A!"))
    description = config["bot"].get("description", "Anime girls bot")
    activity = config["bot"].get("activity", "with anime girls")
    large_image = config["bot"].get("large_image", None)
    mongodb = config["bot"].get("mongodb", None)
