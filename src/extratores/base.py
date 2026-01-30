from abc import ABC, abstractmethod
from typing import List
from src.modelos.produto import Produto

class ExtratorDados(ABC):
    @abstractmethod
    def extrair(self, caminho_arquivo: str) -> List[Produto]:
        pass
