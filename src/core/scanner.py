import os
from typing import List

import typer

from core.models import Carta
from core.parsing import parse_files


def scan_folder(folder_path: str) -> List[Carta]:
    """
    - Escaneia a pasta selecionada e identifica duplicatas
    - Cada item (PDF ou pasta) é considerado uma 'carta'
    - Outros tipos de arquivo são ignorados
    """

    itens: List[str] = []

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Só escaniea PDFs ou pastas
        if os.path.isfile(item_path):
            if not item.lower().endswith(".pdf"):
                continue
        elif not os.path.isdir(item_path):
            continue

        itens.append(item_path)
        typer.echo(f"Selecionado: {item_path}")

    # Usa parsing para transformar em objetos Carta
    nomes = [os.path.basename(p) for p in itens]
    cartas = parse_files(nomes)

    # Reatribui caminho completo ao nome_arquivo
    path_map = {os.path.basename(p): p for p in itens}
    for c in cartas:
        c.nome_arquivo = path_map.get(c.nome_arquivo, c.nome_arquivo)

    return cartas
