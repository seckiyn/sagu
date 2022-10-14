from lexer import TokenType, Token
from typing import List, Union
from dataclasses import dataclass
from sys import exit
from logs import *


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
            LOGICAL_OPERATORS
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

AST_COUNT += 1
@dataclass
class SetVariable(AST):
    token: Token
    expr: AST

AST_COUNT += 1
@dataclass
class Variable(AST):
    token: Token

AST_COUNT += 1
@dataclass
class Block(AST):
    ast_list: List[AST]

AST_COUNT += 1
@dataclass
class Program(AST):
    ast_list: List[AST]

AST_COUNT += 1
@dataclass
class Bool(AST):
    token: Token

AST_COUNT += 1
@dataclass
class Condition(AST):
    condition_expr: AST
    condition_block: Block

AST_COUNT += 1
@dataclass
class Flow(AST):
    if_condition: Condition
    elseif: List[AST]
    else_block: AST

AST_COUNT += 1
@dataclass
class FunctionDecl(AST):
    function_name: AST
    function_variables: AST
    function_block: Block

AST_COUNT += 1
@dataclass
class FunctionCall(AST):
    function_name: AST
    function_variables: AST

AST_COUNT += 1
@dataclass
class ReturnStatement(AST):
    expression: AST


assert AST_COUNT == 15, f"You forgot to handle an AST {AST_COUNT}"
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.current_token = None
        self.next_token()
    def error(self, text, *args, **kwargs):
        raise Exception(text, *args, **kwargs)
    def parse(self):
        return self.program()
    def next_token(self):
        self.position += 1
        self.current_token = self.tokens[self.position]
    def eat(self, token_type: TokenType):
        print(self.current_token)
        if self.current_token.token_type == token_type:
            self.next_token()
        else:
            self.error(f"Unexpected token ({self.current_token}) expected ({token_type})")
    def peek(self):
        position = self.position + 1
        if position < len(self.tokens):
            return self.tokens[position]
        return None
    def get_ast_list(self, isfunction=False):
        ast_list = list()
        while self.current_token.token_value and self.current_token.token_type in (
                # AST List
                TokenType.BLOCK_START,
                TokenType.SETVAR,
                TokenType.IF,
                TokenType.FUNC,
                TokenType.WORD,
                TokenType.RETURN
                ):

            if self.current_token.token_type == TokenType.SETVAR:
                ast_list.append(self.variable())
            elif self.current_token.token_type == TokenType.BLOCK_START:
                ast_list.append(self.block())
            elif self.current_token.token_type == TokenType.IF:
                ast_list.append(self.flow())
            elif self.current_token.token_type == TokenType.FUNC:
                ast_list.append(self.function_decl())
            elif self.current_token.token_type == TokenType.WORD:
                ast_list.append(self.function_call())
            elif self.current_token.token_type == TokenType.RETURN and isfunction:
                ast_list.append(self.return_statement())
            else:
                self.error(f"There's something wrong {self.current_token}")
        return ast_list
    def return_statement(self):
        self.eat(TokenType.RETURN)
        return_statement = self.logical()
        return ReturnStatement(return_statement)

    def function_decl(self):
        self.eat(TokenType.FUNC)
        function_name = self.current_token
        self.eat(TokenType.WORD)
        function_variables = self.variable_bundle()
        function_block = self.block(True)
        function = FunctionDecl(function_name, function_variables, function_block)
        return function
    def function_call(self):
        function_name = self.current_token
        self.eat(TokenType.WORD)
        function_variables = list()
        self.eat(TokenType.LPAREN)
        expr = (TokenType.INTEGER,
                TokenType.LPAREN,
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.TRUE,
                TokenType.FALSE)
        if self.current_token.token_type in expr:
            function_variables.append(self.expr())
        while self.current_token.token_type == TokenType.SEP:
            self.eat(TokenType.SEP)
            function_variables.append(self.expr())
        self.eat(TokenType.RPAREN)
        print_done(function_variables)
        function_call = FunctionCall(function_name, function_variables)
        return function_call
    def variable_bundle(self):
        function_variables = list()
        self.eat(TokenType.LPAREN)
        if self.current_token.token_type == TokenType.WORD:
            token = self.current_token
            self.eat(TokenType.WORD)
            function_variables.append(token)
        while self.current_token.token_type == TokenType.SEP:
            self.eat(TokenType.SEP)
            token = self.current_token
            self.eat(TokenType.WORD)
            function_variables.append(token)
        self.eat(TokenType.RPAREN)
        return function_variables
    def flow(self):
        self.eat(TokenType.IF)
        if_expr = self.expr()
        if_block = self.block()
        # First condition of flow
        if_condition = Condition(if_expr, if_block)
        # Second condition of flow
        elseif_condition_list = list()
        while self.current_token.token_type == TokenType.ELSEIF:
            self.eat(TokenType.ELSEIF)
            elseif_expr = self.expr()
            elseif_block = self.block()
            elseif_condition = Condition(elseif_expr, elseif_block)
            elseif_condition_list.append(elseif_condition)
        # Third condition of flow
        else_condition = Condition(Bool(Token(TokenType.TRUE, "true")), Void())
        if self.current_token.token_type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_expr = Bool(Token(TokenType.TRUE, "true"))
            else_block = self.block()
            else_condition = Condition(else_expr, else_block)
        return Flow(if_condition, elseif_condition_list, else_condition)
    def program(self):
        ast_list = self.get_ast_list()
        return Program(ast_list)
    def block(self, isfunction=False):
        self.eat(TokenType.BLOCK_START)
        ast_list = self.get_ast_list(isfunction)
        self.eat(TokenType.BLOCK_END)
        return Block(ast_list)
    def variable(self):
        self.eat(TokenType.SETVAR)
        variable_name = self.current_token
        self.eat(TokenType.WORD)
        self.eat(TokenType.SET)
        variable_set = self.logical()
        return SetVariable(variable_name, variable_set)
    def logical(self):
        node = self.expr()
        print_error(self.current_token)
        while self.current_token.token_type in (TokenType.EQUALS, TokenType.LTHAN, TokenType.GTHAN):
            print_error("LOGICAL")
            token = self.current_token
            if token.token_type == TokenType.EQUALS:
                self.eat(TokenType.EQUALS)
            if token.token_type == TokenType.LTHAN:
                self.eat(TokenType.LTHAN)
            if token.token_type == TokenType.GTHAN:
                self.eat(TokenType.GTHAN)
            node = BinOp(node, token, self.expr())
        return node
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
        print("FACTOR", self.current_token)
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
        if self.current_token.token_type in (TokenType.WORD, TokenType.TRUE, TokenType.FALSE):
            return self.get_variable()
        if self.current_token.token_type == TokenType.EOF:
            self.error(f"This is a empty string, current_token: {self.current_token}")
        self.error(f"Unreachable token {self.current_token}")
    def get_variable(self):
        token = self.current_token
        if token.token_type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Bool(token)
        if token.token_type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Bool(token)
        if token.token_type == TokenType.WORD and self.peek().token_type == TokenType.LPAREN:
            return self.function_call()
        self.eat(TokenType.WORD)
        return Variable(token)

