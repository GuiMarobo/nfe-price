from typing import List
from src.modelos.produto import Produto

class ServicoPrecificacao:
    def __init__(self, markup_padrao: float = 1.6):
        self.markup_padrao = markup_padrao

    def processar_produtos(self, produtos: List[Produto], markup: float = None) -> List[Produto]:
        markup_alvo = markup if markup is not None else self.markup_padrao
        
        for produto in produtos:
            produto.calcular_custo()
            produto.markup = markup_alvo
            produto.preco_sugerido = produto.preco_custo * markup_alvo
            
        return produtos
