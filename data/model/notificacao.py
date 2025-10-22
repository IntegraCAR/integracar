from dataclasses import dataclass
from typing import Optional

@dataclass
class Notificacao:
    cod_notificacao: int
    motivo_notificacao: Optional[str]
