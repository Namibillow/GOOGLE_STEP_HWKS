def readNumber(line, index):
    """ handles number """
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


TOKEN_MINUS = {'type': 'MINUS', 'precedence': 0}
TOKEN_PLUS = {'type': 'PLUS', 'precedence': 0}
TOKEN_MULTYPLY = {'type': 'MULTIPLY', 'precedence': 1}
TOKEN_DIVIDE = {'type': 'DIVIDE', 'precedence': 1}
TOKEN_OPEN_PARENT = {'type': 'OPEN_PARENT', 'precedence': 0}
TOKEN_CLOSE_PARENT = {'type': 'CLOSE_PARENT', 'precedence': 0}


def tokenize(line):
    ''' break an expression into tokens'''
    operators = {'+': TOKEN_PLUS, '-': TOKEN_MINUS, '/': TOKEN_DIVIDE, '*': TOKEN_MULTYPLY,
                 '(': TOKEN_OPEN_PARENT, ')': TOKEN_CLOSE_PARENT}

    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] in operators.keys():
            token = operators[line[index]]
            index += 1
        else:
            print('Invalid character found: ' + line[index])
            exit(1)

        tokens.append(token)
    return tokens


def parse(tokens):

    def greater_precedence(o1, o2): return o1['precedence'] >= o2['precedence']

    def last_element(l): return l[-1] if l else None

    # STACKS
    numbers = []
    operators = []

    for token in tokens:
        if token['type'] == 'NUMBER':
            numbers.append(token)
        elif token['type'] == 'OPEN_PARENT':
            operators.append(token)
        elif token['type'] == 'CLOSE_PARENT':  # if its ) then do the calculation untill encounter to (
            top = last_element(operators)
            while top and top['type'] != 'OPEN_PARENT':
                apply_op(operators, numbers)
                top = last_element(operators)
            operators.pop()  # remove (
        else:
            top = last_element(operators)
            # process the old operator before appending new one if it has high precedence
            while top and top['type'] != "OPEN_PARENT" and greater_precedence(top, token):
                apply_op(operators, numbers)
                top = last_element(operators)
            operators.append(token)

    while last_element(operators):
        apply_op(operators, numbers)

    return numbers[0]['number']


def apply_op(operators, numbers):
    '''apply the operation and append its answer to the stack'''
    operator = operators.pop()
    right = numbers.pop()
    left = numbers.pop()
    equation = {'left': left, 'operator': operator, 'right': right}
    numbers.append(evaluate(equation))


def evaluate(tokens):
    ans = 0
    op = tokens['operator']['type']
    if op == "MINUS":
        ans = tokens['left']['number'] - tokens['right']['number']
    elif op == "PLUS":
        ans = tokens['left']['number'] + tokens['right']['number']
    elif op == "MULTIPLY":
        ans = tokens['left']['number'] * tokens['right']['number']
    elif op == "DIVIDE":  # cover 0 division
        try:
            ans = tokens['left']['number'] / tokens['right']['number']
        except:
            raise ZeroDivisionError
    else:
        print('Invalid syntax')
        exit(1)

    return {'type': 'NUMBER', 'number': ans}


def calculate(line):
    ''' returns the actual answer '''
    return parse(tokenize(line))


def test(line):
    actualAnswer = calculate(line)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1")
    test("1/0")
    test("6/2")
    test("1+2")
    test("1.0+2.1-3")
    test("5*4/2")
    test('1.1+2.2-3.3')
    test('3.14/2+4')
    test("3*3*3/9")
    test("4.0/2.0+2")
    test("0.1+2.1*2")
    test("0.001*10")
    test("10/2/5")
    test('3.14*3.0')
    test("5/2.0")
    test("10./5")
    test('1*1*1*2/2')
    test('(1+2)*4*5')
    test('((1*2)+3)-4')
    test('5*4-(4/2+3)+(2*2+(2+2))')
    test('((1+1))')
    test('((2+2)*(3*3))')
    print("==== Test finished! ====\n")


if __name__ == "__main__":
    runTest()

    # decimal cannot be first character. eg: 0.13
    # input must be valid.
    # parenthesis must be matched

    # while True:
    #     print('> ', end="")
    #     line = input()
    #     tokens = tokenize(line)
    #     answer = parse(tokens)
    #     print("answer = %f\n" % answer)
