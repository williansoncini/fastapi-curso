from time import sleep

def fake_db():
  try:
    print('Conectando ao banco de dados')
    sleep(0.5)
  finally:
    print('Finalizando conexão com o banco de dados')
    sleep(0.5)