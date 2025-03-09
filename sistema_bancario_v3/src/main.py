from src.utils import documento_existe
from src.validators import (
    validar_data,
    validar_documento,
    validar_endereco,
    validar_nome,
)  # noqa
from src.transacao import Deposito, Saque
from src.cliente import Cliente, PessoaFisica, PessoaJuridica
from src.conta import Conta
from src.conta_factory import ContaFactory


def menu_principal():
    usuarios = Cliente.clientes

    while True:
        option = input(
            "\nBem-vindo(a) ao Banco Python!\nEscolha uma opção:\n\n"
            "[0] - Saldo\n[1] - Saque\n[2] - Depósito\n[3] - Extrato\n[4] - Criar Usuário\n[5] - Editar Usuários\n"  # noqa
            "[6] - Listar Usuários\n[7] - Excluir Usuário\n[8] - Criar Conta\n[9] - Listar Contas\n[10] - Encerrar Conta\n[11] - Sair\n\n"  # noqa
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
            criar_usuario(usuarios)
        elif option == "5":
            Cliente.editar_usuario()
        elif option == "6":
            Cliente.listar_usuarios()
        elif option == "7":
            Cliente.excluir_usuario()
        elif option == "8":
            ContaFactory.criar_conta(usuarios)
        elif option == "9":
            Conta.listar_contas()
        elif option == "10":
            Conta.encerrar_conta()
        elif option == "11":
            print("\n\n👋 Obrigado por usar o Banco Python! Até mais!\n\n")
            break
        else:
            print("\n\n❌ Opção inválida! Tente novamente.\n\n")


def solicitar_senha(conta):
    senha = input("Digite a senha da conta: ")
    if conta.validar_senha(senha):
        return True
    else:
        print("\n❌ Senha incorreta! Tente novamente.\n")
        return False


def exibir_saldo():
    conta = Conta.obter_conta()
    if conta and solicitar_senha(conta):
        conta.exibir_saldo()


def realizar_saque():
    conta = Conta.obter_conta()
    if conta and solicitar_senha(conta):
        valor = float(input("Digite o valor do saque: R$ "))
        transacao = Saque(valor)
        transacao.registrar(conta)


def realizar_deposito():
    conta = Conta.obter_conta()
    if conta and solicitar_senha(conta):
        valor = float(input("Digite o valor do depósito: R$ "))
        transacao = Deposito(valor)
        transacao.registrar(conta)


def exibir_extrato():
    conta = Conta.obter_conta()
    if conta and solicitar_senha(conta):
        conta.exibir_extrato()


def criar_usuario(usuarios):
    while True:
        documento = input("Digite o CPF ou CNPJ do usuário: ")

        valido, mensagem = validar_documento(documento)
        if not valido:
            print(f"\n{mensagem}\n")
            continue

        break

    if documento_existe(documento, usuarios):
        if len(documento) == 11:
            print("\n❌ CPF já cadastrado!\n")
        else:
            print("\n❌ CNPJ já cadastrado!\n")

        return

    while True:
        nome = input("Digite o nome: ")
        valido, mensagem = validar_nome(nome)
        if valido:
            break
        print(f"\n{mensagem}\n")

    while True:
        if len(documento) == 11:
            data = input("Digite a data de nascimento (dd/mm/aaaa): ")
        else:
            data = input("Digite a data de abertura (dd/mm/aaaa): ")

        valido, mensagem = validar_data(data)
        if valido:
            break
        print(f"\n{mensagem}\n")

    while True:
        endereco = input("Digite o endereço: ")
        valido, mensagem = validar_endereco(endereco)
        if valido:
            break
        print(f"\n{mensagem}\n")

    if len(documento) == 11:
        PessoaFisica(
            nome=nome,
            cpf=documento,
            endereco=endereco,
            data_nascimento=data,
        )
    else:
        PessoaJuridica(
            nome=nome,
            cnpj=documento,
            endereco=endereco,
            data_abertura=data,
        )

    print("\n✅ Usuário criado com sucesso!")


if __name__ == "__main__":
    menu_principal()
