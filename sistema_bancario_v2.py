from datetime import datetime

BALANCE = 5000.0
DAILY_LIMIT = 1500.0
MAX_WITHDRAWALS = 3
extract: list[dict] = []
usuarios = []
contas = []
numero_conta_sequencial = 1
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


def verificar_limites_saque(
    valor, saldo, limite, numero_saques, limite_saques, total_cashed_today
):
    if numero_saques >= limite_saques:
        print("\n\n❌ Limite de 3 saques diários atingido!\n\n")
        return False
    elif valor > saldo:
        print("\n\n❌ Saldo insuficiente!\n\n")
        return False
    elif total_cashed_today + valor > limite:
        print("\n\n❌ Limite diário de saque atingido!\n\n")
        return False
    return True


def saque(*, saldo, valor, extract, limite, numero_saques, limite_saques):
    today = datetime.now().date()

    daily_withdrawals = [
        t
        for t in extract
        if t["tipo"] == "Saque" and datetime.fromisoformat(t["data"]).date() == today
    ]

    total_cashed_today = sum(t["valor"] for t in daily_withdrawals)

    if verificar_limites_saque(
        valor, saldo, limite, numero_saques, limite_saques, total_cashed_today
    ):
        saldo -= valor
        extract.append(
            {
                "tipo": "Saque",
                "valor": valor,
                "data": datetime.now().isoformat(),
            }
        )
        print(f"\n\n✅ Saque de R$ {valor:.2f} realizado com sucesso!\n\n")

    return saldo, extract


def deposito(saldo, valor, /, extrato):
    saldo += valor
    extrato.append(
        {
            "tipo": "Depósito",
            "valor": valor,
            "data": datetime.now().isoformat(),
        }
    )
    print(f"\n\n✅ Depósito de R$ {valor:.2f} realizado com sucesso!\n\n")
    return saldo, extrato


def mostrar_extrato(saldo, *, extrato):
    print("\n📜 Extrato Bancário 📜\n")
    for transaction in extrato:
        formatted_date = datetime.fromisoformat(transaction["data"]).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        print(
            f"{formatted_date} - {transaction['tipo']}: R$ {transaction['valor']:.2f}"  # noqa
        )
    print(f"\n💰 Saldo atual: R$ {saldo:.2f}\n")


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
        print("\n\n❌ A data de nascimento deve estar no formato dd/mm/aaaa!\n\n")
        return False
    return True


def validar_cpf(cpf):
    if not cpf:
        print("\n\n❌ O CPF não pode ser vazio!\n\n")
        return False
    if cpf_existe(cpf, usuarios):
        print("\n\n❌ Usuário com este CPF já cadastrado!\n\n")
        return False
    return True


def validar_endereco(endereco):
    if not endereco:
        print("\n\n❌ O endereço não pode ser vazio!\n\n")
        return False
    return True


def cpf_existe(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    return False


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

        nome = input("Digite o nome do usuário: ").strip()
        if not validar_nome(nome):
            continue

        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ").strip()
        if not validar_data_nascimento(data_nascimento):
            continue

        endereco = input(
            "Digite o endereço (logradouro, número - bairro - cidade/UF): "
        ).strip()
        if not validar_endereco(endereco):
            continue

        # Criar o novo usuário
        novo_usuario = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        }

        # Adicionar o novo usuário à lista de usuários
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
        print(f"Endereço: {usuario['endereco']}\n")


def criar_conta(cpf):
    global numero_conta_sequencial

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        print("\n\n❌ Usuário não encontrado!\n\n")
        return

    print("\n📋 Tipos de Conta Disponíveis 📋\n")
    for i, tipo in enumerate(TIPOS_DE_CONTA, 1):
        print(f"[{i}] - {tipo}")

    tipo_conta_index = int(input("\nDigite o número do tipo de conta desejado: ")) - 1
    if tipo_conta_index < 0 or tipo_conta_index >= len(TIPOS_DE_CONTA):
        print("\n\n❌ Tipo de conta inválido!\n\n")
        return

    tipo_conta = TIPOS_DE_CONTA[tipo_conta_index]

    nova_conta = {
        "tipo": tipo_conta,
        "agencia": AGENCIA,
        "numero": numero_conta_sequencial,
        "usuario": usuario,
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
        print(f"Usuário: {conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})\n")


while True:
    option = input(
        "\nBem-vindo(a) ao Banco Python!\nEscolha uma opção:\n\n"
        "[1] - Saque\n[2] - Depósito\n[3] - Extrato\n[4] - Criar Usuário\n[5] - Listar Usuários\n[6] - Abrir Conta\n[7] - Listar Contas\n[8] - Sair\n\n"
        "Digite o número da opção desejada: "
    )

    if option == "1":
        valor = float(input("Digite o valor do saque: R$ "))
        BALANCE, extract = saque(
            saldo=BALANCE,
            valor=valor,
            extract=extract,
            limite=DAILY_LIMIT,
            numero_saques=len([t for t in extract if t["tipo"] == "Saque"]),
            limite_saques=MAX_WITHDRAWALS,
        )
    elif option == "2":
        valor = float(input("Digite o valor do depósito: R$ "))
        BALANCE, extract = deposito(BALANCE, valor, extract)
    elif option == "3":
        mostrar_extrato(BALANCE, extrato=extract)
    elif option == "4":
        criar_usuario()
    elif option == "5":
        listar_usuarios()
    elif option == "6":
        cpf = (
            input("Digite o CPF do usuário: ").replace(".", "").replace("-", "").strip()
        )
        if not cpf_existe(cpf, usuarios):
            print("\n\nUsuário não encontrado. Vamos criar um novo usuário.\n\n")
            criar_usuario(cpf)
        criar_conta(cpf)
    elif option == "7":
        listar_contas()
    elif option == "8":
        print("\n\n👋 Obrigado por usar o Banco Python! Até mais!\n\n")
        break
    else:
        print("\n\n❌ Opção inválida! Tente novamente.\n\n")
