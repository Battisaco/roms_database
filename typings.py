from typing import TypedDict


class Console(TypedDict):
    name: str
    image: str
    games: int
    downloads: int
    provider: str
    url: str


class Game(TypedDict):
    name: str
    image: str
    rating: float
    downloads: int
    provider: str
    url: str


class Rom(TypedDict):
    name: str
    size: str
    type: str
    url: str
