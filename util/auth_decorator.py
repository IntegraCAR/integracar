from functools import wraps
from typing import List, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
import os

# URL do frontend para redirecionamentos de login (ajuste conforme ambiente)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


def obter_usuario_logado(request: Request) -> Optional[dict]:
    if not hasattr(request, 'session'):
        return None
    return request.session.get('usuario')


def esta_logado(request: Request) -> bool:
    usuario = obter_usuario_logado(request)
    return usuario is not None and len(usuario) > 0


def criar_sessao(request: Request, usuario: dict) -> None:
    if hasattr(request, 'session'):
        # Remove senha da sessão por segurança
        usuario_sessao = usuario.copy()
        usuario_sessao.pop('senha', None)
        usuario_sessao.pop('senha_usuario', None)
        request.session['usuario'] = usuario_sessao


def destruir_sessao(request: Request) -> None:
    if hasattr(request, 'session'):
        request.session.clear()


def requer_autenticacao(perfis_autorizados: List[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            # Verifica se o usuário está logado
            usuario = obter_usuario_logado(request)
            if not usuario:
                accept = request.headers.get('accept', '')
                xrw = request.headers.get('x-requested-with', '')
                redirect_path = "/login?redirect=" + str(request.url.path)
                redirect_url = FRONTEND_URL.rstrip('/') + redirect_path
                if 'application/json' in accept or xrw.lower() == 'xmlhttprequest':
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                        'error': 'not_authenticated',
                        'redirect': redirect_url
                    })

                return RedirectResponse(
                    url=redirect_url,
                    status_code=status.HTTP_303_SEE_OTHER
                )
            
            # Verifica autorização se perfis foram especificados
            if perfis_autorizados:
                perfil_usuario = usuario.get('role_usuario', 'cliente')
                # Permite comparação case-insensitive
                perfil_usuario = perfil_usuario.lower() if isinstance(perfil_usuario, str) else perfil_usuario
                perfis_autorizados_lower = [p.lower() for p in perfis_autorizados]
                if perfil_usuario not in perfis_autorizados_lower:
                    # Retorna erro 403 se não autorizado
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Você não tem permissão para acessar este recurso"
                    )
            
            # Adiciona o usuário aos kwargs para fácil acesso na rota
            kwargs['usuario_logado'] = usuario
            
            # Chama a função original
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Importação necessária para funções assíncronas
import asyncio