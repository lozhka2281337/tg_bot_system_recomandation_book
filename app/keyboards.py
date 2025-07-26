from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# кнопка для поиска по жанру
random_genre_book = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='слудующая книга', callback_data='next_book_by_genre')]])

# кнопки для книг по рекомендации
recommend_book_forw = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='слудующая книга', callback_data='next_recommend_book')]])

recommend_book_back = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='предыдущая книга', callback_data='previous_recommend_book')]])

recommend_book_forw_and_back = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='предыдущая книга', callback_data='previous_recommend_book'),
                     InlineKeyboardButton(text='слудующая книга', callback_data='next_recommend_book')]])