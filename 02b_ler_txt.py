"""
02b_ler_txt.py

Lê um arquivo .txt no formato "email:senha" (uma credencial por
linha) e retorna uma lista de dicionários, no mesmo formato usado
pelo restante do pipeline (plataforma, email, senha, status_esperado).

A "plataforma" é derivada do nome do arquivo (ex.:
"combo_exemplo.txt" -> "combo_exemplo"), só para fins de
organização nos relatórios.
"""

import os

TXT_PATH = "data/combo_exemplo.txt"


def extrair_registros(txt_path=TXT_PATH):
    nome_base = os.path.splitext(os.path.basename(txt_path))[0]
    registros = []
    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or ":" not in linha:
                continue
            email, _, senha = linha.partition(":")
            email = email.strip()
            senha = senha.strip()
            if not email or not senha:
                continue
            registros.append({
                "plataforma": nome_base,
                "email": email,
                "senha": senha,
                "status_esperado": None,  # não aplicável para .txt
            })
    return registros


if __name__ == "__main__":
    registros = extrair_registros()
    print(f"Registros extraídos do TXT: {len(registros)}")
    for r in registros[:5]:
        print(r)
    print("...")
