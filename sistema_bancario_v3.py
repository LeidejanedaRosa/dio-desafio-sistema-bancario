import re
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List


def documento_existe(documento, clientes):
    return any(
        cliente.get("cpf") == documento or cliente.get("cnpj") == documento
        for cliente in clientes
    )


def validar_documento(documento):
    if not documento:
        return False, "❌ O CPF ou CNPJ é obrigatório!"

    if len(documento) < 11:
        return False, "❌ CPF inválido!"
    elif len(documento) > 11 and len(documento) < 14:
        return False, "❌ CNPJ inválido!"

    return True, ""


def validar_nome(nome):
    if not nome:
        return False, "❌ O nome é obrigatório!"
    return True, ""


def validar_data(data):
    if not data:
        return False, "❌ A data é obrigatória!"
    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        return False, "❌ A data deve estar no formato dd/mm/aaaa!"
    return True, ""


def validar_endereco(endereco):
    if not endereco:
        return False, "❌ O endereço é obrigatório!"
    return True, ""


def validar_numero_conta(numero):
    if not re.match(r"^\d{3}/\d$", numero):
        return (
            False,
            "❌ Formato de número de conta inválido! Use o formato xxx/x.",
        )  # noqa
    return True, ""


def obter_documento():
    documento = input(
        "Digite o CPF ou CNPJ do usuário a ser editado (somente números): "
    )
    return documento.replace(".", "").replace("-", "").strip()


def encontrar_usuario(usuarios, documento):
    return next(
        (
            u
            for u in usuarios
            if ("cpf" in u and u["cpf"] == documento)
            or ("cnpj" in u and u["cnpj"] == documento)
        ),  # noqa
        None,
    )


def exibir_dados_usuario(usuario):
    print("\n📋 Dados Atuais do Usuário 📋\n")
    print(f"Nome: {usuario['nome']}")
    if "cpf" in usuario:
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"CPF: {usuario['cpf']}")
    else:
        print(f"Data de Abertura: {usuario['data_abertura']}")
        print(f"CNPJ: {usuario['cnpj']}")
    print(f"Endereço: {usuario['endereco']}\n")


def obter_novos_dados(usuario):
    print(
        "Digite os novos dados do usuário (deixe em branco para manter o valor atual):"  # noqa
    )
    novo_nome = input(f"Nome [{usuario['nome']}]: ").strip()

    data_label = (
        "Data de Nascimento" if "cpf" in usuario else "Data de Abertura"
    )  # noqa
    nova_data = input(
        f"{data_label} [{usuario.get('data_nascimento', usuario.get('data_abertura'))}]: "  # noqa
    ).strip()
    valido, mensagem = validar_data(nova_data)

    while valido is False:
        print(f"\n{mensagem}\n")
        nova_data = input(
            f"{data_label} [{usuario.get('data_nascimento', usuario.get('data_abertura'))}]: "  # noqa
        ).strip()
        valido, mensagem = validar_data(nova_data)

    novo_endereco = input(f"Endereço [{usuario['endereco']}]: ").strip()
    return novo_nome, nova_data, novo_endereco


def atualizar_usuario(usuario, novo_nome, nova_data, novo_endereco):
    if novo_nome:
        usuario["nome"] = novo_nome
    if nova_data:
        if "cpf" in usuario:
            usuario["data_nascimento"] = nova_data
        else:
            usuario["data_abertura"] = nova_data

    if novo_endereco:
        usuario["endereco"] = novo_endereco


def editar_usuario(usuarios):
    documento = obter_documento()
    valido, mensagem = validar_documento(documento)
    if not valido:
        print(f"\n{mensagem}\n")
        return

    usuario = encontrar_usuario(usuarios, documento)
    if not usuario:
        print("\n\n❌ Usuário não encontrado!\n\n")
        return

    exibir_dados_usuario(usuario)
    novo_nome, nova_data, novo_endereco = obter_novos_dados(usuario)
    atualizar_usuario(usuario, novo_nome, nova_data, novo_endereco)
    print("\n\n✅ Dados do usuário atualizados com sucesso!\n\n")


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


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


