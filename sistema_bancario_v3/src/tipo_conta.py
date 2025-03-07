from src.conta import Conta


class ContaCorrente(Conta):
    def __init__(
        self,
        cliente,
        numero_conta,
        agencia="0001",
        limite=1500,
        limite_saques=3,
    ):
        super().__init__(cliente, numero_conta, agencia)
        self._limite = limite
        self._limite_saques = limite_saques

    def deposito_inicial(self):
        return 100


class ContaPoupanca(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001"):
        super().__init__(cliente, numero_conta, agencia)

    def deposito_inicial(self):
        return 50


class ContaUniversitaria(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001", limite=500):
        super().__init__(cliente, numero_conta, agencia)
        self._limite = limite

    def deposito_inicial(self):
        return 20


class ContaSalario(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001"):
        super().__init__(cliente, numero_conta, agencia)

    def deposito_inicial(self):
        return 0


class ContaConjunta(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001", co_titular=None):
        super().__init__(cliente, numero_conta, agencia, co_titular=co_titular)
        self._co_titular = co_titular

    def deposito_inicial(self):
        return 100

    @property
    def co_titular(self):
        return self._co_titular


class ContaMenorIdade(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001", responsavel=None):  # noqa
        super().__init__(cliente, numero_conta, agencia)
        self._responsavel = responsavel

    def deposito_inicial(self):
        return 10

    @property
    def responsavel(self):
        return self._responsavel


class ContaJuridicaCorrente(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001", limite=1000):
        super().__init__(cliente, numero_conta, agencia)
        self._limite = limite

    def deposito_inicial(self):
        return 200


class ContaJuridicaPoupanca(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001"):
        super().__init__(cliente, numero_conta, agencia)

    def deposito_inicial(self):
        return 150
