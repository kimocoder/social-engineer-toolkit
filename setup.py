#!/usr/bin/python
#
# quick installer for SET
#
#
from __future__ import print_function
import subprocess
import os
print("[*] Installing requirements.txt...")
subprocess.Popen("pip3 install -r requirements.txt --break-system-packages", shell=True).wait()
print("[*] Installing setoolkit to /usr/local/share/setoolkit")
print(os.getcwd())
subprocess.Popen("mkdir /usr/local/share/setoolkit/;mkdir /etc/setoolkit/;cp -rf * /usr/local/share/setoolkit/;cp src/core/config.baseline /etc/setoolkit/set.config", shell=True).wait()
print("[*] Creating launcher for setoolkit...")
filewrite = open("/usr/local/bin/setoolkit", "w")
filewrite.write("#!/bin/sh\ncd /usr/local/share/setoolkit\n./setoolkit")
filewrite.close()
print("[*] Done. Chmoding +x.... ")
subprocess.Popen("chmod +x /usr/local/bin/setoolkit", shell=True).wait()
print("[*] Finished. Run 'setoolkit' to start the Social Engineer Toolkit.")
