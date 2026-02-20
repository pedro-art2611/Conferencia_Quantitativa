from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Carta:
    """
    Representa uma carta no sistema

    - setor: código do setor (ex.: 'AA')
    - codigo: identificador único da carta (8 dígitos)
    - nome_arquivo: caminho do arquivo ou pasta correspondente
    - origem: origem da carta (ex.: 'pasta' ou 'planilha')
    """

    setor: str
    codigo: str
    nome_arquivo: Optional[str] = None
    origem: Optional[str] = None  # "Pasta" ou "Planilha"
    status: str = "Padrão"  # "Padrão" ou "Fora do padrão"
