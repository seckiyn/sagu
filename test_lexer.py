from typing import List
from lexer import Token, Lexer
from logs import print_info
def lex_to_tokens(text) -> List[Token]:
    lexer = Lexer(text)
    token = lexer.get_next_token()
    tokens = list()
    while token.token_value:
        tokens.append(token)
        token = lexer.get_next_token()
    return tokens

def tokenize(string):
    print_info(lex_to_tokens(string))

def test_lexer_tokens():
    # No input empty string
    string = ""
    tokenize(string)

    # Test integer
    string = "123"
    tokenize(string)

    # Test math tokens
    string = "1 + 2 - 3 / 4"
    tokenize(string)

    # Test parenthesis
    string = "(1 + 3) - 4"
    tokenize(string)

if __name__ == "__main__":
    test_lexer_tokens()
