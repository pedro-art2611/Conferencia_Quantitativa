import typer
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from core.scanner import scan_folder
from core.reconcile import find_duplicates

app = typer.Typer()
console = Console()

def mostrar_tabela(cartas, titulo, cor_status, emoji):
    table = Table(title=f"{emoji} {titulo}", header_style="bold magenta", style="bold blue")
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

    # resumo
    total = len(cartas)
    padrao = sum(1 for c in cartas if c.status == "Dentro do padrão")
    fora = sum(1 for c in cartas if c.status == "Fora do padrão")
    nao_identificado = sum(1 for c in cartas if c.status == "Não identificado")

    pasta_nome = os.path.basename(folder)

    console.print(f"Relatório da pasta: [bold cyan]{pasta_nome}")

    typer.echo("Cartas encontradas:")
    for c in cartas:
        typer.echo(f"- {c.nome_arquivo} ({c.status})")

    typer.echo("\nResumo: ")
    typer.echo(f"Total de cartas encontradas: {total}")
    typer.echo(f"Cartas no padrão: {padrao}")
    typer.echo(f"Cartas fora do padrão: {fora}")
    typer.echo(f"Cartas não identificadas: {nao_identificado}")

    # duplicatas
    duplicatas = find_duplicates(cartas)
    typer.echo("\nDuplicatas encontradas: ")
    if not duplicatas:
        typer.echo("Nenhuma duplicata encontrada!")
    else:
        for (setor, codigo), grupo in duplicatas.items():
            typer.echo(f"- {setor} | {codigo}: {len(grupo)} cartas")
            for carta in grupo:
                typer.echo(f"   * {carta.nome_arquivo} ({carta.status})")
