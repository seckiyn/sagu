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
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test integer
    string = "123"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test math tokens
    string = "1 + 2 - 3 / 4"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test parenthesis
    string = "(1 + 3) - 4"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test SETVAR and WORD
    string = "var hesa"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test equals sign
    string = "var hesa = 12 + 21"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test block start and end
    string = "{var hesa = 12 + 21}"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test logical operators
    string = "var hesa = 12 == 12"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test less than logical operator
    string = "var hesa = 12 < 12"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test less than logical operator
    string = "var hesa = 12 > 12"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test true literal
    string = "var hesa = true"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test false literal
    string = "var hesa = false"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test control flow
    string = "var hesa = true if hesa {var a = 12}"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test elif flow
    string = "var hesa = true var mustafa = false if hesa {var a = 12} elif mustafa {var b= 23}"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Test else flow
    string = "if hesa {var a = 12} else {var b = 23}"
    print_info(f"Testing string({string})")
    tokenize(string)

    # Function declaration
    string = "func name (a, b) {var a = a + 12}"
    print_info(f"Testing string({string})")
    tokenize(string)




if __name__ == "__main__":
    test_lexer_tokens()
