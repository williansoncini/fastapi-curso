from fastapi import APIRouter

router = APIRouter()

@router.get('/cursos/')
async def get_cursos():
  return {'info':'cursos'}