import json
from lxml import html
import requests
from time import sleep
from random import randint
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    try:

        for i in range(20):

            sleep(randint(1, 3))

            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200:
                doc = html.fromstring(response.content)
                XPATH_NAME = '//h1[@id="title"]//text()'
                XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
                XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
                XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
                XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

                RAW_NAME = doc.xpath(XPATH_NAME)
                RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
                RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
                RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
                RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

                NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
                CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
                ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
                AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

                if not ORIGINAL_PRICE:
                    ORIGINAL_PRICE = SALE_PRICE
                # retrying in case of captcha
                if not NAME:
                    raise ValueError('captcha')

                data = {
                    'NAME': NAME,
                    'SALE_PRICE': SALE_PRICE,
                    'CATEGORY': CATEGORY,
                    'ORIGINAL_PRICE': ORIGINAL_PRICE,
                    'AVAILABILITY': AVAILABILITY,
                    'URL': url,
                }
                return data

            elif response.status_code == 404:
                break

    except Exception as e:
        print (e)
def ReadAsin():
  #Change the list below with the ASINs you want to track.
    AsinList = ['B075LP14CZ']
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.in/dp/"+i
        extracted_data.append(parse(url))
        sleep(5)
    #Save the collected data into a json file.
    f=open('data.json','w')
    json.dump(extracted_data,f,indent=4)

if __name__ == "__main__":
    ReadAsin()