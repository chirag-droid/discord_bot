import pkgutil
from typing import Iterator

from discord_bot import cogs


def walk_extensions() -> Iterator[str]:
    for ext in pkgutil.walk_packages(cogs.__path__, f"{cogs.__name__}."):
        if ext.ispkg:
            continue
        yield ext.name
