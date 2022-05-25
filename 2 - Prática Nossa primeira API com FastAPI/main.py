from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def raiz():
  return {"init":"Hello World!"}
