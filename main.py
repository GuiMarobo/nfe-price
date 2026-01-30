import os
import sys
import json
from src.extratores.extrator_danfe import ExtratorDanfe
from src.servicos.servico_precificacao import ServicoPrecificacao
from src.servicos.servico_exportacao import ServicoExportacao

def carregar_configuracao():
    caminho_config = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(caminho_config):
        with open(caminho_config, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "markup_padrao": 1.9,
        "caminho_entrada": "nfe.pdf",
        "caminho_saida_excel": "precificacao.xlsx",
        "caminho_saida_pdf": "precificacao.pdf"
    }

def executar():
    config = carregar_configuracao()
    
    caminho_entrada = config.get("caminho_entrada")
    saida_excel = config.get("caminho_saida_excel")
    saida_pdf = config.get("caminho_saida_pdf")
    markup = config.get("markup_padrao")
    
    print(f"--- Sistema de Precificação de Notas Fiscais ---")
    
    if not os.path.exists(caminho_entrada):
        print(f"Erro: Arquivo de entrada não encontrado: {caminho_entrada}")
        return

    print(f"Extraindo dados do DANFE...")
    extrator = ExtratorDanfe()
    produtos = extrator.extrair(caminho_entrada)
    
    if not produtos:
        print("Nenhum produto identificado. Verifique o PDF.")
        return

    print(f"{len(produtos)} produtos extraídos com sucesso.")
    
    print(f"Calculando custos e preços sugeridos (Markup: {markup})...")
    servico_precificacao = ServicoPrecificacao(markup_padrao=markup)
    produtos_processados = servico_precificacao.processar_produtos(produtos)
    
    print(f"Gerando relatório Excel em: {saida_excel}")
    ServicoExportacao.para_excel(produtos_processados, saida_excel)
    
    print(f"Gerando relatório PDF em: {saida_pdf}")
    ServicoExportacao.para_pdf(produtos_processados, saida_pdf)
    
    print(f"--- Processamento Finalizado com Sucesso ---")

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    executar()
