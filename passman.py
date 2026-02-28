"""
CLI Password Manager(PassMan)
"""
import os
import sys
import textwrap


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
# create pass
#######################################
def create_password() -> str:
    password = None
    return password

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
    if "create" in user_item:
        print(f"{GREEN}Создаем пароль{RESET}")
    elif "write" in user_item:
        print(f"{GREEN}Записываем пароль{RESET}")
    elif "update" in user_item:
        print(f"{YELLOW}Обновляем пароль{RESET}")
    elif "delete" in user_item:
        print(f"{RED}Удаляем пароль{RESET}")

def main():
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
