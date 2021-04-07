# The runTest.py script will make sure the site is down, bring it up, run the test showing any errors, then bring the site back down. 
#
# To execute this script type in the command line: python3 ./runTests.py
# Note: Must be in the /vger-devel1-dream-team directory to execute

import os
import sys
import subprocess
import time


def linuxTest():
    print("*************** Making sure site is down ***************")
    os.system('docker compose down')
    print("*************** Running Tests ***************")
    os.system('python3 run.py test')
    os.system('docker compose down')
    print("Test were ran on your Linux OS and your site is back down.")

def macTest():
    print("*************** Making sure site is down ***************")
    os.system('docker compose down')
    print("*************** Running Tests ***************")
    os.system('python3 run.py test')
    os.system('docker compose down')
    print("Test were ran on your MacOS and your site is back down.")
    
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
