from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Carta:
    setor: str
    codigo: str
    nome_arquivo: Optional[str] = None
    origem: Optional[str] = None # "Pasta" ou "Planilha"
