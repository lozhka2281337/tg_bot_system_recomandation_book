from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import (
    String,
    Text,
    BigInteger,
    Integer,
    DateTime,
    func
)


# AsyncAttrs для паралельных запросов
class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String)
    registration_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    def __str__(self):
        return self.username


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    genre: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)

    def __str__(self):
        return self.title


class Favorite(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    book_id: Mapped[int] = mapped_column(Integer)

    def __str__(self):
        return self.__tablename__






