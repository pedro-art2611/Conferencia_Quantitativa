import os
import re
from typing import List

from core.models import Carta


def extract_identifiers(filepath: str) -> Carta | None:
    """
    Extrai o setor (duas letras maiúsculas) e o código (8 dígitos) do nome de um arquivo ou pasta
    Retorna objetos de Carta com status de padrão ou fora do padrão
    """
    filename = os.path.basename(filepath)
    if filename.lower().endswith(".pdf"):
        filename = filename[:-4]

    tokens = re.split(r"[-_ ]+", filename)

    sede = None
    setor = None
    codigo = None
    assunto_parts = []

    for i, token in enumerate(tokens):
        if token.isdigit() and len(token) == 8:
            codigo = token
        elif token.isalpha():
            if sede is None and len(token) == 2:
                sede = token.upper()
            elif setor is None and 1 <= len(token) <= 3:
                setor = token.upper()
            else:
                assunto_parts.append(token)
        else:
            if token:
                assunto_parts.append(token)

    if not (sede and setor and codigo):
        return None
        
    assunto = "_".join(assunto_parts) if assunto_parts else None

    # Padrão oficial: XX_XX_XXXXXXXX_assunto
    oficial_pattern = f"{sede}_{setor}_{codigo}"
    if assunto:
        oficial_pattern += f"_{assunto}"

    if len(setor) in (2, 3) and filename == oficial_pattern:
        status = "Dentro do padrão"
    else:
        status = "Fora do padrão"

    return Carta(setor=setor, codigo=codigo, nome_arquivo=filepath, origem="Pasta", status=status)



def parse_files(arquivos: List[str]) -> List[Carta]:
    """
    Transforma nome de arquivos em objetos Carta
    """

    cartas: List[Carta] = []
    for nome in arquivos:
        identifier = extract_identifiers(nome)
        if not identifier:
            continue

        setor = identifier.setor
        codigo = identifier.codigo
        if not setor or not codigo:
            continue

        cartas.append(Carta(setor=setor, codigo=codigo, nome_arquivo=nome, origem="pasta"))
    return cartas
