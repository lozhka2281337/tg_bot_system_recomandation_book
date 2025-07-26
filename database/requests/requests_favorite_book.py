from database.modules import Book, Favorite
from database.engine import async_session

from sqlalchemy import select


async def add_favorite_book(tg_id, book_id) -> str:
    async with async_session() as session:
        resp = await session.execute(select(Book).where(Book.book_id == book_id))
        book = resp.scalar()

        if not book:
            await session.commit()
            return 'книга с таким id отсутствует :('

        resp = await session.execute(
            select(Favorite).where(
            Favorite.book_id == book_id and Favorite.user_id == tg_id))
        favorite_book = resp.scalar()

        if favorite_book:
            await session.commit()
            return "эта книга уже добавлена в избранное"

        book = Favorite(book_id=book_id, user_id=tg_id)
        session.add(book)
        await session.commit()
        return "книга успешно добавлена"


async def remove_favorite_book(tg_id, book_id) -> str:
    async with async_session() as session:
        resp = await session.execute(
            select(Favorite).where(
                Favorite.book_id == book_id and Favorite.user_id == tg_id))
        favorite_book = resp.scalar()

        if favorite_book:
            await session.delete(favorite_book)
            await session.commit()
            return 'книга удалена из избранного'

        await session.commit()
        return 'книга не найдена'


async def print_favorites(tg_id) -> list | str:
    async with async_session() as session:
        resp = await session.execute(select(
            Favorite).where(
            Favorite.user_id == tg_id
        ))
        favorites = resp.scalars().all()
        print(favorites)
        if len(favorites) == 0:
            await session.commit()
            return 'в избранном пусто :('

        mes = []
        for i, favorite in enumerate(favorites):

            resp_book = await session.scalar(select(
                Book).where(Book.book_id == favorite.book_id))

            book_mes = f'{i+1}) '
            book_mes += f'название: {resp_book.title}\n'
            book_mes += f'   автор: {resp_book.author}\n'
            book_mes += f'   id: {resp_book.book_id}\n'
            book_mes += f'   жанр: {resp_book.genre}\n'
            # book_mes += f'   описание: {resp_book.description}\n'

            mes.append(book_mes)

        await session.commit()
        return mes

