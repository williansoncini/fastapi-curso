from fastapi import FastAPI
from core.config import settings
from api.v1.api import router

app = FastAPI()
app.include_router(router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
  import uvicorn
  
  uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, log_level='info')