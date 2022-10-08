
class Walker:
    def walk(self, ast):
        ast_name = "walk_" + type(ast).__name__
        func = getattr(self, ast_name)
        return func

class Interpreter(Walker):
    def __init__(self, ast):
        self.ast = ast
    def interpret(self):
        return self.walk(self.ast)
    def 
