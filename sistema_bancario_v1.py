from datetime import datetime

BALANCE = 5000.0
DAILY_LIMIT = 1500.0
MAX_WITHDRAWALS = 3
extract: list[dict] = []

while True:
    option = input(
        "\nBem-vindo(a) ao Banco Python!\nEscolha uma opção:\n\n"
        "[1] - Saque\n[2] - Depósito\n[3] - Extrato\n[4] - Sair\n\n"
        "Digite o número da opção desejada: "
    )

    if option == "1":
        value = float(input("Digite o valor do saque: R$ "))

        today = datetime.now().date()

        daily_withdrawals = [
            t
            for t in extract
            if t["tipo"] == "Saque"
            and datetime.fromisoformat(t["data"]).date() == today
        ]

        total_cashed_today = sum(t["valor"] for t in daily_withdrawals)

        if len(daily_withdrawals) >= MAX_WITHDRAWALS:
            print("\n\n❌ Limite de 3 saques diários atingido!\n\n")
        elif value > BALANCE:
            print("\n\n❌ Saldo insuficiente!\n\n")
        elif total_cashed_today + value > DAILY_LIMIT:
            print("\n\n❌ Limite diário de saque atingido!\n\n")
        else:
            BALANCE -= value
            extract.append(
                {
                    "tipo": "Saque",
                    "valor": value,
                    "data": datetime.now().isoformat(),
                }
            )
            print(f"\n\n✅ Saque de R$ {value:.2f} realizado com sucesso!\n\n")

    elif option == "2":
        value = float(input("Digite o valor do depósito: R$ "))
        BALANCE += value
        extract.append(
            {
                "tipo": "Depósito",
                "valor": value,
                "data": datetime.now().isoformat(),
            }
        )
        print(f"\n\n✅ Depósito de R$ {value:.2f} realizado com sucesso!\n\n")

    elif option == "3":
        print("\n📜 Extrato Bancário 📜\n")
        for transaction in extract:
            formatted_date = datetime.fromisoformat(
                transaction["data"]
            ).strftime(  # noqa
                "%d/%m/%Y %H:%M:%S"
            )
            print(
                f"{formatted_date} - {transaction['tipo']}: R$ {transaction['valor']:.2f}"  # noqa
            )
        print(f"\n💰 Saldo atual: R$ {BALANCE:.2f}\n")

    elif option == "4":
        print("\n\n👋 Obrigado por usar o Banco Python! Até mais!\n\n")
        break

    else:
        print("\n\n❌ Opção inválida! Tente novamente.\n\n")
