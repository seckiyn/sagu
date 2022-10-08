from lexer import TokenType
from parser import AST_COUNT
from logs import *
class Walker:
    def walk(self, ast):
        ast_name = "walk_" + type(ast).__name__
        func = getattr(self, ast_name)
        return func(ast)

assert AST_COUNT == 5, "You've forgotten to interpret an AST"
class Interpreter(Walker):
    def __init__(self, ast):
        self.ast = ast
    def error(self, text):
        raise Exception(text)
    def interpret(self):
        return self.walk(self.ast)
    def walk_Integer(self, ast):
        return ast.token_value
    def walk_BinOp(self, ast):
        left_value = self.walk(ast.left_token)
        op_token = ast.op_token.token_type
        right_value = self.walk(ast.right_token)
        if op_token == TokenType.PLUS:
            return left_value + right_value
        if op_token == TokenType.MINUS:
            return left_value - right_value
        if op_token == TokenType.MUL:
            return left_value * right_value
        if op_token == TokenType.DIV:
            return left_value // right_value
        self.error(f"Something in wrong in BinOp {ast}")
    def walk_UnaryOp(self, ast):
        op_token = ast.op_token.token_type
        right_value = self.walk(ast.right_token)
        if op_token == TokenType.PLUS:
            return right_value
        if op_token == TokenType.MINUS:
            return -right_value
        self.error("Something in wrong in UnaryOp {ast}")
    def walk_Integer(self, ast):
        return ast.token.token_value
    def walk_Void(self, ast):
        pass
