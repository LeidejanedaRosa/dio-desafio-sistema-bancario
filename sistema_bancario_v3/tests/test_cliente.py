from src.cliente import Cliente, PessoaFisica, PessoaJuridica

def test_cliente_creation():
    # Test creation of a PessoaFisica
    pf = PessoaFisica(cpf="12345678901", nome="João Silva", data_nascimento="01/01/1990", endereco="Rua A, 123")
    assert pf._cpf == "12345678901"
    assert pf._nome == "João Silva"
    assert pf._data_nascimento == "01/01/1990"
    assert pf._endereco == "Rua A, 123"
    assert len(Cliente.clientes) == 1  # Ensure the client is added to the list

    # Test creation of a PessoaJuridica
    pj = PessoaJuridica(cnpj="12345678000195", nome="Empresa XYZ", data_abertura="01/01/2020", endereco="Avenida B, 456")
    assert pj._cnpj == "12345678000195"
    assert pj._nome == "Empresa XYZ"
    assert pj._data_abertura == "01/01/2020"
    assert pj._endereco == "Avenida B, 456"
    assert len(Cliente.clientes) == 2  # Ensure the client is added to the list

def test_cliente_editing():
    pf = PessoaFisica(cpf="12345678901", nome="João Silva", data_nascimento="01/01/1990", endereco="Rua A, 123")
    pf._nome = "João da Silva"
    pf._endereco = "Rua A, 456"
    
    assert pf._nome == "João da Silva"
    assert pf._endereco == "Rua A, 456"

def test_cliente_listing():
    Cliente.clientes.clear()  # Clear existing clients for testing
    pf1 = PessoaFisica(cpf="12345678901", nome="João Silva", data_nascimento="01/01/1990", endereco="Rua A, 123")
    pf2 = PessoaFisica(cpf="10987654321", nome="Maria Oliveira", data_nascimento="02/02/1992", endereco="Rua B, 456")
    
    assert len(Cliente.clientes) == 2  # Ensure both clients are listed

def test_cliente_not_found():
    Cliente.clientes.clear()  # Clear existing clients for testing
    pf = PessoaFisica(cpf="12345678901", nome="João Silva", data_nascimento="01/01/1990", endereco="Rua A, 123")
    
    assert pf not in Cliente.clientes  # Ensure the client is not found in an empty list