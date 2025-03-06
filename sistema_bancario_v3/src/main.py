from src.cliente import Cliente
from src.conta import Conta


def menu_principal():
    usuarios = Cliente.clientes

    while True:
        option = input(
            "\nBem-vindo(a) ao Banco Python!\nEscolha uma opção:\n\n"
            "[0] - Saldo\n[1] - Saque\n[2] - Depósito\n[3] - Extrato\n[4] - Criar Usuário\n[5] - Editar Usuários\n"  # noqa
            "[6] - Listar Usuários\n[7] - Criar Conta\n[8] - Listar Contas\n[9] - Encerrar Conta\n[10] - Sair\n\n"  # noqa
            "Digite o número da opção desejada: "
        )

        if option == "0":
            exibir_saldo()
        elif option == "1":
            realizar_saque()
        elif option == "2":
            realizar_deposito()
        elif option == "3":
            exibir_extrato()
        elif option == "4":
            Cliente.editar_usuario()
        elif option == "5":
            Cliente.editar_usuario()
        elif option == "6":
            Cliente.listar_usuarios()
        elif option == "7":
            ContaFactory.criar_conta(usuarios)
        elif option == "8":
            Conta.listar_contas()
        elif option == "9":
            Conta.encerrar_conta()
        elif option == "10":
            print("\n\n👋 Obrigado por usar o Banco Python! Até mais!\n\n")
            break
        else:
            print("\n\n❌ Opção inválida! Tente novamente.\n\n")


if __name__ == "__main__":
    menu_principal()
