from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    cod_usuario: int
    cod_campus: Optional[int]
    nome_usuario: str
    role_usuario: str
    organizacao_usuario: str
