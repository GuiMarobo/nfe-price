# Leitor de Notas Fiscais DANFE e Precificador Automatizado

Este software automatiza a extração de dados de produtos de Notas Fiscais Eletrônicas (DANFE) em PDF e realiza o cálculo de precificação sugerida.

## 🏗️ Arquitetura do Software

O projeto foi desenvolvido utilizando uma **Arquitetura em Camadas (Layered Architecture)**, focada em **Clean Code** e princípios **SOLID**. Abaixo, detalho cada componente:

### 1. Camada de Modelos (`src/modelos`)
Contém a definição da classe `Produto`. Esta é uma "Anêmica Data Class" que serve como a única fonte de verdade para os dados do produto em todo o sistema. Ela possui o método `calcular_custo()`, encapsulando a lógica básica de como o custo real é derivado dos dados da nota.

### 2. Camada de Extratores (`src/extratores`)
Responsável pela interface com o mundo externo (PDFs).
- **Base**: Define um contrato (`ExtratorDados`) para que novos extratores possam ser criados (ex: para XML ou outros layouts de nota) sem quebrar o sistema.
- **ExtratorDanfe**: Implementação específica que usa `pdfplumber` e **Expressões Regulares (Regex)** para converter o texto bruto do PDF em objetos `Produto`.

### 3. Camada de Serviços (`src/servicos`)
Onde reside a lógica de negócio e orquestração.
- **ServicoPrecificacao**: Recebe a lista de produtos e aplica as regras de negócio (markup, impostos adicionais) para gerar o preço sugerido.
- **ServicoExportacao**: Transforma os objetos `Produto` processados em formatos de saída legíveis (Excel e PDF).

### 4. Camada de Orquestração (`main.py`)
O ponto de entrada que coordena o fluxo de dados entre as camadas:
`Entrada (PDF) -> Extrator -> Serviço de Precificação -> Serviço de Exportação -> Saída (Excel/PDF)`.

---

## 🚀 Funcionalidades

- **Extração Robusta**: Parsing via Regex para alta precisão.
- **Cálculo de Custo Real**: Considera IPI e valores unitários.
- **Saída Dupla**: Gera relatórios em **Excel** e **PDF**.
- **Totalmente em Português**: Código, variáveis e documentação em PT-BR.

## ⚙️ Como Usar

1. Configure o `config.json` com os caminhos dos arquivos e o markup desejado.
2. Execute:
   ```bash
   python main.py
   ```

## 🛠️ Tecnologias
- Python 3.11
- pdfplumber (Extração PDF)
- fpdf2 (Geração PDF)
- Pandas & Openpyxl (Excel)
