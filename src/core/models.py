from dataclasses import dataclass
from typing import Optional

@dataclass
class Carta:
    """
    Representa uma carta no sistema

    - setor: código do setor (ex.: 'AA')
    - codigo: identificador único da carta (8 dígitos)
    - nome_arquivo: nome do arquivo (basename) ou caminho completo
    - origem: origem da carta (ex.: 'Pasta' ou 'Planilha')
    - status: se está no padrão ou fora do padrão
    """

    setor: str
    codigo: str
    nome_arquivo: str
    origem: Optional[str] = None  # "Pasta" ou "Planilha"
    status: str = "Indefinido"        # "Dentro do padrão", "Fora do padrão" ou "Não identificado"
