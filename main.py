import logging
import asyncio

from decouple import config
from aiogram import Bot, Dispatcher

from app.handlers import router as router_handlers
from app.callback_query import router as router_callback

from database.engine import create_tables
from app.middleware import RegistrationMiddleware

bot = Bot(token=config("TOKEN"))

dp = Dispatcher()

dp.message.outer_middleware(RegistrationMiddleware())


async def main():
    dp.include_routers(
        router_handlers,
        router_callback
    )

    await create_tables()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')