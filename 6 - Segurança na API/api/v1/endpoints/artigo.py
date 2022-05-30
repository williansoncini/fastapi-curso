from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigosSchema import ArtigoSchema, ArtigoSchemaUp
from core.deps import get_current_user, get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema,
                     usuario_logado: UsuarioModel = Depends(get_current_user),
                     db: AsyncSession = Depends(get_session)):
  novo_artigo: ArtigoModel = ArtigoModel(
    titulo=artigo.titulo,
    url_fonte=artigo.url_fonte,
    descricao=artigo.descricao,
    usuario_id=usuario_logado.id,
    # criador=artigo
  )
  db.add(novo_artigo)
  await db.commit()
  return novo_artigo

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(ArtigoModel)
    result = await session.execute(query)
    artigos: List[ArtigoModel] = result.scalars().unique().all()
    
    return artigos
  
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ArtigoSchema)
async def get_artigo(id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(ArtigoModel).filter(ArtigoModel.id == id)
    result = await session.execute(query)
    artigo: ArtigoModel = result.scalars().unique().one_or_none()
    
    if artigo:
      return artigo
    else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado')
      
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ArtigoSchema)
async def put_artigo(id: int, 
                     artigo: ArtigoSchemaUp, 
                     usuario_logado: UsuarioModel = Depends(get_current_user), 
                     db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(ArtigoModel).filter(ArtigoModel.id == id)
    result = await session.execute(query)
    artigoUp: ArtigoModel = result.scalars().unique().one_or_none()
    
    if artigoUp:
      if artigo.descricao:
        artigoUp.descricao = artigo.descricao
      if artigo.titulo:  
        artigoUp.titulo = artigo.titulo
      if artigo.url_fonte:
        artigoUp.url_fonte = artigo.url_fonte
      if artigoUp.usuario_id != usuario_logado.id:
        artigoUp.usuario_id = usuario_logado.id
      
      await session.commit()
      
      return artigoUp
    else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado')

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(id: int, 
                        db: AsyncSession = Depends(get_session),
                        usuario_logado: UsuarioModel = Depends(get_current_user), ):
  async with db as session:
    query = select(ArtigoModel).filter(ArtigoModel.id == id).filter(ArtigoModel.usuario_id == usuario_logado.id)
    result = await session.execute(query)
    artigo: ArtigoModel = result.scalars().unique().one_or_none()
    
    if artigo:
      await session.delete(artigo)
      await session.commit()
      return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado')