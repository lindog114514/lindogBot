import pyttsx3
import random
import string
from graiax import silkcoder

message_14514 = '''
鸠:咏歌别玩了，我们来玩个小游戏吧
咏歌:什么小游戏？
鸠:我们进房间里面再玩

鸠:玩这个小游戏之前需要关上房间门


(空气僵持了一会后)

咏歌:到底是什么游戏呀？
(鸠把咏歌一把按在床上)
咏歌:唔…姐姐你要干嘛…
鸠:当然是和你玩小游戏啊(笑)
咏歌:唔…这个小游戏还需要被按在床上吗…
(鸠没说话，把灯关上然后就开始和咏歌玩“小游戏”)

鸠:妹妹…你的*好大啊…为什么
咏歌:唔…姐姐…你干嘛…
(鸠没回复)
鸠:唔…好软喵…
咏歌:唔…你为什么要摸…
鸠:因为这才是“小游戏”所需的步骤啊(笑)
咏歌:姐姐你…(睡着了)
鸠:我的妹妹…让我再摸一会儿你的*吧…
(几小时后)
“我的孩子啊！你怎么重伤啦！！”
医生:下体出血严重，我们也无法为你的孩子回天
“啊！！！你还我孩命啊！！！”

(完)'''



def generate_random_filename(extension=".silk", length=5):
    """生成随机文件名"""
    letters = string.ascii_letters + string.digits
    random_name = ''.join(random.choice(letters) for _ in range(length))
    return f"{random_name}{extension}"

def text_to_speech(text: str, output_file: str = "super.wav"):
    # 初始化引擎
    engine = pyttsx3.init()
    # 设置语言
    engine.setProperty('voice', 'zh-CN')  # 确保设置为可用的语音
    # 运行
    engine.save_to_file(text, output_file)
    engine.runAndWait()

    # 生成随机文件名并转换为 SILK 格式
    silk_filename = generate_random_filename()
    silkcoder.encode(output_file, silk_filename)
    print(f"转换完成：{silk_filename}")

if __name__ == "__main__":
    text = message_14514

    text_to_speech(text)
