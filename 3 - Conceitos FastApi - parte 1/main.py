from typing import Any, List
from fastapi import FastAPI, HTTPException, Header, Path, Query, Response, status, Depends
from models import Curso, cursos
from fakeDb import fake_db

app = FastAPI(title='Primeira api com fastApi', 
              description='Fazendo a Api através d eum curso no Udemy', 
              version='1.0.0')

@app.get('/cursos', 
         description='Retorna uma lista com os cursos',
         summary='Retorna todos os cursos existentes',
         response_model=List[Curso],
         response_description='Cursos encontrado com sucesso!')
async def get_cursos(db: Any = Depends(fake_db)):
  return cursos

@app.get('/cursos/{id}', response_model=Curso, response_description='')
async def getCurso(id:int = Path(default=None,title='Id do curso', 
                                 description='Deve ser entre 1 e 2', 
                                 gt=0, 
                                 lt=3), 
                   db: Any = Depends(fake_db)):
  try:
    curso = cursos[id]
    return curso
  except KeyError:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado')
  
@app.post('/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso:Curso, db: Any = Depends(fake_db)):
  next_id: int = len(cursos) +1
  curso.id = next_id
  cursos.append(curso)
  
  return curso

@app.put('/cursos/{id}')
async def put_curso(id: int, curso:Curso, db: Any = Depends(fake_db)):
  if checkHaving(id, cursos):
    curso.id = id
    cursos[id] = curso
    return curso
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id do curso não encontrado')

@app.delete('/cursos/{id}')
async def delete_curso(id: int, db: Any = Depends(fake_db)):
  if checkHaving(id, cursos):
    del cursos[id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
  else:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Id do curso não encontrado')

def checkHaving(id, list):
  for index, item in enumerate(list):
    if id == index:
      return True
  return False

@app.get('/calculadora')
async def calcular(x: int= Query(default=None), 
                   y: int = Query(default=None, gt=10), 
                   z_geek:int = Header(default=None)):
  soma : int = x + y + z_geek
  return {'Resultado': soma}
  
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', log_level='info', port=8000, reload=True)