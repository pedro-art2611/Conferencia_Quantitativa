import typer

from core.parsing import extract_identifiers
from core.reconcile import find_duplicates
from core.report import generate_report
from core.scanner import scan_folder

app = typer.Typer(help="Sistema para detectar duplicatas em arquivos de cartas e gerar relatórios.")


@app.command()
def scan(pasta: str):
    '''
    Função que escaneia a pasta selecionada e mostra
    quantas estão no padrão e fora do padrão
    '''

    import os

    cartas = []
    for nome in os.listdir(pasta):
        caminho = os.path.join(pasta, nome)
        carta = extract_identifiers(caminho)
        if carta:
            cartas.append(carta)

    # Contagem de cartas no padrão e fora do padrão
    total = len(cartas)
    padrao = sum(1 for c in cartas if c.status == "Dentro do padrão")
    fora_padrao = sum(1 for c in cartas if c.status == "Fora do padrão")

    # Exibição dos resultados
    typer.echo(f"Total de cartas encontradas: ")
    for c in cartas:
        typer.echo(f"- {c.nome_arquivo}: {c.status}")

    typer.echo(f"\nResumo:")
    typer.echo(f"Total de cartas: {total}")
    typer.echo(f"Cartas no padrão: {padrao}")
    typer.echo(f"Cartas fora do padrão: {fora_padrao}")


@app.command()
def duplicates(folder: str):
    """
    Função que exibe as duplicatas encontradas na pasta selecionada
    """

    cartas = scan_folder(folder)
    duplicates = find_duplicates(cartas)
    typer.echo(f"Duplicatas encontradas: {len(duplicates)}")
    for (setor, codigo), grupo in duplicates.items():
        typer.echo(f"- {setor} | {codigo}: {len(grupo)} cartas")


@app.command()
def report(folder: str, output: str = "relatorio.docx"):
    '''
    Função que gera um relatório em docx, das cartas escaneadas e duplicadas pelo sistema
    '''

    cartas = scan_folder(folder)
    duplicatas = find_duplicates(cartas)
    generate_report(duplicatas, output)
    typer.echo(f"Relatório salvo em: {output}")


def main():
    app()


if __name__ == "__main__":
    main()
