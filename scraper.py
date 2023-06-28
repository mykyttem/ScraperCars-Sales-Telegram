import requests
from bs4 import BeautifulSoup

url = "https://auto.ria.com/uk/search/?categories.main.id=1&brand.id[0]=79&model.id[0]=2104&indexName=auto&abroad.not=0&customnot=1&damage.not=0&country.import.id=840"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

#TODO: scraping for all pages paginations 

"""
Getting results for scraper
Add in list list cars
Call function in bot, and from list, dict, get data car
"""


def parse_cars() -> list:

    cars_list = []
    search_result = soup.find_all('div', id='searchResults')

    for cars in search_result:
        block_car = cars.find_all('section', class_='ticket-item')

        for info in block_car:
            car_dict = {}
            
            state_number_text = info.find_all('span', class_='state-num ua')           

            # under the <span> tag element
            for numbers in state_number_text:
                text_state_number = numbers.text.strip()
                list_numbers_state = text_state_number.split()[:3]
                state_number = ''.join(list_numbers_state)
                break


            car_dict['state_number'] = state_number
            
            # getting elements
            photo_link = info.find('img')['src']

            brand = info.find('a', class_='address').get_text(strip=True)
            urls_car = info.find('a', class_='m-link-ticket').get('href')
            price_usd = info.find('span', class_='bold size22 green').get_text(strip=True)
            race = info.find('li', class_='item-char js-race').get_text(strip=True)
            location = info.find('li', class_='item-char view-location js-location').get_text(strip=True)


            # parse page cars
            response_page_cars = requests.get(urls_car)
            soup_page_cars = BeautifulSoup(response_page_cars.text, "lxml")
            
            photos_block = soup_page_cars.find_all('div', id='photosBlock')
            for photos in photos_block:
                list_photo = photos.find_all('picture')
                album_photos = []

                for photo in list_photo:
                    album_photos.append(photo.find('img')['src'])

                car_dict['album_photos'] = album_photos 


            # save in dict
            car_dict['brand'] = brand
            car_dict['price'] = price_usd
            car_dict['race'] = race
            car_dict['location'] = location
            car_dict['url_auto_ria'] = urls_car

            cars_list.append(car_dict)


    return cars_list