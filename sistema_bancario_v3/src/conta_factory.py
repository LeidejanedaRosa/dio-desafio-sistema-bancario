from datetime import datetime
from src.cliente import Cliente
from src.utils import encontrar_usuario
from src.conta import Conta
from src.tipo_conta import (
    ContaConjunta,
    ContaCorrente,
    ContaJuridicaCorrente,
    ContaJuridicaPoupanca,
    ContaMenorIdade,
    ContaPoupanca,
    ContaSalario,
    ContaUniversitaria,
)
from src.transacao import Deposito


class ContaFactory:
    @staticmethod
    def criar_conta(usuarios):
        documento = ContaFactory._obter_documento_usuario()
        usuario = encontrar_usuario(usuarios, documento)

        if not usuario:
            print("\n 🔔 Usuário não encontrado! Cadastre-o primeiro.\n")
            return

        if not ContaFactory._validar_idade_usuario(usuario):
            responsavel = ContaFactory._obter_responsavel(documento, usuario)
            if not ContaFactory.verificar_usuario_possui_conta_ativa(responsavel):
                print(
                    "\n❌ Responsável não possui conta ativa! Precisa abrir uma conta primeiro.\n"
                )
                return
            print("\nResponsável encontrado. Continuando...\n")

        tipo_conta = ContaFactory._selecionar_tipo_conta(usuario)
        if not tipo_conta:
            return

        co_titular = None
        if tipo_conta == "5":  # Conta Conjunta
            co_titular = ContaFactory._obter_co_titular(documento, usuarios)
            if not co_titular:
                return

        conta = ContaFactory._criar_instancia_conta(tipo_conta, usuario, co_titular)
        if not conta:
            return

        ContaFactory._realizar_deposito_inicial(conta)
        Conta.contas.append(conta)
        Cliente.adicionar_conta(usuario, conta)
        if tipo_conta == "5":  # Conta Conjunta
            Cliente.adicionar_conta(co_titular, conta)

        print("\n✅ Conta criada com sucesso!\n")

    @staticmethod
    def _validar_idade_usuario(usuario):
        data_nascimento = datetime.strptime(usuario["data_nascimento"], "%d/%m/%Y")
        idade = (datetime.now() - data_nascimento).days // 365
        if idade < 18:
            print("\n🔔 Usuário menor de idade. Informe o responsável...\n")
            return False
        return True

    @staticmethod
    def _obter_documento_usuario():
        return input("Digite o CPF ou CNPJ do usuário: ")

    @staticmethod
    def _selecionar_tipo_conta(usuario):
        tipos_conta = ContaFactory._obter_tipos_conta(usuario)

        # Remover tipos de conta que o usuário já possui
        contas_usuario = [
            conta._numero_conta.split("/")[1]
            for conta in Conta.contas
            if conta._cliente == usuario
        ]
        tipos_conta = {
            key: value
            for key, value in tipos_conta.items()
            if key not in contas_usuario
        }

        if not tipos_conta:
            print("\n❌ Usuário já possui todas as contas possíveis.\n")
            return None

        print("\nSelecione o tipo de conta:")
        for key, value in tipos_conta.items():
            print(f"[{key}] - {value}")

        tipo_conta = input("\nDigite o número da opção desejada: ")
        if tipo_conta not in tipos_conta:
            print("\n❌ Tipo de conta inválido! Tente novamente.\n")
            return None

        return tipo_conta

    @staticmethod
    def _obter_tipos_conta(usuario):
        if "cpf" in usuario:
            data_nascimento = datetime.strptime(
                usuario["data_nascimento"], "%d/%m/%Y"
            )  # noqa
            idade = (datetime.now() - data_nascimento).days // 365

            if idade < 18:
                return {"6": "Pessoa Física - Conta Menor de Idade"}
            else:
                return {
                    "1": "Pessoa Física - Corrente",
                    "2": "Pessoa Física - Poupança",
                    "3": "Pessoa Física - Universitária",
                    "4": "Pessoa Física - Conta Salário",
                    "5": "Pessoa Física - Conta Conjunta",
                }
        else:
            return {
                "7": "Jurídica - Corrente",
                "8": "Jurídica - Poupança",
            }

    @staticmethod
    def verificar_usuario_possui_conta_ativa(usuario):
        for conta in Conta.contas:
            if conta._cliente == usuario and conta.verificar_conta_ativa():
                return True
        print(
            f"\n❌ {usuario['tipo_usuario'].capitalize()} não possui conta ativa!\n"  # noqa
        )  # noqa
        return False

    @staticmethod
    def _obter_usuario(tipo_usuario, documento, usuarios):
        usuario_documento = input(f"Digite o CPF do {tipo_usuario}: ")
        return encontrar_usuario(usuarios, usuario_documento)

    @staticmethod
    def _validar_usuario_diferente_titular(usuario_documento, documento, tipo_usuario):
        if usuario_documento == documento:
            print(f"\n❌ O {tipo_usuario} não pode ser o mesmo que o titular!\n")
            return False
        return True

    @staticmethod
    def _obter_co_titular(documento, usuarios):
        return ContaFactory._obter_usuario("cônjuge", documento, usuarios)

    @staticmethod
    def _obter_responsavel(documento, usuarios):
        return ContaFactory._obter_usuario("responsável", documento, usuarios)

    @staticmethod
    def _criar_instancia_conta(tipo_conta, usuario, co_titular=None):
        novo_numero_conta = ContaFactory._gerar_numero_conta()
        numero_conta_formatado = ContaFactory._formatar_numero_conta(
            tipo_conta, novo_numero_conta
        )

        conta_classes = {
            "1": ContaCorrente,
            "2": ContaPoupanca,
            "3": ContaUniversitaria,
            "4": ContaSalario,
            "5": ContaConjunta,
            "6": ContaMenorIdade,
            "7": ContaJuridicaCorrente,
            "8": ContaJuridicaPoupanca,
        }

        instancia_conta = conta_classes.get(tipo_conta)
        if instancia_conta is None:
            print("\n❌ Tipo de conta inválido! Tente novamente.\n")
            return None

        return instancia_conta(usuario, numero_conta_formatado, co_titular=co_titular)

    @staticmethod
    def _realizar_deposito_inicial(conta):
        valor_deposito_inicial = conta.deposito_inicial()

        if valor_deposito_inicial == 0:
            return

        print(
            f"\n 🔔 Para que a conta criada possa ser ativada é necessário um depósito inicial de R$ {valor_deposito_inicial:.2f} \n"  # noqa
        )

        while True:
            valor_deposito = float(
                input("-> Digite o valor do depósito inicial: R$ ")
            )  # noqa
            if valor_deposito >= valor_deposito_inicial:
                conta.depositar(valor_deposito)
                transacao = Deposito(valor_deposito)
                transacao.registrar(conta)
                break
            else:
                print(
                    f"\n❌ O valor do depósito inicial deve ser de pelo menos R$ {valor_deposito_inicial:.2f}!\n"  # noqa
                )

    @staticmethod
    def _gerar_numero_conta():
        nova_conta = int(Conta.ultima_conta_criada) + 1
        Conta.ultima_conta_criada = str(nova_conta).zfill(3)
        return Conta.ultima_conta_criada

    @staticmethod
    def _formatar_numero_conta(tipo_conta: str, numero_conta: str):
        return f"{numero_conta}/{tipo_conta}"
