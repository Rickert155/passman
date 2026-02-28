"""
CLI Password Manager(PassMan)
"""
import os
import random
import sys
import sqlite3
import shutil
import textwrap
from typing import Optional
import time

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
#           Current Time              #
#######################################
def current_time() -> str:
    ctime = time.strftime("%d-%m-%y %H:%M:%S")
    return ctime

def divine_line() -> str:
    len_line = int(shutil.get_terminal_size().columns)
    line = "-"*len_line
    return line

#######################################
#               Database              #
#######################################
def create_db() -> None:
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
    con.close()

#######################################
# create pass
#######################################
def create_password() -> Optional[str]:
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
            sys.exit(f"{RED}minimal length: {MINIMAL_LEN_PASSWORD}{RESET}")
    
    except ValueError:
        sys.exit(f"{RED}Value Error{RESET}")

#######################################
# write pass
#######################################
def write_password() -> Optional[str]:
    con = sqlite3.connect(PASSMAN_DB_PATH)
    cursor = con.cursor()

    service = input("Service: ").strip()
    email = input("Email: ").strip()
    login = input("Login: ").strip()
    password = input("Password: ").strip()
    write_time = current_time()

    write_command = (
            f"INSERT INTO {PASSMAN_TABLE_NAME} "
            f"(service, email, login, password, date_create) "
            f"VALUES (?, ?, ?, ?, ?)"
            )
    cursor.execute(write_command, (service, email, login, password, write_time))
    con.commit()
    con.close()
#######################################
# show pass
#######################################
def show_access(cursor) -> None:
    """Отображение данных service, email, login"""
    show_command = (
            f"SELECT service, email, login FROM {PASSMAN_TABLE_NAME};"
            )
    cursor.execute(show_command)
    table = (
            f"|{divine_line()[:-1]}\n"
            f"| Service\tEmail\t\t\tLogin\n"
            f"|{divine_line()[:-1]}\n"
            )
    access = cursor.fetchall()

    for info in access:
        table+=f"| {info[0]}\t{info[1]}\t{info[2]}\n"

    print(table.strip())

def show_password() -> None:
    con = sqlite3.connect(PASSMAN_DB_PATH)
    cursor = con.cursor()
    
    show_access(cursor)

    service = input("|\n| Service: ").strip()
    email = input("| Email: ").strip()
    show_command = (
            f"SELECT service, email, login, password FROM {PASSMAN_TABLE_NAME} "
            f"WHERE service = ? AND email = ?"
            )
    cursor.execute(show_command, (service, email))
    all_data = cursor.fetchall()
    for data in all_data:
        print(
                f"|{divine_line()[:-1]}\n"
                f"| Service:\t\t{data[0]}\n"
                f"| Email:\t\t{data[1]}\n"
                f"| Login:\t\t{data[2]}\n"
                f"| Password:\t\t{data[3]}"
                )
    con.close()
    

#######################################
# update pass
#######################################

#######################################
# delete pass
#######################################


def all_actions() -> dict[str, str]:
    actions = {
            "1":"Create password",
            "2":"Show password",
            "3":"Write password",
            "4":"Update password",
            "5":"Delete password"
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
        
        elif "show" in user_item:
            show_password()
        
        elif "write" in user_item:
            write_password()
        
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
