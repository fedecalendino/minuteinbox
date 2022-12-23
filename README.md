 # minuteinbox

[![Version](https://img.shields.io/pypi/v/minuteinbox?logo=pypi)](https://pypi.org/project/minuteinbox)
[![Quality Gate Status](https://img.shields.io/sonar/alert_status/fedecalendino_minuteinbox?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_minuteinbox)
[![CodeCoverage](https://img.shields.io/sonar/coverage/fedecalendino_minuteinbox?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_minuteinbox)

Unofficial python wrapper for minuteinbox.com


### usage

```python
from minuteinbox import Inbox

# use without parameters to create a new inbox
# inbox = Inbox()

# use with address and token to reuse an existing inbox
inbox = Inbox(
    address="maximo.kayo@moontrack.net",
    token="86d6b9308a1a482ba348533a457146c4",
)

address = inbox.address
token = inbox.token

print(address, "(", token, ")")
print()

# extend the expiration of the inbox by 10 minutes
inbox.extend_10m()

print("Expires in:", inbox.expires_in, "seconds")
print()

# fetch all emails in the inbox
for mail in inbox.mails:
    print("FROM:", mail.sender.name, mail.sender.address)
    print("SUBJECT:", mail.subject)
    print("SENT AT:", mail.sent_at)
    print("IS NEW:", mail.is_new)

    print("CONTENT")
    print(mail.content)
```