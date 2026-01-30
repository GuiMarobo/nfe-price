# Leitor de Notas Fiscais DANFE e Precificador Automatizado

Este software automatiza a extração de dados de produtos de Notas Fiscais Eletrônicas (DANFE) em PDF e realiza o cálculo de precificação sugerida.

---

## Como Usar

1. Configure o `config.json` com os caminhos dos arquivos e o markup desejado.
2. Execute:
   ```bash
   python main.py
   ```

## Tecnologias
- Python 3.11
- pdfplumber (Extração PDF)
- fpdf2 (Geração PDF)
- Pandas & Openpyxl (Excel)
