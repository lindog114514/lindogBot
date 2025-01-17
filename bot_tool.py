"""
负责签名校验的加密算法
以及读取文件等
"""
import yaml
from typing import Dict, Any
import bot_log
from cryptography.hazmat.primitives.asymmetric import ed25519

log = bot_log.HandleLog()


def read(yaml_path) -> Dict[str, Any]: #读取指定目录的yaml文件
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

"""

"""
def signature(botSecret, eventTs, plainToken):
    log.info('开始进行回调验证 ')
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
    return signature_hex
