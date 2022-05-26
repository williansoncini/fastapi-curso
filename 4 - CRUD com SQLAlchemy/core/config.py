from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
  API_V1_STR = '/api/v1'
  DB_URL: str = "postgresql+asyncpg://admin:admin@172.20.196.57:5432/cursos"
  DBBaseModel = declarative_base()
  
  class Config:
    case_sensitive = True
    
settings = Settings()