# Conferência Quantitativa

Sistema em Python que automatiza  a conferência quantitativa de cartas enviadas pelo setor, identificando duplicatas, inconsistências e arquivos fora do padrão

## Estrutura do projeto

CONFERENCIA_QUANTITATIVA/
│
├── src/               # Código-fonte
│   ├── core/          # Lógica principal (parsing, scanner, reconcile, models)
│   └── infra/         # Infraestrutura (CLI, reporter, excel_reader, fs_scanner)
│
├── data/              # Arquivos de entrada (ex.: Cartas)
├── results/           # Saídas geradas (relatórios, logs)
├── tests/             # Testes automatizados
├── requirements.txt    # Dependências
├── README.md           # Documentação
└── .gitignore         # Arquivos ignorados

## Padrão de nome das cartas

As cartas devem seguir o formato: XX_XX_xxxxxxxx_assunto
Exemplo prático de carta: GF_GO_12345678_asssunto

- **GF** -> Sede
- **GO** -> Setor
- **12345678** -> Código da carta
- **assunto** -> Descrição resumida referente ao conteúdo da carta

Cartas fora desse padrão serão indetificadas e listadas como inválidas para a exclução dessas cartas ou renomeação das mesmas

## Como rodar o sistema(Versão inicial)

1. Crie o ambiente virtual(venv)
    '''bash
    python -m venv venv
    source venv/bin/active # Para Linux ou Mac
    venv\Scripts\activate # Para Windows

2. Instale as dependências
    pip install -r requirements.txt

3. Execute o CLI apontando para a pasta das cartas
    python -m src.infra.cli "C:\Users\XXXXXXXX\Downloads\Conferencia_Quantitativa" (Caminho fictício)

## Saída

O sistema gera:

Relatório no terminal com:
    ✅ Cartas válidas

    🔁 Cartas duplicadas

    ⚠️ Cartas fora do padrão
    
Relatórios exportados em results/
