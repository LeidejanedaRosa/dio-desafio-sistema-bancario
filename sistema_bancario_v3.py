from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from sistema_bancario_v2 import menu_principal
from sistema_bancario_v3 import Conta


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


def listar_usuarios(usuarios):
    if not usuarios:
        print("\n 🔔 Nenhum usuário cadastrado.\n")
        return

    print("\n📋 Usuários cadastrados: \n")

    for usuario in usuarios:
        documento_label = "CPF" if "cpf" in usuario else "CNPJ"
        documento = usuario.get("cpf") or usuario.get("cnpj")
        print(
            f"{documento_label}: {documento}, Nome: {usuario['nome']}, Endereço: {usuario['endereco']}"  # noqa
        )


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
            conta.historico.adicionar_transacao(f"Depósito de {self.valor}")


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(f"Saque de {self.valor}")


class Conta:
    numero_conta = "001"
    ultima_conta_criada = ""
    contas: List["Conta"] = []

    def __init__(self, cliente, numero_conta, agencia="0001"):
        self._saldo = 0
        self._cliente = cliente
        self._numero_conta = numero_conta
        self._agencia = agencia
        self._historico = Historico()

    @property
    def historico(self):
        return self._historico

    def saldo(self):
        return self._saldo

    @staticmethod
    def criar_conta(usuarios):
        documento = input("Digite o CPF ou CNPJ do usuário: ")

        usuario = encontrar_usuario(usuarios, documento)

        if usuario:
            print("\nSelecione o tipo de conta:")
            print("[1] - Pessoa Física - Corrente")
            print("[2] - Pessoa Física - Poupança")
            print("[3] - Pessoa Física - Universitária")
            print("[4] - Pessoa Física - Conta Salário")
            print("[5] - Pessoa Física - Conta Conjunta")
            print("[6] - Pessoa Física - Conta Menor de Idade")
            print("[7] - Jurídica - Corrente")
            print("[8] - Jurídica - Poupança")
            tipo_conta = input("Digite o número da opção desejada: ")

            novo_numero_conta = Conta._gerar_numero_conta()

            numero_conta_formatado = Conta._formatar_numero_conta(
                tipo_conta, novo_numero_conta
            )  # noqa
            conta = Conta(usuario, numero_conta_formatado)

            Conta.contas.append(conta)  # Armazena a instância da conta
            Cliente.adicionar_conta(usuario, conta)

            print("Conta criada com sucesso!")
        else:
            print("\n 🔔 Usuário não encontrado! Cadastre-o primeiro.\n")
            menu_principal()

    @staticmethod
    def _gerar_numero_conta():
        nova_conta = (
            Conta.numero_conta
            if Conta.ultima_conta_criada != ""
            else int(Conta.ultima_conta_criada) + 1
        )  # noqa

        Conta.ultima_conta_criada = str(nova_conta)

        return str(nova_conta)

    @staticmethod
    def _formatar_numero_conta(tipo_conta: str, numero_conta: str):
        tipo_conta_map = {
            "1": "1",  # Pessoa Física - Corrente
            "2": "2",  # Pessoa Física - Poupança
            "3": "3",  # Pessoa Física - Universitária
            "4": "4",  # Pessoa Física - Conta Salário
            "5": "5",  # Pessoa Física - Conta Conjunta
            "6": "6",  # Pessoa Física - Conta Menor de Idade
            "7": "7",  # Jurídica - Corrente
            "8": "8",  # Jurídica - Poupança
        }
        return f"{numero_conta.zfill(3)}/{tipo_conta_map[tipo_conta]}"

    def sacar(self, valor):
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            self._historico.adicionar_transacao(f"Saque de {valor}")
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(f"Depósito de {valor}")
            return True
        return False


class ContaCorrente(Conta):
    def __init__(
        self, cliente, numero_conta, agencia="0001", limite=0, limite_saques=0
    ):
        super().__init__(cliente, numero_conta, agencia)
        self._limite = limite
        self._limite_saques = limite_saques


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
                cliente["contas"].append(conta)
                break

    def realizar_transacao(self, conta, transacao: Transacao):
        transacao.registrar(conta)

    @classmethod
    def listar_usuarios(cls):
        if not cls.clientes:
            print("\n 🔔 Nenhum usuário cadastrado.\n")
            return

        print("\n📋 Usuários cadastrados: \n")

        for usuario in cls.clientes:
            documento_label = "CPF" if "cpf" in usuario else "CNPJ"
            documento = usuario.get("cpf") or usuario.get("cnpj")
            print(
                f"{documento_label}: {documento}, Nome: {usuario['nome']}, Endereço: {usuario['endereco']}"  # noqa
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
    contas = {}

    while True:
        option = input(
            "\nBem-vindo(a) ao Banco Python!\nEscolha uma opção:\n\n"
            "[1] - Saque\n[2] - Depósito\n[3] - Extrato\n[4] - Criar Usuário\n[5] - Editar Usuários\n"  # noqa
            "[6] - Listar Usuários\n[7] - Criar Conta\n[8] - Listar Contas\n[9] - Encerrar Conta\n[10] - Sair\n\n"  # noqa
            "Digite o número da opção desejada: "
        )

        if option == "1":
            conta = obter_conta(contas)
            if conta:
                valor = float(input("Digite o valor do saque: "))
                transacao = Saque(valor)
                transacao.registrar(conta)

        elif option == "2":
            conta = obter_conta(contas)
            if conta:
                valor = float(input("Digite o valor do depósito: "))
                transacao = Deposito(valor)
                transacao.registrar(conta)

        elif option == "3":
            conta = obter_conta(contas)
            if conta:
                mostrar_extrato(conta)

        elif option == "4":
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

                menu_principal()

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

            print("Usuário criado com sucesso!")

        elif option == "5":
            Cliente.editar_usuario()

        elif option == "6":
            Cliente.listar_usuarios()

        elif option == "7":
            Conta.criar_conta(usuarios)

        elif option == "8":
            pass
            # listar_contas(contas)

        elif option == "9":
            pass
            # encerrar_conta(contas)

        elif option == "10":
            print("\n\n👋 Obrigado por usar o Banco Python! Até mais!\n\n")
            break
        else:
            print("\n\n❌ Opção inválida! Tente novamente.\n\n")


def obter_conta(contas):
    numero = int(input("Digite o número da conta: "))
    return contas.get(numero, None)


def mostrar_extrato(conta):
    print("\nExtrato da conta:")
    for transacao in conta.historico.transacoes:
        print(transacao)


def listar_contas(contas):
    print("\nContas cadastradas:")
    for numero, conta in contas.items():
        print(f"Conta {numero}, Saldo: {conta.saldo()}")


def encerrar_conta(contas):
    numero = int(input("Digite o número da conta a ser encerrada: "))
    if numero in contas:
        del contas[numero]
        print("Conta encerrada com sucesso!")
    else:
        print("Conta não encontrada!")


menu_principal()
    """
    preciso verificar se menu_principal() é necessário depois da mensagem: Cadastre um usuário primeiro.
    Testar a criação de Conta
    conferir se precisa refatorar o código de criar conta
()    """