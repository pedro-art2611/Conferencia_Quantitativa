from src.core.models import Carta
from .reconcile import find_duplicates

c1 = Carta(setor="GF", codigo="12111102", nome_arquivo="teste1.pdf", origem="pasta")
c2 = Carta(setor="GF", codigo="12111102", nome_arquivo="teste2.pdf", origem="pasta")

print(find_duplicates([c1, c2]))
