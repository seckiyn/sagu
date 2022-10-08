from lexer import TokenType, Token
from typing import List, Union
from dataclasses import dataclass
from sys import exit

AST_COUNT = 0
# AST NODES

AST_COUNT += 1
@dataclass
class AST:
    """ Main AST class """
    pass

AST_COUNT += 1
@dataclass
class BinOp(AST):
    """
        AST class for operations for binary operations like:
            PLUS
            MINUS
            MUL
            DIV
    """
    left_token: Union[AST, TokenType]
    op_token: Union[AST, TokenType]
    right_token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class UnaryOp(AST):
    op_token: Union[AST, TokenType]
    right_token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class Integer(AST):
    token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class Void(AST):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.current_token = None
        self.next_token()
    def error(self, text, *args, **kwargs):
        raise Exception(text, *args, **kwargs)
    def parse(self):
        return self.expr()
    def next_token(self):
        self.position += 1
        self.current_token = self.tokens[self.position]
    def eat(self, token_type: TokenType):
        if self.current_token.token_type == token_type:
            self.next_token()
        else:
            self.error(f"Unexpected token ({self.current_token}) expected ({token_type})")
    def expr(self):
        node = self.term()
        while self.current_token.token_type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.token_type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            if token.token_type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(node, token, self.factor())
        return node
    def term(self):
        node = self.factor()
        while self.current_token.token_type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.token_type == TokenType.MUL:
                self.eat(TokenType.MUL)
            if token.token_type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(node, token, self.factor())
        return node
    def factor(self):
        if self.current_token.token_type == TokenType.INTEGER:
            token = self.current_token
            self.eat(TokenType.INTEGER)
            return Integer(token)
        if self.current_token.token_type == TokenType.PLUS:
            token = self.current_token
            self.eat(TokenType.PLUS)
            return UnaryOp(token, self.factor())
        if self.current_token.token_type == TokenType.MINUS:
            token = self.current_token
            self.eat(TokenType.MINUS)
            return UnaryOp(token, self.factor())
        if self.current_token.token_type == TokenType.LPAREN:
            token = self.current_token
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        if self.current_token.token_type == TokenType.EOF:
            self.error("This is a empty string")
        self.error(f"Unreachable token {self.current_token}")

