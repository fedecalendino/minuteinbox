from typing import Iterator, Tuple
from uuid import uuid4

import requests
from requests import Response


def _get(service: str, token: str, address: str = None) -> Response:
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
    return response


def inbox() -> Tuple[str, str]:
    token = str(uuid4()).replace("-", "")

    json = _get("index/index", token).json()
    return json["email"], token


def content(address: str, token: str, id: str) -> str:
    response = _get(f"email/id/{id}", token, address)

    return response.text


def refresh(address: str, token: str) -> Iterator[dict]:
    json = _get("index/refresh", token, address).json()

    for mail in json:
        sender_name, sender_address = mail["od"].split(" <")

        yield {
            "id": mail["id"],
            "sent_at": mail["kdy"],
            "is_new": mail["precteno"] == "new",
            "sender": {
                "name": sender_name,
                "address": sender_address[:-1],
            },
            "subject": mail["predmet"],
            "content": content(address, token, mail["id"]),
        }


def times(address: str, token: str) -> dict:
    json = _get("index/zivot", token, address).json()

    return {
        "created_at": json["ted"],
        "expires_at": json["konec"],
    }


def extend(address: str, token: str, seconds: int) -> dict:
    _get(f"expirace/{seconds}", token, address)
