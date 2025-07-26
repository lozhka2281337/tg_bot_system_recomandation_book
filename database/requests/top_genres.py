from misc import redis

from sqlalchemy import select

from database.engine import async_session
from database.modules import Favorite, Book


def create_format_top_genres(top_genres, in_redis):
    top_5_genres = 'топ 5 жанров:\n'

    for i, genre in enumerate(top_genres):
        if not in_redis:
            redis.lpush('top_5_genres', genre.encode('utf-8'))
        redis.expire('top_5_genres', 60*60*24)

        top_5_genres += f'{i + 1}) {genre}\n'
    return top_5_genres


def check_redis_top_genres():
    cache_redis = [genre.decode('utf-8') for genre in redis.lrange('top_5_genres', 0, -1)]
    if cache_redis:
        top_5_genres = create_format_top_genres(cache_redis, True)
        return top_5_genres


async def search_top_genres():
    async with async_session() as session:
        resp = await session.execute(select(Favorite))
        favs = resp.scalars().all()

        if not favs:
            mes = 'топ 5 жанров:\n'
            mes += '1) Роман\n'
            mes += '2) Проза\n'
            mes += '3) Рассказ\n'
            mes += '4) Бизнес\n'
            mes += '5) LitRPG\n'

            return mes

        cache_redis = check_redis_top_genres()
        if cache_redis:
            return cache_redis

        book_ids = [fav.book_id for fav in favs]
        genres = []

        for book_id in book_ids:
            resp = await session.execute(select(Book).where(Book.book_id == book_id))
            book = resp.scalar()
            genres.append(book.genre.replace(',', '').split('  '))

        genres = sum(genres, [])
        set_genres = set(genres)

        top_genres = sorted([[genres.count(genre), genre] for genre in set_genres])[::-1]
        top_genres = [genre for i, genre in top_genres[:5]]

        top_5_genres = create_format_top_genres(top_genres, False)
        return top_5_genres


