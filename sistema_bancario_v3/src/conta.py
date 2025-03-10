from typing import List
from datetime import datetime
from abc import ABC, abstractmethod

from src.validadores import validar_numero_conta
from src.transacao import Historico


class Conta(ABC):
    ultima_conta_criada = "000"
    contas: List["Conta"] = []

    def __init__(
        self,
        cliente,
        numero_conta,
        agencia="0001",
        historico=None,
        co_titular=None,
        responsavel=None,
        limite=0,
        limite_saques=0,
    ):
        self._saldo = 0
        self._cliente = cliente
        self._numero_conta = numero_conta
        self._agencia = agencia
        self._historico = historico if historico else Historico()
        self._data_encerramento = None
        self._co_titular = co_titular
        self._responsavel = responsavel
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def historico(self):
        return self._historico

    @property
    def saldo(self):
        return self._saldo

    @property
    def data_encerramento(self):
        return self._data_encerramento

    def verificar_conta_ativa(self):
        if self._data_encerramento:
            print(
                "\n❌ Esta conta está encerrada e não pode realizar operações.\n"  # noqa
            )  # noqa
            return False
        return True

    def validar_senha(self, conta, senha):
        conta_corrente = conta._cliente["contas"][0]  # Obtém a conta

        return conta_corrente.get_senha(autorizado=True) == senha

    def exibir_saldo(self):
        if not self.verificar_conta_ativa():
            return

        print(f"\n 🔔 Saldo: R$ {self.saldo:.2f}\n")

    def contar_saques_diarios(self):
        hoje = datetime.now().strftime("%d/%m/%Y")
        saques_hoje = [
            transacao
            for transacao in self._historico.transacoes
            if "-" in transacao and hoje in transacao
        ]
        return len(saques_hoje)

    def verificar_limites(self, valor_saque) -> bool:
        print("self._limite_saques", self._limite_saques)
        print("self._limite", self._limite)
        if (
            self._limite_saques > 0
            and self.contar_saques_diarios() >= self._limite_saques
        ):
            print("\n❌ Limite de saques diários atingido\n")
            return False
        if self._limite > 0 and valor_saque > self._limite:
            print("\n❌ Valor do saque excede o limite permitido\n")
            return False
        return True

    def sacar(self, valor):
        if not self.verificar_conta_ativa():
            return

        if not self.verificar_limites(valor):
            return

        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            print(f"\n ✅ Saque de R$ {valor:.2f} realizado com sucesso! \n")
            return True
        else:
            print("\n❌ Saldo insuficiente para realizar o saque.\n")
        return False

    @abstractmethod
    def deposito_inicial(self) -> float:
        pass

    def depositar(self, valor):
        if not self.verificar_conta_ativa():
            return

        if valor > 0:
            self._saldo += valor
            print(f"\n✅ Depósito de R$ {valor:.2f} realizado com sucesso!\n")
            return True
        return False

    def exibir_extrato(self):
        if not self.verificar_conta_ativa():
            return

        print("\n📋 Extrato de Transações 📋\n")
        if not self._historico.transacoes:
            print("🔔 Nenhuma transação realizada.")
        else:
            print(f"Agência: {self._agencia}, Conta: {self._numero_conta}\n")
            for transacao in self._historico.transacoes:
                print(transacao)
        print(f"\n🔔 Saldo Atual: R$ {self.saldo:.2f}\n")

    @classmethod
    def obter_conta(cls):
        numero = input("Digite o número da conta: ")

        valido, mensagem = validar_numero_conta(numero)
        if not valido:
            print(f"\n{mensagem}\n")
            return None

        conta = next((c for c in cls.contas if c._numero_conta == numero), None)  # noqa
        if not conta:
            print("\n❌ Conta não encontrada!\n")
        return conta

    @classmethod
    def listar_contas(cls):
        if not cls.contas:
            print("\n🔔 Nenhuma conta cadastrada.\n")
            return

        print("\n📋 Contas cadastradas:\n")
        for conta in cls.contas:
            print(conta)

    @classmethod
    def encerrar_conta(cls):
        numero = input("Digite o número da conta a ser encerrada: ")

        valido, mensagem = validar_numero_conta(numero)
        if not valido:
            print(f"\n{mensagem}\n")
            return None

        conta = next((c for c in cls.contas if c._numero_conta == numero), None)  # noqa
        if conta:
            if conta.saldo > 0:
                print(
                    f"\n❌ A conta possui saldo de R$ {conta.saldo:.2f}. Por favor, saque o valor antes de encerrar a conta.\n"  # noqa
                )
                return None

            conta._data_encerramento = datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )  # noqa
            print(
                f"\n 🔔 Conta {numero} encerrada com sucesso em {conta._data_encerramento}! \n"  # noqa
            )
        else:
            print("\n ❌ Conta não encontrada! \n")

    def __str__(self):
        documento = self._cliente.get("cpf") or self._cliente.get("cnpj")
        encerramento = (
            f", Encerrada em: {self._data_encerramento}"
            if self._data_encerramento
            else ""
        )
        co_titular = (
            f"Cônjuge: {self._co_titular['cpf']}," if self._co_titular else ""
        )  # noqa
        responsavel = (
            f"Responsável: {self._responsavel['cpf']},"
            if self._responsavel
            else ""  # noqa
        )  # noqa
        return f"Cliente: {documento}, {co_titular}{responsavel} Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa
