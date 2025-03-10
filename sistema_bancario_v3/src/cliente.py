from src.validadores import validar_documento
from src.utilitarios import (
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
    def adicionar_conta(cls, conta):
        documento_cliente = (
            conta._cliente.get("cpf") or conta._cliente.get("cnpj")
            if conta._cliente
            else None
        )

        conjuge_responsavel = (
            conta._co_titular.get("cpf") if conta._co_titular else None
        ) or (conta._responsavel.get("cpf") if conta._responsavel else None)

        cliente_principal = next(
            (
                c
                for c in cls.clientes
                if c.get("cpf") == documento_cliente
                or c.get("cnpj") == documento_cliente
            ),
            None,  # noqa
        )
        documento_conjuge_responsavel = next(
            (
                c
                for c in cls.clientes
                if c.get("cpf") and c.get("cpf") == conjuge_responsavel
            ),
            None,
        )
        if cliente_principal:
            cliente_principal.setdefault("contas", []).append(conta)

        if documento_conjuge_responsavel is not None:
            documento_conjuge_responsavel.setdefault("contas", []).append(conta)  # noqa

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
        documento = obter_documento(eEdicao=True)
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

    @classmethod
    def excluir_usuario(cls):
        documento = obter_documento()
        valido, mensagem = validar_documento(documento)
        if not valido:
            print(f"\n{mensagem}\n")
            return

        usuario = encontrar_usuario(cls.clientes, documento)
        if not usuario:
            print("\n\n❌ Usuário não encontrado!\n\n")
            return

        # Verificar se o usuário tem contas ativas
        contas_ativas = [
            conta
            for conta in usuario.get("contas", [])
            if not getattr(conta, "_data_encerramento", False)
        ]
        contas_str = (
            "\n ".join(str(conta) for conta in contas_ativas)
            if contas_ativas
            else "Nenhuma conta cadastrada!"
        )

        if contas_ativas:
            print(
                "\n❌ Usuário possui conta(s) ativa(s)! Por favor, encerre as contas e saque os valores antes de excluir o cadastro."  # noqa
            )
            print("\n📌 Contas ativas do usuário:")
            print(contas_str)
            return

        print("\n📌 Dados do usuário:")
        for chave, valor in usuario.items():
            if chave != "contas":
                print(f"{chave.capitalize()}: {valor}")

        confirmacao = (
            input("\n❗ Tem certeza que deseja excluir este usuário? (S/N): ")
            .strip()
            .lower()
        )
        if confirmacao != "s":
            print("\n🚫 Operação cancelada!\n")
            return

        cls.clientes.remove(usuario)
        print("\n\n✅ Usuário excluído com sucesso!\n\n")

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