class Conta(ABC):
    ultima_conta_criada = "000"
    contas: List["Conta"] = []

    def __init__(
        self,
        cliente,
        numero_conta,
        agencia="0001",
        historico=None,
        co_titular=None,  # noqa
    ):
        self._saldo = 0
        self._cliente = cliente
        self._numero_conta = numero_conta
        self._agencia = agencia
        self._historico = historico if historico else Historico()
        self._data_encerramento = None
        self._co_titular = co_titular

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

    def exibir_saldo(self):
        if not self.verificar_conta_ativa():
            return

        print(f"\n 🔔 Saldo: R$ {self.saldo:.2f}\n")

    def sacar(self, valor):
        if not self.verificar_conta_ativa():
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
        return f"Cliente: {documento}, {co_titular} Agência: {self._agencia}, Conta: {self._numero_conta}, Saldo: R$ {self._saldo:.2f}, {encerramento}"  # noqa


class CriarConta:
    @staticmethod
    def criar_conta(usuarios):
        documento = CriarConta._obter_documento_usuario()
        usuario = encontrar_usuario(usuarios, documento)

        if not usuario:
            print("\n 🔔 Usuário não encontrado! Cadastre-o primeiro.\n")
            return

        tipo_conta = CriarConta._selecionar_tipo_conta(usuario)
        co_titular = None

        if tipo_conta == "5":  # Conta Conjunta
            co_titular_documento = input("Digite o CPF do cônjuge: ")

            if co_titular_documento == documento:
                print("\n❌ O cônjuge não pode ser o mesmo que o titular!\n")
                return

            co_titular = encontrar_usuario(usuarios, co_titular_documento)

            if not co_titular:
                print("\n❌ Cônjuge não encontrado! Cadastre-o primeiro.\n")
                return
            conta = CriarConta._criar_instancia_conta(
                tipo_conta, usuario, co_titular
            )  # noqa
        else:
            conta = CriarConta._criar_instancia_conta(tipo_conta, usuario)
        if not conta:
            print("\n❌ Tipo de conta inválido! Tente novamente.\n")
            return

        CriarConta._realizar_deposito_inicial(conta)
        Conta.contas.append(conta)
        Cliente.adicionar_conta(usuario, conta)
        if tipo_conta == "5":  # Conta Conjunta
            Cliente.adicionar_conta(co_titular, conta)

        print("\n✅ Conta criada com sucesso!\n")

    @staticmethod
    def _obter_documento_usuario():
        return input("Digite o CPF ou CNPJ do usuário: ")

    @staticmethod
    def _selecionar_tipo_conta(usuario):
        tipos_conta = {
            "1": "Pessoa Física - Corrente",
            "2": "Pessoa Física - Poupança",
            "3": "Pessoa Física - Universitária",
            "4": "Pessoa Física - Conta Salário",
            "5": "Pessoa Física - Conta Conjunta",
            "6": "Pessoa Física - Conta Menor de Idade",
            "7": "Jurídica - Corrente",
            "8": "Jurídica - Poupança",
        }

        # Verificar idade do usuário se for Pessoa Física
        if "cpf" in usuario:
            data_nascimento = datetime.strptime(
                usuario["data_nascimento"], "%d/%m/%Y"
            )  # noqa
            idade = (datetime.now() - data_nascimento).days // 365

            if idade < 18:
                print("\nUsuário menor de idade. Informe o responsável...\n")
                responsavel = CriarConta._obter_responsavel()
                if not responsavel:
                    print(
                        "\n❌ Nenhum responsável encontrado com conta ativa!\n"
                    )  # noqa
                    return None
                print("\nResponsável encontrado. Continuando...\n")
                tipos_conta = {"6": "Pessoa Física - Conta Menor de Idade"}
            else:
                tipos_conta = {
                    "1": "Pessoa Física - Corrente",
                    "2": "Pessoa Física - Poupança",
                    "3": "Pessoa Física - Universitária",
                    "4": "Pessoa Física - Conta Salário",
                    "5": "Pessoa Física - Conta Conjunta",
                }
        else:
            tipos_conta = {
                "7": "Jurídica - Corrente",
                "8": "Jurídica - Poupança",
            }

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
    def _obter_responsavel():
        documento_responsavel = input("Digite o CPF do responsável: ")
        responsavel = encontrar_usuario(Cliente.clientes, documento_responsavel)  # noqa
        if responsavel:
            conta_responsavel = next(
                (
                    conta
                    for conta in Conta.contas
                    if conta._cliente == responsavel
                    and not conta._data_encerramento  # noqa
                ),
                None,
            )
            if conta_responsavel:
                return responsavel
        return None

    @staticmethod
    def _criar_instancia_conta(tipo_conta, usuario, co_titular=None):
        novo_numero_conta = CriarConta._gerar_numero_conta()
        numero_conta_formatado = CriarConta._formatar_numero_conta(
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

        if tipo_conta == "5":  # Conta Conjunta
            return instancia_conta(
                usuario, numero_conta_formatado, co_titular=co_titular
            )  # noqa
        else:
            return instancia_conta(usuario, numero_conta_formatado)

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


class ContaCorrente(Conta):
    def __init__(
        self,
        cliente,
        numero_conta,
        agencia="0001",
        limite=1500,
        limite_saques=3,  # noqa
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
    def __init__(self, cliente, numero_conta, agencia="0001", responsavel=None):
        super().__init__(cliente, numero_conta, agencia)
        self._responsavel = responsavel

    def deposito_inicial(self):
        return 10


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


class Cliente:
    clientes: list[dict] = []

    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @classmethod
    def adicionar_conta(cls, usuario, conta):
        for cliente in cls.clientes:
            if cliente.get("cpf") == usuario.get("cpf") or cliente.get(
                "cnpj"
            ) == usuario.get("cnpj"):
                if "contas" not in cliente:
                    cliente["contas"] = []
                if conta not in cliente["contas"]:
                    cliente["contas"].append(conta)

    def realizar_transacao(self, conta, transacao: Transacao):
        transacao.registrar(conta)

    @classmethod
    def listar_usuarios(cls):
        if not cls.clientes:
            print("\n 🔔 Nenhum usuário cadastrado.\n")
            return

        print("\n📋 Usuários cadastrados:")

        for usuario in cls.clientes:
            documento_label = "CPF" if "cpf" in usuario else "CNPJ"
            documento = usuario.get("cpf") or usuario.get("cnpj")

            data_label = (
                "Data de Nascimento" if "cpf" in usuario else "Data de Abertura"  # noqa
            )  # noqa
            data = usuario.get("data_nascimento", usuario.get("data_abertura"))

            contas = usuario.get("contas", [])
            contas_str = (
                "\n ".join(str(conta) for conta in contas)
                if contas
                else "Nenhuma conta cadastrada!"
            )

            print(
                f"\n {documento_label}: {documento},\n Nome: {usuario['nome']},\n {data_label}: {data},\n Endereço: {usuario['endereco']}, \n Conta(s): \n {contas_str}"  # noqa
            )

    @classmethod
    def editar_usuario(cls):
        documento = obter_documento()
        valido, mensagem = validar_documento(documento)
        if not valido:
            print(f"\n{mensagem}\n")
            return

        usuario = encontrar_usuario(cls.clientes, documento)
        if not usuario:
            print("\n\n❌ Usuário não encontrado!\n\n")
            return

        exibir_dados_usuario(usuario)
        novo_nome, nova_data, novo_endereco = obter_novos_dados(usuario)
        atualizar_usuario(usuario, novo_nome, nova_data, novo_endereco)
        print("\n\n✅ Dados do usuário atualizados com sucesso!\n\n")

    def __str__(self):
        return f"Clientes: {self.clientes}"


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        Cliente.clientes.append(
            {
                "cpf": cpf,
                "nome": nome,
                "endereco": endereco,
                "data_nascimento": data_nascimento,
            }
        )

    def __str__(self):
        return f"Nome: {self._nome}, CPF: {self._cpf}, Endereço: {self._endereco}, Data de Nascimento: {self._data_nascimento}"  # noqa


class PessoaJuridica(Cliente):
    def __init__(self, cnpj, nome, data_abertura, endereco):
        super().__init__(endereco)
        self._cnpj = cnpj
        self._nome = nome
        self._data_abertura = data_abertura
        Cliente.clientes.append(
            {
                "cnpj": cnpj,
                "nome": nome,
                "endereco": endereco,
                "data_abertura": data_abertura,
            }
        )

    def __str__(self):
        return f"Nome: {self._nome}, CNPJ: {self._cnpj}, Endereço: {self._endereco}, Data de Nascimento: {self._data_abertura}"  # noqa


def menu_principal():
    usuarios = Cliente.clientes

    while True:
        option = input(
            "\nBem-vindo(a) ao Banco Python!\nEscolha uma opção:\n\n"
            "[0] - Saldo\n[1] - Saque\n[2] - Depósito\n[3] - Extrato\n[4] - Criar Usuário\n[5] - Editar Usuários\n"  # noqa
            "[6] - Listar Usuários\n[7] - Criar Conta\n[8] - Listar Contas\n[9] - Encerrar Conta\n[10] - Sair\n\n"  # noqa
            "Digite o número da opção desejada: "
        )

        if option == "0":
            exibir_saldo()
        elif option == "1":
            realizar_saque()
        elif option == "2":
            realizar_deposito()
        elif option == "3":
            exibir_extrato()
        elif option == "4":
            criar_usuario(usuarios)
        elif option == "5":
            Cliente.editar_usuario()
        elif option == "6":
            Cliente.listar_usuarios()
        elif option == "7":
            CriarConta.criar_conta(usuarios)
        elif option == "8":
            Conta.listar_contas()
        elif option == "9":
            Conta.encerrar_conta()
        elif option == "10":
            print("\n\n👋 Obrigado por usar o Banco Python! Até mais!\n\n")
            break
        else:
            print("\n\n❌ Opção inválida! Tente novamente.\n\n")


def exibir_saldo():
    conta = Conta.obter_conta()
    if conta:
        conta.exibir_saldo()


def realizar_saque():
    conta = Conta.obter_conta()
    if conta:
        valor = float(input("Digite o valor do saque: R$ "))
        transacao = Saque(valor)
        transacao.registrar(conta)


def realizar_deposito():
    conta = Conta.obter_conta()
    if conta:
        valor = float(input("Digite o valor do depósito: R$ "))
        transacao = Deposito(valor)
        transacao.registrar(conta)


def exibir_extrato():
    conta = Conta.obter_conta()
    if conta:
        conta.exibir_extrato()


def criar_usuario(usuarios):
    while True:
        documento = input("Digite o CPF ou CNPJ do usuário: ")

        valido, mensagem = validar_documento(documento)
        if not valido:
            print(f"\n{mensagem}\n")
            continue

        break

    if documento_existe(documento, usuarios):
        if len(documento) == 11:
            print("\n❌ CPF já cadastrado!\n")
        else:
            print("\n❌ CNPJ já cadastrado!\n")

        return

    while True:
        nome = input("Digite o nome: ")
        valido, mensagem = validar_nome(nome)
        if valido:
            break
        print(f"\n{mensagem}\n")

    while True:
        if len(documento) == 11:
            data = input("Digite a data de nascimento (dd/mm/aaaa): ")
        else:
            data = input("Digite a data de abertura (dd/mm/aaaa): ")

        valido, mensagem = validar_data(data)
        if valido:
            break
        print(f"\n{mensagem}\n")

    while True:
        endereco = input("Digite o endereço: ")
        valido, mensagem = validar_endereco(endereco)
        if valido:
            break
        print(f"\n{mensagem}\n")

    if len(documento) == 11:
        PessoaFisica(
            nome=nome,
            cpf=documento,
            endereco=endereco,
            data_nascimento=data,
        )
    else:
        PessoaJuridica(
            nome=nome,
            cnpj=documento,
            endereco=endereco,
            data_abertura=data,
        )

    print("\n✅ Usuário criado com sucesso!")


menu_principal()
