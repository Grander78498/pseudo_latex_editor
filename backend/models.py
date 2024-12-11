'''
Модуль создания таблиц и сессии в базе данных
'''


import os
import json
from typing import AsyncGenerator
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, Relationship, select, insert, update
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(Path().absolute().parent /
            os.environ.get('ENV_FILE', default='.env'),
            override=True)
db_host = os.environ.get('DB_HOST', default='localhost')
db_port = os.environ.get('DB_PORT', default='5432')
db_name = os.environ.get('DB_NAME')
if db_name is None:
    raise OSError('База данных не указана в переменных среды.'
                  '\nПроверьте, что она указана в переменной DB_NAME')
db_user = os.environ.get('DB_USER', default='postgres')
db_password = os.environ.get('DB_PASSWORD', default='postgres')

db_url = f"postgresql+asyncpg://{db_user}:{db_password}" \
         f"@{db_host}:{db_port}/{db_name}"
connect_args = {"check_same_thread": False}
engine = create_async_engine(db_url)


class Formula(SQLModel, table=True):
    '''
    Таблица для хранения формул
    '''
    __tablename__ = 'formula'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    formula: str = Field(index=True)


class ExpressionGroup(SQLModel, table=True):
    '''
    Таблица для сгруппированных формул
    '''
    __tablename__ = 'expr_group'
    id: int | None = Field(default=None, primary_key=True)
    main_expr: str = Field()

    expressions: list["Expression"] = Relationship(back_populates="group")


class Expression(SQLModel, table=True):
    '''
    Таблица для хранения возможных кнопок в редакторе формул
    '''
    __tablename__ = 'expression'
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(nullable=True)
    expr: str = Field()

    group_id: int | None = Field(default=None, foreign_key="expr_group.id")
    group: ExpressionGroup | None = Relationship(back_populates="expressions")


async def init_db() -> None:
    '''
    Инициализация БД
    '''
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    '''
    Функция для создания сессии БД
    '''
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
