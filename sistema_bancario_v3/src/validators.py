import re
from datetime import datetime


def validar_documento(documento):
    if not documento:
        return False, "Documento não pode ser vazio."

    if len(documento) < 11:
        return False, "Documento deve ter pelo menos 11 caracteres."

    if len(documento) > 14:
        return False, "Documento deve ter no máximo 14 caracteres."

    return True, ""


def validar_nome(nome):
    if not nome:
        return False, "Nome não pode ser vazio."

    return True, ""


def validar_data(data):
    if not data:
        return False, "Data não pode ser vazia."

    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        return False, "Data deve estar no formato dd/mm/aaaa."

    return True, ""


def validar_endereco(endereco):
    if not endereco:
        return False, "Endereço não pode ser vazio."

    return True, ""


def validar_numero_conta(numero):
    if not re.match(r"^\d{3}/\d$", numero):
        return False, "Número da conta deve estar no formato XXX/X."

    return True, ""
