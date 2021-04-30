# The runTest.py script will make sure the site is down, bring it up, run the test showing any errors, then bring the site back down.
#
# To execute this script type in the command line: python3 ./runTests.py
# Note: Must be in the /vger-devel1-dream-team directory to execute

import os
import sys
import subprocess
import time

def linuxTest():
    if(os.path.isfile('verifiedInstall.txt') == True):
        print("*************** Making sure site is down ***************")
        os.system('docker compose down')
        print("*************** Running Tests ***************")
        os.system('python3 run.py test')
        os.system('docker compose down')
        print(" ")
        print("*************** Test were ran on your Linux OS and your site is back down ***************")
    else:
        print("*** You must run runInitial.py first! See README.md for more information. ***")

def macTest():
    if(os.path.isfile('verifiedInstall.txt') == True):
        print("*************** Making sure site is down ***************")
        os.system('docker compose down')
        print("*************** Running Tests ***************")
        os.system('python3 run.py test')
        os.system('docker compose down')
        print(" ")
        print("*************** Test were ran on your MacOS and your site is back down ***************")
    else:
        print("*** You must run runInitial.py first! See README.md for more information. ***")

def windowsTest():
    if(os.path.isfile('verifiedInstall.txt') == True):
        print("*************** Making sure site is down ***************")
        os.system('docker-compose down')
        print("*************** Running Tests ***************")
        os.system('docker-compose run django python3 manage.py test')
        os.system('docker-compose down')
        print(" ")
        print("*************** Test were ran on your Windows OS and your site is back down ***************")
    else:
        print("*** You must run runInitial.py first! See README.md for more information. ***")

def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]

def main():
    if get_platform() == "linux":
        linuxTest()
    elif get_platform() == "Windows":
        windowsTest()
    elif get_platform() == "OS X":
        macTest()
    else:
        print("Your Operating System is not supported")

if __name__ == "__main__":
    main()
