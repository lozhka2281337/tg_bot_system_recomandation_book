from sqlalchemy import select

from database.engine import async_session
from database.modules import User
from misc import redis


async def reg_user(tg_id, username) -> None | str:
    async with async_session() as session:
        red_resp = redis.hget("users_tg", str(tg_id))

        if not red_resp:
            resp = await session.execute(select(User).where(User.user_id == tg_id))
            user = resp.scalar()
            redis.hset("users_tg", str(tg_id), str(username))
            if not user:
                session.add(User(user_id=tg_id, username=username))
                await session.commit()
                return 'теперь вы зарегистрированы'
        await session.commit()
