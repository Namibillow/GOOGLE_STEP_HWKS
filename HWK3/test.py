import unittest

from HWK3 import calculate


class TestCalculator(unittest.TestCase):

    def test_no_op(self):
        pos = '1'
        decimal = '3.141519'

        self.assertEqual(calculate(pos), eval(pos))
        self.assertEqual(calculate(decimal), eval(decimal))

    def test_addition(self):
        addition1 = '2+2'
        addition2 = '4+3+4'
        addition3 = '3.14+2.22'
        addition4 = '0+0.11'
        addition5 = '1.1+2'

        self.assertEqual(calculate(addition1), eval(addition1))
        self.assertEqual(calculate(addition2), eval(addition2))
        self.assertEqual(calculate(addition3), eval(addition3))
        self.assertEqual(calculate(addition4), eval(addition4))
        self.assertEqual(calculate(addition5), eval(addition5))

    def test_subtraction(self):
        sub1 = '5-2'
        sub2 = '2-4'
        sub3 = '3.14-2.22'
        sub4 = '999-1.111'
        sub5 = '-10-11'
        sub5 = '3.14-2'

        self.assertEqual(calculate(sub1), eval(sub1))
        self.assertEqual(calculate(sub2), eval(sub2))
        self.assertEqual(calculate(sub3), eval(sub3))
        self.assertEqual(calculate(sub4), eval(sub4))
        self.assertEqual(calculate(sub5), eval(sub5))

    def test_multiply(self):
        mul1 = '5*2'
        mul2 = '992*3'
        mul3 = '3.14*3.35'
        mul4 = '0*4'
        mul5 = '1.1*100'

        self.assertEqual(calculate(mul1), eval(mul1))
        self.assertEqual(calculate(mul2), eval(mul2))
        self.assertEqual(calculate(mul3), eval(mul3))
        self.assertEqual(calculate(mul4), eval(mul4))
        self.assertEqual(calculate(mul5), eval(mul5))

    def test_division(self):
        div1 = '5/2'
        div2 = '10/2/5'
        div3 = '100/10/10'
        div4 = '1/2'
        div5 = '3.12/2'
        div6 = '2/1.1'
        self.assertEqual(calculate(div1), eval(div1))
        self.assertEqual(calculate(div2), eval(div2))
        self.assertEqual(calculate(div3), eval(div3))
        self.assertEqual(calculate(div4), eval(div4))
        self.assertEqual(calculate(div5), eval(div5))
        self.assertEqual(calculate(div6), eval(div6))

    def test_errors(self):
        zero_div = '1/0'
        self.assertRaises(ZeroDivisionError, calculate, zero_div)

    def test_two_op(self):
        minus_plus = '1-2+10'
        minus_plus2 = '100+2+10-4-19'
        self.assertEqual(calculate(minus_plus), eval(minus_plus))
        self.assertEqual(calculate(minus_plus2), eval(minus_plus2))

        plus_multiply = '10*2*3+5'
        plus_multiply2 = '7+1+5*5+2+3'
        self.assertEqual(calculate(plus_multiply), eval(plus_multiply))
        self.assertEqual(calculate(plus_multiply2), eval(plus_multiply2))

        plus_div = '1+1/2'
        plus_div_decimal = '5/2+2.53'
        self.assertEqual(calculate(plus_div), eval(plus_div))
        self.assertEqual(calculate(plus_div_decimal), eval(plus_div_decimal))

        minus_div = '10-2/2'
        minus_mul = '1*5-2'
        self.assertEqual(calculate(minus_div), eval(minus_div))
        self.assertEqual(calculate(minus_mul), eval(minus_mul))

        div_mul = '10/2*5'
        div_mul2 = '45*2/2'
        self.assertEqual(calculate(div_mul), eval(div_mul))
        self.assertEqual(calculate(div_mul2), eval(div_mul2))

        minus_div_decimal = '10.11*2-10'
        div_mul_decimal = '100/5.5*1.9'
        self.assertEqual(calculate(minus_div_decimal), eval(minus_div_decimal))
        self.assertEqual(calculate(div_mul_decimal), eval(div_mul_decimal))

    def test_three_op(self):
        op1 = '1+2*3-4'
        op2 = '3*3/9-1+2.11'
        op3 = '1*1*1*2/2'
        op4 = '5+5-2.4/2'
        self.assertEqual(calculate(op1), eval(op1))
        self.assertEqual(calculate(op2), eval(op2))
        self.assertEqual(calculate(op3), eval(op3))
        self.assertEqual(calculate(op4), eval(op4))

    def test_parenthesis(self):
        op1 = '(1+2)*4*5'
        op2 = '((1*2)+3)-4'
        op3 = '((1+1))'
        op4 = '(1)'
        op5 = '((2+2)*(3*3))'
        op6 = '5*4-(4/2+3)+(2*2+(2+2))'
        self.assertEqual(calculate(op1), eval(op1))
        self.assertEqual(calculate(op2), eval(op2))
        self.assertEqual(calculate(op3), eval(op3))
        self.assertEqual(calculate(op4), eval(op4))
        self.assertEqual(calculate(op5), eval(op5))
        self.assertEqual(calculate(op6), eval(op6))


if __name__ == '__main__':
    unittest.main()
