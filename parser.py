from typing import List, Union
from dataclasses import dataclass
import logs
from logs import print_error, print_done, print_debug
from lexer import TokenType, Token


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
    """
        AST class for Unary Operations
        op_token is PLUS or MINUS
        right_token is an AST
    """
    op_token: Union[AST, TokenType]
    right_token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class Integer(AST):
    """
        AST container for Integers
    """
    token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class Void(AST):
    """
        AST for none
    """
    pass

AST_COUNT += 1
@dataclass
class SetVariable(AST):
    """
        AST variable for setting variables
    """
    token: Token
    expr: AST

AST_COUNT += 1
@dataclass
class Variable(AST):
    """
        AST for return variable
    """
    token: Token

AST_COUNT += 1
@dataclass
class Block(AST):
    """
        AST for blocks
    """
    ast_list: List[AST]

AST_COUNT += 1
@dataclass
class Program(AST):
    """
        AST class for whole program
    """
    ast_list: List[AST]

AST_COUNT += 1
@dataclass
class Bool(AST):
    """
        AST container for Boolean
    """
    token: Token

AST_COUNT += 1
@dataclass
class Condition(AST):
    """
        AST for conditions
        lessthan
        greaterthan
        equals
    """
    condition_expr: AST
    condition_block: Block

AST_COUNT += 1
@dataclass
class Flow(AST):
    """
        AST for if elseif else statement
    """
    if_condition: Condition
    elseif: List[AST]
    else_block: AST

AST_COUNT += 1
@dataclass
class FunctionDecl(AST):
    """
        AST for declaring functions
    """
    function_name: AST
    function_variables: AST
    function_block: Block

AST_COUNT += 1
@dataclass
class FunctionCall(AST):
    """
        AST for calling function
    """
    function_name: AST
    function_variables: AST

AST_COUNT += 1
@dataclass
class ReturnStatement(AST):
    """
        AST for return statements in functions
    """
    expression: AST

AST_COUNT += 1
@dataclass
class While(AST):
    """
        AST for while loops
    """
    expression: AST
    block: Block

AST_COUNT += 1
@dataclass
class String(AST):
    """
        AST container string_literals
    """
    token: AST

assert AST_COUNT == 17, f"You forgot to handle an AST {AST_COUNT}"
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        print_debug("="*200)
        print_debug(*self.tokens, sep="\n")
        print_debug("="*200)
        self.position = -1
        self.current_token = None
        self.next_token()
    def error(self, text, *args, **kwargs):
        """
            Handle the errors
        """
        raise Exception(text, *args, **kwargs)
    def parse(self):
        """
            Parse the whole self.text
        """
        return self.program()
    def next_token(self):
        """
            advances and sets the current_token
        """
        self.position += 1
        if self.position >= len(self.tokens):
            print_done(f"Tokens of these makes the wrong {self.tokens}")

        self.current_token = self.tokens[self.position]
    def eat(self, token_type: TokenType):
        """
            Checks if given token is true and advances token
            else gives and error
        """
        print_debug(self.current_token)
        if self.current_token.token_type == token_type:
            self.next_token()
        else:
            self.error(f"Unexpected token ({self.current_token}) expected ({token_type})")
    def peek(self):
        """
            Returns the next token without advancing
        """
        position = self.position + 1
        if position < len(self.tokens):
            return self.tokens[position]
        return None
    def get_ast_list(self, isfunction=False):
        """
            Returns a bundle of AST's
        """
        ast_list = list()
        while self.current_token.token_value and self.current_token.token_type in (
                # ADD THE TOKENS THAT YOU WANT TO USE IN BLOCKS
                # AST List
                TokenType.BLOCK_START,
                TokenType.SETVAR,
                TokenType.IF,
                TokenType.FUNC,
                TokenType.WORD,
                TokenType.RETURN,
                TokenType.WHILE
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
            elif self.current_token.token_type == TokenType.WHILE:
                ast_list.append(self.while_loop())
            else:
                self.error(f"There's something wrong {self.current_token}")
        return ast_list
    def while_loop(self):
        """
            Handles the WHILE token
        """
        self.eat(TokenType.WHILE)
        expression = self.logical()
        block = self.block()
        return While(expression, block)
    def return_statement(self):
        """
            Handles the RETURN statement for functions
        """
        self.eat(TokenType.RETURN)
        return_statement = self.logical()
        return ReturnStatement(return_statement)

    def function_decl(self):
        """
            Handles the function declaration
        """
        self.eat(TokenType.FUNC)
        function_name = self.current_token
        self.eat(TokenType.WORD)
        function_variables = self.variable_bundle()
        function_block = self.block(True)
        function = FunctionDecl(function_name, function_variables, function_block)
        return function
    def function_call(self):
        """
            Handles the function call ast
        """
        function_name = self.current_token
        self.eat(TokenType.WORD)
        function_variables = list()
        self.eat(TokenType.LPAREN)
        # THINGS THAT ALLOWED INSIDE A FUNCTION
        expr = (TokenType.INTEGER,
                TokenType.LPAREN,
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.TRUE,
                TokenType.FALSE,
                TokenType.WORD,
                TokenType.STRING_LITERAL)
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
        """
            Returns WORD's separeted with SEP(,)
        """
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
        """
            Returns a Flow(if elseif else statement)
        """
        self.eat(TokenType.IF)
        if_expr = self.logical()
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
        """
            Returns the whole program as Program
        """
        ast_list = self.get_ast_list()
        return Program(ast_list)
    def block(self, isfunction=False):
        """
            Returns a block and if it's a function returns it with a
            RETURN
        """
        self.eat(TokenType.BLOCK_START)
        ast_list = self.get_ast_list(isfunction)
        self.eat(TokenType.BLOCK_END)
        return Block(ast_list)
    def variable(self):
        """
            Returns a WORD as variable
        """
        self.eat(TokenType.SETVAR)
        variable_name = self.current_token
        self.eat(TokenType.WORD)
        self.eat(TokenType.SET)
        variable_set = self.logical()
        return SetVariable(variable_name, variable_set)
    def logical(self):
        """
            Does the math and logical
        """
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
        """
            Expr part of the logical
        """
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
        """
            Term part of the logical
        """
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
        """
            Factor part of logical
        """
        print_debug("FACTOR", self.current_token)
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
        if self.current_token.token_type == TokenType.STRING_LITERAL:
            return self.get_variable()
        if self.current_token.token_type == TokenType.EOF:
            self.error(f"This is a empty string, current_token: {self.current_token}")
        return self.error(f"Unreachable token {self.current_token}")
    def get_variable(self):
        """
            Last part of the logical returns
            TRUE
            FALSE
            FUNCTION_CALL
            STRING_LITERAL
            VARIABLE
        """
        token = self.current_token
        if token.token_type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Bool(token)
        if token.token_type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Bool(token)
        if token.token_type == TokenType.WORD and self.peek().token_type == TokenType.LPAREN:
            return self.function_call()
        if token.token_type == TokenType.STRING_LITERAL:
            token = self.current_token
            self.eat(TokenType.STRING_LITERAL)
            return String(token)
        self.eat(TokenType.WORD)
        return Variable(token)

