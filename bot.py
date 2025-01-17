from flask import Flask, request, jsonify
import bot_log
import json


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


@app.route('/')
def help_a():
    log.info('接收非POST请求')
    try:
        json_data = json.loads(request.data)
        log.info(f"非POST请求中json数据为: {json_data}")
        return {json_data}
    except:
        log.info('无法解析非POST请求，已返回网页数据 ')
    return help_page


@app.route("/webhook", methods=['POST'])
def webhook():
    try:
        # 解析请求数据
        json_data = json.loads(request.data)
        log.info(f"接收到json数据 : {json_data}")
        # 在这里添加处理 json_data 的逻辑，例如根据不同的数据内容进行不同的操作
        # 以下是一个简单的示例，你可以根据实际需求修改
        if 'type' in json_data:
            if json_data['type'] == 'message':
                log.info("Received a message type of data.")
                # 处理消息类型的数据
            elif json_data['type'] == 'event':
                log.info("Received an event type of data.")
                # 处理事件类型的数据
        return jsonify({"status": "success", "data": json_data}), 200
    except json.JSONDecodeError:
        log.error("Invalid JSON data received.")
        return jsonify({"error": "Invalid JSON data"}), 400


if __name__ == "__main__":
    app.run(port=8433)