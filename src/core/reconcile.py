from collections import defaultdict
from typing import List, Dict, Tuple
from .models import Carta

def find_duplicates(cartas: List[Carta]) -> Dict[Tuple[str,str], List[Carta]]:
    groups: Dict[Tuple[str, str], List[Carta]] = defaultdict(list)
    for c in cartas:
        groups[(c.setor, c.codigo)].append(c)
    return{k: v for k, v in groups.items() if len(v) > 1}