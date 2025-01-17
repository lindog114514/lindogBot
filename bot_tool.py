"""
负责签名校验的加密算法
以及读取文件等
"""
import yaml
from typing import Dict, Any
import bot_log
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import json
import logging

log = bot_log.HandleLog()


def read(yaml_path) -> Dict[str, Any]: #读取指定目录的yaml文件
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

"""
    Signature = HTTP Header 中透传 Signature
    Timestamp = HTTP Header 透传的签名时间戳	
    Body = HTTP 请求中 Body 值
    secret = 机器人密钥 
"""


def handle_validation(bot_secret, event_ts, plain_token):
    # 生成种子
    seed = bot_secret
    while len(seed) < 32:
        seed += seed
    seed = seed[:32]
    # 生成私钥
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed.encode())
    # 生成签名
    msg = event_ts + plain_token
    signature = private_key.sign(msg.encode())
    return signature


# 示例调用
if __name__ == "__main__":
    bot_secret = "your_bot_secret"
    event_ts = "1234567890"
    plain_token = "abcdefg"
    result = handle_validation(bot_secret, event_ts, plain_token)
    print(result)