import asyncio
import json
from botpy.manage import GroupManageEvent
import os
import botpy
from botpy import logging
from botpy.message import GroupMessage, Message
from botpy.types.permission import APIPermissionDemandIdentify
from botpy.ext.cog_yaml import read
from datetime import datetime
from botpy.message import  C2CMessage
from email.mime.text import MIMEText
import random


test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))




_log = logging.get_logger()
sign = 0

ziaoliggog_num = 0


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        _log.info(f"收到了消息：{message.content}")
        splited_content = message.content.split()
        if splited_content[0] == '我要玩林狗':

            if random.choice([True, False]):
                global ziaoliggog_num
                ziaoliggog_num =+ 1
                uploadMedia = await message._api.post_group_file(
                  file_type=1,
                  url="https://cn-sy1.rains3.com/lindog/lingdog_.over.png",
                  group_openid= message.group_openid
                )
                messageResult = await message._api.post_group_message(
                  group_openid=message.group_openid,
                  msg_type=7,  # 7表示富媒体类型
                  msg_id=message.id,
                  media=uploadMedia,
                  content="啊~~~~~~~~~~~~~~~~~~~~~~~~~"
                )
            else:
                uploadMedia = await message._api.post_group_file(
                  file_type=1,
                  url="https://cn-sy1.rains3.com/lindog/lindog_win.jpg",
                  group_openid= message.group_openid
                )
                messageResult = await message._api.post_group_message(
                  group_openid=message.group_openid,
                  msg_type=7,  # 7表示富媒体类型
                  msg_id=message.id,
                  media=uploadMedia,
                  content="林狗躲过去了，并狠狠的嘲笑你：～杂鱼～～杂鱼～～杂鱼～～杂鱼～～杂鱼～～杂鱼～"
                )
        elif splited_content[0] =='签到':
                now = datetime.now()
                await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0, 
                     msg_id=message.id,
                     content=f"签到中")
                if 6 <= now.hour < 23:
                    global sign
                    sign += 1
                    await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        msg_seq= 2,
                        content=f"签到成功，你是第%d个人签到的"%(sign))
                else:
                     await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0, 
                     msg_id=message.id,
                     msg_seq=2,
                     content=f"签到失败，原因：时间这么晚了，赶紧洗洗睡了，明天的6点到23点再试")


        elif splited_content[0] =='我的运气值':
            q= random.randint(1, 100)
            if 1 <= q <= 10:
                await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0,
                     msg_id=message.id,
                     content=f"您的运气值是：%q,看来您的运气很不好，你记得出门注意点")
            elif 20 <= number <= 40:
                await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0,
                     msg_id=message.id,
                     content=f"您的运气值是：%q,看来你的运气有点差，记得做点开心的事情٩(๑^o^๑)۶")
            elif 50 <= number <= 60:
                await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0,
                     msg_id=message.id,
                     content=f"您的运气值是：%q,看来您的运气中等")
            elif 60 < number <= 90:
                await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0,
                     msg_id=message.id,
                     content=f"您的运气值是：%q,你的运气比较好，应该可以去刮个彩票了")
            elif 90 <= number < 100:
                await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0,
                     msg_id=message.id,
                     content=f"您的运气值是：%q,你的运气非比寻常了")
            elif number == 100:
                await message._api.post_group_message(
                     group_openid=message.group_openid,
                     msg_type=0,
                     msg_id=message.id,
                     content=f"您的运气值是：%q！居然是100，看来欧皇就是你了！！！！！！")
        elif splited_content[0] =='3':
                pass
        else:
            await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0, 
              msg_id=message.id,
              content=f"凯凯没教过我如何回应:{splited_content[0]}啊？")
            await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0, 
              msg_id=message.id,
              msg_seq= 2,
              content=f"你是不是输错了")

 



if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件 通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])