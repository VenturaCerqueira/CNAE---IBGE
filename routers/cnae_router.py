from fastapi import APIRouter, HTTPException
from typing import List
from services.cnae_service import get_cnae_classe_subclasse_data
from models.cnae_model import CnaeTratado

router = APIRouter()

@router.get(
    "/cnae-classe-subclasse",
    response_model=List[CnaeTratado],
    summary="Retorna todos os CNAEs com classe e subclasse",
    description="Busca todos os CNAEs com o código concatenado de classe e subclasse."
)
async def get_cnaes():
    """
    Retorna todos os CNAEs com o código completo da classe + subclasse.
    """
    try:
        data = await get_cnae_classe_subclasse_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a requisição: {e}")