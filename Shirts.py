from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
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
def size_functions(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    doc = html.fromstring(page.content)

    XPATH_SIZE = '//span[@class="a-dropdown-container"]//select[@class="a-native-dropdown"]//text()'
    RAW_SIZE = doc.xpath(XPATH_SIZE)

    SIZE = ' '.join(''.join(RAW_SIZE).split()) if RAW_SIZE else ''
    engine.say('The available sizes are')
    engine.say(SIZE)


with sr.Microphone() as source:
    print('Say Something!')
    engine.say('Are you bored! Want to have a look at different shirts?')
    engine.runAndWait()
    audio = r.listen(source)
    print('Done!')
try:

    text = 'no'#r.recognize_google(audio)
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
            text1 = 'yes'#r.recognize_google(audio)

            if ('yes' in text1):
                engine.say('Then please tell me what do you want to buy and also specify the price criteria if needed')
                engine.runAndWait()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    try:
                        text2 = 'white shirt'#r.recognize_google(audio)
                        text2.split(" ")
                        text3="https://www.amazon.in/s/field-keywords="+text2 +" "+ "men"
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
                                    XPATH_AGGREGATE_RATING = '//div[@class="a-row a-spacing-small"]//text()'
                                    XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
                                    XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
                                    XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
                                    #XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
                                    XPATH_COLOR='//div[@class="a-row"]//span[@class="selection"]//text()'
                                    XPATH_NUM_OF_CUSTOMES='//div[@class="a-row"]//span[@class="a-size-medium totalReviewCount"]//text()'

                                    RAW_NAME = doc.xpath(XPATH_NAME)
                                    RAW_COLOR=doc.xpath(XPATH_COLOR)
                                    total_ratings = doc.xpath(XPATH_AGGREGATE_RATING)
                                    RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
                                    RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
                                    RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
                                    RAW_NUM_OF_CUSTOMERS=doc.xpath(XPATH_NUM_OF_CUSTOMES)
                                    #RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

                                    NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else ''
                                    COLOR = ' '.join(''.join(RAW_COLOR).split()) if RAW_COLOR else None
                                    SALE_PRICE = ' '.join(
                                        ''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
                                    CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
                                    ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
                                    #AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
                                    NUM_OF_CUSTOMES = ''.join(RAW_NUM_OF_CUSTOMERS).strip(' ') if RAW_NUM_OF_CUSTOMERS else '1'
                                    TOTAL_RATINGS = ''.join(total_ratings).replace('s','0').replace(' ','.').strip(' ') if total_ratings else None
                                    TOTAL=0.0
                                    ASIN=url[24:34]
                                    rat=[]
                                    RATINGS_NEEDED=''
                                    dictionary_needed={}
                                    a={}
                                    TOTAL_1=0
                                    if TOTAL_RATINGS!=None:
                                        RATINGS_NEEDED=TOTAL_RATINGS[0:3]
                                        TOTAL =str(int( float(RATINGS_NEEDED) * int(NUM_OF_CUSTOMES)))+''
                                        TOTAL_1=int(TOTAL)
                                        rat.append(TOTAL)

                                    else:
                                        print("SORRY")


                                    #links is the list for all the ASIN numbers
                                    #rat is the list of all the total ratings after the multiplication


                                    if not ORIGINAL_PRICE:
                                        ORIGINAL_PRICE = SALE_PRICE

                                    data = {
                                        'NAME': NAME,
                                        'COLOR' : COLOR,
                                        'TOTAL' : TOTAL_1,
                                        #'RATINGS': RATINGS_NEEDED,
                                        'SALE_PRICE': SALE_PRICE,
                                        'CATEGORY': CATEGORY,
                                        'ORIGINAL_PRICE': ORIGINAL_PRICE,
                                        'CUSTOMERS' : NUM_OF_CUSTOMES,
                                        'ASIN' :ASIN,
                                        #'AVAILABILITY': AVAILABILITY,
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
                                #sleep(3)
                                extracted_data.append(AmzonParser(url))

                                f = open('data.json', 'w')
                                json.dump(extracted_data, f, indent=4)


                        if __name__ == "__main__":

                            ReadAsin()



                        input_file = open('data.json', 'r')
                        json_decode = json.load(input_file)
                        for item in json_decode:
                            my_dict = {}
                            my_dict['NAME'] = item.get('NAME')
                            my_dict['CUSTOMERS'] = item.get('CUSTOMERS')
                            my_dict['TOTAL'] = item.get('TOTAL')
                            my_dict['ASIN'] = item.get('ASIN')
                            my_dict['RATINGS']=item.get('RATINGS')
                            my_dict['ORIGINAL PRICE'] = item.get('ORIGINAL_PRICE')
                            my_dict['SALE_PRICE'] = item.get('SALE_PRICE')
                            my_dict['URL']=item.get('URL')
                            my_dict['COLOR'] = item.get('COLOR')
                            print(my_dict)

                        all_names = [i['NAME'] for i in json_decode]
                        print(all_names)

                        all_colors = [i['COLOR'] for i in json_decode]
                        print(all_colors)

                        all_urls = [i['URL'] for i in json_decode]
                        print(all_urls)


                        all_sales = [i['SALE_PRICE'] for i in json_decode]
                        print(all_sales)

                        all_orig = [i['ORIGINAL_PRICE'] for i in json_decode]
                        print(all_orig)

                        all_asins = [i['ASIN'] for i in json_decode]
                        print(all_asins)

                        all_ratings =[i['TOTAL'] for i in json_decode]
                        print(all_ratings)
                        b=all_ratings.index(max(all_ratings))
                        print(b+1)
                        print(all_asins[b])

                        with sr.Microphone() as source:

                            engine.say('So, Do you want me to selct one shirt for you?')
                            engine.runAndWait()
                            audio = r.listen(source)
                            print('Done!')
                        try:
                            text = 'no'#r.recognize_google(audio)
                            print('You said:\n' + text)
                            if ('yes' in text):
                                wb.get(chrome_path).open(all_urls[b])
                                engine.say('We have selected you a shirt named')
                                engine.say(all_names[b])
                                engine.say('with original price')
                                engine.say(all_orig[b ])
                                engine.say('and sale price')
                                engine.say(all_sales[b])
                                engine.say('of color')
                                engine.say(all_colors[b])
                                engine.runAndWait()
                                chrome_options = webdriver.ChromeOptions()
                                driver = webdriver.Chrome(executable_path="C:/chromedriver_win32/chromedriver.exe",
                                                          chrome_options=chrome_options)
                                driver.get(all_urls[b])

                                # Create new object for drop down
                                select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
                                size_functions(all_urls[b])

                                with sr.Microphone() as source:
                                    engine.say('Just tell me what is the size or your shirt to add to your cart')
                                    engine.runAndWait()
                                    audio = r.listen(source)
                                    print('Done!')
                                try:
                                    text ='Small'#r.recognize_google(audio)
                                    print('You said:\n' + text)
                                    # Select "Small" size
                                    select.select_by_visible_text(text)
                                    wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//input[@id="add-to-cart-button" and not(@style="cursor: not-allowed;")]'))).click()
                                except Exception as e:
                                    print(e)

                            elif ('no' in text):
                                engine.say('So, you want to modify the search and select your own shirts,')
                                engine.runAndWait()

                                with sr.Microphone() as source:
                                    engine.say('Tell me the brand name')
                                    engine.runAndWait()
                                    audio = r.listen(source)
                                    print('Done!')
                                try:
                                    brand_name = 'Lee Cooper '#r.recognize_google(audio)
                                    brand_name_1=brand_name.lower()
                                    print('You said:\n' + brand_name)

                                    print(brand_name_1)
                                    text4 = "https://www.amazon.in/s/field-keywords=" + brand_name_1 + " " +text2+ " for men"
                                    wb.get(chrome_path).open(text4)
                                    engine.say('Here are your shirts! Happy shopping!')
                                    engine.runAndWait()
                                    url_1 = text4
                                    htmlfile_1 = urllib.request.urlopen(url_1)
                                    htmltext_1 = htmlfile_1.read()
                                    links = []
                                    a = []
                                    soup = bs.BeautifulSoup(htmltext_1, 'lxml')
                                    all_tables = soup.find_all('li', {'class': 'a-link-normal a-text-normal'})
                                    for link in soup.find_all('li'):
                                        if link.get('data-asin') != None:
                                            links.append(link.get('data-asin'))

                                    print(set(links))
                                    links = (set(links))
                                    extracted_data = []
                                    for i in links:
                                        url = "http://www.amazon.in/dp/" + i
                                        print("Processing: " + url)
                                        sleep(3)
                                        extracted_data.append(AmzonParser(url))

                                        f = open('data.json', 'w')
                                        json.dump(extracted_data, f, indent=4)

                                    input_file = open('data.json', 'r')
                                    json_decode = json.load(input_file)
                                    for item in json_decode:
                                        my_dict = {}
                                        my_dict['NAME'] = item.get('NAME').lower()
                                        my_dict['CUSTOMERS'] = item.get('CUSTOMERS')
                                        my_dict['TOTAL'] = item.get('TOTAL')
                                        my_dict['ASIN'] = item.get('ASIN')
                                        my_dict['RATINGS'] = item.get('RATINGS')
                                        my_dict['ORIGINAL PRICE'] = item.get('ORIGINAL_PRICE')
                                        my_dict['SALE_PRICE'] = item.get('SALE_PRICE')
                                        my_dict['URL'] = item.get('URL')
                                        my_dict['COLOR'] = item.get('COLOR')
                                        print(my_dict)

                                    all_names = [i['NAME'].lower() for i in json_decode]
                                    print(all_names)


                                    all_colors = [i['COLOR'] for i in json_decode]
                                    #print(all_colors)

                                    all_urls = [i['URL'] for i in json_decode]
                                    #print(all_urls)

                                    all_sales = [i['SALE_PRICE'] for i in json_decode]
                                    #print(all_sales)

                                    all_orig = [i['ORIGINAL_PRICE'] for i in json_decode]
                                    #print(all_orig)

                                    all_asins = [i['ASIN'] for i in json_decode]
                                    #print(all_asins)

                                    all_ratings = [i['TOTAL'] for i in json_decode]
                                    #print(all_ratings)

                                    new_names = []
                                    new_colors = []
                                    new_urls = []
                                    new_sales = []
                                    new_orig = []
                                    new_asins = []
                                    new_ratings = []
                                    j = []
                                    for i in all_names:
                                        if ((('t-shirt' or 'shirt') in i) and ((brand_name_1) in i)):
                                            j = all_names.index(i)
                                            new_names.append(i)
                                            new_colors.append(all_colors[j])
                                            new_urls.append(all_urls[j])
                                            new_sales.append((all_sales[j][:-3].replace(',','')))
                                            new_orig.append(all_orig[j])
                                            new_asins.append(all_asins[j])
                                            new_ratings.append(all_ratings[j])

                                    print(new_names)
                                    print(new_colors)
                                    print(new_urls)
                                    print(new_sales)
                                    print(new_orig)
                                    print(new_asins)
                                    print(new_ratings)
                                    engine.say('Do you want to specify a price range....I mean your budget price')
                                    engine.runAndWait()
                                    with sr.Microphone() as source:
                                        audio = r.listen(source)
                                        print('Done!')
                                    try:
                                        decision_for_price='yes'#r.recognize_google(audio)
                                        if(decision_for_price=='no'):
                                            arr = np.array(new_ratings)
                                            arr=arr.argsort()[-2:][::-1]
                                            print(arr)

                                            engine.say('We have selected 2 shirts out for you! Pick one!!')
                                            engine.runAndWait()

                                            for i in arr:
                                                engine.say(i)
                                                engine.runAndWait()
                                                engine.say('The shirt is')
                                                engine.say(new_names[i])
                                                engine.say('of  price')
                                                engine.say(new_sales[i])
                                                engine.say('of color')
                                                engine.say(new_colors[i])
                                                engine.runAndWait()
                                                a=arr[0]
                                                #b=arr[1]


                                            engine.say('So, what do you want')
                                            engine.runAndWait()

                                            with sr.Microphone() as source:
                                                audio = r.listen(source)
                                                print('Done!')
                                            try:

                                                choosing = 'first'#r.recognize_google(audio)
                                                if ('first' in choosing):
                                                    engine.say('So you have selcted the first one')
                                                    engine.say('The shirt is')
                                                    engine.say(new_names[arr[0]])
                                                    engine.say('of  price')
                                                    engine.say(new_sales[arr[0]])
                                                    engine.say('of color')
                                                    engine.say(new_colors[arr[0]])
                                                    engine.runAndWait()

                                                    chrome_options = webdriver.ChromeOptions()
                                                    driver = webdriver.Chrome(executable_path="C:/chromedriver_win32/chromedriver.exe", chrome_options=chrome_options)
                                                    driver.get(new_urls[a])
                                                    select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
                                                    size_functions(new_urls[a])
                                                '''elif ('second' in choosing):
                                                    engine.say('So you have selcted the second one')
                                                    engine.say('The shirt is')
                                                    engine.say(new_names[arr[1]])
                                                    engine.say('of  price')
                                                    engine.say(new_sales[arr[1]])
                                                    engine.say('of color')
                                                    engine.say(new_colors[arr[1]])
                                                    engine.runAndWait()

                                                    chrome_options = webdriver.ChromeOptions()
                                                    driver = webdriver.Chrome(executable_path="C:/chromedriver_win32/chromedriver.exe", chrome_options=chrome_options)
                                                    driver.get(new_urls[b])
                                                    select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
                                                    size_functions(new_urls[b])'''
                                                with sr.Microphone() as source:
                                                    engine.say('Just tell me what is the size or your shirt to add to your cart')
                                                    engine.runAndWait()
                                                    audio = r.listen(source)
                                                    print('Done!')
                                                try:
                                                    text_10 = 'Small'  # r.recognize_google(audio)
                                                    # text_10=text_10.title()

                                                    print('You said:\n' + text_10)
                                                    # Select "Small" size

                                                    # Create new object for drop down
                                                    select.select_by_visible_text(text_10)


                                                    wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//input[@id="add-to-cart-button" and not(@style="cursor: not-allowed;")]'))).click()

                                                except Exception as e:
                                                    print(e)
                                            except Exception as e:
                                                print(e)

                                        elif(decision_for_price=='yes'):
                                            engine.say('These are the price ranges avalaibale')
                                            engine.say(min(new_sales))
                                            engine.say('to')
                                            engine.say(max(new_sales))
                                            c=''

                                            with sr.Microphone() as source:
                                                engine.say('Please specify your budget')
                                                engine.runAndWait()
                                                audio = r.listen(source)
                                                print('Done!')
                                            try:
                                                text_11 = '999'
                                                c = int(text_11)  # r.recognize_google(audio)
                                                print(int(text_11))
                                                b = []
                                                for i in new_sales:
                                                    a = int(i)
                                                    d = abs(c - a)
                                                    print(d)
                                                    b += [d]

                                                print(b)

                                                arr_1 = np.array(b)
                                                arr_1 = arr_1.argsort()[:2]
                                                print(arr_1)

                                                for i in arr_1:
                                                    new_sales[i]
                                                    a = new_names[i]
                                                    print(a)
                                                engine.say('We have selected 2 shirts out for you! Pick one!!')
                                                engine.runAndWait()

                                                for i in arr_1:
                                                    engine.say(i)
                                                    engine.runAndWait()
                                                    engine.say('The shirt is')
                                                    engine.say(new_names[i])
                                                    engine.say('of  price')
                                                    engine.say(new_sales[i])
                                                    engine.say('of color')
                                                    engine.say(new_colors[i])
                                                    engine.runAndWait()
                                                    a = arr_1[0]
                                                    #b = arr_1[1]

                                                engine.say('So, what do you want')
                                                engine.runAndWait()

                                                with sr.Microphone() as source:
                                                    audio = r.listen(source)
                                                    print('Done!')
                                                try:

                                                    choosing = 'first'  # r.recognize_google(audio)
                                                    if ('first' in choosing):
                                                        engine.say('So you have selcted the first one')
                                                        engine.say('The shirt is')
                                                        engine.say(new_names[arr_1[0]])
                                                        engine.say('of  price')
                                                        engine.say(new_sales[arr_1[0]])
                                                        engine.say('of color')
                                                        engine.say(new_colors[arr_1[0]])
                                                        engine.runAndWait()

                                                        chrome_options = webdriver.ChromeOptions()
                                                        driver = webdriver.Chrome(
                                                            executable_path="C:/chromedriver_win32/chromedriver.exe",
                                                            chrome_options=chrome_options)
                                                        driver.get(new_urls[a])
                                                        select = Select(driver.find_element_by_id(
                                                            "native_dropdown_selected_size_name"))
                                                        size_functions(new_urls[a])
                                                    '''elif ('second' in choosing):
                                                        engine.say('So you have selcted the second one')
                                                        engine.say('The shirt is')
                                                        engine.say(new_names[arr_1[1]])
                                                        engine.say('of  price')
                                                        engine.say(new_sales[arr_1[1]])
                                                        engine.say('of color')
                                                        engine.say(new_colors[arr_1[1]])
                                                        engine.runAndWait()

                                                        chrome_options = webdriver.ChromeOptions()
                                                        driver = webdriver.Chrome(
                                                            executable_path="C:/chromedriver_win32/chromedriver.exe",
                                                            chrome_options=chrome_options)
                                                        driver.get(new_urls[b])
                                                        select = Select(driver.find_element_by_id(
                                                            "native_dropdown_selected_size_name"))
                                                        size_functions(new_urls[b])'''
                                                    with sr.Microphone() as source:
                                                        engine.say(
                                                            'Just tell me what is the size or your shirt to add to your cart')
                                                        engine.runAndWait()
                                                        audio = r.listen(source)
                                                        print('Done!')
                                                    try:
                                                        text_10 = 'Small'  # r.recognize_google(audio)
                                                        # text_10=text_10.title()

                                                        print('You said:\n' + text_10)
                                                        # Select "Small" size

                                                        # Create new object for drop down
                                                        select.select_by_visible_text(text_10)

                                                        wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//input[@id="add-to-cart-button" and not(@style="cursor: not-allowed;")]'))).click()

                                                    except Exception as e:
                                                        print(e)
                                                except Exception as e:
                                                    print(e)

                                            except Exception as e :
                                                print(e)

                                    except Exception as e:
                                        print(e)


                                except Exception as e:
                                    print(e)
                        except Exception as e:
                            print(e)


                    except Exception as e:
                        print(e)


        except Exception as e:
            print(e)


except Exception as e:
    print(e)


