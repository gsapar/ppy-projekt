import curses
import os
from manager import Manager

menu_items = [
    "Add account.",
    "Get account.",
    "Edit account.",
    "Delete account.",
    "List all accounts.",
    "Save to file.",
    "Load file.",
    "Exit"  
]

def main_menu(stdscr, manager):
    curses.curs_set(0)
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "Simple Password Manager", curses.A_BOLD)

        for i, item in enumerate(menu_items):
            x = 4
            y = i + 2

            if i == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, f"> {item}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, f"  {item}")
        stdscr.refresh()

        key = stdscr.getch()
        if key in [curses.KEY_UP, ord('k')]:
            current_row = (current_row - 1) % len(menu_items)
        elif key in [curses.KEY_DOWN, ord('j')]:
            current_row = (current_row + 1) % len(menu_items)
        elif key in [curses.KEY_ENTER, ord('\n')]:
            match current_row:
                case 0:
                    add_account(stdscr, manager)
                case 1:
                    get_account(stdscr, manager) 
                case 2:
                    edit_account(stdscr, manager)
                case 3:
                    delete_account(stdscr, manager)
                case 4:
                    list_accounts(stdscr, manager)
                case 5:
                    save_file(stdscr, manager)
                case 6:
                    load_file(stdscr, manager)
                case 7:
                    stdscr.clear()
                    stdscr.addstr(0, 2, "Exiting Password Manager.", curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(1200)
                    break

def prompt_input(stdscr, prompt_str):
    curses.echo() 
    stdscr.clear()
    stdscr.addstr(2, 2, prompt_str)    
    stdscr.refresh()
    input_str = stdscr.getstr(3, 2).decode("utf-8")
    curses.noecho()
    return input_str

def add_account(stdscr, manager):
    name = prompt_input(stdscr, "Enter account name:")
    if not name:
        stdscr.addstr(5, 2, "Account name cannot be empty!")
        stdscr.addstr(7, 2, "Press any key to try again. Press ESC to return to menu.")
        stdscr.refresh()
        stdscr.getch()
        return
    if manager.get_account(name):
        stdscr.addstr(5, 2, "Account with that name already exists.")
        stdscr.addstr(7, 2, "Press any key to try again. Press ESC to return to menu.")
        stdscr.refresh()
        stdscr.getch()
        return 

    username = prompt_input(stdscr, "Enter username:")
    stdscr.clear()
    key = prompt_input(stdscr, "Do you want to generate a password? (y/n)")
    
    if key in ['y', 'Y']:
        length = int(prompt_input(stdscr, "Enter password length (minimum 4):"))
        include_uppercase = prompt_input(stdscr, "Include uppercase letters? (y/n):").lower() == 'y'
        include_numbers = prompt_input(stdscr, "Include numbers? (y/n):").lower() == 'y'
        include_special_chars = prompt_input(stdscr, "Include special characters? (y/n):").lower() == 'y'
        password = manager.generate_password(
            length=length,
            include_uppercase=include_uppercase,
            include_numbers=include_numbers,
            include_special_chars=include_special_chars
        )
        stdscr.addstr(5, 2, f"Generated Password: {password}")
        manager.add_account(name, username, password)
    else:
        password = prompt_input(stdscr, "Enter password:")
        is_leaked = manager.check_password_leak(password)
        if is_leaked:
            key = prompt_input(stdscr, "Password was leaked previously. Do you want to enter it anyway? (y/n):")
            if key in ['y', 'Y']:
                manager.add_account(name, username, password)
                stdscr.addstr(5, 2, f"Account {name} added.")
    stdscr.addstr(7, 2, "Press any key to return to the main menu.")

    stdscr.refresh()
    stdscr.getch() 

def get_account(stdscr, manager):
    name = prompt_input(stdscr, "Enter account name to retrieve:")
    acc = manager.get_account(name)
    stdscr.clear()
    if acc:
        stdscr.addstr(2, 2, f"Account: {acc.name}")
        stdscr.addstr(3, 2, f"Username: {acc.username}")
        stdscr.addstr(4, 2, f"Password: {acc.password}")
    else:
        stdscr.addstr(2, 2, f"Account '{name}' not found.")
    stdscr.addstr(6, 2, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def delete_account(stdscr, manager):
    name = prompt_input(stdscr, "Enter account name to retrieve:")
    if manager.delete_account(name):
        stdscr.addstr(5, 2, f"Account {name} deleted.")
    else:
        stdscr.addstr(5, 2, f"Account {name} not found.")
    stdscr.addstr(7, 2, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def list_accounts(stdscr, manager):
    stdscr.clear()
    stdscr.addstr(2, 2, "Stored accounts:")
    accounts = manager.list_all()
    if not accounts:
        stdscr.addstr(4, 4, "No accounts stored.")
    else:
        for idx, acc in enumerate(accounts):
            stdscr.addstr(4 + idx, 4, f"{1+idx}. {acc.name}. (Username: {acc.username})" )
    stdscr.addstr(7 + len(accounts), 2, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def edit_account(stdscr, manager):
    name = prompt_input(stdscr, "Enter the name of the account to edit:")
    account = manager.get_account(name)
    if not account:
        stdscr.addstr(5, 2, f"Account '{name}' not found.")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    stdscr.addstr(2, 2, f"Editing account '{name}'.")
    stdscr.addstr(4, 2, "Leave fields blank to keep the current value. Press any key to continue.")
    stdscr.refresh()
    stdscr.getch()


    new_name = prompt_input(stdscr, f"Enter new name (current: {account.name}):")
    new_username = prompt_input(stdscr, f"Enter new username (current: {account.username}):")
    new_password = prompt_input(stdscr, f"Enter new password (current: {'*' * len(account.password)}):")

    try:
        manager.edit_account(name, new_name=new_name or None, new_username=new_username or None, new_password=new_password or None)
        stdscr.addstr(7, 2, f"Account '{name}' edited.")
    except ValueError as e:
        stdscr.addstr(7, 2, str(e))
    stdscr.refresh()
    stdscr.getch()

def save_file(stdscr, manager):
    filepath = prompt_input(stdscr, f"Enter enter file path to save accounts (current directory: {os.getcwd()}):")
    password = prompt_input(stdscr, "Enter encryption password:")
    try:
        manager.save_to_file(manager, filepath, password)
        stdscr.addstr(5, 2, f"Accounts saved to '{filepath}'.")
    except Exception as e:
        stdscr.addstr(8, 2, f"Failed to save accounts: {str(e)}")
    stdscr.refresh()
    stdscr.getch()

def load_file(stdscr, manager):
    filepath = prompt_input(stdscr, f"Enter enter file path to load accounts (current directory: {os.getcwd()}):")
    stdscr.addstr(5, 2, "Enter master password:") 
    password = stdscr.getstr(6, 2).decode("utf-8")
    try:
        manager.load_from_file(manager, filepath, password)
        stdscr.addstr(8, 2, f"Accounts loaded from '{filepath}'.")
    except Exception as e:
        stdscr.addstr(8, 2, f"Failed to load accounts: {str(e)}")
    stdscr.refresh()
    stdscr.getch()

def run_curses():
    curses.wrapper(init_curses)

def init_curses(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    manager = Manager()
    main_menu(stdscr, manager)
