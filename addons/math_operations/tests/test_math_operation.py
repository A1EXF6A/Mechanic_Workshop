from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import time

class TestMathOperation(TransactionCase):

    def setUp(self):
        super().setUp()
        self.MathOperation = self.env['math.operation']

    def test_sum_operation(self):
        start = time.time()
        op = self.MathOperation.create({
            'operand_1': 2,
            'operand_2': 3,
            'operation_type': 'suma'
        })
        self.assertEqual(op.result, 5)
        end = time.time()
        print(f"Sum operation time: {end - start}")


    def test_subtraction_operation(self):
        start = time.time()
        op = self.MathOperation.create({
            'operand_1': 10,
            'operand_2': 4,
            'operation_type': 'resta'
        })
        self.assertEqual(op.result, 6)
        end = time.time()
        print(f"Subtraction operation time: {end - start}")

    def test_multiplication_operation(self):
        start = time.time()
        op = self.MathOperation.create({
            'operand_1': 4,
            'operand_2': 5,
            'operation_type': 'multiplicacion'
        })
        self.assertEqual(op.result, 20)
        end = time.time()
        print(f"Multiplication operation time: {end - start}")

    def test_division_operation(self):
        start = time.time()
        op = self.MathOperation.create({
            'operand_1': 20,
            'operand_2': 4,
            'operation_type': 'division'
        })
        self.assertEqual(op.result, 5)
        end = time.time()
        print(f"Division operation time: {end - start}")

    def test_division_by_zero(self):
        start = time.time()
        with self.assertRaises(ValidationError):
            self.MathOperation.create({
                'operand_1': 10,
                'operand_2': 0,
                'operation_type': 'division'
            })
        end = time.time()
        print(f"Division by zero operation time: {end - start}")