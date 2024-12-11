from typing import Annotated, AsyncGenerator
from itertools import product
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from sqlalchemy.sql.operators import is_
from pydantic import BaseModel
from contextlib import asynccontextmanager
from .models import init_db, get_session
from .models import Formula, Expression, ExpressionGroup


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, docs_url='/api/docs')

ip_addresses = ['localhost', '127.0.0.1', '192.168.1.12']
ports = ['3000', '1337', '80', '']
origins = [f'http://{ip}{":" + port if port else ""}' for (ip, port) in product(ip_addresses, ports)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api')
async def main() -> dict[str, str]:
    return {"message": "Hello world"}


@app.get('/api/formula')
async def get_formulas(session: Annotated[Session, Depends(get_session)]) -> list[Formula]:
    formulas = await session.exec(select(Formula))
    return formulas


@app.get('/api/expressions')
async def get_expressions(session: Annotated[Session, Depends(get_session)]):
    exprs = await session.exec(select(Expression).where(is_(Expression.group_id, None)))
    groups = (await session.exec(select(ExpressionGroup))).all()
    return {"expressions": exprs.all(),
            "groups": [{"main_expr": gr.main_expr,
                        "expressions": (await session.exec(select(Expression)
                                                           .where(Expression.group_id == gr.id))).all()}
                        for gr in groups]}
