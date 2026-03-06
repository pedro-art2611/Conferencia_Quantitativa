import os
import re
from typing import List

from core.models import Carta


def extract_identifiers(filepath: str) -> Carta | None:
    """
    Extrai o setor (duas letras maiúsculas) e o código (8 dígitos) do nome de um arquivo ou pasta
    Retorna objetos de Carta com status:
    - "Dentro do padrão" → segue o padrão oficial
    - "Fora do Padrão" → tem sede/setor/código mas não segue o padrão completo
    - "Não identificado" → não conseguimos extrair sede/setor/código
    """

    filename = os.path.basename(filepath)
    if filename.lower().endswith(".pdf"):
        filename = filename[:-4]

    tokens = re.split(r"[-_ ]+", filename)

    sede = None
    setor = None
    codigo = None
    gerencia = None
    assunto_parts = []

    for token in tokens:
        if token.isdigit() and len(token) == 8:
            codigo = token
        elif token.isalpha():
            if sede is None and len(token) == 2:
                sede = token.upper()
            elif setor is None and 1 <= len(token) <= 3:
                setor = token.upper()
            elif gerencia is None:
                gerencia = token.upper()
            else:
                assunto_parts.append(token)
        else:
            if token:
                assunto_parts.append(token)

    if not (sede and setor and codigo):
        return Carta(setor="", codigo="", nome_arquivo=filename, origem="Pasta", status="Não identificado")

    assunto = " ".join(assunto_parts) if assunto_parts else None

    oficial_pattern = f"{sede}_{setor}_{codigo}_{gerencia}"
    if assunto:
        oficial_pattern += f"_{assunto}"

    if filename == oficial_pattern:
        status = "Dentro do padrão"
    elif filename.startswith(f"{sede}_{setor}_{codigo}_{gerencia}"):
        # tem sede, setor, código e gerencia mas não bate 100% → fora do padrão
        status = "Fora do padrão"
    else:
        status = "Fora do padrão"

    return Carta(setor=setor, codigo=codigo, nome_arquivo=filename, origem="Pasta", status=status)


def parse_files(arquivos: List[str]) -> List[Carta]:
    """
    Transforma nome de arquivos em objetos Carta
    """

    cartas: List[Carta] = []
    for nome in arquivos:
        identifier = extract_identifiers(nome)
        if not identifier:
            continue
        cartas.append(identifier)
    return cartas
