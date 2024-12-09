from typing import Annotated, AsyncGenerator
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from .models import init_db, get_session
from .models import Formula, Expression


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, docs_url='/api/docs')

origins = [
    'http://localhost:3000',
    'http://frontend:3000',
    'http://127.0.0.1:3000',
    'http://localhost:1337',
    'http://frontend:1337',
    'http://127.0.0.1:1337'
]



@app.get('/api')
async def main() -> dict[str, str]:
    return {"message": "Hello world"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/formula')
async def get_formulas(session: Annotated[Session, Depends(get_session)]) -> list[Formula]:
    formulas = await session.exec(select(Formula))
    return formulas


@app.get('/api/expressions')
async def get_expressions(session: Annotated[Session, Depends(get_session)]) -> list[Expression]:
    exprs = await session.exec(select(Expression))
    return exprs
