__all__ = ['router']

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
import app.callback_query as cbq

from database.requests.recommend import search_recommend, search_random_book
from database.requests.search_requests import search_book_by_genre, search_book_by_id
from database.requests.top_genres import search_top_genres
from database.requests.requests_favorite_book import (
    add_favorite_book,
    remove_favorite_book,
    print_favorites
)

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('пр\n'
                         'команды бота:\n'
                         '- /search_by_genre <жанр> – поиск книг по жанру\n'
                         '- /favorites – показать избранные книги пользователя\n'
                         '- /add_fav <id книги> – добавить книгу в избранное\n'
                         '- /remove_fav <id книги> – удалить книгу из избранного\n'
                         '- /top_genres – показать топ-5 популярных жанров\n'
                         '- /recommend – персонализированная рекомендация\n'
                         '- /search_by_id <id книги> – поиск книги по айди(с описанием)')


@router.message(F.text.startswith('/add_fav '))
async def add_favorite_book_handle(message: Message):
    try:
        book_id = int(message.text.split()[1])
        user_id = message.from_user.id

        mes = await add_favorite_book(str(user_id), book_id)
        await message.answer(mes)
    except Exception as e:
        print(f"error: {e}")
        await message.answer('неверный ввод')


@router.message(F.text.startswith('/remove_fav '))
async def remove_favorite(message: Message):
    book_id = message.text.split()[1]
    user_id = message.from_user.id

    mes = await remove_favorite_book(user_id, book_id)
    await message.answer(mes)


@router.message(Command('favorites'))
async def answer_favorites(message: Message):
    user_id = message.from_user.id
    mes = await print_favorites(user_id)
    if mes == 'в избранном пусто :(':
        await message.answer(mes)
    else:
        for i in mes:
            await message.answer(i)


@router.message(F.text.startswith('/search_by_genre '))
async def cmd_search_book_by_genre(message: Message):
    genre = message.text[len('/search_by_genre '):]
    cbq.SearchBookByGenre.genre = genre
    mes = await search_book_by_genre(genre)
    if mes != 'книг в таком жанре не нашлось':
        await message.answer(mes, reply_markup=kb.random_genre_book)
    else:
        await message.answer(mes)


@router.message(F.text.startswith('/search_by_id '))
async def cmd_search_book_by_id(message: Message):
    book = await search_book_by_id(message.text[len('/search_by_id'):])
    await message.answer(book)


@router.message(Command('top_genres'))
async def cmd_top_5_genres(message: Message):
    top = await search_top_genres()
    await message.answer(top)


@router.message(Command('recommend'))
async def cmd_recommend(message: Message):
    personal_books_id = await search_recommend(message.from_user.id)

    if not personal_books_id:
        mes = await search_random_book()
        await message.answer(mes)
    else:
        cbq.SearchPersonalBooks.books_id = personal_books_id
        cbq.SearchPersonalBooks.number_book = 0

        mes = await search_book_by_id(personal_books_id[0])
        await message.answer(mes, reply_markup=kb.recommend_book_forw)