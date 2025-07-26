import random

from sqlalchemy import select, insert

from database.modules import Book
from database.engine import async_session

from misc import redis


async def search_book_by_genre(gen):
    async with async_session() as session:
        resp = await session.execute(select(Book).filter(Book.genre.contains(gen)))
        books = resp.scalars().all()

        if not books:
            return 'книг в таком жанре не нашлось'

        list_genre = redis.lrange(f'{gen.replace(' ', '_')}_books', 0, -1)
        if not list_genre:
            for book in books:
                redis.lpush(f'{gen.replace(' ', '_')}_books', book.book_id)
            list_genre = redis.lrange(f'{gen.replace(' ', '_')}_books', 0, -1)

        random_book = random.choice(list_genre)
        return await search_book_by_id(int(random_book))


async def search_book_by_id(book_id) -> str:
    async with async_session() as session:
        resp = await session.execute(select(Book).where(Book.book_id == book_id))
        book = resp.scalar()

        if book is None:
            return 'книги с таким id нет :('
        if book:
            book_mes = f' название: {book.title}\n'
            book_mes += f' автор: {book.author}\n'
            book_mes += f' id: {book.book_id}\n'
            book_mes += f' жанр: {book.genre}\n'
            book_mes += f' описание: {book.description}\n'

        return book_mes

