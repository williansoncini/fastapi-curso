from pydantic import BaseSettings
from sqlalchemy import false

class Settings(BaseSettings):
  API_V1_STR = '/api/v1'
  DB_URL = "postgresql+asyncpg://admin:admin@172.29.43.1:5432/cursos"
  
  class Config():
    case_sensitive = False
    
settings: Settings = Settings()
