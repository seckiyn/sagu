"""
    The script that interprets the parsed file
"""
from parser import AST_COUNT
from lexer import TokenType
import logs

# pylint: disable=invalid-name
# pylint: disable=no-self-use
handle_function = 0

# Handle bin print
handle_function += 1


def handle_bin_print(*args):
    """
        Handles the built-in function print
    """
    print(*args)


# Handle bin input
handle_function += 1


def handle_bin_input(*args):
    """
        Handles the built-in function input
    """
    return input(*args)


BUILT_IN_FUNCTIONS = {
        "print": handle_bin_print,
        "input": handle_bin_input
        }

assert handle_function == len(BUILT_IN_FUNCTIONS),\
        "You forgot to write a handle_bin function\
        for new BUILT_IN_FUNCTION"


class Walker:
    """
        Main walker class for walking the parsed tokens
    """
    def walk(self, ast):
        """
            Walk the parsed
        """
        logs.print_done("AST:", ast)
        ast_name = "walk_" + type(ast).__name__
        logs.print_debug(ast_name)
        func = getattr(self, ast_name)
        return func(ast)


# Interpreter
assert AST_COUNT == 17, "You've forgotten to interpret an AST"


class Interpreter(Walker):
    """
        Main class that interprets the parsed tokens
    """
    def __init__(self, ast):
        self.ast = ast
        self.global_variables = dict()
        self.functions = dict()
        logs.print_info(self.ast)
        self.to_return = None

    def error(self, text):
        """
            Raise Error
        """
        raise Exception(text)

    def interpret(self):
        """
            Interpret the given list of tokens
        """
        self.walk(self.ast)
        if logs.VERBOSITY:
            print("Variables:", self.global_variables)
            print("Functions:", self.functions.keys())
        return self.to_return

    def walk_Integer(self, ast):
        """
            Handle Integer AST
        """
        return ast.token.token_value

    def walk_BinOp(self, ast):
        """
            Handle BinOp AST
        """
        left_value = self.walk(ast.left_token)
        op_token = ast.op_token.token_type
        logs.print_info(op_token)
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
        return self.error(f"Something in wrong in BinOp {ast}")

    def walk_UnaryOp(self, ast):
        """
            Handle UnaryOp AST
        """
        op_token = ast.op_token.token_type
        right_value = self.walk(ast.right_token)
        if op_token == TokenType.PLUS:
            return right_value
        if op_token == TokenType.MINUS:
            return -right_value
        return self.error("Something in wrong in UnaryOp {ast}")

    def walk_Void(self, ast):
        """
            Handle Void AST
        """
        return None

    def walk_Program(self, ast):
        """
            Handle Program AST
        """
        for program in ast.ast_list:
            self.walk(program)

    def walk_Block(self, ast):
        """
            Handle Block AST
        """
        for program in ast.ast_list:
            self.walk(program)

    def walk_SetVariable(self, ast):
        """
            Handle SetVariable AST
        """
        var_name = ast.token.token_value
        var_expr = self.walk(ast.expr)
        self.global_variables[var_name] = var_expr

    def walk_Variable(self, ast):
        """
            Handle Variable AST
        """
        var_name = ast.token.token_value
        return self.global_variables[var_name]

    def walk_Bool(self, ast):
        """
            Handle Bool AST
        """
        token = ast.token
        token_type = token.token_type
        if token_type == TokenType.TRUE:
            return True
        if token_type == TokenType.FALSE:
            return False
        return self.error("This is not a boolean")

    def walk_Flow(self, ast):
        """
            Handle Flow AST
        """
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
        """
            Handle Condition AST
        """
        if self.walk(ast.condition_expr):
            self.walk(ast.condition_block)

    def walk_FunctionDecl(self, ast):
        """
            Handle FunctionDecl AST
        """
        function_name = ast.function_name.token_value
        self.functions[function_name] = ast

    def walk_FunctionCall(self, ast):
        """
            Handle FunctionCall AST
        """
        # TODO: Find a better way to call functions
        function_name = ast.function_name.token_value
        assert len(BUILT_IN_FUNCTIONS) == 2,\
            "You forgot to handle the walk_FunctionCall\
            for new BUILT_IN_FUNCTION"
        if function_name in BUILT_IN_FUNCTIONS:
            function_arguments = list()
            for expr in ast.function_variables:
                function_arguments.append(self.walk(expr))
            return BUILT_IN_FUNCTIONS[function_name](*function_arguments)
        function_variables = ast.function_variables
        function = self.functions[function_name]
        function_block = function.function_block
        function_variable_places = [
            place.token_value
            for place in function.function_variables
                ]
        logs.print_error("Funciton variables:", function_variable_places)
        variables = dict()
        zipped = zip(function_variable_places, function_variables)
        for var_name, var_value in zipped:
            variables[var_name] = self.walk(var_value)
        new_interpreter = Interpreter(function_block)
        new_interpreter.global_variables = variables
        return new_interpreter.interpret()

    def walk_ReturnStatement(self, ast):
        """
            Handle ReturnStatement AST
        """
        self.to_return = self.walk(ast.expression)

    def walk_While(self, ast):
        """
            Handle While AST
        """
        expression = ast.expression
        block = ast.block
        while self.walk(expression):
            self.walk(block)

    def walk_String(self, ast):
        """
            Handle String AST
        """
        return ast.token.token_value
