import pyttsx3
import random
import string
from graiax import silkcoder


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

