from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
  id: Optional[int] = None
  titulo: str
  aulas: int
  horas: int
  
  @validator('titulo')
  def valida_titulo(cls, value :str):
    palavras = value.split(' ')
    if len(palavras) < 3:
      raise ValueError('É necessário pelo menos 3 palavras')
    return value
  
cursos = [
  Curso(id=1, titulo='Algoritimos', aulas=30, horas=120),
  Curso(id=2, titulo='Banco de dados', aulas=754, horas=85)
]