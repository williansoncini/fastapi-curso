from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificarSenha(senha: str, hash:str) -> bool:
  return CRIPTO.verify(senha, hash)
  
def gerarHashSenha(senha:str) -> str :
  return CRIPTO.hash(senha)