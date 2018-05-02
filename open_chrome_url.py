import speech_recognition as sr
import webbrowser as wb
import pyttsx3
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

r = sr.Recognizer()
r.energy_threshold = 4000
engine = pyttsx3.init()

with sr.Microphone() as source:
    print('Say Something!')
    engine.say('Hola! I would help you in redirecting you to the web page! Please give me the url')
    engine.runAndWait()
    audio = r.listen(source)
    print('Done!')

try:
    text = r.recognize_google(audio)
    print('You said:\n' + text)
    wb.get(chrome_path).open(text)
    print('Welcome to '+text)
    engine.say('Welcome to '+text)
    engine.runAndWait()

except Exception as e:
    print(e)
