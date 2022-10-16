#!/usr/bin/env python3
"""
    Main script
"""
import sys
import os
import argparse
import logs

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

def print_the_tokens(filename) -> None:
    text = read_file(filename)
    print("TOKENS")
    tokens = lex_to_tokens(text)
    print(*tokens, sep="\n")

def print_the_parsing(filename) -> None:
    text = read_file(filename)
    print("PARSING")
    tokens = lex_to_tokens(text)
    parser = Parser(tokens)
    print(parser.parse())

def parse_arguments() -> None:
    arguments = sys.argv
    if len(arguments) != 2:
        usage()
        sys.exit()
    file_name, *arguments = arguments
    program_name, *arguments = arguments
    lex_parse_interpret(read_file(program_name))

def parse_arguments_argparse() -> None:
    parser = argparse.ArgumentParser()
    # Handle positional file name
    positional_file_name = "file_path"
    positional_file_name_help = "Path of the file to be interpreted"

    # Add positional file name
    parser.add_argument(positional_file_name,\
            help=positional_file_name_help)

    # Handle verbosity
    debug = "--debug"
    debug_help = "Print the debug outputs"

    # Add debug argument
    parser.add_argument(debug,\
            help=debug_help,\
            action="store_true")
    # Add lex option
    is_lex = "--lex"
    is_lex_help = "Lex the file"

    # Add lex argument
    parser.add_argument(is_lex,\
            help=is_lex_help,\
            action="store_true")

    # Add parse option
    is_parse = "--parse"
    is_parse_help = "Parse the file"

    # Add parse argument
    parser.add_argument(is_parse,\
            help=is_parse_help,\
            action="store_true")

    args = parser.parse_args()



    # Check verbosity
    logs.DEBUG = args.debug
    if args.lex:
        print_the_tokens(args.file_path)
    elif args.parse:
        print_the_parsing(args.file_path)
    else:
        lex_parse_interpret(read_file(args.file_path))


def main() -> None:
    parse_arguments_argparse()

if __name__ == "__main__":
    main()
