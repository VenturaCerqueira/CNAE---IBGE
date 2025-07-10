from pydantic import BaseModel

class CnaeTratado(BaseModel):
    Codigo: str
    Descricao: str
    Percentual: float