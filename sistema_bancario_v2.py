from datetime import datetime

SALDO_INICIAL = 5000.0
LIMITE_DIARIO_PARA_SAQUE = 1500.0
MAX_RETIRADAS = 3
AGENCIA = "0001"
TIPOS_DE_CONTA = [
    "Corrente",
    "Poupança",
    "Conta Salário",
    "Conta de Investimentos",
    "Conta Conjunta",
    "Conta de Menor de Idade",
    "Conta Universitária",
]

extrato: list[dict] = []
usuarios: list[dict] = []
contas: list[dict] = []
numero_conta_sequencial = 1


def validar_nome(nome):
    if not nome:
        print("\n\n❌ O nome não pode ser vazio!\n\n")
        return False
    return True


def validar_data_nascimento(data_nascimento):
    if not data_nascimento:
        print("\n\n❌ A data de nascimento é obrigatória!\n\n")
        return False
    try:
        datetime.strptime(data_nascimento, "%d/%m/%Y")
    except ValueError:
        print(
            "\n\n❌ A data de nascimento deve estar no formato dd/mm/aaaa!\n\n"
        )  # noqa
        return False
    return True


def validar_cpf(cpf):
    if not cpf:
        print("\n\n❌ O CPF não pode ser vazio!\n\n")
        return False
    if cpf_existe(cpf):
        print("\n\n❌ Usuário com este CPF já cadastrado!\n\n")
        return False
    return True


def validar_endereco(endereco):
    if not endereco:
        print("\n\n❌ O endereço não pode ser vazio!\n\n")
        return False
    return True


def cpf_existe(cpf):
    return any(usuario["cpf"] == cpf for usuario in usuarios)


def obter_dado(campo, validacao):
    while True:
        dado = input(f"Digite o {campo}: ").strip()
        if validacao(dado):
            return dado


def verificar_limites_saque(
    valor, saldo, limite, numero_saques, limite_saques, total_sacado_hoje
):
    if numero_saques >= limite_saques:
        print("\n\n❌ Limite de 3 saques diários atingido!\n\n")
        return False
    elif valor > saldo:
        print("\n\n❌ Saldo insuficiente!\n\n")
        return False
    elif total_sacado_hoje + valor > limite:
        print("\n\n❌ Limite diário de saque atingido!\n\n")
        return False
    return True


def obter_conta():
    agencia = input("Digite a agência: ").strip()
    numero_conta = int(input("Digite o número da conta: ").strip())
    tipo_conta = input("Digite o tipo da conta: ").strip()
    conta = next(
        (
            c
            for c in contas
            if c["agencia"] == agencia
            and c["numero"] == numero_conta
            and c["tipo"] == tipo_conta
        ),
        None,
    )
    if not conta:
        print("\n\n❌ Conta não encontrada!\n\n")
        return menu_principal()
    elif "data_encerramento" in conta:
        print(f"    Conta encerrada em: {conta['data_encerramento']}")  # noqa
        return menu_principal()
    return conta


def sacar(conta):

    valor = float(input("Digite o valor do saque: R$ "))
    saldo = conta["saldo"]
    limite = LIMITE_DIARIO_PARA_SAQUE
    numero_saques = len(
        [t for t in extrato if t["tipo"] == "Saque" and t["conta"] == conta]
    )
    limite_saques = MAX_RETIRADAS
    hoje = datetime.now().date()
    retiradas_diarias = [
        t
        for t in extrato
        if t["tipo"] == "Saque"
        and t["conta"] == conta
        and datetime.fromisoformat(t["data"]).date() == hoje
    ]
    total_sacado_hoje = sum(t["valor"] for t in retiradas_diarias)

    if verificar_limites_saque(
        valor, saldo, limite, numero_saques, limite_saques, total_sacado_hoje
    ):
        conta["saldo"] -= valor
        extrato.append(
            {
                "tipo": "Saque",
                "valor": valor,
                "data": datetime.now().isoformat(),
                "conta": conta,
            }
        )
    print(f"\n\n✅ Saque de R$ {valor:.2f} realizado com sucesso!\n\n")
    print(
        f"Conta: {conta['tipo']} - Agência: {conta['agencia']} - Número: {conta['numero']}"  # noqa
    )
    print(
        f"Usuário: {conta['usuario']['nome']} - CPF: {conta['usuario']['cpf']}"  # noqa
    )
    return valor


