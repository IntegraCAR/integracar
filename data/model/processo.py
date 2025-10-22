from dataclasses import dataclass

@dataclass
class Processo:
    cod_processo: int
    codigo_edocs: str
    numero_processo_florestal: str
    codigo_empreendimento: str
