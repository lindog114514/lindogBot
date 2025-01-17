"""
负责QQ机器人整个后端
"""
from flask import Flask, request, jsonify
import bot_log
import bot_tool
import json
import os


help_page = ('''
            <!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <title>SuperQQBot管理后端</title>
</head>
<body>
<div style="text-align: center">
    <img alt="lindogBot图标" src="../Logo.png" style="display: inline-block;">
    <h1 style="color: #00a1d6">lindogBot管理后端</h1>
    <h2 style="color: #00a1d6">管理后端正在运行</h2>
    <h2 style="color: #00a1d6">请使用专用工具访问</h2>
</div>
</body>
</html>''')


log = bot_log.HandleLog()
app = Flask(__name__)
test_config = bot_tool.read(os.path.join(os.path.dirname(__file__), "config.yaml") )    # 读取bot配置文件
appid = test_config["appid"]
secret = test_config["secret"]


@app.route('/')
def help_a():           # 接收到非webhook请求时将返回网页
    log.info('接收非POST请求')
    try:
        json_data = json.loads(request.data)
        log.info(f"非POST请求中json数据为: {json_data}")
        return jsonify(json_data)  # 使用 jsonify 函数正确返回 JSON 数据
    except Exception as e:  # 细化异常处理
        log.info(f'无法解析非POST请求，已返回网页数据，错误信息: {str(e)}')
    return help_page


@app.route("/webhook", methods=['POST'])
def webhook():
    try:
        # 解析请求数据
        json_data = json.loads(request.data)
        log.info(f"接收到json数据 : {json_data}")
        if 'd' in json_data:
            # 开始签名校验
            log.info('接收到回调验证请求')
            plain_token = json_data["d"]["plain_token"]
            event_ts = json_data["d"]["event_ts"]
            log.info('接收到plain_token: %s' % plain_token)
            log.info('接收到event_ts: %s' % event_ts)
            signature_response = bot_tool.signature(bot_secret=secret, event_ts=event_ts, plain_token=plain_token)
            try:
                signature_data = json.loads(signature_response)
                log.info('签名成功已正常返回')
                return jsonify(signature_data), 200
            except json.JSONDecodeError:
                log.error("Invalid signature response received.")
                return jsonify({"error": "Invalid signature response."}), 400
        return jsonify({"status": "success", "data": json_data}), 200
    except json.JSONDecodeError:            # 非json数据异常处理
        log.error("Invalid JSON data received.")
        return jsonify({"error": "Invalid JSON data"}), 400


if __name__ == "__main__":
    app.run(port=8433)