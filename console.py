"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""
from os import system, name
from colorama import init, Fore

init(autoreset=True)


def clear():
    """Clear console screen"""
    os = name
    if os == "posix":
        print("clear")
        system("clear")
    elif os == "nt":
        system("cls")


def banner(subtitle):
    """Print the banner"""
    clear()
    print(Fore.LIGHTRED_EX + r"""
  _____ _   _ _______________ ____  
 |  ___| | | |__  /__  / ____|  _ \ 
 | |_  | | | | / /  / /|  _| | |_) |
 |  _| | |_| |/ /_ / /_| |___|  _ < 
 |_|    \___//____/____|_____|_| \_\
                                    
    """)
    print(Fore.LIGHTGREEN_EX + subtitle)


def cont():
    input("Press enter to continue...")