def depositar(conta):

    valor = float(input("Digite o valor do depósito: R$ "))
    conta["saldo"] += valor
    extrato.append(
        {
            "tipo": "Depósito",
            "valor": valor,
            "data": datetime.now().isoformat(),
            "conta": conta,
        }
    )
    print(f"\n\n✅ Depósito de R$ {valor:.2f} realizado com sucesso!\n\n")
    print(
        f"Conta: {conta['tipo']} - Agência: {conta['agencia']} - Número: {conta['numero']}"  # noqa
    )
    print(
        f"Usuário: {conta['usuario']['nome']} - CPF: {conta['usuario']['cpf']}"
    )  # noqa
    return conta["saldo"]


def mostrar_extrato(conta):

    print("\n📜 Extrato Bancário 📜\n")
    for transacao in extrato:
        if transacao["conta"] == conta:
            formatted_date = datetime.fromisoformat(transacao["data"]).strftime(  # noqa
                "%d/%m/%Y %H:%M:%S"
            )
            print(
                f"{formatted_date} - {transacao['tipo']}: R$ {transacao['valor']:.2f}"  # noqa
            )
    print(f"\n💰 Saldo atual: R$ {conta['saldo']:.2f}\n")
    print(
        f"Conta: {conta['tipo']} - Agência: {conta['agencia']} - Número: {conta['numero']}"  # noqa
    )
    print(
        f"Usuário: {conta['usuario']['nome']} - CPF: {conta['usuario']['cpf']}"
    )  # noqa


def criar_usuario(cpf=None):
    while True:
        if not cpf:
            cpf = (
                input("Digite o CPF (somente números): ")
                .replace(".", "")
                .replace("-", "")
                .strip()
            )
        if not validar_cpf(cpf):
            cpf = None
            continue

        nome = obter_dado("nome", validar_nome)
        data_nascimento = obter_dado(
            "data de nascimento (dd/mm/aaaa)", validar_data_nascimento
        )
        endereco = obter_dado(
            "endereço (logradouro, número - bairro - cidade/UF)",
            validar_endereco,  # noqa
        )

        novo_usuario = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        }
        usuarios.append(novo_usuario)
        print("\n\n✅ Usuário cadastrado com sucesso!\n\n")
        break


def listar_usuarios():
    if not usuarios:
        print("\n\n📭 Nenhum usuário cadastrado!\n\n")
        return

    print("\n📋 Lista de Usuários 📋\n")
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}")
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Endereço: {usuario['endereco']}")

        contas_usuario = [
            conta
            for conta in contas
            if conta["usuario"]["cpf"] == usuario["cpf"]  # noqa
        ]
        if contas_usuario:
            print("Contas:")
            for conta in contas_usuario:
                print(
                    f"  - Tipo: {conta['tipo']}, Agência: {conta['agencia']}, Número: {conta['numero']}, Saldo: R$ {conta['saldo']:.2f}"  # noqa
                )
                if "data_encerramento" in conta:
                    print(
                        f"    Conta encerrada em: {conta['data_encerramento']}"
                    )  # noqa
        else:
            print("  - Nenhuma conta cadastrada")
        print("\n")


def editar_usuario():
    cpf = (
        input("Digite o CPF do usuário a ser editado (somente números): ")
        .replace(".", "")
        .replace("-", "")
        .strip()
    )
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if not usuario:
        print("\n\n❌ Usuário não encontrado!\n\n")
        return

    print("\n📋 Dados Atuais do Usuário 📋\n")
    print(f"Nome: {usuario['nome']}")
    print(f"Data de Nascimento: {usuario['data_nascimento']}")
    print(f"CPF: {usuario['cpf']}")
    print(f"Endereço: {usuario['endereco']}\n")

    print(
        "Digite os novos dados do usuário (deixe em branco para manter o valor atual):"  # noqa
    )
    novo_nome = input(f"Nome [{usuario['nome']}]: ").strip()
    nova_data_nascimento = input(
        f"Data de Nascimento [{usuario['data_nascimento']}]: "
    ).strip()
    novo_endereco = input(f"Endereço [{usuario['endereco']}]: ").strip()

    if novo_nome:
        usuario["nome"] = novo_nome
    if nova_data_nascimento:
        if validar_data_nascimento(nova_data_nascimento):
            usuario["data_nascimento"] = nova_data_nascimento
        else:
            print(
                "\n\n❌ Data de nascimento inválida! Manter o valor atual.\n\n"
            )  # noqa
    if novo_endereco:
        usuario["endereco"] = novo_endereco

    print("\n\n✅ Dados do usuário atualizados com sucesso!\n\n")


