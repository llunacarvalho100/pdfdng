"""
01b_gerar_txt_exemplo.py

Gera um arquivo .txt de EXEMPLO no formato "email:senha" por linha,
que é o formato comum de listas de credenciais (combo lists).

IMPORTANTE:
- Todos os dados são FICTÍCIOS (domínio @exemplo.test).
- Isto serve só para termos um arquivo de entrada no mesmo FORMATO
  de um combo list real, sem usar nenhuma credencial real de
  ninguém. O objetivo é estudar o pipeline de parsing de texto,
  não testar login em serviço nenhum.
"""

import random

OUTPUT_PATH = "data/combo_exemplo.txt"

random.seed(7)


def gerar_senha_variada(i: int) -> str:
    padroes = [
        f"SenhaTeste{i:03d}!",
        f"senha{i}",
        f"abcdefgh{i}",
        f"Pw{i}!",
        f"SegurancaForte{i:03d}#",
        f"{i}{i}{i}",
    ]
    return random.choice(padroes)


def gerar_linhas(qtd=50):
    linhas = []
    for i in range(1, qtd + 1):
        email = f"usuario{i:03d}@exemplo.test"
        senha = gerar_senha_variada(i)
        linhas.append(f"{email}:{senha}")
    return linhas


if __name__ == "__main__":
    linhas = gerar_linhas(50)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"Arquivo .txt de exemplo gerado em: {OUTPUT_PATH} ({len(linhas)} linhas fictícias)")
