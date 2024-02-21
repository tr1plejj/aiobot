from aiogram import Bot, Dispatcher
import asyncio
from handlers import handlers_router
from os import getenv
import logging
import sys

TOKEN = getenv('TOKEN')


async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
