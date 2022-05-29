from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.curso_model import CursoModel
from core.deps import get_session
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

routes = APIRouter()

@routes.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
  novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
  db.add(novo_curso)
  await db.commit()
  return novo_curso

@routes.get('/', response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel)
    result = await session.execute(query)
    cursos: List[CursoModel] = result.scalars().all()
    return cursos