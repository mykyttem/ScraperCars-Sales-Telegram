import asyncio
import schedule

from bot import send_results_scraper, dp


""" After instant start of bot, scraping starts on timer """

async def loop_bot():
    while True:
        # Checks for scheduled tasks and runs any tasks that need to be executed according to the specified schedule
        schedule.run_pending()

        # 10 minutes
        await asyncio.sleep(600) 
        await send_results_scraper()


async def start_bot():
    await dp.start_polling()


if __name__ == '__main__':
    async def main():
        await asyncio.gather(start_bot(), loop_bot())

    asyncio.run(main())