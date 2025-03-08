import re
from datetime import datetime


def validar_documento(documento):
    if not documento:
        return False, "❌ Documento é obrigatório."

    if len(documento) == 11 or len(documento) == 14:
        return True, ""
    else:
        return (
            False,
            "❌ Documento inválido. Deve conter 11 (CPF) ou 14 (CNPJ) dígitos.",
        )


def validar_nome(nome):
    if not nome:
        return False, "❌ Nome não pode ser vazio."

    return True, ""


def validar_data(data, eEdicao=False):
    if eEdicao and not data:
        return True, ""
    elif not data:
        return False, "❌ Data é obrigatória."

    try:
        data_nascimento = datetime.strptime(data, "%d/%m/%Y")
        data_atual = datetime.today()

        # Verifica se a data informada é no futuro
        if data_nascimento > data_atual:
            return False, "❌ Data de nascimento não pode ser no futuro."

    except ValueError:
        return False, "❌ Data deve estar no formato dd/mm/aaaa."

    return True, ""


def validar_endereco(endereco):
    if not endereco:
        return False, "❌ Endereço não pode ser vazio."

    return True, ""


def validar_numero_conta(numero):
    if not re.match(r"^\d{3}/\d$", numero):
        return False, "❌ Número da conta deve estar no formato XXX/X."

    return True, ""
