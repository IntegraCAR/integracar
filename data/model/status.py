from dataclasses import dataclass
from datetime import datetime

@dataclass
class Status:
    cod_status: int
    data_hora_ultima_atualizacao: datetime
    tipo_status: str