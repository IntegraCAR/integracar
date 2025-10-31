from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Gerar chave secreta (em produção, use variável de ambiente!)
# Chave fixa para manter sessões após reload do servidor
SECRET_KEY = "integracar_development_secret_key_12345678901234567890123456789012"

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=28800,  # Sessão expira em 8 horas (28800 segundos)
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Importando os routers públicos
from routes.publico.publico_login import router as publico_router
from routes.orientador.orientador import router as orientador_router
from routes.gestor_tecnico.gestor_tecnico import router as gestor_tecnico_router
from routes.gestor_administrativo.gestor_administrativo import router as gestor_administrativo_router
from routes.coordenador.coordenador import router as coordenador_router
from routes.consultor.consultor import router as consultor_router
from routes.bolsista.bolsista import router as bolsista_router

#routers públicos
app.include_router(publico_router)
app.include_router(orientador_router)
app.include_router(gestor_tecnico_router)
app.include_router(gestor_administrativo_router)
app.include_router(coordenador_router)
app.include_router(consultor_router)
app.include_router(bolsista_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)