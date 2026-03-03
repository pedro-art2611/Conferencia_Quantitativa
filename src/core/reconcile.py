from collections import defaultdict

def find_duplicates(cartas):
    grupos = defaultdict(list)
    for carta in cartas:
        if carta.status == "Não identificado":
            continue
        chave = (carta.setor, carta.codigo)
        grupos[chave].append(carta)

    return {chave: grupo for chave, grupo in grupos.items() if len(grupo) > 1}
