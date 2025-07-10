from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import cnae_router

app = FastAPI(
    title="API CNAE Processada",
    version="1.0.0",
    description="API para buscar e formatar dados CNAE do IBGE.",
    contact={
        "name": "Keep Informática - Desenvolvimento",
        "email": "contato@keepinformatica.com.br",
    },
    docs_url="/api-docs",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# --- Rotas da API ---
app.include_router(cnae_router.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API CNAE Processada! Acesse /api-docs para a documentação."}