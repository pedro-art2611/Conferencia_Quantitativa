import argparse
from src.core.reconcile import find_duplicates

def main():
    parser = argparse.ArgumentParser(description= "Sistema de Conferência Quantitativa")
    parser.add_argument("pasta", help= "Caminho da pasta com os arquivos")
    args = parser.parse_args()

    resultado = find_duplicates(args.pasta)

if __name__ == "__main__":
    main()