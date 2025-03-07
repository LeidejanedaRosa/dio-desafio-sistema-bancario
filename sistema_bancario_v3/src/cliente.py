from src.validators import validar_documento
from src.utils import (
    atualizar_usuario,
    encontrar_usuario,
    exibir_dados_usuario,
    obter_documento,
    obter_novos_dados,
)


class Cliente:
    clientes: list[dict] = []

    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @classmethod
    def adicionar_conta(cls, usuario, conta):
        print("conta", conta.__dict__)
        print("usuario", usuario)
        for cliente in cls.clientes:
            if cliente.get("cpf") == usuario.get(
                "cpf"
            ) or cliente.get(  # aqui eu testo se o cliente tem o mesmo cpf ou cnpj que o usuario
                "cnpj"  # posso testar o mesmo para co_titular e responsavel
            ) == usuario.get(
                "cnpj"
            ):
                if "contas" not in cliente:
                    cliente["contas"] = []
                if conta not in cliente["contas"]:
                    cliente["contas"].append(conta)

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
