# Sakura Python Client

This is a Python client for the Sakura API. It provides methods to authenticate, send messages, get selfies, and more.

## Installation

You can install the Sakura Python Client using pip:

```bash
pip install sakura
```

## Usage

First, import the `Client` class from the `sakura` package:

```python
from sakura import Client
```

Next, create an instance of the `Client` class, passing your Sakura username, password and mongo uri to the constructor:

```python
client = Client({
    "username": your_username,
    "password": your_password,
    "mongo": your_mongodb_uri
})
```

Now you can use the methods of the `Client` class to interact with the Sakura API.

## Sending a Message

To send a message, use the `sendMessage` method by passing a random unique integer as UID you want and a character id and prompt:

```python
# https://www.sakura.fm/chat/dmDCgmq
# the parameter after /chat/ is character id (/chat/{char_id})

response = client.sendMessage(1234, 'dmDCgmq', 'Hello Kazuko')
print(response)
```

reponse will return a json like this:
```json
{
    "chat_id": "u3q9YN7",
    "reply": "*jumps slightly* Oh! Uh, hi there. I didn't see you come in."
}
```

## Getting a Selfie

To get a selfie, use the `get_selfie` method we have to pass that old unique id which we sent in sendMessage:

```python
response = client.get_selfie(1234)
print(response)
```

response will return an image url

## Deleting the database

To delete the databse containing this whole uid to chat id connection, use this function:

```python
response = client.delete_db()
print(response)
```

response will return `True` if it is success

## That's all for now