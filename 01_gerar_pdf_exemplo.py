"""
01_gerar_pdf_exemplo.py

Gera um PDF de EXEMPLO contendo uma lista de cadastros FICTÍCIOS
(email, senha de teste, plataforma, status esperado).

IMPORTANTE:
- Todos os dados aqui são inventados (domínio @exemplo.test, que nem
  existe na internet) só para termos um arquivo de entrada para o
  pipeline de estudo.
- Em um cenário real de uso legítimo, este PDF representaria, por
  exemplo, uma planilha de QA interna de UMA empresa testando SUAS
  PRÓPRIAS contas de homologação em SEUS PRÓPRIOS sistemas — nunca
  credenciais de terceiros obtidas sem autorização.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import random

OUTPUT_PATH = "data/cadastros_exemplo.pdf"

PLATAFORMAS = ["StreamFlix (fake)", "MusicWave (fake)", "CloudDocs (fake)", "GameHub (fake)"]

random.seed(42)

def gerar_senha_variada(i: int) -> str:
    """Gera senhas fictícias com padrões variados, para que o mock
    de validação produza uma mistura realista de 'ativo'/'inativo'."""
    padroes = [
        f"SenhaTeste{i:03d}!",   # forte: >=10 chars, dígito, especial
        f"senha{i}",             # fraca: curta, sem especial
        f"abcdefgh{i}",          # média-fraca: sem especial
        f"Pw{i}!",                # curta com especial, mas <10 chars
        f"SegurancaForte{i:03d}#",  # forte
        f"{i}{i}{i}",            # bem fraca
    ]
    return random.choice(padroes)


def gerar_registros(qtd=40):
    registros = []
    for i in range(1, qtd + 1):
        plataforma = random.choice(PLATAFORMAS)
        email = f"usuario{i:03d}@exemplo.test"
        senha = gerar_senha_variada(i)
        # "status_esperado" simula se, no nosso mock, essa credencial
        # fictícia deveria passar na validação de formato ou não.
        status_esperado = random.choice(["válida", "válida", "inválida"])
        registros.append((plataforma, email, senha, status_esperado))
    return registros


def montar_pdf(registros):
    doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=A4,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatório de Cadastros de Teste (DADOS FICTÍCIOS)", styles["Title"]))
    elementos.append(Paragraph(
        "Este documento contém exclusivamente dados inventados para fins de "
        "estudo de um pipeline PDF → SQL → Relatórios. Nenhuma credencial "
        "real está presente.", styles["Normal"]))
    elementos.append(Spacer(1, 1*cm))

    dados_tabela = [["Plataforma", "Email", "Senha (teste)", "Status esperado"]]
    for p, e, s, st in registros:
        dados_tabela.append([p, e, s, st])

    tabela = Table(dados_tabela, repeatRows=1, colWidths=[5*cm, 6*cm, 4.5*cm, 3*cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    elementos.append(tabela)

    doc.build(elementos)
    print(f"PDF de exemplo gerado em: {OUTPUT_PATH} ({len(registros)} registros fictícios)")


if __name__ == "__main__":
    registros = gerar_registros(40)
    montar_pdf(registros)
