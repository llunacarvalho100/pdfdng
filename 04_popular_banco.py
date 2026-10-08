"""
04_popular_banco.py

Cria o banco SQLite (db/cadastros.db) e insere os registros extraídos
do PDF, já com o resultado do validador mock aplicado.

Schema:
  plataformas(id, nome)
  credenciais(id, plataforma_id, email, senha_teste, status_mock,
              status_esperado, criado_em)
"""

import sys
import sqlite3
from datetime import datetime

from importlib import import_module

ler_pdf = import_module("02_ler_pdf")
ler_txt = import_module("02b_ler_txt")
validador = import_module("03_validador_mock")

DB_PATH = "db/cadastros.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS plataformas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS credenciais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plataforma_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    senha_teste TEXT NOT NULL,
    status_mock TEXT NOT NULL CHECK (status_mock IN ('ativo', 'inativo')),
    status_esperado TEXT,
    criado_em TEXT NOT NULL,
    FOREIGN KEY (plataforma_id) REFERENCES plataformas(id)
);
"""


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def criar_schema(conn):
    conn.executescript(SCHEMA)
    conn.commit()


def obter_ou_criar_plataforma(conn, nome: str) -> int:
    cur = conn.execute("SELECT id FROM plataformas WHERE nome = ?", (nome,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur = conn.execute("INSERT INTO plataformas (nome) VALUES (?)", (nome,))
    conn.commit()
    return cur.lastrowid


def popular(conn, registros):
    agora = datetime.now().isoformat(timespec="seconds")
    for r in registros:
        plataforma_id = obter_ou_criar_plataforma(conn, r["plataforma"])
        status_mock = validador.validar_credencial_mock(r["email"], r["senha"])
        conn.execute(
            """INSERT INTO credenciais
               (plataforma_id, email, senha_teste, status_mock, status_esperado, criado_em)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (plataforma_id, r["email"], r["senha"], status_mock, r["status_esperado"], agora),
        )
    conn.commit()


if __name__ == "__main__":
    # Uso: python3 04_popular_banco.py [pdf|txt]
    fonte = sys.argv[1] if len(sys.argv) > 1 else "pdf"

    if fonte == "txt":
        registros = ler_txt.extrair_registros()
        print("Fonte: arquivo .txt (data/combo_exemplo.txt)")
    else:
        registros = ler_pdf.extrair_registros()
        print("Fonte: arquivo .pdf (data/cadastros_exemplo.pdf)")

    conn = conectar()
    criar_schema(conn)

    # Evita duplicar se rodar o script mais de uma vez
    conn.execute("DELETE FROM credenciais;")
    conn.execute("DELETE FROM plataformas;")
    conn.commit()

    popular(conn, registros)

    total = conn.execute("SELECT COUNT(*) FROM credenciais").fetchone()[0]
    print(f"Banco populado em {DB_PATH} com {total} registros.")
    conn.close()
