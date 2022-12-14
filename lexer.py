"""
    Lex a text into tokens
"""
from enum import Enum, auto
from dataclasses import dataclass
from typing import Union


class TokenType(Enum):
    """
        An enumeration for tokens
    """
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    DIV = auto()
    MUL = auto()
    LPAREN = auto()
    RPAREN = auto()

    # Language
    SET = auto()
    BLOCK_START = auto()
    BLOCK_END = auto()

    # Words
    WORD = auto()
    SETVAR = auto()
    EOF = auto()
    TRUE = auto()
    FALSE = auto()

    # Logical Operators
    EQUALS = auto()
    LTHAN = auto()
    GTHAN = auto()

    # Flow Control
    IF = auto()
    ELSEIF = auto()
    ELSE = auto()

    # Functions
    FUNC = auto()
    SEP = auto()
    RETURN = auto()

    # Loops
    WHILE = auto()

    # BUILT-IN DATA TYPES
    STRING_LITERAL = auto()


@dataclass
class Token:
    """
        Container for token
    """
    token_type: TokenType
    token_value: Union[int, str, None]


BUILT_IN_WORDS = {
        "var": TokenType.SETVAR,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "if": TokenType.IF,
        "elseif": TokenType.ELSEIF,
        "else": TokenType.ELSE,
        "func": TokenType.FUNC,
        "return": TokenType.RETURN,
        "while": TokenType.WHILE,
    }
DIGITS = "1234567890"
IGNORE_CHARACTERS = "\n "


class Lexer:
    """
        Main class to lexing
    """
    def __init__(self, text):
        self.text = text
        self.position = -1
        self.current_char = None
        self.advance()

    def error(self, text):
        """
            Raise error when necessary
        """
        position = self.position
        raise Exception(f"At position {position}" + text)

    def advance(self):
        """
            Advance the position and sets the new character
            according to this position
        """
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None

    def in_range(self):
        """
            Return if position in text range
        """
        return self.position < len(self.text)

    def peek(self):
        """
            Returns the next position char without advancing the pointer
        """
        position = self.position + 1
        if self.position < len(self.text):
            return self.text[position]
        return None

    def get_integer(self):
        """
            Returns an integer from text
        """
        integer = ""
        while self.current_char and self.current_char in DIGITS:
            integer += self.current_char
            self.advance()
        return int(integer)

    def get_math_token(self):
        """
            Returns a token related to math exprs
        """
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
        raise Exception("There's something really wrong")

    def get_word_token(self):
        """
            Returns a word or built-in word
        """
        word = ""
        while self.current_char and self.current_char.isalnum():
            word += self.current_char
            self.advance()
        token_type = TokenType.WORD

        assert len(BUILT_IN_WORDS) == 9, "You've forgotten to lex\
                a new builtin word"
        token_type = BUILT_IN_WORDS.get(word, token_type)

        return Token(token_type, word)

    def get_string_literal(self) -> str:
        """
            Starts the pointer at quote and advances once
            then advances and combines every thing until
            it finds a quote that didn't have a backslash before
            and returns the unicode_escaped value of this
            string
        """
        self.advance()  # Point after the quote
        string = ""
        while self.current_char and self.current_char != '"':
            if self.current_char == "\\" and self.peek() == '"':
                string += '"'
                self.advance()
                self.advance()
                continue
            string += self.current_char
            self.advance()
        string = string.encode().decode("unicode_escape")
        return string

    def get_next_token(self):
        """Returns the next token from string"""
        assert len(TokenType) == 26, "You forgot to implement a token"
        while self.current_char:
            if self.current_char in DIGITS:
                token_type = TokenType.INTEGER
                token_value = self.get_integer()
                token = Token(token_type, token_value)
                # self.advance()
                return token
            if self.current_char in "+-/*()":
                # Mathematical tokens
                return self.get_math_token()
            if self.current_char.isalnum():
                # Word tokens
                return self.get_word_token()
            # Logical operators
            if self.current_char == "=" and self.peek() == "=":
                token_type = TokenType.EQUALS
                token_value = "=="
                token = Token(token_type, token_value)
                self.advance()
                self.advance()
                return token
            if self.current_char == "<":
                token_type = TokenType.LTHAN
                token_value = "<"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == ">":
                token_type = TokenType.GTHAN
                token_value = ">"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "=":
                token_type = TokenType.SET
                token_value = "="
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "=":
                token_type = TokenType.SET
                token_value = "="
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "=":
                token_type = TokenType.SET
                token_value = "="
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "{":
                token_type = TokenType.BLOCK_START
                token_value = "{"
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == "}":
                token_type = TokenType.BLOCK_END
                token_value = "}"
                token = Token(token_type, token_value)
                self.advance()
                return token

            if self.current_char == ",":
                token_type = TokenType.SEP
                token_value = ","
                token = Token(token_type, token_value)
                self.advance()
                return token
            if self.current_char == '"':
                token_type = TokenType.STRING_LITERAL
                token_value = self.get_string_literal()
                token = Token(token_type, token_value)
                self.advance()  # RETURN
                return token

            if self.current_char in IGNORE_CHARACTERS:
                self.advance()
                continue
            self.error(f"Unreachable character {self.current_char}")

        return Token(TokenType.EOF, None)
