import pytest
from typing import List
from lexer import Token, Lexer
from logs import print_info, print_debug
from parser import Parser
def lex_to_tokens(text) -> List[Token]:
    lexer = Lexer(text)
    token = lexer.get_next_token()
    tokens = list([token])
    while token.token_value:
        token = lexer.get_next_token()
        tokens.append(token)
    return tokens

def parse(string):
    tokens = lex_to_tokens(string)
    print_debug(tokens)
    parser = Parser(tokens)
    print_info(parser.parse())

def test_lexer_tokens():
    # No input empty string
    string = ""
    print_info("Testing empty("") string")
    with pytest.raises(Exception):
        parse(string)

    # Test integer
    string = "123"
    print_info("Testing string('123') string")
    parse(string)

    # Test basic math
    string = "1 + 2"
    print_info("Testing string('1 + 2') string")
    parse(string)

    # Test math tokens
    print_info("Testing string('1 + 2 - 3 / 4') string")
    string = "1 + 2 - 3 / 4"
    parse(string)

    # Test parenthesis
    print_info("Testing paren('(1 + 3) - 4') string")
    string = "(1 + 3) - 4"
    parse(string)

    # Test unary op
    print_info("Testing unary('-1 + +2') string")
    string = "-1 + +2"
    parse(string)

if __name__ == "__main__":
    test_lexer_tokens()
