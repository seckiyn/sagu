"""
    A module to use logging and printing
"""
from colorama import Fore, init
init(autoreset=True)
DEBUG = False and True


def print_error(*args, **kwargs):
    """
        Print wrapper to write errors
    """
    if DEBUG:
        print(Fore.RED + "[ERROR]: ", *args, **kwargs)


def print_info(*args, **kwargs):
    """
        Print wrapper to write info
    """
    if DEBUG:
        print(Fore.BLUE + "[INFO]: ", *args, **kwargs)


def print_done(*args, **kwargs):
    """
        Print wrapper to write completes
    """
    if DEBUG:
        print(Fore.GREEN + "[DONE]", *args, **kwargs)


def print_debug(*args, **kwargs):
    """
        Print wrapper to write debugs
    """
    if DEBUG:
        print(Fore.YELLOW + "[DEBUG]", *args, **kwargs)
