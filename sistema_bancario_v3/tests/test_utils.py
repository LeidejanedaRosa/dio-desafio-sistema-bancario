import unittest
from src.utils import documento_existe, encontrar_usuario, exibir_dados_usuario

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.clientes = [
            {"cpf": "12345678901", "nome": "Cliente A", "endereco": "Endereço A"},
            {"cnpj": "12345678000195", "nome": "Cliente B", "endereco": "Endereço B"},
        ]

    def test_documento_existe_cpf(self):
        self.assertTrue(documento_existe("12345678901", self.clientes))

    def test_documento_existe_cnpj(self):
        self.assertTrue(documento_existe("12345678000195", self.clientes))

    def test_documento_nao_existe(self):
        self.assertFalse(documento_existe("00000000000", self.clientes))

    def test_encontrar_usuario_cpf(self):
        usuario = encontrar_usuario(self.clientes, "12345678901")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario["nome"], "Cliente A")

    def test_encontrar_usuario_cnpj(self):
        usuario = encontrar_usuario(self.clientes, "12345678000195")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario["nome"], "Cliente B")

    def test_encontrar_usuario_nao_existe(self):
        usuario = encontrar_usuario(self.clientes, "00000000000")
        self.assertIsNone(usuario)

    def test_exibir_dados_usuario(self):
        usuario = {"nome": "Cliente A", "cpf": "12345678901", "endereco": "Endereço A"}
        with self.assertLogs() as log:
            exibir_dados_usuario(usuario)
        self.assertIn("Nome: Cliente A", log.output[0])
        self.assertIn("CPF: 12345678901", log.output[0])
        self.assertIn("Endereço: Endereço A", log.output[0])

if __name__ == '__main__':
    unittest.main()