from lexer import TokenType
from parser import AST_COUNT
from logs import *
import logs
class Walker:
    def walk(self, ast):
        print_done("AST:", ast)
        if ast is None:
            if logs.DEBUG: print_done("="*100)
        ast_name = "walk_" + type(ast).__name__
        if logs.DEBUG: print(ast_name)
        func = getattr(self, ast_name)
        return func(ast)

assert AST_COUNT == 17, "You've forgotten to interpret an AST"
class Interpreter(Walker):
    def __init__(self, ast):
        self.ast = ast
        self.global_variables = dict()
        self.functions = dict()
        print_info(self.ast)
        self.to_return = None
    def error(self, text):
        raise Exception(text)
    def interpret(self):
        walked = self.walk(self.ast)
        print("Variables:", self.global_variables)
        print("Functions:", self.functions.keys())
        return self.to_return
    def walk_Integer(self, ast):
        return ast.token_value
    def walk_BinOp(self, ast):
        left_value = self.walk(ast.left_token)
        op_token = ast.op_token.token_type
        print_info(op_token)
        right_value = self.walk(ast.right_token)
        if op_token == TokenType.PLUS:
            return left_value + right_value
        if op_token == TokenType.MINUS:
            return left_value - right_value
        if op_token == TokenType.MUL:
            return left_value * right_value
        if op_token == TokenType.DIV:
            return left_value // right_value
        if op_token == TokenType.GTHAN:
            return left_value > right_value
        if op_token == TokenType.LTHAN:
            return left_value < right_value
        if op_token == TokenType.EQUALS:
            return left_value == right_value
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
    def walk_Program(self, ast):
        for program in ast.ast_list:
            self.walk(program)
    def walk_Block(self, ast):
        for program in ast.ast_list:
            self.walk(program)
    def walk_SetVariable(self, ast):
        var_name = ast.token.token_value
        var_expr = self.walk(ast.expr)
        self.global_variables[var_name] = var_expr
    def walk_Variable(self, ast):
        var_name = ast.token.token_value
        return self.global_variables[var_name]
    def walk_Bool(self, ast):
        token = ast.token
        token_type = token.token_type
        if token_type == TokenType.TRUE:
            return True
        if token_type == TokenType.FALSE:
            return False
        self.error("This is not a boolean")
    def walk_Flow(self, ast):
        if_condition = self.walk(ast.if_condition.condition_expr)
        elseif_condition = False
        self.walk(ast.if_condition)
        if not if_condition:
            for elseif in ast.elseif:
                elseif_condition = self.walk(elseif.condition_expr)
                self.walk(elseif.condition_block)
                if elseif_condition:
                    break
        if not if_condition and not elseif_condition:
            self.walk(ast.else_block)
    def walk_Condition(self, ast):
        if logs.DEBUG: print("="*20 , ast.condition_expr)
        if self.walk(ast.condition_expr):
            self.walk(ast.condition_block)
    def walk_FunctionDecl(self, ast):
        function_name = ast.function_name.token_value
        function_variables = ast.function_variables
        function_block = ast.function_block
        self.functions[function_name] = ast
    def walk_FunctionCall(self, ast):
        # TODO: Find a better way to call functions
        function_name = ast.function_name.token_value
        function_variables = ast.function_variables
        function = self.functions[function_name]
        function_block = function.function_block
        function_variable_places = [place.token_value for place in function.function_variables]
        print_error("Funciton variables:", function_variable_places)
        variables = dict()
        for var_name, var_value in zip(function_variable_places, function_variables):
            variables[var_name] = self.walk(var_value)
        new_interpreter = Interpreter(function_block)
        new_interpreter.global_variables = variables
        return new_interpreter.interpret()
    def walk_ReturnStatement(self, ast):
        self.to_return = self.walk(ast.expression)
    def walk_While(self, ast):
        expression = ast.expression
        block = ast.block
        while self.walk(expression):
            self.walk(block)
    def walk_String(self, ast):
        return ast.token.token_value

