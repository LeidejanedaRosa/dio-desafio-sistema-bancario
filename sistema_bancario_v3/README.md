# 💰 Sistema Bancário em Python

## 📌 Introdução  

Este projeto foi desenvolvido com objetivo educacional durante o bootcamp **"Suzano - Python Developer"** na [DIO](https://www.dio.me/).  
O desafio consiste em criar um sistema bancário simples utilizando Python, reforçando conceitos básicos da linguagem. Agora utilizando herança, polimorfismo, decoradores e classes abstratas.

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
sistema_bancario_v3
├── src
│   ├── __init__.py          # Marca o diretório como um pacote Python
│   ├── main.py              # Ponto de entrada da aplicação, menu
│   ├── cliente.py           # Classe relacionada a clientes
│   ├── criar_conta.py       # Classe relacionada a criação das contas
│   ├── conta.py             # Classe relacionada a validação e operações das contas
│   ├── tipo_conta.py        # Classes relacionadas aos tipos de contas existentes
│   ├── transacao.py         # Classes relacionadas a transações
│   ├── utilitarios.py       # Funções utilitárias
│   └── validadores.py       # Funções de validação
├
└── README.md                 # Documentação do projeto
```

## 🔥 Funcionalidades 

### 📌 Versão 3:

✅ Realiza depósitos na conta</br>
✅ Permite saques com limite diário de valor e de saques por dia, de acordo com o tipo de conta</br>
✅ Exibe extrato com registro de transações e horários</br>
✅ Permite criar usuários com validação de CPF, nome, data de nascimento e endereço </br>
✅ Permite criar contas bancárias associadas a um usuário </br>
✅ Um usuário pode ter até 7 tipos de contas associadas </br>
✅ Permite editar os dados do usuário </br>
✅ Permite excluir os dados do usuário, validando se a conta está ativa ou se tem valores a sacar </br>
✅ Permite listar os usuários cadastrados e as contas bancárias </br>
✅ Permite encerrar uma conta </br>
✅ Melhorias na estrutura do código utilizando funções para modularização</br>
✅ Implementação de um menu interativo para facilitar a navegação   </br>
✅ Melhor tratamento de erros e validações  </br>
✅ Interface via terminal  

## 🚀 Como Rodar o Projeto  

### ✅ Pré-requisitos:
- Ter o **Python 3** instalado na máquina

### ▶️ Para executar o projeto:
1. Clone o repositório:  
   ```bash
   git clone https://github.com/LeidejanedaRosa/dio-desafio-sistema-bancario.git
   ```

2. Entre na pasta do projeto:  
   ```bash
   cd dio-desafio-sistema-bancario/sistema_bancario_v3
   ```

3. Para iniciar o sistema bancário, execute o arquivo `main.py`:
    ```
    python3 src/main.py
    ```
   
## 🛠️ Tecnologias Utilizadas  
- 🐍 Python 3  
- ⏰ Biblioteca `datetime` para manipulação de datas  

## ✍️ Autor(a)  
Desenvolvido por [Leidejane da Rosa](https://github.com/LeidejanedaRosa)

