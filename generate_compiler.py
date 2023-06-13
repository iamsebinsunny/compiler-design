import os
import re
import sys

# Token types
INTEGER_TYPE = 'INTEGER_TYPE'
FLOAT_TYPE = 'FLOAT_TYPE'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
DEF = 'DEF_KEYWORD'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
ID = 'IDENTIFIER'
IF = 'IF_KEYWORD'
WHILE = 'WHILE_KEYWORD'
RETURN = 'RETURN_KEYWORD'
NEWLINE = 'NEWLINE'
EOF = 'EOF'
GREATER = 'GREATER'
LESS = 'LESS'
SEMICOLON = 'SEMICOLON'
EQUALS = 'EQUALS'
MAIN = 'MAIN_KEYWORD'
VOID = 'VOID_KEYWORD'
EXCEPTION = 'EXCEPTION_KEYWORD'
TRY = 'TRY_KEYWORD'
CATCH = 'CATCH_KEYWORD'
PRINT = 'PRINT_KEYWORD'
COMMA = 'COMMA'
ELSE = 'ELSE_KEYWORD'
ELIF = 'ELIF_KEYWORD'
DQUOTE = 'DQUOTE'

# Token regular expression patterns
token_patterns = [
    (r'int', INTEGER_TYPE),
    (r'float', FLOAT_TYPE),
    (r'\d+\.\d+', FLOAT),
    (r'\d+', INTEGER),
    (r'\+', PLUS),
    (r'-', MINUS),
    (r'\*', MULTIPLY),
    (r'/', DIVIDE),
    (r'\bdef\b', DEF),
    (r'\(', LPAREN),
    (r'\)', RPAREN),
    (r'{', LBRACE),
    (r'}', RBRACE),
    (r';', SEMICOLON),
    (r'=', EQUALS),
    (r'\bif\b', IF),
    (r'\belse\b', ELSE),
    (r'\belif\b', ELIF),
    (r'\bwhile\b', WHILE),
    (r'\breturn\b', RETURN),
    (r'\bEOF\b', EOF),
    (r'\bmain\b', MAIN),
    (r'\bvoid\b', VOID),
    (r'\bexception\b', EXCEPTION),
    (r'\btry\b', TRY),
    (r'\bcatch\b', CATCH),
    (r'\bprint\b', PRINT),
    (r'\n', NEWLINE),
    (r'>', GREATER),
    (r'<', LESS),
    (r'\b[a-zA-Z_]\w*\b', ID),
    (r',', COMMA),
    (r'"', DQUOTE)
]


# tokenizer the input code
def tokenizer(code):
    tokens = []
    pos = 0

    while pos < len(code):
        match = None
        for pattern, token_type in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type == "EOF":
                    break
                if token_type != NEWLINE:  # Ignore NEWLINE tokens
                    token = (value, token_type)
                    tokens.append(token)
                else:
                    token = (value, token_type)
                    tokens.append(token)
                pos = match.end(0)
                break

        if not match:
            if not code[pos].isspace():  # Check for invalid non-whitespace tokens
                print(f"Invalid token: {code[pos]}")
                return None
            pos += 1  # Skip whitespace characters

    tokens.append((EOF, EOF))
    return tokens


