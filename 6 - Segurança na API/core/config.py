from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
  API_V1_STR = '/api/v1'
  DB_URL: str = "postgresql+asyncpg://admin:admin@172.20.196.57:5432/cursos"
  DBBaseModel = declarative_base()
  JWT_SECRET = "pQOaP5j6-fNdyimJhO6qc7bVl80HL3WOJtNZEAQP9AQ"
  """
  Para gerar um segredo utilizando o python faça assim:
  
  import secrets
  
  token: int = secrets.token_urlsafe(32)
  """
  ALGORITHM = 'HS256'
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*27*7
  
  
  class Config:
    case_sensitive = True
    
settings: Settings = Settings()