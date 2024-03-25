from functools import wraps
from datetime import datetime
from typing import (
    Callable,
    TypeVar,
)


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


def correct_tag(tag: str, prefix: str = "#") -> str:
    return prefix + tag.lstrip(prefix).upper()


def corrected_tag(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        print(args, kwargs)
        args = list(args)
        args[1] = correct_tag(args[1])
        return func(*tuple(args), **kwargs)

    return wrapper


def from_timestamp(timestamp) -> datetime:
    if isinstance(timestamp, datetime):
        return timestamp
    else:
        return datetime.strptime(timestamp, "%Y%m%dT%H%M%S.000Z")
