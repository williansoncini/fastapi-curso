from fastapi import APIRouter

router = APIRouter()

@router.get('/usuarios')
async def get_usuarios():
  return {'info':'usuários'}