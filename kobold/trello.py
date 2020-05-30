import requests
import json
from typing import Dict

from .taskdb import TaskDB
from .task import Task

boards = "https://api.trello.com/1/members/me/boards"
cards = "https://api.trello.com/1/members/me/cards"


def request(url, config):
    secrets = ["token", "key"]
    access = dict((k, v) for k, v in config.items() if k in secrets)
    headers = {"Accept": "application/json"}
    return requests.request("GET", url, headers=headers, params=access)


def get_boards(config):
    response = request(boards, config)
    content = json.loads(response.content)
    print("\n".join([f"{board['id']}: {board['name']}" for board in content]))


def get_cards(config):
    response = request(cards, config)
    content = json.loads(response.content)
    return content


def tasks(config) -> TaskDB:
    cards = get_cards(config)
    board = lambda c: config["ids"][c["idBoard"]]

    def to_task(c):
        return Task(
            name=c["name"],
            project=board(c)["name"],
            due=c["due"],
            state="done" if c["idList"] == board(c)["done"] else "todo",
        )

    tdb = TaskDB({})
    for c in cards:
        tdb.add(to_task(c))
    return tdb
