from typing import Optional
from pydantic import BaseModel as BaseModelSC

class CursoSchema(BaseModelSC):
  id: Optional[int]
  titulo: str
  aulas: int
  horas: int
  
  class Config:
    orm_mode=True