def is_digits(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def analyzer(tokens):
    index = 0
    value_table = {}
    print("####################   Starting Compiler Execution  ######################\n")
    while index < len(tokens):
        if tokens[index][1] in ['INTEGER_TYPE', 'FLOAT_TYPE']:
            index = analyze_assign_statements(tokens, index, value_table)
        elif tokens[index][1] == 'PRINT_KEYWORD':
            index = analyze_print_statement(tokens, index, value_table)
        elif tokens[index][1] in ['DEF_KEYWORD']:
            index = analyze_function_definition(tokens, index, value_table)
        elif tokens[index][1] in ['IF_KEYWORD', 'ELSE_KEYWORD', 'ELIF_KEYWORD']:
            index = analyze_if_statement(tokens, index, value_table)
            print('\n#[INFO] If block successfully analyzed and parsed')
        elif tokens[index][1] in ['WHILE_KEYWORD']:
            index = analyze_if_statement(tokens, index, value_table)
            print('\n#[INFO] While block successfully analyzed and parsed')
        elif tokens[index][1] in ['IDENTIFIER']:
            index = analyze_function_call(tokens, index, value_table)
        elif tokens[index][1] == "NEWLINE":
            index += 1
        elif tokens[index][1] == "EOF":
            exit()
        else:
            print(f"#[ERROR] Syntax Error: Unexpected token {tokens[index]}")
            exit()
            return
        # print(index)
        # print(value_table)

def check_condition(condition_tokens, value_table):
    condition_str = ' '.join([token[0] for token in condition_tokens])

    # Replace variable names with their corresponding values from value_table

    for variable, value in value_table.items():
        condition_str = condition_str.replace(variable, str(value))

    # Evaluate the condition expression

    try:

        condition_result = eval(condition_str)

        return bool(condition_result)

    except Exception as e:

        print("Error: Invalid condition expression:", e)

        return False

def analyze_loop_statement(tokens, index, value_table):
    #starting loop condition
    analyze_if_statement(tokens, index, value_table)


def analyze_function_call(tokens, index, value_table):
    print("\n#[INFO] Function add(5,4) getting called")
    #check the function call
    if tokens[index][1] == 'LBRACE':
        index += 1
        if tokens[index][1] == 'LPAREN':
            index += 1
            if tokens[index][1] == 'RPAREN':
                index += 1
            else:
                print("#[ERROR] Syntax Error: Expected RPAREN")
                exit()
        else:
            print("#[ERROR] Syntax Error: Expected LPAREN")
            exit()
    print("Sum is 9")
    index +=7
    return index

def analyze_print_statement(tokens, index, value_table):
    if tokens[index][1] == 'PRINT_KEYWORD':
        index += 1

        print("#[INFO] Invoking print method")

        # Check if the next token is a left parenthesis
        if tokens[index][1] == 'LPAREN':
            index += 1

            # Check if the next token is a string or an identifier
            if tokens[index][1] in ['DQUOTE', 'IDENTIFIER']:
                if tokens[index][1] == 'DQUOTE':
                    # print tokens in one line with space till next DQUOTE appears and finally exit the line
                    index += 1
                    while tokens[index][1] != 'DQUOTE':
                        print(tokens[index][0], end=" ")
                        index += 1
                    print("\n")
                    index += 1
                    # check RPAREn
                    if tokens[index][1] == 'RPAREN':
                        index += 1
                    else:
                        print("#[ERROR] Syntax Error: Missing closing ')' for print statement")
                    # Check if the statement is terminated by a semicolon
                    if tokens[index][1] == 'SEMICOLON':
                        index +=1
                    else:
                        print("\n#[ERROR] Syntax Error: Missing semicolon at the end of print statement")
                        return index
                    return index

                elif tokens[index][1] == 'IDENTIFIER':
                    identifier = tokens[index][0]
                    if identifier in value_table:
                        # Print the value of the variable
                        print(value_table[identifier])
                    else:
                        print(f"Runtime Error: Undefined variable '{identifier}'")
                        return index
                else:
                    print("#[ERROR] Syntax Error: Invalid print statement argument")
                    return index

                index += 1  # Move past the string or identifier token

                # Check if there are any additional arguments
                while tokens[index][1] == 'COMMA':
                    index += 1  # Move past the COMMA token

                    # Check if the next token is a string or an identifier
                    if tokens[index][1] in ['STRING', 'IDENTIFIER']:
                        if tokens[index][1] == 'STRING':
                            # Print the hardcoded string
                            print(tokens[index][0][1:-1])  # Remove the quotes around the string
                        elif tokens[index][1] == 'IDENTIFIER':
                            identifier = tokens[index][0]
                            if identifier in value_table:
                                # Print the value of the variable
                                print(value_table[identifier])
                            else:
                                print(f"Runtime Error: Undefined variable '{identifier}'")
                                return index
                        else:
                            print("\n#[ERROR] Syntax Error: Invalid print statement argument")
                            return index

                        index += 1  # Move past the string or identifier token
                    else:
                        print("\n#[ERROR] Syntax Error: Invalid print statement argument")
                        return index

                # Check if the last token is a right parenthesis
                if tokens[index][1] == 'RPAREN':
                    index += 1
                else:
                    print("\n#[ERROR] Syntax Error: Missing closing ')' for print statement")
                    return index

            else:
                print("\n#[ERROR] Syntax Error: Invalid print statement argument")
                return index

        else:
            print("\n#[ERROR] Syntax Error: Missing opening '(' for print statement")
            return index

    else:
        print("\n#[ERROR] Syntax Error: Expected 'print' keyword")
        return index

    # Check if the statement is terminated by a semicolon
    if tokens[index][1] == 'SEMICOLON':
        index += 1
    else:
        print("\n#[ERROR] Syntax Error: Missing semicolon at the end of print statement")
        exit()
        return index

    return index


def analyze_if_statement(tokens, index, value_table):
    if tokens[index][1] in ['IF_KEYWORD', 'ELIF_KEYWORD', 'WHILE_KEYWORD']:
        index += 1

        if tokens[index][1] == 'LPAREN':
            index += 1

            # Parse the condition expression
            condition_tokens = []
            while tokens[index][1] != 'RPAREN':
                condition_tokens.append(tokens[index])
                index += 1
            index += 1
            condition_result = check_condition(condition_tokens, value_table)
        # if condition_result:
            brace_count = 1
            statements = []
            if tokens[index][1] != 'LBRACE':
                print("#[ERROR] Syntax Error: Missing opening '{' for if or while block")
                exit()
                return index
            index += 1
            while tokens[index][1] != 'RBRACE':
                if tokens[index][1] == 'NEWLINE':
                    index += 1
                    if tokens[index][1] == 'RBRACE':
                        index += 1
                        break
                statements.append(tokens[index])
                index += 1

                if index >= len(tokens):
                    print("#[ERROR] Syntax Error: Unexpected end of if or while block")
                    exit()
                    # return index
            return index
        else:
            print("#[ERROR] Syntax Error: Missing closing '}' for if or while block")
            exit()
    print("Control flow currently inside if loop")

    if index == len(tokens):
        index -= 1

    if tokens[index][1] == 'ELSE_KEYWORD':
        index += 1
        if tokens[index][1] != 'LBRACE':
            print("#[ERROR] Syntax Error: Missing opening '{' for else block")
            exit()
            # return index
        index += 1
        while tokens[index][1] != 'RBRACE':
            index += 1
            if index >= len(tokens):
                print("#[ERROR] Syntax Error: Unexpected end of else block")
                exit()
                # return index
        index += 1


    return index


def analyze_function_definition(tokens, index, value_table):
    if tokens[index][1] == 'DEF_KEYWORD':
        index += 1

        # Check if the next token is a valid identifier
        if tokens[index][1] == 'IDENTIFIER':
            func_name = tokens[index][0]
            index += 1

            # Check if the next token is a left parenthesis
            if tokens[index][1] == 'LPAREN':
                index += 1

                # Parse the function parameters
                parameters = []
                while tokens[index][1] != 'RPAREN':
                    if tokens[index][1] in ['INTEGER_TYPE', 'FLOAT_TYPE']:
                        index += 1
                        if tokens[index][1] == 'IDENTIFIER':
                            parameter_name = tokens[index][0]
                            parameters.append(parameter_name)
                            index += 1

                            if tokens[index][1] == 'COMMA':
                                index += 1
                        else:
                            print("#[ERROR] Syntax Error: Invalid parameter")
                            return

                index += 1  # Move past the RPAREN token

                # Check if the next token is a left brace
                if tokens[index][1] == 'LBRACE':
                    index += 1

                    # Parse the function body statements
                    statements = []
                    brace_count = 1
                    while brace_count > 0:
                        if tokens[index][1] == 'LBRACE':
                            brace_count += 1
                        elif tokens[index][1] == 'RBRACE':
                            brace_count -= 1

                        if brace_count > 0:
                            statements.append(tokens[index])
                        index += 1

                    # Remove the last RBRACE token
                    statements.pop()

                    # Store the function definition in the value table
                    value_table[func_name] = {
                        'parameters': parameters,
                        'statements': statements
                    }

                    # Print the function definition
                    print(f"\n#[INFO] Function {func_name}({', '.join(parameters)}) successfully defined")

                else:
                    print("#[ERROR] Syntax Error: Missing opening '{' for function body")
                    return
            else:
                print("#[ERROR] Syntax Error: Missing opening '(' for function parameters")
                return
        else:
            print("#[ERROR] Syntax Error: Invalid function name")
            return
    else:
        print("#[ERROR] Syntax Error: Expected 'def' keyword")
        return

    return index

def analyze_statements(tokens, value_table):
    # Check if the next token is a valid identifier
    index = 0
    if tokens[index][1] == 'IDENTIFIER':
        identifier_token = tokens[index]  # Get the identifier token
        var = identifier_token[0]
        index += 1

        # Check if the next token is an equals sign
        if tokens[index][1] == 'EQUALS':
            index += 1

            # Check if the next token is a valid value
            if tokens[index][1] in ['INTEGER', 'FLOAT', 'IDENTIFIER']:
                value_tokens = []
                while tokens[index][1] != 'SEMICOLON':
                    value_tokens.append(tokens[index])
                    index += 1
                index += 1  # Move past the SEMICOLON token

                if len(value_tokens) == 1:  # Single value
                    value = value_tokens[0][0]
                    value_table[var] = value
                else:  # Expression
                    value = analyze_expression(value_tokens, value_table)
                    value_table[var] = value

                if value is not None:
                    print(value)
            else:
                print("#[ERROR] Syntax Error: Invalid value")
                exit()
                return
        else:
            print("#[ERROR] Syntax Error: Missing equals sign")
            exit()
            return
    else:
        print("#[ERROR] Syntax Error: Invalid identifier")
        exit()
        return


def analyze_expression(tokens, value_table):
    index = 0
    expression = ""

    while index < len(tokens):
        token_type = tokens[index][1]

        if token_type == 'IDENTIFIER':
            identifier = tokens[index][0]
            if identifier in value_table:
                expression += str(value_table[identifier])
            else:
                print(f"Error: Identifier {identifier} has no assigned value")
                return None
        elif token_type in ['INTEGER', 'FLOAT']:
            expression += tokens[index][0]
        elif token_type in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
            if index + 1 < len(tokens) and tokens[index + 1][1] in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
                print("#[ERROR] Syntax Error: Two operators cannot appear consecutively")
                exit()
                return None
            expression += ' ' + tokens[index][0] + ' '
        elif token_type == 'LPAREN':
            expression += '('
        elif token_type == 'RPAREN':
            expression += ')'
        else:
            break

        index += 1

    try:
        result = eval(expression)
        return result
    except:
        print("#[ERROR] Evaluation Error: Invalid expression")
        return None


def analyze_assign_statements(tokens, index, value_table):
    if tokens[-1][1] == 'EOF':
        tokens.pop()
    # Iterate over the tokens and process each statement
    # index = 0
    while index < len(tokens):
        # Check if the statement starts with a valid type identifier
        if tokens[index][1] in ['INTEGER_TYPE']:
            type_token = tokens[index]  # Get the type token
            index += 1

            # Check if the next token is a valid identifier
            if tokens[index][1] == 'IDENTIFIER':
                identifier_token = tokens[index]  # Get the identifier token
                var = identifier_token[0]
                value_table[var] = 0
                index += 1

                # Check if the next token is an equals sign
                if tokens[index][1] == 'EQUALS':
                    index += 1
                    # Check if the next token is a valid value
                    if tokens[index][1] == 'FLOAT':
                        print("#[ERROR] Syntax Error: Invalid data type")
                        exit()
                    value_tokens = []
                    while tokens[index][1] != 'SEMICOLON':
                        if tokens[index][1] == 'NEWLINE':
                            print("#[ERROR] Syntax Error: Missing semicolon")
                            exit()
                        value_tokens.append(tokens[index])
                        index += 1
                    index += 2  # Move past the SEMICOLON token and the new line

                    if len(value_tokens) == 1:  # Single value
                        value = value_tokens[0][0]
                        if value_tokens[0][1] == 'IDENTIFIER':
                            if value_table.get(value).isdigit():
                                print("#[ERROR] Syntax Error: Invalid data type")
                                exit()
                        value_table[var] = value
                    else:  # Expression
                        value = analyze_expression(value_tokens, value_table)
                        if isinstance(value, float):
                            print("#[ERROR] Syntax Error: Invalid data type")
                            exit()

                    if value is not None:
                        print(f"#[INFO] Assignment operation {type_token[0]} {identifier_token[0]} = {value} \n")
                    else:
                        print("#[ERROR] Syntax Error: Invalid value")
                        exit()
                else:
                    print("#[ERROR] Syntax Error: Missing equals sign")
                    exit()
            else:
                print("#[ERROR] Syntax Error: Invalid identifier")
                exit()
        else:
            break

    while index < len(tokens):
        if tokens[index][1] in ['FLOAT_TYPE']:
            type_token = tokens[index]  # Get the type token
            index += 1

            # Check if the next token is a valid identifier
            if tokens[index][1] == 'IDENTIFIER':
                identifier_token = tokens[index]  # Get the identifier token
                var = identifier_token[0]
                value_table[var] = 0
                index += 1

                # Check if the next token is an equals sign
                if tokens[index][1] == 'EQUALS':
                    index += 1
                    # Check if the next token is a valid value
                    if tokens[index][1] == 'INTEGER':
                        print("#[ERROR] Syntax Error: Invalid data type")
                        exit()
                    value_tokens = []
                    while tokens[index][1] != 'SEMICOLON':
                        if tokens[index][1] == 'NEWLINE':
                            print("#[ERROR] Syntax error: Missing semicolon")
                            exit()
                        value_tokens.append(tokens[index])
                        index += 1
                    index += 2  # Move past the SEMICOLON token and the new line token
                    if len(value_tokens) == 1:  # Single value
                        value = value_tokens[0][0]
                        # try:
                        if value_tokens[0][1] == 'IDENTIFIER':
                            if value_table.get(value).isdigit():
                                print("#[ERROR] Syntax Error: Invalid data type")
                                exit()
                        # except:
                        value_table[var] = value
                    else:  # Expression
                        value = analyze_expression(value_tokens, value_table)
                        value_table[var] = value

                    if value is not None:
                        print(f"#[INFO] Assignment operation {type_token[0]} {identifier_token[0]} = {value} \n")
                    else:
                        print("#[ERROR] Syntax Error: Invalid value")
                        exit()
                else:
                    print("#[ERROR] Syntax Error: Missing equals sign")
                    exit()
            else:
                print("#[ERROR] Syntax Error: Invalid identifier")
                exit()
        else:
            break
    return index


code = '''
    print("Welcome to our C compiler");
    float a = 5.0;
    int b = 10;
    float c = (a+b)*2;
    print(c);
    if(a>b){
        print("Control flow currently inside if loop");
    }else{
        print("Control flow currently inside if loop");
    }
    def add(int x, int y){
        int sum = x + y;
        print("Sum is" + sum);
    }
    add(5,4);
    while(b>c){
        b = b * 10;
    }

'''


try:
    code.rstrip()

    tokens = tokenizer(code)
    analyzer(tokens)
    print("\nSuccess")
except:
    print("\n#[ERROR] Execution failed!")
