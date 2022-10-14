import pytest
from typing import List
from lexer import Token, Lexer, TokenType
from logs import print_info, print_debug
from parser import Parser
def lex_to_tokens(text) -> List[Token]:
    lexer = Lexer(text)
    token = lexer.get_next_token()
    tokens = list([token])
    while token.token_type != TokenType.EOF:
        token = lexer.get_next_token()
        tokens.append(token)
    return tokens

def parse(string):
    tokens = lex_to_tokens(string)
    print("-"*200)
    print(*tokens, sep="\n")
    print("-"*200)
    parser = Parser(tokens)
    parsed = parser.parse()
    print_debug(parsed)
    print_info(parsed)

def test_lexer_tokens():
    # No input empty string
    string = ""
    print_info("Testing empty("") string")
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

    # Test SETVAR and WORD
    string = "var hesa = 1"
    print_info(f"Testing string({string})")
    parse(string)

    # Test equals sign
    string = "var hesa = 12 + 21"
    print_info(f"Testing string({string})")
    parse(string)

    # Test block start and end
    string = "{var hesa = 12 + 21}"
    print_info(f"Testing string({string})")
    parse(string)

    # Test logical operators
    string = "var hesa = 12 == 12"
    print_info(f"Testing string({string})")
    parse(string)

    # Test less than logical operator
    string = "var hesa = 12 < 12"
    print_info(f"Testing string({string})")
    parse(string)

    # Test less than logical operator
    string = "var hesa = 12 > 12"
    print_info(f"Testing string({string})")
    parse(string)

    # Test control flow
    string = "var hesa = true if hesa {var a = 12}"
    print_info(f"Testing string({string})")
    parse(string)

    # Test elif flow
    string = "var hesa = true var mustafa = false if hesa {var a = 12} elseif mustafa {var b= 23}"
    print_info(f"Testing string({string})")
    parse(string)

    # Test else flow
    string = "if hesa {var a = 12} else {var b = 23}"
    print_info(f"Testing string({string})")
    parse(string)

    # Function declaration
    string = "func name (a, b) {var a = 12}"
    print_info(f"Testing string({string})")
    parse(string)

    # Function call
    string = "func name (a, b) {var a = 12} name(12 + 23, true)"
    print_info(f"Testing string({string})")
    parse(string)

    # Function call at logical
    string = "func hesa (a, b) {var a = 12} var a = hesa(12 + 23, true)"
    print_info(f"Testing string({string})")
    parse(string)

    # Function returns
    string = "func hesa (a, b) {var a = 12 return a} var a = hesa(12 + 23, true)"
    print_info(f"Testing string({string})")
    parse(string)

    # While loops
    string =\
"""func fib(count)
        {
            var sum = 0
            var counter = 0
            while counter < count
            {
                var sum = counter + sum
            }
        }
"""
    print_info(f"Testing string({string})")
    parse(string)
if __name__ == "__main__":
    test_lexer_tokens()
