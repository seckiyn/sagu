from enum import Enum, auto
from dataclasses import dataclass
from typing import Union

class TokenType(Enum):
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    DIV = auto()
    MUL = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

@dataclass
class Token:
    token_type: TokenType
    token_value: Union[int, str, None]

DIGITS = "1234567890"
IGNORE_CHARACTERS = "\n "
class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = -1
        self.current_char = None
        self.advance()
    def error(text):
        raise Exception(text)
    def advance(self):
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None
    def in_range(self):
        """
            Return if position in text range
        """
        return self.position < len(text)
    def get_integer(self):
        integer = ""
        while self.current_char and self.current_char in DIGITS:
            integer += self.current_char
            self.advance()
        return int(integer)
    def get_next_token(self):
        assert len(TokenType) == 8, "You forgot to implement a token"
        while self.current_char:
            if self.current_char in DIGITS:
                token_type = TokenType.INTEGER
                token_value = self.get_integer()
                token = Token(token_type, token_value)
                # self.advance()
                return token
            if self.current_char == "+":
                token_type = TokenType.PLUS
                token_value = "+"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "-":
                token_type = TokenType.MINUS
                token_value = "-"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "*":
                token_type = TokenType.MUL
                token_value = "*"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "/":
                token_type = TokenType.DIV
                token_value = "/"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "(":
                token_type = TokenType.LPAREN
                token_value = "("
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == ")":
                token_type = TokenType.RPAREN
                token_value = ")"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char in IGNORE_CHARACTERS:
                self.advance()
                continue
            self.error(f"Unreachable character {self.current_char}")

        return Token(TokenType.EOF, None)
