import pytest
from typing import List
from lexer import Token, Lexer
from logs import print_info, print_debug
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
    parser = Parser(tokens)
    parsed = parser.parse()
    interpreter = Interpreter(parsed)
    print_info(interpreter.interpret())

def test_interpreter_tokens():
    # No input empty string
    string = ""
    print_info("Testing empty("") string")
    with pytest.raises(Exception):
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

if __name__ == "__main__":
    test_interpreter_tokens()
