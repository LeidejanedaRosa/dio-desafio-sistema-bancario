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
    def _cadastrar_senha():
        while True:
            senha = input("🔐 Defina uma senha para a conta: ")
            if len(senha) < 6:
                print("❌ A senha deve ter pelo menos 6 caracteres.")
                continue
            confirmar = input("🔁 Confirme sua senha: ")
            if senha != confirmar:
                print("❌ As senhas não coincidem. Tente novamente.")
                continue
            return senha

    @staticmethod
    def criar_conta(usuarios):
        documento = ContaFactory._obter_documento_usuario()
        usuario = encontrar_usuario(usuarios, documento)

        if not usuario:
            print("\n 🔔 Usuário não encontrado! Cadastre-o primeiro.\n")
            return

        responsavel = None
        if len(documento) == 11:
            valido, mensagem = ContaFactory._validar_idade_usuario(usuario)

            if not valido:
                print(mensagem)
                responsavel = ContaFactory._obter_responsavel(usuarios)
                if not responsavel:
                    print(
                        "\n🔔 Responsável não encontrado! Cadastre-o primeiro.\n"  # noqa
                    )  # noqa
                    return
                if not ContaFactory._validar_usuario_diferente_titular(
                    usuario["cpf"], responsavel["cpf"], "responsável"
                ):
                    return
                if not ContaFactory.verificar_usuario_possui_conta_ativa(
                    responsavel
                ):  # noqa
                    print(
                        "\n❌ Responsável não possui conta ativa! Precisa abrir uma conta primeiro.\n"  # noqa
                    )
                    return
                print("\nResponsável encontrado. Continuando...\n")

        tipo_conta = ContaFactory._selecionar_tipo_conta(usuario)
        if not tipo_conta:
            return

        co_titular = None
        if tipo_conta == "5":  # Conta Conjunta
            co_titular = ContaFactory._obter_co_titular(usuarios)
            if not co_titular:
                print("\n🔔 Cônjuge não encontrado! Cadastre-o primeiro.\n")
                return

            if "cpf" not in co_titular or len(co_titular["cpf"]) != 11:
                print("\n❌ Cônjuge não pode ser uma pessoa jurídica.\n")
                return

            if not ContaFactory._validar_usuario_diferente_titular(
                usuario["cpf"], co_titular["cpf"], "cônjuge"
            ):
                return

            valido, mensagem = ContaFactory._validar_idade_usuario(co_titular)
            if not valido:
                print("\n❌ Cônjuge não pode ser menor de idade. \n")
                return

        senha = ContaFactory._cadastrar_senha()
        conta = (
            ContaFactory._criar_instancia_conta(
                tipo_conta=tipo_conta,
                usuario=usuario,
                senha=senha,
                co_titular=co_titular,
                responsavel=responsavel,
            )
            if tipo_conta in ["5", "6"]
            else ContaFactory._criar_instancia_conta(
                tipo_conta=tipo_conta, usuario=usuario, senha=senha
            )  # noqa
        )  # noqa
        if not conta:
            return

        ContaFactory._realizar_deposito_inicial(conta)
        Conta.contas.append(conta)
        Cliente.adicionar_conta(conta)

        print("\n✅ Conta criada com sucesso!\n")

    @staticmethod
    def _validar_idade_usuario(usuario):
        data_nascimento = datetime.strptime(
            usuario["data_nascimento"], "%d/%m/%Y"
        )  # noqa
        idade = (datetime.now() - data_nascimento).days // 365
        if idade < 18:
            return (
                False,
                "\n🔔 Usuário menor de idade. Informe o responsável...\n",
            )  # noqa
        return True, ""

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

        # Verificar se o usuário é co-titular em outra conta conjunta
        for conta in Conta.contas:
            if conta._co_titular == usuario:
                tipos_conta.pop("5", None)  # Remove a opção de conta conjunta

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
            print("conta", conta)
            if (
                conta._cliente == usuario
                or conta._co_titular == usuario
                and conta.verificar_conta_ativa()
            ):
                return True
        return False

    @staticmethod
    def _obter_usuario(tipo_usuario, usuarios):
        cpf = input(f"Digite o CPF do {tipo_usuario}: ")
        usuario = encontrar_usuario(usuarios, cpf)
        return usuario

    @staticmethod
    def _validar_usuario_diferente_titular(
        usuario_documento, documento, tipo_usuario
    ):  # noqa
        if usuario_documento == documento:
            print(f"\n❌ O {tipo_usuario} não pode ser o titular!\n")  # noqa
            return False
        return True

    @staticmethod
    def _obter_co_titular(usuarios):
        return ContaFactory._obter_usuario("cônjuge", usuarios)

    @staticmethod
    def _obter_responsavel(usuarios):
        usuario = ContaFactory._obter_usuario("responsável", usuarios)
        return usuario

    @staticmethod
    def _criar_instancia_conta(
        tipo_conta, usuario, senha, co_titular=None, responsavel=None
    ):  # noqa
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

        if tipo_conta == "5":  # Conta Conjunta
            return instancia_conta(
                cliente=usuario,
                numero_conta=numero_conta_formatado,
                senha=senha,  # noqa
                co_titular=co_titular,
            )  # noqa
        elif tipo_conta == "6":  # Conta Menor Idade
            return instancia_conta(
                cliente=usuario,
                numero_conta=numero_conta_formatado,
                senha=senha,  # noqa
                responsavel=responsavel,
            )  # noqa
        else:
            return instancia_conta(
                cliente=usuario,
                numero_conta=numero_conta_formatado,
                senha=senha,  # noqa
            )  # noqa

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