def criar_conta(cpf):
    global numero_conta_sequencial

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        print("\n\n❌ Usuário não encontrado!\n\n")
        return

    tipos_conta_usuario = [
        conta["tipo"] for conta in contas if conta["usuario"]["cpf"] == cpf
    ]
    tipos_disponiveis = [
        tipo for tipo in TIPOS_DE_CONTA if tipo not in tipos_conta_usuario
    ]

    if not tipos_disponiveis:
        print(
            "\n\n❌ Usuário já possui todos os tipos de conta disponíveis!\n\n"
        )  # noqa
        return

    print("\n📋 Dados do Usuário 📋\n")
    print(f"Nome: {usuario['nome']}")
    print(f"Data de Nascimento: {usuario['data_nascimento']}")
    print(f"CPF: {usuario['cpf']}")
    print(f"Endereço: {usuario['endereco']}\n")

    print("\n\n📋 Tipos de Conta Disponíveis 📋\n")
    for i, tipo in enumerate(tipos_disponiveis, 1):
        print(f"[{i}] - {tipo}")

    tipo_conta_index = (
        int(input("\nDigite o número do tipo de conta desejado: ")) - 1
    )  # noqa
    if tipo_conta_index < 0 or tipo_conta_index >= len(tipos_disponiveis):
        print("\n\n❌ Tipo de conta inválido!\n\n")
        return

    tipo_conta = tipos_disponiveis[tipo_conta_index]
    nova_conta = {
        "tipo": tipo_conta,
        "agencia": AGENCIA,
        "numero": numero_conta_sequencial,
        "usuario": usuario,
        "saldo": SALDO_INICIAL,
    }
    contas.append(nova_conta)
    numero_conta_sequencial += 1
    print("\n\n✅ Conta criada com sucesso!\n\n")


def listar_contas():
    if not contas:
        print("\n\n📭 Nenhuma conta cadastrada!\n\n")
        return

    print("\n📋 Lista de Contas 📋\n")
    for conta in contas:
        print(f"Tipo: {conta['tipo']}")
        print(f"Agência: {conta['agencia']}")
        print(f"Número: {conta['numero']}")
        print(
            f"Usuário: {conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})"  # noqa
        )  # noqa
        if "data_encerramento" in conta:
            print(f"Conta encerrada em: {conta['data_encerramento']}")
        print("\n")


def encerrar_conta():
    agencia = input("Digite a agência: ").strip()
    numero_conta = int(input("Digite o número da conta: ").strip())
    tipo_conta = input("Digite o tipo da conta: ").strip()
    conta = next(
        (
            c
            for c in contas
            if c["agencia"] == agencia
            and c["numero"] == numero_conta
            and c["tipo"] == tipo_conta
        ),
        None,
    )
    if not conta:
        print("\n\n❌ Conta não encontrada!\n\n")
        return

    if "data_encerramento" in conta:
        print("\n\n❌ Esta conta já foi encerrada!\n\n")
        return

    conta["data_encerramento"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(
        f"\n\n✅ Conta encerrada com sucesso em {conta['data_encerramento']}!\n\n"  # noqa
    )  # noqa


def menu_principal():
    while True:
        option = input(
            "\nBem-vindo(a) ao Banco Python!\nEscolha uma opção:\n\n"
            "[1] - Saque\n[2] - Depósito\n[3] - Extrato\n[4] - Criar Usuário\n[5] - Editar Usuários\n"  # noqa
            "[6] - Listar Usuários\n[7] - Criar Conta\n[8] - Listar Contas\n[9] - Encerrar Conta\n[10] - Sair\n\n"  # noqa
            "Digite o número da opção desejada: "
        )

        if option == "1":
            conta = obter_conta()
            sacar(conta=conta)

        elif option == "2":
            conta = obter_conta()
            depositar(conta)
        elif option == "3":
            conta = obter_conta()
            mostrar_extrato(conta)
        elif option == "4":
            criar_usuario()
        elif option == "5":
            editar_usuario()
        elif option == "6":
            listar_usuarios()
        elif option == "7":
            cpf = (
                input("Digite o CPF do usuário: ")
                .replace(".", "")
                .replace("-", "")
                .strip()
            )
            if not cpf_existe(cpf):
                criar_usuario(cpf)
            criar_conta(cpf)
        elif option == "8":
            listar_contas()
        elif option == "9":
            encerrar_conta()
        elif option == "10":
            print("\n\n👋 Obrigado por usar o Banco Python! Até mais!\n\n")
            break
        else:
            print("\n\n❌ Opção inválida! Tente novamente.\n\n")


menu_principal()
