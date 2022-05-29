from fastapi import APIRouter
from api.v1.endpoints import artigo, usuario

router = APIRouter

router.include_router(artigo.router, prefix='/artigo', tags=['artigo'])
router.include_router(usuario.router, prefix='/usuario', tags=['usuario'])