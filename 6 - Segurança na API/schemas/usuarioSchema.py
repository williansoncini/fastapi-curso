from typing import List, Optional
from pydantic import BaseModel as BaseModelSC, EmailStr
from schemas.artigosSchema import ArtigoSchema

class UsuarioSchemaBase(BaseModelSC):
  id: Optional[int] = None
  nome: str
  email: EmailStr
  eh_admin: bool = False
  
  class Config:
    orm_mode = True
  
class UsarioSchemaCreate(UsuarioSchemaBase):
  senha: str
  
class UsarioSchemaArtigo(UsuarioSchemaBase):
  artigos: Optional[List[ArtigoSchema]]
  
class UsuarioSchemaUp(UsuarioSchemaBase):
  nome:  Optional[str]
  senha: Optional[str]
  email: Optional[EmailStr]
  eh_admin: Optional[bool]
  