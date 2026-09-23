from .errors import EmptyExpression, UnknownSymbol, InvalidNumber, MissingOperand, TwoOperators, DivisionByZero
def tokenize_fsm(expr):
    tokens = []
    state = "START"
    current_token = ""
    flag = 0

    for char in expr:
        if state == "START":
            if char.isspace():
                continue
            if char.isdigit():
                state = "NUMBER"
                current_token = char
            # дописать, не забываем про числа с точкой
            elif char in ["+", "-", "*", "/"]:
                tokens.append(("OP", char))
            else:
                raise UnknownSymbol(f"Недопустимый символ: {char}")

        elif state == "NUMBER":
            if char.isspace():
                tokens.append(("NUMBER", float(current_token)))
                state = "START"
                flag = 1
                current_token = ""
            elif char.isdigit():
                current_token += char
            elif char in ["-", "+", "/", "*"]:
                tokens.append(("NUMBER", float(current_token)))
                flag = 1
                tokens.append(("OP", char))
                current_token = ""
                state = "START"
            elif char == ".":
                if current_token.count(".") < 1:
                    current_token += char
                else:
                    raise InvalidNumber(f"Недопустимое число: {char}")
            else:
                raise UnknownSymbol(f"Недопустимый символ: {char}")

    # Завершающая обработка
    if state == "NUMBER":
        tokens.append(("NUMBER", float(current_token)))
        flag = 1

    if flag == 0:
        raise EmptyExpression("Выражение не содержит чисел")
    elif len(tokens) > 0:
        return tokens
    else:
        raise EmptyExpression("Пустая строка ввода")


def unary(tokens):
    res_tokens = []
    prev = ""
    for typ, value in tokens:
        if typ == "OP" and value in "-+" and (prev == "" or prev == "OP"):
            res_tokens.append(("OP", "u" + value))

        elif typ == "OP" and prev == "OP":
            raise TwoOperators("Недопустимая операция")
        
        elif typ == "NUMBER":
            res_tokens.append(("NUMBER", value))
        else:
            res_tokens.append(("OP", value))
        prev = typ

    if prev == "OP":
        raise MissingOperand("Пропущен операнд")
    return res_tokens


my_dict = {"u+": 3, "u-": 3, "*": 2, "/": 2, "+": 1, "-": 1}


def to_rpn(tokens):
    my_stack = []
    output = []
    for char in tokens:
        if char[0] == "NUMBER":
            output.append(char[1])
        elif char[0] == "OP":
            while my_stack and my_dict[my_stack[-1]] >= my_dict[char[1]]:
                output.append(my_stack.pop())
            my_stack.append(char[1])
    while my_stack:
        output.append(my_stack.pop())
    return output


def eval_rpn(rpn_expr):
    my_stack = []
    for char in rpn_expr:
        if isinstance(char, float):
            my_stack.append(char)
        elif char == "u-":
            my_stack.append(-my_stack.pop())
        elif char == "u+":
            pass
        else:
            b = my_stack.pop()
            a = my_stack.pop()
            if char == "+":
                my_stack.append(a + b)
            elif char == "-":
                my_stack.append(a - b)
            elif char == "*":
                my_stack.append(a * b)
            elif char == "/":
                if b == 0:
                    raise DivisionByZero(f"Деление на 0 недопустимо: {a}/{b}")
                else:
                    my_stack.append(a / b)
    return my_stack[0]


def calculate(expression):
    tokens = tokenize_fsm(expression)
    tokens = unary(tokens)
    rpn = to_rpn(tokens)
    return eval_rpn(rpn)
     
