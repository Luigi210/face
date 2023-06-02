import speech_recognition as sr
import pyttsx3
# from appKi

# Создаем объекты распознавания и синтеза речи
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Функция для распознавания голоса
def recognize_speech():
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="en-EN")
        return text
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print("Ошибка сервиса распознавания речи; {0}".format(e))

# Функция для синтеза речи
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Пример использования
text = recognize_speech()
print("Распознанный текст:", text)
speak_text(text)
