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


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """ 
        Call function
        and getting dict keys
        Save in DB 
    """

    # getting existing state number

    #TODO: album photos
    
    # call function
    list_cars = parse_cars()
    for car in list_cars:

        # send data
        state_number = car['state_number']

        await bot.send_photo(ID_CHANNEL, car['photo'],
            caption=f"""
                💵 {car['price']} $
                ⚙️ {car['speed']}
                📌 {car['location']}
            """
        )
 
 
        cur.execute("SELECT * FROM cars WHERE state_number = ?", (state_number,))
        car_db = cur.fetchone()

        if not car_db:
            
            # save state number
            cur.execute(f"INSERT INTO cars (state_number) values (?);", (state_number,))
            con.commit()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)