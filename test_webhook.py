"""
测试 bot.py

headers: User-Agent:[QQBot-Callback] X-Bot-Appid:[11111111]
body: {"d":{"plain_token":"Arq0D5A61EgUu4OxUvOp","event_ts":"1725442341"},"op":13},
"""

import requests
import json


def send_post_request():
    url = "http://127.0.0.1:8433/webhook"
    headers = {
        "User-Agent": "[QQBot-Callback]",
        "X-Bot-Appid": "[11111111]"
    }
    data = {
        "d": {
            "plain_token": "Arq0D5A61EgUu4OxUvOp",
            "event_ts": "1725442341"
        },
        "op": 13
    }
    response = requests.post(url, headers=headers, json=data)
    print(response)
    if response.status_code == 200:
        print("Request was successful")
        print(response.text)

    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    send_post_request()