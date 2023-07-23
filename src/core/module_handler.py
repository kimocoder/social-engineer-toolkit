#!/usr/bin/env python

# module_handler.py

import glob
import re
import sys
from src.core.setcore import *

# base counter to identify numbers
counter = 0

# get the menu going
print("\n")
print_info_spaces("Social-Engineer Toolkit Third Party Modules menu.")
print_info_spaces(
    "Please read the readme/modules.txt for information on how to create your own modules.\n")

for name in glob.glob("modules/*.py"):

    counter = counter + 1
    fileopen = open(name, "r")

    for line in fileopen:
        line = line.rstrip()
        if match := re.search("MAIN=", line):
            line = line.replace('MAIN="', "")
            line = line.replace('"', "")
            line = f"  {str(counter)}. {line}"
            print(line)

print("\n  99. Return to the previous menu\n")
choice = raw_input(setprompt(["9"], ""))

if choice == 'exit':
    exit_set()

menu_return = "true" if choice == '99' else "false"
# throw error if not integer
try:
    choice = int(choice)
except:
    print_warning("An integer was not used try again")
    choice = raw_input(setprompt(["9"], ""))

# start a new counter to match choice
counter = 0

if menu_return == "false":
    # pull any files in the modules directory that starts with .py
    for name in glob.glob("modules/*.py"):

        counter = counter + 1

        if counter == int(choice):
            # get rid of .modules extension
            name = name.replace("modules/", "")
            # get rid of .py extension
            name = name.replace(".py", "")
            # changes our system path to modules so we can import the files
            sys.path.append("modules/")
            # this will import the third party module

            try:
                exec(f"import {name}")
            except:
                pass

            # this will call the main() function inside the python file
            # if it doesn't exist it will still continue just throw a warning
            try:
                exec(f"{name}.main()")
            except Exception as e:
                raw_input(f"   [!] There was an issue with a module: {e}.")
                return_continue()
