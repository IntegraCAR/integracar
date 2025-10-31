from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campus_repo, usuario_repo
from util.security import criar_hash_senha, verificar_senha
from fastapi.responses import RedirectResponse
from util.auth_decorator import criar_sessao, requer_autenticacao
from fastapi import Form, status

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Rota de login
@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_por_email(email)
    from fastapi.responses import JSONResponse
    if usuario:
        resultado_verificacao = verificar_senha(senha, usuario.senha_usuario)
    else:
        resultado_verificacao = False
    if not usuario or not resultado_verificacao:
        return JSONResponse(
            status_code=401,
            content={"erro": "Email ou senha inválidos"}
        )

    # Criar sessão
    usuario_dict = {
        "cod_usuario": usuario.cod_usuario,
        "cod_campus": usuario.cod_campus,
        "cod_orientador": usuario.cod_orientador,
        "nome_usuario": usuario.nome_usuario,
        "email_usuario": usuario.email_usuario,
        "senha_usuario": usuario.senha_usuario,
        "cpf_usuario": usuario.cpf_usuario,
        "role_usuario": usuario.role_usuario,
        "organizacao_usuario": usuario.organizacao_usuario
    }
    criar_sessao(request, usuario_dict)
    print(usuario_dict)

    # Retornar JSON com dados do usuário autenticado
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=200,
        content={"usuario": usuario_dict}
    )