"""
02_ler_pdf.py

Lê o PDF gerado em 01_gerar_pdf_exemplo.py e extrai os registros da
tabela (plataforma, email, senha de teste, status esperado).

Retorna uma lista de dicionários, pronta para ser inserida no banco
SQL no próximo passo.
"""

import pdfplumber

PDF_PATH = "data/cadastros_exemplo.pdf"


def extrair_registros(pdf_path=PDF_PATH):
    registros = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                cabecalho = tabela[0]
                for linha in tabela[1:]:
                    if not linha or len(linha) < 4:
                        continue
                    plataforma, email, senha, status_esperado = linha[:4]
                    registros.append({
                        "plataforma": plataforma.strip(),
                        "email": email.strip(),
                        "senha": senha.strip(),
                        "status_esperado": status_esperado.strip(),
                    })
    return registros


if __name__ == "__main__":
    registros = extrair_registros()
    print(f"Registros extraídos do PDF: {len(registros)}")
    for r in registros[:5]:
        print(r)
    print("...")
