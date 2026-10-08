"""
executar_tudo.py

Roda o pipeline completo, na ordem:
  1. Gera o arquivo de exemplo (PDF ou TXT, dados fictícios)
  2. Popula o banco SQLite (aplica o validador mock)
  3. Gera Excel por plataforma + relatório estatístico + CSV completo

Uso:
  python3 executar_tudo.py          # usa PDF como fonte
  python3 executar_tudo.py txt      # usa TXT (formato email:senha) como fonte
"""

import subprocess
import sys

fonte = sys.argv[1] if len(sys.argv) > 1 else "pdf"

if fonte == "txt":
    PASSOS = [
        ["01b_gerar_txt_exemplo.py"],
        ["04_popular_banco.py", "txt"],
        ["05_relatorios_e_exportacao.py"],
    ]
else:
    PASSOS = [
        ["01_gerar_pdf_exemplo.py"],
        ["04_popular_banco.py", "pdf"],
        ["05_relatorios_e_exportacao.py"],
    ]

for comando in PASSOS:
    print(f"\n=== Executando {' '.join(comando)} ===")
    resultado = subprocess.run([sys.executable, *comando])
    if resultado.returncode != 0:
        print(f"Erro ao executar {comando[0]}, abortando.")
        sys.exit(1)

print("\nPipeline completo executado com sucesso.")
print("Veja: data/, db/, reports/ e exports/")
