from typing import List
from asyncpg import RaiseError
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.cursoModel import CursoModel
from schemas.cursoSchema import CursoSchema
from core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
  novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
  
  db.add(novo_curso)
  await db.commit()
  
  return novo_curso

@router.get('/', response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel)
    result = await session.execute(query)
    cursos: List[CursoModel] = result.scalars().all()
    
    return cursos
  
@router.get('/{id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == id)
    result = await session.execute(query)
    curso = result.scalars_one_or_none()
    
    if curso:
      return curso
    raise HTTPException(detail='Curso não encontrado', status_code=status.HTTP_400_BAD_REQUEST)
  
  
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=CursoModel)
async def put_curso(id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == id)
    result = await session.execute(query)
    cursoUp: CursoSchema = result.scalars_one_or_none()
    
    if cursoUp:
      cursoUp.titulo = curso.titulo
      cursoUp.aulas = curso.aulas
      cursoUp.horas = curso.horas
      
      await session.commit()
      
      return cursoUp
    
    raise HTTPException(detail='Curso não encontrado', status_code=status.HTTP_400_BAD_REQUEST)
      
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == id)
    result = await session.execute(query)
    curso: CursoSchema = result.scalars_one_or_none()
    
    if curso:
      await session.delete(curso)
      await session.commit()
      
      return Response(status_code=status.HTTP_204_NO_CONTENT)
      
    raise HTTPException(detail='Curso não encontrado', status_code=status.HTTP_400_BAD_REQUEST)      
