import requests
import json
from . import secrets

boards = "https://api.trello.com/1/members/me/boards"
cards = "https://api.trello.com/1/members/me/cards"

access = {
    "key": secrets.key,
    "token": secrets.token,
}

headers = {
    "Accept": "application/json",
}


def get_boards(metadata=None):
    response = requests.request("GET", boards, headers=headers, params=access)
    content = json.loads(response.content)
    from IPython import embed

    embed()
    print([board["name"] for board in content])
    print([board["name"] for board in content])


def get_cards(metadata=None):
    response = requests.request("GET", cards, headers=headers, params=access)
    content = json.loads(response.content)
    from IPython import embed

    embed()
    print("\n".join([board["name"] for board in content]))
