# Sistema Bancário V3

Este projeto é um sistema bancário simples desenvolvido em Python. Ele permite a criação de usuários, gerenciamento de contas e realização de transações como depósitos e saques.

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
sistema_bancario_v3
├── src
│   ├── __init__.py          # Marca o diretório como um pacote Python
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── cliente.py           # Classes relacionadas a clientes
│   ├── conta.py             # Classes relacionadas a contas
│   ├── transacao.py         # Classes relacionadas a transações
│   ├── utils.py             # Funções utilitárias
│   └── validators.py        # Funções de validação
├── tests
│   ├── __init__.py          # Marca o diretório de testes como um pacote Python
│   ├── test_cliente.py      # Testes para as classes de cliente
│   ├── test_conta.py        # Testes para as classes de conta
│   ├── test_transacao.py    # Testes para as classes de transação
│   ├── test_utils.py        # Testes para funções utilitárias
│   └── test_validators.py   # Testes para funções de validação
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação do projeto
```

## Instalação

Para instalar as dependências do projeto, execute o seguinte comando:

```
pip install -r requirements.txt
```

## Uso

Para iniciar o sistema bancário, execute o arquivo `main.py`:

```
python src/main.py
```

Siga as instruções no menu para criar usuários, contas e realizar transações.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto é de código aberto e pode ser utilizado e modificado livremente.