# Projeto Demo — Pipeline PDF → SQL → Relatórios (dados fictícios)

Projeto de estudo que demonstra um pipeline completo de dados:

```
PDF de entrada → extração (pdfplumber) → validação (mock) →
banco SQLite → Excel com abas por "plataforma" → relatório
estatístico → exportação CSV
```

## ⚠️ Importante — o que este projeto NÃO faz

Este projeto **não realiza nenhuma tentativa de login real** em
nenhum serviço (streaming, email, etc.) e **não contém nenhuma
credencial real de ninguém**. Todos os dados são gerados
sinteticamente (domínio fictício `@exemplo.test`).

O "validador" em `03_validador_mock.py` é **100% local e offline**:
ele só checa regras simples de formato de senha (tamanho, dígito,
caractere especial) para simular um resultado de "ativo/inativo" e
gerar variação nos dados — nenhuma requisição de rede é feita.

Testar credenciais reais (obtidas de vazamentos ou qualquer outra
fonte) contra contas de terceiros em serviços reais é **crime**
(acesso indevido/invasão de dispositivo informático, Lei
12.737/2012 no Brasil, entre outras) e viola os termos de uso de
qualquer plataforma. Se você quiser adaptar este projeto para um
cenário real, o único uso legítimo é testar **suas próprias**
contas em **seus próprios** sistemas de homologação, com
autorização explícita.

## Estrutura

```
projeto-demo/
├── 01_gerar_pdf_exemplo.py       # Gera PDF fictício de entrada
├── 01b_gerar_txt_exemplo.py      # Gera TXT fictício (formato email:senha)
├── 02_ler_pdf.py                 # Extrai registros do PDF
├── 02b_ler_txt.py                # Extrai registros do TXT (email:senha)
├── 03_validador_mock.py          # Validação local de formato (sem rede)
├── 04_popular_banco.py           # Cria/popula o banco SQLite (aceita pdf|txt)
├── 05_relatorios_e_exportacao.py # Gera Excel por aba + relatório + CSV
├── executar_tudo.py              # Roda o pipeline completo (aceita pdf|txt)
├── data/        -> arquivo de entrada (PDF ou TXT)
├── db/          -> banco SQLite (cadastros.db)
├── reports/     -> Excel por plataforma + relatório estatístico (CSV)
└── exports/     -> dump completo em CSV
```

## Como rodar

```bash
pip install reportlab pdfplumber pandas openpyxl

# usando PDF como fonte
python3 executar_tudo.py

# usando TXT (formato email:senha, uma credencial por linha) como fonte
python3 executar_tudo.py txt
```

O formato `.txt` suportado é o clássico `email:senha` por linha —
o mesmo formato de "combo lists" que circulam por aí, mas aqui
sempre gerado com dados fictícios localmente (nunca listas reais
obtidas de vazamentos ou de terceiros).

## Schema do banco (SQLite)

```sql
plataformas(id, nome)
credenciais(id, plataforma_id, email, senha_teste,
            status_mock, status_esperado, criado_em)
```

## Saídas geradas

- `reports/credenciais_por_plataforma.xlsx` — uma aba por
  plataforma, listando apenas os registros com `status_mock = 'ativo'`
- `reports/relatorio_estatistico.csv` — total, ativos, inativos e
  taxa de "ativo" (%) por plataforma
- `exports/credenciais_completo.csv` — dump completo da tabela

## Ideias para evoluir o estudo

- Trocar o SQLite por PostgreSQL/MySQL
- Adicionar índices e testar performance de consulta
- Criar um dashboard (ex. com `streamlit`) em cima do banco
- Adicionar testes automatizados (`pytest`) para cada módulo
- Substituir o validador mock por uma chamada real à **sua própria**
  API de autenticação de homologação (nunca a serviços de terceiros)
