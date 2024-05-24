import asyncio
from dotenv import load_dotenv
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from handlers import router
from database.models import async_main
from middleware.throttling_mdlw import ThrottlingMiddleware

async def main():
    await async_main()
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    bot = Bot(os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # storage = RedisStorage.from_url('redis://localhost:6379/0')
    # dp.message.middleware.register(ThrottlingMiddleware(storage=storage))
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")