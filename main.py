from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

app = FastAPI()

# Gerar chave secreta (em produção, use variável de ambiente!)
# Chave fixa para manter sessões após reload do servidor
# SECRET_KEY = "hemotec_development_secret_key_12345678901234567890123456789012"

'''# Adicionar middleware de sessão
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=28800,  # Sessão expira em 8 horas (28800 segundos)
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)'''

#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Importando os routers públicos
from routes.publico.publico_inicio import router as publico_router

#routers públicos
app.include_router(publico_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)