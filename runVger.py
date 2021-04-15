# The runVger.py script will start up the website and make any mirgations necessary
#
# To execute this script type in the command line: python3 ./runVger.py
# Note: Must be in the /vger-devel1-dream-team directory to execute

import os
import sys
import subprocess
import time


def linuxStart():
    if(os.path.isfile('verifiedInstall.txt') == True):
        print('I am in a Docker Container')
        print("*************** Starting the Server ***************")
        os.popen('docker-compose up')
        time.sleep(5.5)
        print(" ")
        print("*************** Making Migrations ***************")
        os.system('cd src/vger')
        os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py makemigrations')
        os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py migrate')
        os.system('cd ../..')
        print(" ")
        print("***** Website is up and migrations are complete on your Linux OS *****")
        print(" ")
    else:
        print("*** You must run runInitial.py first! See README.md for more information. ***")

def windowsStart():
    if(os.path.isfile('verifiedInstall.txt') == True):
        print("*************** Starting the Server ***************")
        os.popen('docker-compose up')
        time.sleep(5.5)  
        print(" ")
        print("*************** Making Migrations ***************")
        os.system('cd src/vger')
        os.system('docker-compose exec django python manage.py makemigrations')
        os.system('docker-compose exec django python manage.py migrate')
        os.system('cd ../..')
        print(" ")
        print("***** Website is up and migrations are complete on your Windows OS *****")
        print(" ")
    else:
        print("*** You must run runInitial.py first! See README.md for more information. ***")

def macOSStart():
    if(os.path.isfile('verifiedInstall.txt') == True):
        print("*************** Starting the Server ***************")
        os.popen('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose up')
        time.sleep(5.5)
        print(" ")
        print("*************** Making Migrations ***************")
        os.system('cd src/vger')
        os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py makemigrations')
        os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py migrate')
        os.system('cd ../..')
        print(" ")
        print("***** Website is up and migrations are complete on your Mac OS *****")
        print(" ")
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
        linuxStart()
    elif get_platform() == "Windows":
        windowsStart()
    elif get_platform() == "OS X":
        macOSStart()
    else:
        print("Your Operating System is not supported")


if __name__ == "__main__":
    main()
