from typing import Annotated, AsyncGenerator
from itertools import product
import PIL.Image
from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, insert
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.operators import is_
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
import PIL
from contextlib import asynccontextmanager
from .models import init_db, get_session
from .models import Formula, Expression, ExpressionGroup
from .analyzer import analyze
from .latex_ocr import get_latex


class FormulaAnalysisBody(BaseModel):
    first_formula: str
    second_formula: str


class ExpressionBody(BaseModel):
    name: str
    expr: str


class FormulaBody(BaseModel):
    name: str
    formula: str



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, docs_url='/api/docs', openapi_url='/api/openapi.json')

ip_addresses = ['localhost', '127.0.0.1', '192.168.1.12']
ports = ['3000', '1337', '80', '', '5173']
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


@app.get('/api/formulas')
async def get_formulas(session: Annotated[AsyncSession, Depends(get_session)]):
    formulas = await session.exec(select(Formula))
    return {'formulas': formulas.all()}


@app.get('/api/expressions')
async def get_expressions(session: Annotated[AsyncSession, Depends(get_session)]):
    exprs = await session.exec(select(Expression).where(is_(Expression.group_id, None)))
    groups = (await session.exec(select(ExpressionGroup).options(selectinload(ExpressionGroup.expressions)))).all()
    return {"expressions": exprs.all(),
            "groups": [{"main_expr": gr.main_expr,
                        "expressions": gr.expressions}
                        for gr in groups]}


@app.post('/api/analyse')
async def analyse_formulas(formulas: FormulaAnalysisBody):
    diff, score = analyze(formulas.first_formula, formulas.second_formula)
    return {'diff': diff, 'score': round(score * 100, 2)}


@app.post('/api/upload_photo')
async def convert_photo_latex(file: UploadFile):
    with PIL.Image.open(file.file) as im:
        latex_string = get_latex(im)
        latex_string = latex_string.replace('\\left', '').replace('\\right', '') \
                                   .replace('(', '{(').replace(')', ')}')
    return {'result': latex_string}


@app.post('/api/post/expr')
async def add_expression(expression: ExpressionBody, session: Annotated[AsyncSession, Depends(get_session)]):
    await session.exec(insert(Expression).values(name=expression.name, expr=expression.expr))
    await session.commit()
    return {'msg': "Good"}


@app.post('/api/post/formula')
async def add_formula(formula: FormulaBody, session: Annotated[AsyncSession, Depends(get_session)]):
    await session.exec(insert(Formula).values(name=formula.name, formula=formula.formula))
    await session.commit()
    return {'msg': "Good"}
