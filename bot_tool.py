"""
负责签名校验的加密算法
以及读取文件和获取调用凭证
"""

import yaml
from typing import Dict, Any
import bot_log
import time
import requests
import json
import sys
from cryptography.hazmat.primitives.asymmetric import ed25519
log = bot_log.HandleLog()


def read(yaml_path) -> Dict[str, Any]: #读取指定目录的yaml文件
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

"""
回调验证
"""
def generate_signature(botSecret, eventTs, plainToken):
    # 对 botSecret 进行处理，确保长度足够
    seed = botSecret
    while len(seed) < 32:  # ed25519.SeedSize 一般为 32
        seed = seed * 2
    seed = seed[:32]
    seed_bytes = seed.encode('utf-8')
    # 使用 cryptography 生成 Ed25519 私钥
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
    # 构造要签名的消息
    msg = (eventTs + plainToken).encode('utf-8')
    # 进行签名
    signature = private_key.sign(msg)
    # 将签名结果转换为十六进制字符串
    signature_hex = signature.hex()
    # 构建包含 plain_token 和 signature 的 JSON 数据
    result = {
        "plain_token": plainToken,
        "signature": signature_hex
    }
    # 将结果转换为 JSON 格式的字符串
    result_json = json.dumps(result)
    return result_json


def signature(bot_secret, event_ts, plain_token):
    result = generate_signature(bot_secret, event_ts, plain_token)
    log.info(result)
    return result
"""
获取调用凭证
access_token
HTTP Method = port
"""
class Token:
    TYPE_BOT = "QQBot"
    TYPE_NORMAL = "Bearer"

    def __init__(self, app_id: str, secret: str):
        self.app_id = app_id
        self.secret = secret
        self.access_token = None
        self.expires_in = 0
        self.token_type = self.TYPE_BOT  # 更改变量名，符合命名规范

    def check_token(self):
        """
        检查令牌是否过期或不存在，如果过期或不存在则更新令牌
        """
        if self.access_token is None or int(time.time()) >= self.expires_in:
            self.update_access_token()

    def update_access_token(self):
        """
        发送 POST 请求更新访问令牌，并处理响应
        """
        url = "https://bots.qq.com/app/getAppAccessToken"
        payload = {
            "appId": self.app_id,
            "clientSecret": self.secret,
        }
        try:
            response = requests.post(url, json=payload, timeout=20)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            if "access_token" not in data or "expires_in" not in data:
                log.error("获取token失败，请检查appid和secret填写是否正确！")
            else:
                self.access_token = data["access_token"]
                self.expires_in = int(data["expires_in"]) + int(time.time())
        except requests.exceptions.RequestException as e:
            log.error(f"更新token时发生错误: {e}")

    def get_access_token(self):
        """
        获取存储的访问令牌
        """
        return self.access_token