#!/usr/bin/env python
import random
from src.core import setcore as core

try:
    print ("\n         [****]  Custom Template Generator [****]\n")
    print ("\n   Always looking for new templates! In the set/src/templates directory send an email\nto davek@secmaniac.com if you got a good template!")
    author = input(core.setprompt("0", "Name of the author"))
    filename = randomgen = random.randrange(1, 99999999999999999999)
    filename = f"{filename}.template"
    subject = input(core.setprompt("0", "Email Subject"))
    try:
        body = input(core.setprompt(
            "0", "Message Body, hit return for a new line. Control+c when you are finished"))
        while body != 'sdfsdfihdsfsodhdsofh':
            try:
                body += (r"\n")
                body += input("Next line of the body: ")
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        pass
    with open(f"src/templates/{filename}", "w") as filewrite:
        filewrite.write(f"# Author: {author}" + "\n#\n#\n#\n")
        filewrite.write('SUBJECT=' + '"' + subject + '"\n\n')
        filewrite.write('BODY=' + '"' + body + '"\n')
        print("\n")
except Exception as e:
    print(f"   An error occured, printing error message: {str(e)}")
