import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import clubs_choice


async def main():
    API_TOKEN = os.getenv("BOT_TOKEN")

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.include_router(clubs_choice.router)

    await dp.start_polling(bot)


asyncio.run(main())