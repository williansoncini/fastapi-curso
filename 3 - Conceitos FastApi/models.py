from typing import Optional
from pydantic import BaseModel

class Curso(BaseModel):
  id: Optional[int] = None
  titulo: str
  aulas: int
  horas: int
  
cursos = [
  Curso(id=1, titulo='Algoritimos', aulas=30, horas=120),
  Curso(id=2, titulo='Banco de dados', aulas=754, horas=85)
]