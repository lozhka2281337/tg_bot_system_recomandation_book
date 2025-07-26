from aiogram import BaseMiddleware

from database.engine import async_session

from database.requests.registration import reg_user
import database.requests.requests_favorite_book as rq


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
       await reg_user(event.from_user.id, event.from_user.username)
       return await handler(event, data)
