import pyttsx3
from graiax import silkcoder

def text_to_speech(text: str, output_file: str = "super.wav"):
    # 初始化引擎
    engine = pyttsx3.init()


    # 设置语言
    engine.setProperty('lang', 'zh-CN')

    # 运行
    engine.save_to_file(text, output_file)
    engine.runAndWait()

if __name__ == "__main__":
    # 将文本转换为语音并保存为WAV文件
    text = "欢迎使用pyttsx3，这是一个将文本转换为语音的库。"
    text_to_speech(text)

    # 将WAV文件转换为silk格式
    # convert_wav_to_silk('output.wav', 'output.silk')
    silkcoder.encode("super.wav", "super.silk")