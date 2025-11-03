from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import analise_processos_repo, status_repo
from util.auth_decorator import requer_autenticacao
from fastapi.responses import JSONResponse
from datetime import datetime, date

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def serializar_datetime(obj):
    """Converte objetos datetime/date para string ISO format recursivamente"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: serializar_datetime(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serializar_datetime(item) for item in obj]
    return obj

def obter_processos_por_usuario(cod_usuario: int):
    """Retorna processos criados por um usuário específico"""
    try:
        # Obter todos os processos detalhados e filtrar pelo usuário
        todos_processos = analise_processos_repo.obter_todos_detalhado()
        return [p for p in todos_processos if p.get('cod_usuario') == cod_usuario]
    except Exception as e:
        print(f"Erro ao obter processos por usuário: {e}")
        return []

def obter_contagem_por_status_usuario(cod_usuario: int):
    """Retorna contagem de processos por status para um usuário específico"""
    try:
        processos_usuario = obter_processos_por_usuario(cod_usuario)
        # Agrupar por status e contar
        contagem = {}
        for processo in processos_usuario:
            status = processo.get('tipo_status')
            if status:
                contagem[status] = contagem.get(status, 0) + 1
        
        # Converter para lista no formato esperado
        return [{'tipo_status': k, 'quantidade': v} for k, v in contagem.items()]
    except Exception as e:
        print(f"Erro ao obter contagem por status do usuário: {e}")
        return []

def obter_ultimas_por_status_usuario(cod_usuario: int):
    """Retorna últimas atualizações por status para um usuário específico"""
    try:
        processos_usuario = obter_processos_por_usuario(cod_usuario)
        # Agrupar por status e pegar a última atualização
        ultimas_por_status = {}
        for processo in processos_usuario:
            status = processo.get('tipo_status')
            if status:
                data_atualizacao = processo.get('data_hora_ultima_atualizacao')
                if status not in ultimas_por_status:
                    ultimas_por_status[status] = {
                        'tipo_status': status,
                        'ultima_atualizacao': data_atualizacao
                    }
                else:
                    # Se já existe, verificar se a nova data é mais recente
                    data_atual = ultimas_por_status[status].get('ultima_atualizacao')
                    if data_atualizacao:
                        if not data_atual or (isinstance(data_atualizacao, (datetime, date)) and 
                            isinstance(data_atual, (datetime, date)) and data_atualizacao > data_atual):
                            ultimas_por_status[status] = {
                                'tipo_status': status,
                                'ultima_atualizacao': data_atualizacao
                            }
        
        # Converter para lista
        return list(ultimas_por_status.values())
    except Exception as e:
        print(f"Erro ao obter últimas por status do usuário: {e}")
        return []

@router.get("/bolsista")
@requer_autenticacao(["bolsista"])
async def get_bolsista_home(request: Request, usuario_logado: dict = None):
    """Retorna dados do bolsista, incluindo apenas processos criados por ele"""
    try:
        cod_usuario = usuario_logado.get('cod_usuario')
        if not cod_usuario:
            return JSONResponse(
                status_code=400,
                content={"error": "Código do usuário não encontrado"}
            )
        
        # Obter processos criados pelo bolsista
        obter_todos = obter_processos_por_usuario(cod_usuario)
        contagem_por_status = obter_contagem_por_status_usuario(cod_usuario)
        ultimas_analises = obter_ultimas_por_status_usuario(cod_usuario)
        
        # Serializar datetime para string
        obter_todos_serializado = serializar_datetime(obter_todos)
        contagem_por_status_serializado = serializar_datetime(contagem_por_status)
        ultimas_analises_serializado = serializar_datetime(ultimas_analises)
        
        return JSONResponse(content={
            "usuario": usuario_logado,
            "obter_todos": obter_todos_serializado,
            "contagem_por_status": contagem_por_status_serializado,
            "ultimas_analises": ultimas_analises_serializado
        })
    except Exception as e:
        print(f"ERRO no endpoint /bolsista: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao buscar dados: {str(e)}"}
        )


@router.get("/processo/{cod_processo}", response_class=JSONResponse)
@requer_autenticacao(["bolsista"])
async def get_por_processo(cod_processo: int, request: Request, usuario_logado: dict = None):
    """Retorna um processo específico, apenas se pertencer ao bolsista logado"""
    try:
        cod_usuario = usuario_logado.get('cod_usuario')
        if not cod_usuario:
            return JSONResponse(
                status_code=400,
                content={"error": "Código do usuário não encontrado"}
            )
        
        # Obter processo do repositório
        por_processo = analise_processos_repo.obter_por_processo(cod_processo)
        
        if not por_processo:
            return JSONResponse(
                status_code=404,
                content={"error": "Processo não encontrado"}
            )
        
        # Verificar se o processo pertence ao bolsista
        processo_encontrado = None
        for proc in por_processo:
            if proc.get('cod_usuario') == cod_usuario:
                processo_encontrado = proc
                break
        
        if not processo_encontrado:
            return JSONResponse(
                status_code=403,
                content={"error": "Você não tem permissão para acessar este processo"}
            )
        
        # Retornar apenas o processo do bolsista
        por_processo_serializado = serializar_datetime([processo_encontrado])
        return JSONResponse(content={"analises": por_processo_serializado})
    except Exception as e:
        print(f"ERRO no endpoint /processo/{cod_processo}: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao buscar processo: {str(e)}"}
        )


@router.get("/status/listar")
@requer_autenticacao(["bolsista"])
async def listar_status(request: Request, usuario_logado: dict = None):
    """Lista todos os status disponíveis"""
    try:
        status_list = status_repo.obter_todos()
        status_serializado = serializar_datetime(status_list)
        return JSONResponse(content={"status": status_serializado})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao listar status: {str(e)}"}
        )
