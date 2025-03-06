from src.validators import validar_documento, validar_nome, validar_data, validar_endereco

def test_validar_documento():
    assert validar_documento("12345678901") == (True, "")
    assert validar_documento("1234567890") == (False, "Documento deve ter 11 ou 14 dígitos.")
    assert validar_documento("12345678901234") == (False, "Documento deve ter 11 ou 14 dígitos.")
    assert validar_documento("") == (False, "Documento não pode ser vazio.")

def test_validar_nome():
    assert validar_nome("João da Silva") == (True, "")
    assert validar_nome("") == (False, "Nome não pode ser vazio.")

def test_validar_data():
    assert validar_data("01/01/2000") == (True, "")
    assert validar_data("31/02/2000") == (False, "Data inválida.")
    assert validar_data("") == (False, "Data não pode ser vazia.")

def test_validar_endereco():
    assert validar_endereco("Rua das Flores, 123") == (True, "")
    assert validar_endereco("") == (False, "Endereço não pode ser vazio.")