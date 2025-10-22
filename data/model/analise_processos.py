from dataclasses import dataclass
from datetime import datetime

@dataclass
class AnaliseProcessos:
    cod_analise: int
    data_hora_inicio_analise: datetime
    data_previsao_fim_analise: datetime
    cod_campus: int
    cod_usuario: int
    cod_status: int
    cod_notificacao: int
    cod_processo: int
