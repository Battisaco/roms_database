from typing import TypedDict

class Console(TypedDict):
    id: str
    name: str
    image: str
    url: dict

class Game(TypedDict):
    id: str
    console_id: str
    name: str
    image: str
    console: str
    url: dict

class Rom(TypedDict):
    id: str
    game_id: str
    name: str
    size: str
    type: str
    link: str
    provider:str
    version: str
