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


def readOpenParenthesis(line, index):
    token = {'type': '('}
    return token, index + 1


def readCloseParenthesis(line, index):
    token = {'type': ')'}
    return token, index + 1


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def readMultiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def readDivision(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def tokenize(line):
    ''' break an expression into tokens'''
    operators = {'+': readPlus, '-': readMinus, '/': readDivision, '*': readMultiply,
                 '(': readOpenParenthesis, ')': readCloseParenthesis}

    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] in operators.keys():
            (token, index) = operators[line[index]](line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def parse(tokens):
    precedences = {'PLUS': 0, 'MINUS': 0, 'MULTIPLY': 1, 'DIVIDE': 1}

    def greater_precedence(o1, o2): return precedences[o1] >= precedences[o2]

    def last_element(l): return l[-1]['type'] if l else None

    # STACKS
    numbers = []
    operators = []

    for token in tokens:
        if token['type'] == 'NUMBER':
            numbers.append(token)
        elif token['type'] == '(':
            operators.append(token)
        elif token['type'] == ')':  # if its ) then do the calculation untill encounter to (
            top = last_element(operators)
            while top and top != '(':
                apply_op(operators, numbers)
                top = last_element(operators)
            operators.pop()  # remove (
        else:
            top = last_element(operators)
            # process the old operator before appending new one if it has high precedence
            while top and top not in "(" and greater_precedence(top, token['type']):
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
    numbers.append(evaluate([left, operator, right]))


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    index = 1

    # Handle * and / first
    while index < len(tokens):
        number = 0
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY':
                number = tokens[index - 2]['number'] * tokens[index]['number']
                tokens = tokens[:index - 2] + [{'type': 'NUMBER', 'number': number}] + tokens[index + 1:]
                index -= 2
            elif tokens[index - 1]['type'] == 'DIVIDE':
                number = tokens[index - 2]['number'] / tokens[index]['number']
                tokens = tokens[:index - 2] + [{'type': 'NUMBER', 'number': number}] + tokens[index + 1:]
                index -= 2
            elif tokens[index - 1]['type'] not in ['MINUS', "PLUS"]:
                print('Invalid syntax')
                exit(1)

        index += 1
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return {'type': 'NUMBER', 'number': answer}


def test(line):
    tokens = tokenize(line)
    actualAnswer = parse(tokens)

    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
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
