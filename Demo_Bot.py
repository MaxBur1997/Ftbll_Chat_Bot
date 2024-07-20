import logging
import asyncio
from aiogram import Bot, Dispatcher
import config
from handlers import career_choice


async def main():
    API_TOKEN = config.token

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.include_router(career_choice.router)


    await dp.start_polling(bot)


asyncio.run(main())