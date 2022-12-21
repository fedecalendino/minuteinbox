from typing import Iterator, Tuple
from uuid import uuid4

import requests


def _get(service: str, token: str, address: str = None) -> dict:
    if not address:
        cookie = f"PHPSESSID={token}"
    else:
        cookie = f"PHPSESSID={token}; MI={address}; wpcc=dismiss"

    headers = {
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "close",
        "Cookie": cookie,
    }

    response = requests.get(
        url=f"https://www.minuteinbox.com/{service}",
        headers=headers,
        allow_redirects=True,
    )

    response.encoding = "utf-8-sig"
    return response.json()


def inbox() -> Tuple[str, str]:
    token = str(uuid4()).replace("-", "")

    json = _get("index/index", token)
    return json["email"], token


def refresh(address: str, token: str) -> Iterator[dict]:
    json = _get("index/refresh", token, address)

    for mail in json:
        sender_name, sender_address = mail["od"].split(" <")

        yield {
            "id": mail["id"],
            "sent_at": mail["kdy"],
            "subject": mail["predmet"],
            "content": mail["akce"],
            "sender": {
                "name": sender_name,
                "address": sender_address[:-1],
            },
        }


def times(address: str, token: str) -> dict:
    json = _get("index/zivot", token, address)

    return {
        "created_at": json["ted"],
        "expires_at": json["konec"],
    }


def extend(address: str, token: str, seconds: int) -> dict:
    _get(f"expirace/{seconds}", token, address)
