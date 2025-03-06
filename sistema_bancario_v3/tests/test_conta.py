from src.conta import Conta, ContaCorrente, ContaPoupanca, ContaUniversitaria, ContaSalario, ContaConjunta, ContaMenorIdade, ContaJuridicaCorrente, ContaJuridicaPoupanca

def test_depositar():
    conta = ContaCorrente(cliente={"nome": "Test User", "cpf": "12345678901"}, numero_conta="001/1")
    conta.depositar(100)
    assert conta.saldo == 100

def test_sacar():
    conta = ContaPoupanca(cliente={"nome": "Test User", "cpf": "12345678901"}, numero_conta="002/2")
    conta.depositar(100)
    conta.sacar(50)
    assert conta.saldo == 50

def test_sacar_saldo_insuficiente():
    conta = ContaUniversitaria(cliente={"nome": "Test User", "cpf": "12345678901"}, numero_conta="003/3")
    conta.depositar(30)
    resultado = conta.sacar(50)
    assert resultado is False
    assert conta.saldo == 30

def test_exibir_extrato():
    conta = ContaSalario(cliente={"nome": "Test User", "cpf": "12345678901"}, numero_conta="004/4")
    conta.depositar(200)
    conta.sacar(100)
    extrato = conta.exibir_extrato()
    assert "Extrato de Transações" in extrato
    assert "R$ 200.00" in extrato
    assert "R$ 100.00" in extrato

def test_encerrar_conta():
    conta = ContaConjunta(cliente={"nome": "Test User", "cpf": "12345678901"}, numero_conta="005/5")
    conta.encerrar_conta()
    assert conta.data_encerramento is not None

def test_criar_conta_juridica():
    conta = ContaJuridicaCorrente(cliente={"nome": "Test Company", "cnpj": "12345678000195"}, numero_conta="006/6")
    conta.depositar(500)
    assert conta.saldo == 500

def test_criar_conta_juridica_poupanca():
    conta = ContaJuridicaPoupanca(cliente={"nome": "Test Company", "cnpj": "12345678000195"}, numero_conta="007/7")
    conta.depositar(300)
    assert conta.saldo == 300