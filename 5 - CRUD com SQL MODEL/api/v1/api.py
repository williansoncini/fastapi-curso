from fastapi import APIRouter
from api.v1.endpoints.curso import routes

router = APIRouter()

router.include_router(routes, prefix='/cursos', tags=['curso'])