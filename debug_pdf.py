import pdfplumber

pdf_path = "{NFE-Path}"
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"--- Página {i+1} ---")
        table = page.extract_table()
        if table:
            for row in table[:10]:
                print(row)
        else:
            print("Nenhuma tabela encontrada nesta página.")
