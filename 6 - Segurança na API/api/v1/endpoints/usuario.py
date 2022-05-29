from ast import Raise
from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.usuario_model import UsuarioModel
from schemas.usuarioSchema import *
from core.deps import get_session, get_current_user
from core.security import gerarHashSenha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

@router.get('/logado', response_model=UsuarioSchemaBase)
async def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
  return usuario_logado

@router.post('/singup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario:UsarioSchemaCreate, db: AsyncSession = Depends(get_session)):
  novo_usario: UsuarioModel = UsuarioModel(
    nome=usuario.nome,
    email=usuario.email,
    senha=gerarHashSenha(usuario.senha),
    eh_admin=usuario.eh_admin
  )

  async with db as session:
    session.add(novo_usario)
    await session.commit()
    
    return novo_usario
  
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db:AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel)
    result = session.execute(query)
    usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
    return usuarios

@router.get('/{id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario(id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel).filter(UsuarioModel.id == id)
    result = session.execute(query)
    usuario = result.scalars().unique().one_or_none()
    
    if usuario:
      return usuario
    else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado')

@router.put('/{id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(id: int, usuario: UsarioSchemaCreate, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel).filter(UsuarioModel.id == id)
    result = session.execute(query)
    usuarioUp: UsuarioSchemaBase = result.scalars().unique().one_or_none()
    
    if usuarioUp:
      if usuario.nome != usuarioUp.nome:
        usuarioUp.nome = usuario.nome
      if usuario.email != usuarioUp.email:
        usuarioUp.email = usuario.email
      if usuario.eh_admin != usuarioUp.eh_admin:
        usuarioUp.eh_admin = usuario.eh_admin
      if usuarioUp.senha:
        usuarioUp.senha = gerarHashSenha(usuario.senha)
      
      await session.commit()
      return usuarioUp
    else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado')

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel).filter(UsuarioModel.id == id)
    result = session.execute(query)
    usuario = result.scalars().unique().one_or_none()
    
    if usuario:
      await session.delete(usuario)
      await session.commit()
      return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado')

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
  usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

  if not usuario:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos')
  
  return JSONResponse(
    content={
      'access_token': criar_token_acesso(sub=usuario.id),
      'token_type': 'bearer'
    }, status_code=status.HTTP_200_OK
  )
    
