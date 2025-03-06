from datetime import datetime
from abc import ABC, abstractmethod


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            conta.historico.adicionar_transacao(
                f"{data_hora} + R$ {self.valor:.2f}"
            )  # noqa


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            conta.historico.adicionar_transacao(
                f"{data_hora} - R$ {self.valor:.2f}"
            )  # noqa
