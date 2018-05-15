import time

import speech_recognition as sr
import webbrowser as wb
import pyttsx3
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

r = sr.Recognizer()
r.energy_threshold = 4000
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


with sr.Microphone() as source:
    print('Say Something!')
    engine.say('Are you bored! Want to have a look at different shirts?')
    engine.runAndWait()
    audio = r.listen(source)
    print('Done!')

try:
    text = r.recognize_google(audio)
    print('You said:\n' + text)
    if('yes' in text ):
     wb.get(chrome_path).open('https://www.amazon.in/Mens-Shirts/b/ref=sd_allcat_sbc_mfashion_shirts?ie=UTF8&node=1968093031')
     engine.say('Here are your shirts! Happy shopping!')
     engine.runAndWait()

    elif ('no' in text):
        engine.say('So you want to look at a specific shirt to buy!')
        engine.runAndWait()
        with sr.Microphone() as source:
            audio = r.listen(source)


        try:
            text1 = r.recognize_google(audio)

            if ('yes' in text1):
                engine.say('Then please tell me what do you want to buy')
                engine.runAndWait()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    try:
                        text2 = r.recognize_google(audio)
                        text2.split(" ")
                        text3="https://www.amazon.in/s/field-keywords="+text2 +"+"+"men"
                        wb.get(chrome_path).open(text3)
                        engine.say('You asked for'+ text2)
                        engine.runAndWait()
                        engine.say('Here are your shirts! Happy shopping!')
                        engine.runAndWait()

                    except Exception as e:
                        print(e)


        except Exception as e:
            print(e)


except Exception as e:
    print(e)

