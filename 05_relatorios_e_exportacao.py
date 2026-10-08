"""
05_relatorios_e_exportacao.py

1) Lê o banco SQLite com todos os registros.
2) Gera uma planilha Excel (reports/credenciais_por_plataforma.xlsx)
   com UMA ABA PARA CADA PLATAFORMA, contendo apenas as credenciais
   cujo status_mock == 'ativo'.
3) Gera um relatório estatístico (taxa de "sucesso" do mock por
   plataforma) em reports/relatorio_estatistico.csv
4) Exporta o dump completo da tabela em exports/credenciais_completo.csv
"""

import sqlite3
import pandas as pd

DB_PATH = "db/cadastros.db"
XLSX_PATH = "reports/credenciais_por_plataforma.xlsx"
RELATORIO_CSV = "reports/relatorio_estatistico.csv"
EXPORT_CSV = "exports/credenciais_completo.csv"


def carregar_dataframe():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT p.nome AS plataforma, c.email, c.senha_teste, c.status_mock,
               c.status_esperado, c.criado_em
        FROM credenciais c
        JOIN plataformas p ON c.plataforma_id = p.id
        ORDER BY p.nome, c.email
    """, conn)
    conn.close()
    return df


def gerar_excel_por_plataforma(df: pd.DataFrame):
    with pd.ExcelWriter(XLSX_PATH, engine="openpyxl") as writer:
        for plataforma, grupo in df.groupby("plataforma"):
            ativos = grupo[grupo["status_mock"] == "ativo"]
            # Nome de aba no Excel tem limite de 31 caracteres
            nome_aba = plataforma[:31]
            if ativos.empty:
                ativos = pd.DataFrame(
                    [["(nenhuma credencial 'ativa' nesta plataforma)"]],
                    columns=["aviso"]
                )
            ativos.to_excel(writer, sheet_name=nome_aba, index=False)
    print(f"Excel com abas por plataforma gerado em: {XLSX_PATH}")


def gerar_relatorio_estatistico(df: pd.DataFrame):
    resumo = (
        df.groupby("plataforma")["status_mock"]
        .value_counts()
        .unstack(fill_value=0)
    )
    resumo["total"] = resumo.sum(axis=1)
    if "ativo" not in resumo:
        resumo["ativo"] = 0
    if "inativo" not in resumo:
        resumo["inativo"] = 0
    resumo["taxa_ativo_%"] = (resumo["ativo"] / resumo["total"] * 100).round(1)

    resumo = resumo.reset_index()[["plataforma", "total", "ativo", "inativo", "taxa_ativo_%"]]
    resumo.to_csv(RELATORIO_CSV, index=False, encoding="utf-8-sig")
    print(f"Relatório estatístico gerado em: {RELATORIO_CSV}")
    print(resumo.to_string(index=False))
    return resumo


def exportar_csv_completo(df: pd.DataFrame):
    df.to_csv(EXPORT_CSV, index=False, encoding="utf-8-sig")
    print(f"Export completo (CSV) gerado em: {EXPORT_CSV}")


if __name__ == "__main__":
    df = carregar_dataframe()
    gerar_excel_por_plataforma(df)
    gerar_relatorio_estatistico(df)
    exportar_csv_completo(df)
