import requests
from bs4 import BeautifulSoup


"""
Getting results for scraper
Add in list list cars
Call function in bot, and from list, dict, get data car
"""


def parse_cars() -> list:

    cars_list = []
    url = "https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=-1&country.import.id=840&price.currency=1&abroad.not=0&custom.not=1&damage.not=0&page=1&size=10"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    search_result = soup.find_all('div', id='searchResults')


    # parse cars
    for cars in search_result:
        block_car = cars.find_all('section', class_='ticket-item')

        for info in block_car:
            car_dict = {}

            # under the <span> tag element
            state_number_text = info.select('span.state-num.ua')
            state_number = ''
            if state_number_text:
                text_state_number = state_number_text[0].get_text(strip=True)
                state_number = ''.join(text_state_number.split()[:3])

            car_dict['state_number'] = state_number

            # getting elements
            brand = info.select_one('a.address').get_text(strip=True)
            urls_car = info.select_one('a.m-link-ticket')['href']
            price_usd = info.select_one('span.bold.size22.green').get_text(strip=True)
            race = info.select_one('li.item-char.js-race').get_text(strip=True)
            location = info.select_one('li.item-char.view-location.js-location').get_text(strip=True)

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