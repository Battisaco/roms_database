from typing import TypedDict

class Console(TypedDict):
    name: str
    image: str

class Game(TypedDict):
    name: str
    image: str
    rating: float
    release_date: str

class Rom(TypedDict):
    name: str
    size: str
    type: str
    provider:str
    url: str
    version: str
