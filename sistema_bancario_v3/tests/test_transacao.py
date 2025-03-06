from src.transacao import Deposito, Saque
from src.conta import Conta
import pytest

@pytest.fixture
def conta():
    return Conta(cliente={"nome": "Test User", "cpf": "12345678901"}, numero_conta="001/1")

def test_deposito_registrar(conta):
    deposito = Deposito(100)
    deposito.registrar(conta)
    assert conta.saldo == 100
    assert len(conta.historico.transacoes) == 1
    assert " + R$ 100.00" in conta.historico.transacoes[0]

def test_saque_registrar(conta):
    deposito = Deposito(200)
    deposito.registrar(conta)
    saque = Saque(100)
    saque.registrar(conta)
    assert conta.saldo == 100
    assert len(conta.historico.transacoes) == 2
    assert " - R$ 100.00" in conta.historico.transacoes[1]

def test_saque_insuficiente(conta):
    saque = Saque(100)
    saque.registrar(conta)
    assert conta.saldo == 0
    assert len(conta.historico.transacoes) == 0  # No transaction should be recorded

def test_deposito_negativo(conta):
    deposito = Deposito(-50)
    deposito.registrar(conta)
    assert conta.saldo == 0
    assert len(conta.historico.transacoes) == 0  # No transaction should be recorded