from typing import Optional
from enum import Enum
from dataclasses import dataclass, asdict


class Status(Enum):
    LOADING = "loading"
    ERROR = "error"
    SUCCESS = "success"
    DONE = "done"
    SEND = "send"


@dataclass
class ImageProgress:
    _id: str
    status: str
    imageUrl: str
    worker: Optional[str] = None


def to_dict(instance):
    return asdict(instance)
