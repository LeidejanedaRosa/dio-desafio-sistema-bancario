from src.validators import validar_data, validar_documento


def documento_existe(documento, clientes):
    return any(
        cliente.get("cpf") == documento or cliente.get("cnpj") == documento
        for cliente in clientes
    )


def obter_documento(eEdicao=False):
    label = "editado" if eEdicao else "excluído"
    documento = input(
        f"Digite o CPF ou CNPJ do usuário a ser {label} (somente números): "
    )
    return documento.replace(".", "").replace("-", "").strip()


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
    valido, mensagem = validar_data(nova_data, True)

    while valido is False:
        print(f"\n{mensagem}\n")
        nova_data = input(
            f"{data_label} [{usuario.get('data_nascimento', usuario.get('data_abertura'))}]: "  # noqa
        ).strip()
        valido, mensagem = validar_data(nova_data)

    novo_endereco = input(f"Endereço [{usuario['endereco']}]: ").strip()
    return novo_nome, nova_data, novo_endereco


def encontrar_usuario(usuarios, documento):
    return next(
        (
            u
            for u in usuarios
            if isinstance(u, dict)
            and (
                ("cpf" in u and u["cpf"] == documento)
                or ("cnpj" in u and u["cnpj"] == documento)
            )
        ),
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
    novo_nome, nova_data, novo_endereco = obter_novos_dados(usuario)  # noqa
    atualizar_usuario(usuario, novo_nome, nova_data, novo_endereco)
    print("\n\n✅ Dados do usuário atualizados com sucesso!\n\n")
