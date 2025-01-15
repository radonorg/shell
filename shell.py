import os
from colorama import Fore

def get_command():
    return input(Fore.MAGENTA + ">>> " + Fore.RESET)

while True:
    try:
        os.system(get_command())
    except Exception as e:
        print(Fore.RED + e + Fore.RESET)