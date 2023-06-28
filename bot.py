import json
import logging
from aiogram import executor
from aiogram import types 
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

""" 
    Connect and add bot for channel
    Send result scraping in channel
"""

from config import API_TOKEN, ID_CHANNEL, TIMER, cur, con    
from scraper import parse_cars

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())       
logging.basicConfig(level=logging.INFO)

#FIXME if not state number

list_parse_cars = []    

@dp.message_handler(commands=['lauch'])
async def start(message: types.Message):
    """ 
        Call function, getting dict keys
        Save in DB car, if not 
    """

    # call function
    list_cars = parse_cars()

    for car in list_cars:
        info_car = []

        # getting info for car, from dict
        album_photos = car['album_photos']
        state_number = car['state_number']

        brand = car['brand']
        price = car['price']
        url_auto_ria = car['url_auto_ria']
        race = car['race']
        location = car['location']

        # get from db cars
        cur.execute("SELECT price FROM cars WHERE state_number = ?", (state_number,))
        car_db = cur.fetchone()
        

        if car_db:    
            car_price_db = car_db[0] 
            price_db = car_price_db.strip("('").replace("',)", "") 

            # Aiogram can accept a maximum of 10 photos
            photo_counter = 0  
            max_photos = 5

            for photo in album_photos:
                if photo_counter >= max_photos:
                    break

                info_car.append(types.InputMediaPhoto(media=photo, caption=f"{brand}\n {url_auto_ria}\n 💵 Ціна: {price}\n ⚙️ {race} 📌 {location}"))
                photo_counter += 1

            #TODO: immediately see the description, and not after clicking
            await bot.send_media_group(ID_CHANNEL, media=info_car)

            # generate unique value, state number and make of the car and add in list
            list_parse_cars.append(state_number + brand)


        # save info for car in DB
        if not car_db:
            
            # save only 10 photos
            json_list_album = json.dumps(album_photos)

            # save state number
            cur.execute(
                f"""INSERT INTO cars (state_number, photo, price, brand, url_auto_ria, race, location) values (?, ?, ?, ?, ?, ?, ?); """,
                (state_number, json_list_album, price, brand, url_auto_ria, race, location)
            )
            con.commit()


            photo_counter = 0  
            max_photos = 5
            for photo in album_photos:
                if photo_counter >= max_photos:
                    break

                info_car.append(types.InputMediaPhoto(media=photo, caption=f"{brand}\n {url_auto_ria}\n 💵 Ціна: {price}\n ⚙️ {race} 📌 {location}"))
                photo_counter += 1

            #TODO: immediately see the description, and not after clicking
            await bot.send_media_group(ID_CHANNEL, media=info_car)
                
    # get all cars from DB
    cur.execute("SELECT state_number, photo, brand, price, race, location, url_auto_ria FROM cars")
    cars_db = cur.fetchall()

    not_found_cars = []

    if cars_db:
        for car_db in cars_db:

            # value 
            db_state_number = car_db[0]
            db_photo = car_db[1]
            db_brand = car_db[2]
            db_price = car_db[3]
            db_race = car_db[4]
            db_location = car_db[5]
            db_url_auto_ria = car_db[6]

            # generate unique value, state number and make of the car
            stateNum_and_brand = str(db_state_number) + str(db_brand)

            if stateNum_and_brand not in list_parse_cars:
                not_found_cars.append(car_db)


        if not_found_cars:

            for car_db in not_found_cars:
                db_brand = car_db[2]
                db_url_auto_ria = car_db[6]

                await bot.send_photo(ID_CHANNEL, db_photo, caption=f"Автомобіль зняли з продажу {db_brand}\n {db_url_auto_ria}\n 💵 {db_price}\n ⚙️ {db_race}\n 📌 {db_location}")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)