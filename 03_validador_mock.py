"""
03_validador_mock.py

MOCK de validação de credenciais.

ATENÇÃO — ISTO NÃO TENTA LOGIN EM NENHUM SERVIÇO REAL.
Não há nenhuma chamada de rede aqui. O objetivo é apenas simular,
de forma determinística, o resultado de uma verificação de "login
ativo" para que o pipeline de estudo (PDF -> SQL -> Relatórios)
tenha dados de status para trabalhar.

Regra do mock (inventada, só para gerar variação nos dados):
  - senha é considerada "válida" se tiver >= 10 caracteres,
    pelo menos 1 dígito e pelo menos 1 caractere especial.
  - caso contrário, "inválida".

Em um projeto real e legítimo, este módulo seria substituído por
chamadas à SUA PRÓPRIA API de autenticação (ex.: ambiente de
homologação da sua empresa), nunca a serviços de terceiros sem
autorização explícita.
"""

import re


def validar_credencial_mock(email: str, senha: str) -> str:
    tem_tamanho = len(senha) >= 10
    tem_digito = re.search(r"\d", senha) is not None
    tem_especial = re.search(r"[^\w\s]", senha) is not None

    if tem_tamanho and tem_digito and tem_especial:
        return "ativo"
    return "inativo"


if __name__ == "__main__":
    exemplos = [
        ("a@exemplo.test", "SenhaTeste001!"),
        ("b@exemplo.test", "123"),
    ]
    for email, senha in exemplos:
        print(email, "->", validar_credencial_mock(email, senha))
