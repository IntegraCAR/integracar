from dataclasses import dataclass
from typing import Optional

@dataclass
class Campus:
    nome_campus: str
    cod_campus: Optional[int] = None