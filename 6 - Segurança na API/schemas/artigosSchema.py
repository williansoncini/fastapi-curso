from typing import Optional
from pydantic import BaseModel as BaseModelSC, HttpUrl

class ArtigoSchema(BaseModelSC):
  id: Optional[int] = None
  titulo: str
  url_fonte: HttpUrl
  descricao: str
  usuario_id: Optional[int]
  
  class Config:
    orm_mode=True