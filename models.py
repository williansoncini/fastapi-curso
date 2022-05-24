from typing import Optional

from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int  # mais de 12
    horas: int  # mais de 10

    @validator('titulo')
    def validar_titulo(cls, value: str):
        # Validacao 1
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras.')

        # Validacao 2
        if value.islower():
            raise ValueError('O título deve ser capitalizado.')

        return value


cursos = [
    Curso(id=1, titulo='Programação para Leigos', aulas=42, horas=56),
    Curso(id=2, titulo='Algoritmos e Lógica de Programação', aulas=52, horas=66),
]
