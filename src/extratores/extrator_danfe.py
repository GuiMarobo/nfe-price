import pdfplumber
import re
from typing import List
from src.modelos.produto import Produto
from src.extratores.base import ExtratorDados

class ExtratorDanfe(ExtratorDados):
    def __init__(self):
        self.padrao_produto = re.compile(
            r'^(\d+)\s+'                # Código
            r'(.+?)\s+'                 # Descrição
            r'(\d{8})\s+'               # NCM
            r'(\d\.\d{2})\s+'           # CST
            r'(\d\.\d{3})\s+'           # CFOP
            r'([A-Z]{1,3})\s+'          # Unidade
            r'([\d.,]+)\s+'             # Quantidade
            r'([\d.,]+)\s+'             # Valor Unitário
            r'([\d.,]+)\s+'             # Valor Total
            r'([\d.,]+)\s+'             # BC ICMS
            r'([\d.,]+)\s+'             # Valor ICMS
            r'([\d.,]+)\s+'             # Valor IPI
            r'(\d+)\s+'                 # Alíquota ICMS
            r'(\d+)'                    # Alíquota IPI
        )

    def _limpar_valor(self, valor: str) -> float:
        if not valor:
            return 0.0
        limpo = valor.replace(".", "").replace(",", ".")
        try:
            return float(limpo)
        except ValueError:
            return 0.0

    def extrair(self, caminho_arquivo: str) -> List[Produto]:
        produtos = []
        with pdfplumber.open(caminho_arquivo) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if not texto:
                    continue
                
                linhas = texto.split('\n')
                for linha in linhas:
                    correspondencia = self.padrao_produto.match(linha.strip())
                    if correspondencia:
                        grupos = correspondencia.groups()
                        try:
                            p = Produto(
                                codigo=grupos[0],
                                descricao=grupos[1],
                                ncm=grupos[2],
                                cst=grupos[3],
                                cfop=grupos[4],
                                unidade=grupos[5],
                                quantidade=self._limpar_valor(grupos[6]),
                                valor_unitario=self._limpar_valor(grupos[7]),
                                valor_total=self._limpar_valor(grupos[8]),
                                base_calculo_icms=self._limpar_valor(grupos[9]),
                                valor_icms=self._limpar_valor(grupos[10]),
                                valor_ipi=self._limpar_valor(grupos[11]),
                                aliquota_icms=self._limpar_valor(grupos[12]),
                                aliquota_ipi=self._limpar_valor(grupos[13])
                            )
                            produtos.append(p)
                        except Exception as erro:
                            print(f"Erro ao processar linha: {linha} - {erro}")
        return produtos
