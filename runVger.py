# The runVger.py script will start up the website and make any mirgations necessary
#
# To execute this script type in the command line: python3 ./runVger.py
# Note: Must be in the /vger-devel1-dream-team directory to execute

import os
import sys
import subprocess
import time


def linuxStart():
    os.popen('docker-compose up')
    time.sleep(5.5)
    os.system('cd src/vger')
    os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py makemigrations')
    os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py migrate')
    os.system('cd ../..')
    print("Website is up and migrations are complete.")

def windowsStart():
    os.popen('docker-compose up')
    time.sleep(5.5)
    os.system('cd src/vger')
    os.system('docker-compose exec django python manage.py makemigrations')
    os.system('docker-compose exec django python manage.py migrate')
    os.system('cd ../..')
    print("Website is up and migrations are complete.")

def macOSStart():
    os.popen('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose up')
    time.sleep(5.5)
    os.system('cd src/vger')
    os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py makemigrations')
    os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 docker-compose exec django python manage.py migrate')
    os.system('cd ../..')
    print("Website is up and migrations are complete.")

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
