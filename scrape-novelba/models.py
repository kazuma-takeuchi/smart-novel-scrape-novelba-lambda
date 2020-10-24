from typing import Dict, List
from datetime import date, datetime

from pydantic import BaseModel, validator

class NovelModel(BaseModel):
    key: str = None
    title: str = None
    url: str = None
    site_name: str = None
    author: str = None
    description: str = None
    created_at: float = None
    updated_time: float = None
    genre: str = None
    tag: List[str] = None
    length: int = None
    like_count: int = None
    pv: int = None
    contents: str = None
    sys_created_at: float = None


DEFAULT_DOCUMENT = {
    "key": None,
    "title": None,
    "url": None,
    "site_name": None,
    "author": None,
    "description": None,
    "created_at": None,
    "updated_time": None,
    "genre": None,
    "tag": None,
    "length": None,
    "like_count": None,
    "pv": None,
    "contents": None,
    "sys_created_at": None
}


if __name__ == "__main__":
    pass