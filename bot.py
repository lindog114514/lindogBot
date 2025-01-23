"""
负责QQ机器人整个后端
"""
from flask import Flask, request, jsonify
import bot_log
import bot_tool
import json,os


log = bot_log.HandleLog()
app = Flask(__name__)
test_config = bot_tool.read(os.path.join(os.path.dirname(__file__), "config.yaml") )    # 读取bot配置文件
appid = test_config["appid"]
secret = test_config["secret"]
host = test_config["host"]
port = test_config["port"]
pem = test_config["pem"]
key = test_config["key"]
token = bot_tool.Token(app_id=appid,secret=secret)
# https://api.sgroup.qq.com



@app.route('/')
def help_a():           # 接收到非webhook请求时将返回网页
    log.info('接收非POST请求')
    try:
        json_data = json.loads(request.data)
        log.info(f"非POST请求中json数据为: {json_data}")
        return jsonify(json_data)  # 使用 jsonify 函数正确返回 JSON 数据
    except Exception as e:  # 细化异常处理
        log.info(f'无法解析非POST请求，已返回网页数据，错误信息: {str(e)}')
    return send_from_directory('.', 'index.html')


@app.route("/webhook", methods=['POST'])
def webhook():
    # 解析请求数据
    data = json.loads(request.data)
    log.info(f"接收到json数据 : {data}")
    token.update_access_token() #获取accesstoken
    # 基本信息
    op = data.get('op', 'Unknown')
    message_id = data.get('id', 'Unknown')
    timestamp = data['d'].get('timestamp', 'No timestamp')
    t = data.get('t', 'Unknown')
    if op == 0:
        if t == "GROUP_AT_MESSAGE_CREATE":   #群消息事件 AT 事件
            # 群组信息
            group_id = data['d'].get('group_id', 'Unknown group ID')
            group_openid = data['d'].get('group_openid', 'Unknown group openid')
            content = data['d'].get('content', 'No content')
            log.info(f"接收到群聊消息内容为:{content}") # 消息内容
            log.info(f"接收到群聊id内容为:{group_openid}")
            if attachments:
                for attachment in attachments:
                    url = attachment.get('url', 'No URL')
                    log.info(f"接收到附件信息 URL: {url}")
        elif t == "GROUP_ADD_ROBOT" : #群添加机器人
            group_id = data['d'].get('group_id', 'Unknown group ID')
            log.info(f"群添加机器人:{group_id}")
        elif t == "GROUP_MSG_RECEIVE": #群打开消息推送
            group_id = data['d'].get('group_id', 'Unknown group ID')
            log.info(f"群打开消息推送:{group_id}")
        elif t == "GROUP_MSG_REJECT":  #群关闭消息推送
            group_id = data['d'].get('group_id', 'Unknown group ID')
            log.info(f"群关闭消息推送:{group_id}")
        elif t == 'C2C_MESSAGE_CREATE':  #C2C消息事件
            user_openid = data.get('user_openid', 'Unknown')
            content = data['d'].get('content', 'No content')
            log.info(f"接收到单聊消息内容为:{content}")  # 消息内容
        elif t == "AT_MESSAGE_CREATE":    #频道内AT机器人的消息的事件
            # 频道信息
            group_id = data['d'].get('group_id', 'Unknown group ID')
            group_openid = data['d'].get('group_openid', 'Unknown group openid')
            content = data['d'].get('content', 'No content')
            log.info(f"接收到频道消息内容为:{content}") # 消息内容
            log.info(f"接收到频道id内容为:{channel_id}")
            if attachments:
                for attachment in attachments:
                    url = attachment.get('url', 'No URL')
                    log.info(f"接收到附件信息 URL: {url}")
    elif op == 13:
        if 'd' in data:
            # 开始签名校验
            log.info('接收到回调验证请求')
            plain_token = json_data["d"]["plain_token"]
            event_ts = json_data["d"]["event_ts"]
            log.info('接收到plain_token: %s' % plain_token)
            log.info('接收到event_ts: %s' % event_ts)
            signature_response = bot_tool.signature(bot_secret=secret, event_ts=event_ts, plain_token=plain_token)
            try:
                signature_data = json.loads(signature_response)
                log.info('回调验证已正常返回')
                return jsonify(signature_data), 200
            except json.JSONDecodeError:
                log.error("Invalid signature response received.")
                return jsonify({"error": "Invalid signature response."}), 400

    return jsonify({"status": "success", "data": json_data}), 200  #防止flash当没有接收返回数据的时候报错

if __name__ == "__main__":
    app.run(port=port,host=host,ssl_context=(pem,key),debug=True)
