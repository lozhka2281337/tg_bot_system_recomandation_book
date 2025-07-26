from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from decouple import config

from database.modules import Base

engine = create_async_engine('sqlite+aiosqlite:///books.sqlite3')#config("DB_LITE"))# , echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
