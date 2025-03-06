def documento_existe(documento, clientes):
    return any(
        cliente.get("cpf") == documento or cliente.get("cnpj") == documento
        for cliente in clientes
    )


def encontrar_usuario(usuarios, documento):
    return next(
        (
            u
            for u in usuarios
            if ("cpf" in u and u["cpf"] == documento)
            or ("cnpj" in u and u["cnpj"] == documento)
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