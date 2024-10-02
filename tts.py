import pyttsx3
import ffmpeg
def test_to_speech(text: str, output_file: str = "super.wav"):
    engine = pyttsx3.init()
    engine.setProperty('lang', 'zh-CN')
    engine.save_to_file(text, output_file)
    engine.runAndWait()

if __name__ == "__main__":
    test = '欢迎使用pyttsx3，这是一个将文本转换为语音的库。'
    test_to_speech(test)
