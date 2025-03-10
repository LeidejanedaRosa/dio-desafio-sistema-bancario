from src.conta import Conta


class ContaCorrente(Conta):
    def __init__(
        self,
        cliente,
        numero_conta,
        agencia="0001",
        limite=1500,
        limite_saques=3,
        senha=None,
    ):
        super().__init__(
            cliente,
            numero_conta,
            agencia,
            limite=limite,
            limite_saques=limite_saques,  # noqa
        )
        self._senha = senha

    def deposito_inicial(self):
        return 100

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cpf = self._cliente.get("cpf", None)
        return f"Cliente: {cliente_cpf}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class ContaPoupanca(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001", senha=None):
        super().__init__(cliente, numero_conta, agencia)
        self._senha = senha

    def deposito_inicial(self):
        return 50

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cpf = self._cliente.get("cpf", None)
        return f"Cliente: {cliente_cpf}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class ContaUniversitaria(Conta):
    def __init__(
        self, cliente, numero_conta, agencia="0001", limite=500, senha=None
    ):  # noqa
        super().__init__(cliente, numero_conta, agencia, limite=limite)
        self._senha = senha

    def deposito_inicial(self):
        return 20

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cpf = self._cliente.get("cpf", None)
        return f"Cliente: {cliente_cpf}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class ContaSalario(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001", senha=None):
        super().__init__(cliente, numero_conta, agencia)
        self._senha = senha

    def deposito_inicial(self):
        return 0

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cpf = self._cliente.get("cpf", None)
        return f"Cliente: {cliente_cpf}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class ContaConjunta(Conta):
    def __init__(
        self, cliente, numero_conta, agencia="0001", co_titular=None, senha=None  # noqa
    ):
        super().__init__(cliente, numero_conta, agencia, co_titular=co_titular)
        self._co_titular = co_titular
        self._senha = senha

    def deposito_inicial(self):
        return 100

    @property
    def co_titular(self):
        return self._co_titular

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cpf = self._cliente.get("cpf", None)
        co_titular_cpf = (
            self._co_titular.get("cpf", None) if self._co_titular else None
        )  # noqa
        return f"Cliente: {cliente_cpf}, Co-titular: {co_titular_cpf}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class ContaMenorIdade(Conta):
    def __init__(
        self,
        cliente,
        numero_conta,
        agencia="0001",
        responsavel=None,
        senha=None,  # noqa
    ):
        super().__init__(cliente, numero_conta, agencia)
        self._responsavel = responsavel
        self._senha = senha

    def deposito_inicial(self):
        return 10

    @property
    def responsavel(self):
        return self._responsavel

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cpf = self._cliente.get("cpf", None)
        responsavel_cpf = (
            self._responsavel.get("cpf", None) if self._responsavel else None
        )
        return f"Cliente: {cliente_cpf}, Responsável: {responsavel_cpf}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class ContaJuridicaCorrente(Conta):
    def __init__(
        self, cliente, numero_conta, agencia="0001", limite=1000, senha=None
    ):  # noqa
        super().__init__(cliente, numero_conta, agencia, limite=limite)
        self._senha = senha

    def deposito_inicial(self):
        return 200

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cnpj = self._cliente.get("cnpj", None)
        return f"Cliente: {cliente_cnpj}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class ContaJuridicaPoupanca(Conta):
    def __init__(self, cliente, numero_conta, agencia="0001", senha=None):
        super().__init__(cliente, numero_conta, agencia)
        self._senha = senha

    def deposito_inicial(self):
        return 150

    def get_senha(self, autorizado=False):
        if autorizado:
            return self._senha
        return "Acesso negado"

    def __str__(self):
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        cliente_cnpj = self._cliente.get("cnpj", None)
        return f"Cliente: {cliente_cnpj}, Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa
