import functools
from collections import OrderedDict
from typing import Any, Callable


class AsyncCache:
    """
    LRU cache implementation for coroutines
    Since functools.lru_cache doesn't support coroutines
    """

    def __init__(self, max_size: int = 128):
        self._cache = OrderedDict()
        self._max_size = max_size

    def __call__(self, arg_offset: int = 0) -> Callable:
        def decorator(function: Callable) -> Callable:
            @functools.wraps(function)
            async def wrapper(*args, **kwargs) -> Any:
                key = args[arg_offset:]

                if key not in self._cache:
                    if len(self._cache) > self._max_size:
                        self._cache.popitem(last=False)

                    self._cache[key] = await function(*args, **kwargs)
                return self._cache[key]
            return wrapper
        return decorator

    def clear(self) -> None:
        self._cache.clear()
