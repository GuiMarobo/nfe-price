from dataclasses import dataclass

@dataclass
class Produto:
    codigo: str
    descricao: str
    ncm: str
    cst: str
    cfop: str
    unidade: str
    quantidade: float
    valor_unitario: float
    valor_total: float
    base_calculo_icms: float
    valor_icms: float
    valor_ipi: float
    aliquota_icms: float
    aliquota_ipi: float
    
    preco_custo: float = 0.0
    markup: float = 0.0
    preco_sugerido: float = 0.0

    def calcular_custo(self):
        if self.quantidade > 0:
            self.preco_custo = (self.valor_total + self.valor_ipi) / self.quantidade
        else:
            self.preco_custo = self.valor_unitario
