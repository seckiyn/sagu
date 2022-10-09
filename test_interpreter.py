import pytest
from typing import List
from lexer import Token, Lexer
from logs import print_info, print_debug, print_error
from parser import Parser
from interpreter import Interpreter

def lex_to_tokens(text) -> List[Token]:
    lexer = Lexer(text)
    token = lexer.get_next_token()
    tokens = list([token])
    while token.token_value:
        token = lexer.get_next_token()
        tokens.append(token)
    return tokens

def interpret(string):
    tokens = lex_to_tokens(string)
    print_error(tokens)
    parser = Parser(tokens)
    interpreter = Interpreter(parser.parse())
    print_info(interpreter.interpret())

def test_interpreter_tokens():
    # No input empty string
    string = ""
    print_info("Testing empty("") string")
    interpret(string)

    # Test integer
    string = "123"
    print_info("Testing string('123') string")
    interpret(string)

    # Test basic math
    string = "1 + 2"
    print_info("Testing string('1 + 2') string")
    interpret(string)

    # Test math tokens
    print_info("Testing string('1 + 2 - 3 / 4') string")
    string = "1 + 2 - 3 / 4"
    interpret(string)

    # Test parenthesis
    print_info("Testing paren('(1 + 3) - 4') string")
    string = "(1 + 3) - 4"
    interpret(string)

    # Test unary op
    print_info("Testing unary('-1 + +2') string")
    string = "-1 + +2"
    interpret(string)

    # Test SETVAR and WORD
    string = "var hesa = 1"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test equals sign
    string = "var hesa = 12 + 21"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test block start and end
    string = "{var hesa = 12 + 21}"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test variable math
    string = "{var hesa = 12 + 21 var mustafa = 12 var hello = 2 * hesa + mustafa}"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test logical math
    string = "var hesa = 12 == 12"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test less than logical operator
    string = "var hesa = 12 < 12"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test less than logical operator
    string = "var hesa = 12 > 12"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test math ops with logical operators
    string = "var hesa = 3 * true + false"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test control flow
    string = "var hesa = true if hesa {var a = 12}"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test elif flow
    string = "var hesa = true var mustafa = false if hesa {var a = 12} elif mustafa {var b= 23}"
    print_info(f"Testing string({string})")
    interpret(string)

    # Test else flow
    string = "var hesa = false if hesa {var a = 12} else {var b = 23}"
    print_info(f"Testing string({string})")
    interpret(string)
if __name__ == "__main__":
    test_interpreter_tokens()
