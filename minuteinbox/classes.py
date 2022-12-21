from datetime import datetime
from typing import Iterator

from minuteinbox import api


class Account:
    def __init__(self, **data):
        self.name: str = data["name"]
        self.address: str = data["address"]


class Mail:
    def __init__(self, **data):
        self.id: str = data["id"]
        self.sent_at: str = data["sent_at"]
        self.is_new: bool = data["is_new"]
        self.sender: Account = Account(**data["sender"])
        self.subject: str = data["subject"]
        self.content: str = data["content"]


class Inbox:
    def __init__(self, address: str = None, token: str = None):
        if not address and not token:
            address, token = api.inbox()

        self.address: str = address
        self.token: str = token

    @property
    def mails(self) -> Iterator[Mail]:
        for mail in api.refresh(self.address, self.token):
            yield Mail(**mail)

    def extend_10m(self):
        api.extend(self.address, self.token, seconds=4200)

    def extend_1h(self):
        api.extend(self.address, self.token, seconds=3600)

    def extend_1d(self):
        api.extend(self.address, self.token, seconds=86400)

    def extend_1w(self):
        api.extend(self.address, self.token, seconds=604800)

    @property
    def expires_in(self):
        times = api.times(self.address, self.token)

        if times["expires_at"] is None:
            raise ValueError(f"{self.address} has expired")

        created_at = datetime.strptime(times["created_at"], "%Y-%m-%d %H:%M:%S")
        expires_at = datetime.strptime(times["expires_at"], "%Y-%m-%d %H:%M:%S")

        return (expires_at - created_at).seconds
