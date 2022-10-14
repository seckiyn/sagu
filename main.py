#!/usr/bin/env python3
"""
    Main script
"""
import sys
import os

from lexer import Lexer
from parser import Parser, Token
from interpreter import Interpreter

from typing import List

def lex_to_tokens(text) -> List[Token]:
    lexer = Lexer(text)
    token = lexer.get_next_token()
    tokens = list([token])
    while token.token_value:
        token = lexer.get_next_token()
        tokens.append(token)
    return tokens

def interpret(string):
    tokens = lex_to_tokens(string)
    parser = Parser(tokens)
    interpreter = Interpreter(parser.parse())
    interpreter.interpret()

PATH = "."
def usage():
    print(__file__ + " <filename>")
def read_file(path: str) -> None:
    with open(os.path.join(PATH, path)) as file:
        return file.read()
def lex_parse_interpret(text: str) -> None:
    interpret(text)

def parse_arguments() -> None:
    arguments = sys.argv
    if len(arguments) != 2:
        usage()
        sys.exit()
    file_name, *arguments = arguments
    program_name, *arguments = arguments
    lex_parse_interpret(read_file(program_name))
def main() -> None:
    parse_arguments()

if __name__ == "__main__":
    main()
