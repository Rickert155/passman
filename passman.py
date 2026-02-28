"""
CLI Password Manager(PassMan)
"""
import os
import random
import sys
import sqlite3
import textwrap

HOME_PATH = os.environ.get("HOME")
CONFIG_PATH = f"{HOME_PATH}/.config"
PASSMAN_PATH = f"{CONFIG_PATH}/passman"
PASSMAN_DB_PATH = f"{PASSMAN_PATH}/passman.db"

PASSMAN_TABLE_NAME = "passman"

MINIMAL_LEN_PASSWORD = 14

#######################################
#           Metadata                  #  
#######################################
__author__ = "CyberWarn"
__version__ = "0.1"

#######################################
#               Colors                #
#######################################
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
BOLD = "\033[1m"

#######################################
#               Database              #
#######################################
def create_db() -> str:
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    if not os.path.exists(PASSMAN_PATH):
        os.makedirs(PASSMAN_PATH)
        print(f"{GREEN}CREATE {PASSMAN_PATH}{RESET}")
    
    con = sqlite3.connect(PASSMAN_DB_PATH)
    con.cursor()
    create_db_command = (
            f"CREATE TABLE IF NOT EXISTS {PASSMAN_TABLE_NAME} ("
            f"_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            f"service TEXT, "
            f"email TEXT DEFAULT NULL, "
            f"login TEXT DEFAULT NULL, "
            f"password TEXT NOT NULL, "
            f"date_create TEXT, "
            f"date_update TEXT"
            f")"
            )
    con.execute(create_db_command)

#######################################
# create pass
#######################################
def create_password() -> str:
    """
    Disclaimer: Генератор использует модуль random,
    по этой причине генератор не является надежным. 
    В рамках прототипа будет использоваться random, в дельнейшем 
    будет переход на более серьезную систему
    """
    all_symbols = (
            "abcdefghijklmnopqrstuvwxyz"
            "1234567890"
            "!@#$%^&*()\"\\;'<,.>/|+=-}{]["
            )
    password = ""
    try:
        len_pass = int(input(
            f"password length(min {MINIMAL_LEN_PASSWORD}): "
            ).strip())
        if len_pass >= MINIMAL_LEN_PASSWORD:
            for _ in range(len_pass):
                symbol = random.choice(all_symbols)
                if random.choice([True, False]):
                    symbol = symbol.upper()
                password+=symbol
            print(create_password.__doc__)
            return password
        else:
            print(f"{RED}minimal length: {RESET}")
            create_password()
    
    except ValueError:
        sys.exit(f"{RED}Value Error{RESET}")

#######################################
# write pass
#######################################

#######################################
# update pass
#######################################

#######################################
# delete pass
#######################################


def all_actions() -> dict[str, str]:
    actions = {
            "1":"Create password",
            "2":"Write password",
            "3":"Update password",
            "4":"Delete password"
            }
    return actions

def get_menu() -> str:
    menu = (
    f"{YELLOW}author:\t\t{__author__}{RESET}\n"
    f"{YELLOW}version:\t{__version__}{RESET}\n\n"
    )
    number_action = 0
    for key, value in all_actions().items():
        number_action += 1
        item = f"{GREEN}[{key}]{RESET} {value}\n"
        menu+=item

    menu = textwrap.dedent(menu)
    return menu

def passMan(user_item:str): 
    try:
        if "create" in user_item:
            password = create_password()
            print(password)
        elif "write" in user_item:
            print(f"{GREEN}Записываем пароль{RESET}")
        elif "update" in user_item:
            print(f"{YELLOW}Обновляем пароль{RESET}")
        elif "delete" in user_item:
            print(f"{RED}Удаляем пароль{RESET}")
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")

def main():
    create_db()
    
    params = sys.argv[1:]
    system_items = all_actions()
    available_params = [
            value.lower().split(" ")[0] for key, value in system_items.items()
            ]
    if len(params) > 0 and params[0].strip() in available_params:
        user_item = params[0].strip()
        passMan(user_item=user_item)
    else:
        try:
            # Получаем текст меню
            menu = get_menu()
            user_item = input(f"{menu}>>> ").strip()
        
            if user_item in [item for item in system_items]:
                user_item = system_items[user_item].lower()
                passMan(user_item=user_item)
            else:
                sys.exit(f"{RED}Item \"{user_item}\" not defined!{RESET}")
        
        except KeyboardInterrupt:
            sys.exit(f"{RED}\nExit...{RESET}")

if __name__ == "__main__":
    main()
