import os
import pickle

import jieba

from tts import text_to_speech
from qrcode_maker import gen_qrcode
from vervity_email import send_mail
from random import randint, seed

import botpy
from botpy.message import GroupMessage, C2CMessage
from botpy.manage import C2CManageEvent
from botpy.ext.cog_yaml import read
from botpy.errors import ServerError
from botpy import logging

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
if "out.pkl" in os.listdir():
    with open("out.pkl", 'rb') as file:
        data = pickle.load(file)
        output_dict = data[0]
        Admin_id = data[1]
        try:
            users = data[2]
        except IndexError:
            users = {"Supercmd": "E181D0921FBB1441982DB09A34B2DB68"}

else:
    output_dict = dict()
    Admin_id = list()
    users = {"Supercmd": "E181D0921FBB1441982DB09A34B2DB68"}

_log = logging.get_logger()
Boss_id = "E181D0921FBB1441982DB09A34B2DB68"
Boss_mode = False
tries = 0
white = False
requests_usr = {}


def upload_img(img):
    with open(img, "rb") as i:
        i.read()


class MyClient(botpy.Client):
    async def on_friend_add(self, event: C2CManageEvent):
        _log.info("用户添加机器人：" + str(event))
        await self.api.post_c2c_message(
            openid=event.openid,
            msg_type=0,
            event_id=event.event_id,
            content="hello",
        )

    async def on_c2c_message_create(self, message: C2CMessage):
        _log.info(message.author.user_openid)
        if message.author.user_openid == Boss_id:
            await message.api.post_c2c_message(
                openid=message.author.user_openid,
                msg_type=0, msg_id=message.id,
                content="欢迎管理员Supercmd"
            )
            messageResult = str()
            _log.info(f"收到了消息：{message.content}")
            splited_content = message.content.split()
            if splited_content[0] == "/修复关联":
                global output_dict
                if len(splited_content) == 1:
                    messageResult = await message.api.post_c2c_message_message(
                        openid=message.author.user_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="若要清除所有关联，请带all参数")
                else:
                    if splited_content[1] == "all":
                        output_dict = {}
                        messageResult = await message.api.post_c2c_message_message(
                            openid=message.author.user_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="已清除所有内容，若要保存更改请关机")
                    else:
                        output_dict.pop(splited_content[1])
                        messageResult = await message.api.post_c2c_message_message(
                            openid=message.author.user_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content=f"已清除{splited_content[1]}，若要保存更改请关机")
                _log.info(messageResult)

    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        global output_dict, Boss_mode, tries, white, Admin_id, requests_usr, users
        messageResult = str()
        _log.info(f"收到了消息：{message.content}")
        splited_content = message.content.split()
        try:
            if len(message.attachments) == 0 and len(splited_content) >= 1:
                if splited_content[0] == "/验证":
                    if len(splited_content) == 1:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="权限不足")
                    else:
                        if int(splited_content[1]) not in requests_usr.keys():
                            messageResult = await message.api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content="验证失败：虚假的注册信息")
                        else:
                            users[requests_usr[int(splited_content[1])]] = message.author.member_openid
                            messageResult = await message.api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content=f"绑定信息已生效，请确认：QQ号为{requests_usr[int(splited_content[1])]}")
                elif splited_content[0] == "/注册":
                    if len(splited_content) == 1:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="非法注册命令，正确命令格式：/注册 QQ号")
                    else:
                        seed(message.author.member_openid)
                        requests_usr[randint(0, 1000)] = splited_content[1]
                        seed(message.author.member_openid)
                        send_mail(splited_content[1], randint(0, 1000))
                        seed(message.author.member_openid)
                        _log.info(randint(0, 1000))
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content=f"已发送邮件至{splited_content[1]}的QQ邮箱，请注意查收")
                elif message.author.member_openid not in users.keys() and message.author.member_openid != Boss_id:
                    messageResult = await message.api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"{message.author.member_openid}还未注册账户，请@我 /注册 你的QQ号进行注册")
                elif Boss_mode:
                    if message.author.member_openid not in Boss_id:
                        if white:
                            messageResult = await message.api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content=f"已记录member_openid：{message.author.member_openid}，设置管理成功")
                            Admin_id.append(message.author.member_openid)
                            white = False
                        else:
                            tries += 1
                            if tries == 1:
                                messageResult = await message.api.post_group_message(
                                    group_openid=message.group_openid,
                                    msg_type=0,
                                    msg_id=message.id,
                                    content="机器人正在调试中，稍安勿躁")
                            elif tries == 2:
                                messageResult = await message.api.post_group_message(
                                    group_openid=message.group_openid,
                                    msg_type=0,
                                    msg_id=message.id,
                                    content="别吵了宝宝，做管理的也不容易啊")
                            elif tries == 3:
                                messageResult = await message.api.post_group_message(
                                    group_openid=message.group_openid,
                                    msg_type=0,
                                    msg_id=message.id,
                                    content="我最后警告你一次，闭嘴！")
                            else:
                                messageResult = await message.api.post_group_message(
                                    group_openid=message.group_openid,
                                    msg_type=0,
                                    msg_id=message.id,
                                    content="烦不烦啊，知不知道怎么闭嘴啊，进就不吃吃罚酒，不跟你吵了，拖出去禁言了！")
                    else:
                        if splited_content[0] == "/结束调试":
                            messageResult = await message.api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content="调试已经结束，嗨起来！")
                            Boss_mode = False
                            tries = 0
                        elif splited_content[0] == "/修复关联":
                            if len(splited_content) == 1:
                                messageResult = await message.api.post_group_message(
                                    group_openid=message.group_openid,
                                    msg_type=0,
                                    msg_id=message.id,
                                    content="若要清除所有关联，请带all参数")
                            else:
                                if splited_content[1] == "all":
                                    output_dict = {}
                                    messageResult = await message.api.post_group_message(
                                        group_openid=message.group_openid,
                                        msg_type=0,
                                        msg_id=message.id,
                                        content="已清除所有内容，若要保存更改请关机")
                                else:
                                    output_dict.pop(splited_content[1])
                                    messageResult = await message.api.post_group_message(
                                        group_openid=message.group_openid,
                                        msg_type=0,
                                        msg_id=message.id,
                                        content=f"已清除{splited_content[1]}，若要保存更改请关机")
                        elif splited_content[0] == "/设置管理员":
                            white = True
                            messageResult = await message.api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content="请管理员目标@我")
                        elif splited_content[0] == "/设置管理员":
                            white = True
                            messageResult = await message.api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content="请管理员目标发消息")
                        else:
                            messageResult = await message.api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content="非法管理员命令")
                elif splited_content[0] == "/开始调试":
                    if message.author.member_openid in Boss_id or message.author.member_openid in Admin_id:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="大Boss好，现在开始调试")
                        Boss_mode = True
                    else:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="滚")
                elif splited_content[0] in output_dict.keys():
                    messageResult = await message.api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=output_dict[splited_content[0]])
                elif splited_content[0] == "/设置关联":
                    if len(splited_content) == 1:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="非法关联，正确语法/设置关联 问题 答案")
                    else:
                        output_dict[splited_content[1]] = splited_content[2]
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content=f"已将问题'{splited_content[1]}'的回答设为'{splited_content[2]}'")
                elif splited_content[0] == "/关机":
                    if message.author.member_openid == Boss_id:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="好的，正在关机，期待与你下次相遇")
                        with open("out.pkl", 'wb') as f:
                            pickle.dump(obj=[output_dict, Admin_id, users], file=f)
                        exit(0)
                    else:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="滚")
                elif splited_content[0] == "/活字印刷":
                    messageResult = await message.api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="此功能正在内测，机器人不回应为正常现象")
                    if len(splited_content) == 1:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="非法活字印刷命令，正确语法：/活字印刷 一大堆文字")
                    else:
                        text_to_speech(splited_content[1])
                elif splited_content[0] == "/分词":
                    if len(splited_content) == 1:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="非法分词命令，正确语法：/分词 原目标 （精准模式【默认】/全模式/搜索引擎模式）")
                    else:
                        out = str()
                        times = 0
                        if len(splited_content) == 2:
                            mode = jieba.cut(splited_content[1])
                        elif splited_content[2] == "搜索引擎模式":
                            mode = jieba.cut_for_search(splited_content[1])
                        elif splited_content[2] == "全模式":
                            mode = jieba.cut(splited_content[1], cut_all=True)
                        else:
                            mode = jieba.cut(splited_content[1])
                        for now in mode:
                            times += 1
                            out += f"\n第{times}项：{now}"
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content=out)
                elif splited_content[0] == "/创建二维码":
                    messageResult = await message.api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="此功能正在内测，机器人不回应为正常现象")
                    if len(splited_content) == 1:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="非法二维码命令，正确语法：/创建二维码 目标")
                    else:
                        gen_qrcode(splited_content[1], "qr.png", "supercmd.jpg")
                elif splited_content[0] == "/必应壁纸":
                    uploadMedia = await message.api.post_group_file(
                        group_openid=message.group_openid,
                        file_type=1,
                        url="http://tool.liumingye.cn/bingimg/img.php"
                    )
                    messageResult = await message.api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=7,  # 7表示富媒体类型
                        media=uploadMedia
                    )
                elif splited_content[0] == "/获取图片":
                    if len(splited_content) == 1:
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content="非法图片获取命令，正确语法：/获取图片 url地址")
                    else:
                        uploadMedia = await message.api.post_group_file(
                            group_openid=message.group_openid,
                            file_type=1,
                            url=splited_content[1]
                        )
                        messageResult = await message.api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=7,  # 7表示富媒体类型
                            media=uploadMedia
                        )
                else:
                    messageResult = await message.api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"没人教过我如何回应{splited_content[0]}啊")
            elif len(splited_content) == 0:
                messageResult = await message.api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="非法命令")
            else:
                messageResult = await message.api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="牛仔暂不支持图片功能哦")
        except ServerError as e:
            await message.api.post_c2c_message(
                openid=message.author.user_openid,
                msg_type=0,
                content=f"牛仔出现问题：{e}"
            )
            messageResult = await message.api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"牛仔出现问题：{e}，已经通知管理员Supercmd")
        _log.info(messageResult)
        _log.info(message.author.member_openid)

if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
