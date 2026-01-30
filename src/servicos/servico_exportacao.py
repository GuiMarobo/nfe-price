from typing import List

import pandas as pd
from fpdf import FPDF
from src.modelos.produto import Produto


class ServicoExportacao:
    @staticmethod
    def para_excel(produtos: List[Produto], caminho_saida: str):
        dados = []
        for p in produtos:
            dados.append({
                "Código": p.codigo,
                "Descrição": p.descricao,
                "NCM": p.ncm,
                "Unidade": p.unidade,
                "Quantidade": p.quantidade,
                "Valor Unit. (NF)": p.valor_unitario,
                "Valor Total (NF)": p.valor_total,
                "Vlr ICMS": p.valor_icms,
                "Vlr IPI": p.valor_ipi,
                "Custo Real Unit.": p.preco_custo,
                "Markup Aplicado": p.markup,
                "Preço Sugerido": p.preco_sugerido
            })
        
        df = pd.DataFrame(dados)
        
        with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Precificação')
            
            planilha = writer.sheets['Precificação']
            for idx, col in enumerate(df.columns):
                comprimento_max = max(df[col].astype(str).map(len).max(), len(col)) + 2
                planilha.column_dimensions[chr(65 + idx)].width = comprimento_max

    @staticmethod
    def para_pdf(produtos: List[Produto], caminho_saida: str):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório de Precificação de Produtos", ln=True, align='C')
        pdf.ln(5)
        
        # Cabeçalho da Tabela
        pdf.set_font("Arial", "B", 8)
        pdf.set_fill_color(200, 200, 200)
        
        colunas = [
            ("Cód", 15), ("Descrição", 80), ("Qtd", 15), 
            ("Vlr Unit", 25), ("IPI", 20), ("Custo Real", 25), 
            ("Markup", 20), ("Sugerido", 25)
        ]
        
        for col_nome, largura in colunas:
            pdf.cell(largura, 8, col_nome, border=1, fill=True, align='C')
        pdf.ln()
        
        # Dados
        pdf.set_font("Arial", "", 7)
        for p in produtos:
            # Truncar descrição se for muito longa
            desc = p.descricao[:50] + "..." if len(p.descricao) > 50 else p.descricao
            
            pdf.cell(15, 7, str(p.codigo), border=1, align='C')
            pdf.cell(80, 7, desc, border=1)
            pdf.cell(15, 7, f"{p.quantidade:.2f}", border=1, align='C')
            pdf.cell(25, 7, f"R$ {p.valor_unitario:.2f}", border=1, align='R')
            pdf.cell(20, 7, f"R$ {p.valor_ipi:.2f}", border=1, align='R')
            pdf.cell(25, 7, f"R$ {p.preco_custo:.2f}", border=1, align='R')
            pdf.cell(20, 7, f"{p.markup:.2f}x", border=1, align='C')
            pdf.cell(25, 7, f"R$ {p.preco_sugerido:.2f}", border=1, align='R')
            pdf.ln()
            
        pdf.output(caminho_saida)
