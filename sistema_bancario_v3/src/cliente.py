from src.validators import validar_documento
from src.utils import (
    atualizar_usuario,
    encontrar_usuario,
    exibir_dados_usuario,
    obter_documento,
    obter_novos_dados,
)


class Cliente:
    clientes: list[dict] = [
        {
            "cpf": "12345678911",
            "nome": "Maria Alice Nascimento da Rosa",
            "endereco": "Via Silvestre Ferraz, 175 - Carioca - São Lourenço/MG",
            "data_nascimento": "17/08/2018",
        },
        {
            "cpf": "08062655741",
            "nome": "Frederico Carlos da Rosa",
            "endereco": "Via Silvestre Ferraz, 175 - Carioca - São Lourenço/MG",
            "data_nascimento": "14/04/1978",
        },
        {
            "cpf": "08368795702",
            "nome": "Leidejane da Silva Nascimento da Rosa",
            "endereco": "Via Silvestre Ferraz, 175 - Carioca - São Lourenço/MG",
            "data_nascimento": "03/05/1981",
        },
    ]

    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @classmethod
    def adicionar_conta(cls, conta):

        documento_cliente = conta._cliente["cpf"] if conta._cliente else None
        conjuge_responsavel = (conta._co_titular and conta._co_titular.get("cpf")) or (
            conta._responsavel and conta._responsavel.get("cpf")
        )

        print("documento_cliente ---------------> ", documento_cliente)
        print("conjuge_responsavel ---------------> ", conjuge_responsavel)

        # Encontrar os clientes na lista
        cliente_principal = next(
            (c for c in cls.clientes if c.get("cpf") == documento_cliente), None  # noqa
        )
        conjuge_responsavel = next(
            (c for c in cls.clientes if c.get("cpf") == conjuge_responsavel),
            None,  # noqa
        )

        if cliente_principal:
            cliente_principal.setdefault("contas", []).append(conta)

        if conjuge_responsavel:
            conjuge_responsavel.setdefault("contas", []).append(conta)

        print("cls.clientes ---------------> ", cls.clientes)

    def realizar_transacao(self, conta, transacao):
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
            )
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
        return f"Nome: {self._nome}, CNPJ: {self._cnpj}, Endereço: {self._endereco}, Data de Abertura: {self._data_abertura}"  # noqa
