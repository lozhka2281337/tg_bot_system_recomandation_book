import random

from database.engine import async_session
from database.modules import Favorite, Book

import database.requests.search_requests as oq

from sqlalchemy import select


async def search_personal_genre(session, favs):

    genres = []

    for fav in favs:
        resp = await session.execute(select(Book).where(Book.book_id == fav.book_id))
        book = resp.scalar()
        genres.append(book.genre.replace(',', '').split('  '))

    book_genres = sum(genres, [])
    set_genres = set(book_genres)

    top_personal_genres = sorted([[genres.count(genre), genre] for genre in set_genres])[::-1]
    top_personal_genres = [genre for i, genre in top_personal_genres[:3]]

    return top_personal_genres


async def search_random_book():
    async with async_session() as session:
        resp = await session.execute(select(Book))
        favs = resp.scalars().all()

        random_book = random.choice(favs)
        book = await oq.search_book_by_id(random_book.book_id)
        return book


async def search_personal_books(session, personal_genres, favs):
    con = [''.join(personal_genres), ''.join(personal_genres[:2]), ''.join(personal_genres[2:]), personal_genres[0] + personal_genres[2], personal_genres[0]]
    books = ''
    i = 0

    while not books:
        resp = await session.execute(select(Book).where(Book.genre.contains(con[i])))
        books = resp.scalars().all()
        i += 1

    personal_books = [book.book_id for book in books]
    favs = [fav.book_id for fav in favs]

    for book in personal_books:
        if book in favs:
            personal_books.remove(book)

    personal_books = personal_books[:10] if len(personal_books) > 10 else personal_books

    return personal_books


# главная функция
async def search_recommend(user_id):
    async with async_session() as session:
        resp = await session.execute(select(Favorite).where(Favorite.user_id == user_id))
        favs = resp.scalars().all()

        if len(favs) == 0:
            return False

        top_personal_genres = await search_personal_genre(session, favs)
        personal_books = await search_personal_books(session, top_personal_genres, favs)

        return personal_books



