import os

import typer
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.reconcile import find_duplicates
from core.scanner import scan_folder

app = typer.Typer()
console = Console()


def mostrar_tabela(cartas, titulo, cor_status):
    table = Table(title=f"{titulo}", header_style="bold magenta", style="bold blue")
    table.add_column("Arquivo", style="cyan", no_wrap=True)
    table.add_column("Setor", style="magenta")
    table.add_column("Código", style="yellow")
    table.add_column("Status", style="bold")

    for c in cartas:
        table.add_row(c.nome_arquivo, c.setor or "-", c.codigo or "-", f"[{cor_status}]{c.status}[/{cor_status}]")

    console.print(table)


@app.command()
def run(folder: str = typer.Argument(..., help="Caminho da pasta com as cartas")):
    """
    Função que roda o sistema completo:
    - Lista todas as cartas lidas
    - Mostra um resumo (total, Dentro do padrão, Fora do padrão e Não identificado)
    - Mostra as duplicatas identificadas
    """
    cartas = scan_folder(folder)

    padrao = [c for c in cartas if c.status == "Dentro do padrão"]
    fora = [c for c in cartas if c.status == "Fora do padrão"]
    nao_identificado = [c for c in cartas if c.status == "Não identificado"]

    pasta_nome = os.path.basename(folder)

    console.print(f"📂 Relatório da pasta: [bold cyan]{pasta_nome}")

    # Mostrar as tabelas de forma separada

    if padrao:
        mostrar_tabela(padrao, "Cartas dentro do padrão ✅", "green")
    if fora:
        mostrar_tabela(fora, "Cartas fora do padrão ❌", "red")
    if nao_identificado:
        mostrar_tabela(nao_identificado, "Cartas não identificadas ⚠️", "yellow")

    # Duplicatas

    duplicatas = find_duplicates(cartas)
    if not duplicatas:
        console.print(Panel(f"Nenhuma duplicata encontrada! 👏", style="bold cyan"))
    else:
        dup_table = Table(title="Duplicatas encontradas ❗", style="bold red")
        dup_table.add_column("Setor: ", style="magenta")
        dup_table.add_column("Código: ", style="yellow")
        dup_table.add_column("Quantidade: ", style="purple4")
        dup_table.add_column("Arquivos: ", style="cyan")

        for (setor, codigo), grupo in duplicatas.items():
            arquivos = "\n".join([c.nome_arquivo for c in grupo])
            dup_table.add_row(setor, codigo, str(len(grupo)), arquivos)

        console.print(dup_table)

    # Resumo geral

    total = len(cartas)

    resumo = [
        Panel(f"Total: [bright_blue]{total}[/]", style="bright_blue"),
        Panel(f"Dentro do padrão: [green]{len(padrao)}[/]", style="green"),
        Panel(f"Fora do padrão: [red]{len(fora)}[/]", style="red"),
        Panel(f"Não identificadas: [dark_goldenrod]{len(nao_identificado)}[/]", style="dark_goldenrod"),
    ]
    console.print(Columns(resumo))
