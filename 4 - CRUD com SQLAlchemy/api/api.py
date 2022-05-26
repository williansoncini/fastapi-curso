from fastapi import APIRouter
from api.v1.endpoints import curso

router = APIRouter()

router.include_router(curso.router, prefix='/cursos', tags=['cursos'])