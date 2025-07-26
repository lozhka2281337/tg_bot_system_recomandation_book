__all__ = ["router"]

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from database.requests.search_requests import search_book_by_genre
from database.requests.search_requests import search_book_by_id
import app.keyboards as kb

router = Router()


class SearchBookByGenre():
    genre = ''


class SearchPersonalBooks:
    books_id = []
    number_book = -1


@router.callback_query(F.data == 'next_book_by_genre')
async def callback_next_random_book_by_genre(callback: CallbackQuery):
    mes = await search_book_by_genre(SearchBookByGenre.genre)
    await callback.message.edit_text(text=mes, reply_markup=kb.random_genre_book)


async def get_one_personal_book(boo):
    SearchPersonalBooks.number_book = SearchPersonalBooks.number_book + 1 if boo else SearchPersonalBooks.number_book - 1
    book_id = SearchPersonalBooks.books_id[SearchPersonalBooks.number_book]

    mes = await search_book_by_id(book_id)
    return mes


@router.callback_query(F.data == 'next_recommend_book')
async def callback_next_recommend_book(callback: CallbackQuery):
    if SearchPersonalBooks.books_id != -1:
        mes = await get_one_personal_book(True)
        if SearchPersonalBooks.number_book < len(SearchPersonalBooks.books_id)-1:
            await callback.message.edit_text(text=mes, reply_markup=kb.recommend_book_forw_and_back)
        else:
            await callback.message.edit_text(text=mes, reply_markup=kb.recommend_book_back)


@router.callback_query(F.data == 'previous_recommend_book')
async def callback_previous_recommend_book(callback: CallbackQuery):
    if SearchPersonalBooks.books_id != -1:
        mes = await get_one_personal_book(False)
        if SearchPersonalBooks.number_book != 0:
            await callback.message.edit_text(text=mes, reply_markup=kb.recommend_book_forw_and_back)
        else:
            await callback.message.edit_text(text=mes, reply_markup=kb.recommend_book_forw)


