from lxml import html
import csv,os,json
import requests
from time import sleep
import urllib.request
import bs4 as bs
import speech_recognition as sr
import webbrowser as wb
import pyttsx3
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
python_path = 'C:/Users/DELL/AppData/Local/Programs/Python/Python36-32/python.exe %s'
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
                        url = text3
                        htmlfile = urllib.request.urlopen(url)
                        htmltext = htmlfile.read()
                        links = []
                        a = []
                        soup = bs.BeautifulSoup(htmltext, 'lxml')
                        all_tables = soup.find_all('li', {'class': 'a-link-normal a-text-normal'})
                        for link in soup.find_all('li'):
                            if link.get('data-asin')!=None:
                                links.append(link.get('data-asin'))
                        print(set(links))
                        links = (set(links))


                        def AmzonParser(url):
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
                            page = requests.get(url, headers=headers)
                            while True:
                                sleep(3)
                                try:
                                    doc = html.fromstring(page.content)
                                    XPATH_NAME = '//h1[@id="title"]//text()'
                                    XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
                                    XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
                                    XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
                                    XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
                                    RAW_NAME = doc.xpath(XPATH_NAME)
                                    RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
                                    RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
                                    RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
                                    RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
                                    NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                                    SALE_PRICE = ' '.join(
                                        ''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
                                    CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
                                    ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
                                    AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
                                    if not ORIGINAL_PRICE:
                                        ORIGINAL_PRICE = SALE_PRICE

                                    data = {
                                        'NAME': NAME,
                                        'SALE_PRICE': SALE_PRICE,
                                        'CATEGORY': CATEGORY,
                                        'ORIGINAL_PRICE': ORIGINAL_PRICE,
                                        'AVAILABILITY': AVAILABILITY,
                                        'URL': url,
                                    }
                                    return data
                                except Exception as e:
                                    print(e)


                        def ReadAsin():

                            extracted_data = []


                            for i in links:
                                url = "http://www.amazon.in/dp/" + i
                                print("Processing: " + url)
                                extracted_data.append(AmzonParser(url))
                                sleep(5)
                                f = open('data.json', 'w')
                                json.dump(extracted_data, f, indent=4)


                        if __name__ == "__main__":
                            ReadAsin()








                    except Exception as e:
                        print(e)


        except Exception as e:
            print(e)


except Exception as e:
    print(e)


