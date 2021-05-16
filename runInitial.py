import os
import sys
import datetime, time

# Builds the Docker images,
# creates necessary directories with appropriate ownership,
# spins up the system to build empty databases,
# and spin the system back down.

# Mac, Linux, Windows
# 1. Build the server
# 2. Make migrations
# 3. Set up a root user
# 4. Spin the server up
# 5. Spin the server down

def linuxInstall():
    print("*************** Build the Server ***************")
    os.system('python3 run.py build')

    print("*************** Making Migrations ***************")
    os.system('sudo docker-compose run django python3 manage.py migrate --run-syncdb')

    print("*************** Set up a Root User ***************")
    os.system('sudo docker-compose run django python3 manage.py createsuperuser')

    print("*************** Spin up the Server ***************")
    os.system('python3 run.py up')

    print("*************** Spin the Server Down ***************")
    os.system('python3 run.py down')

    verifiedFile = open('verifiedInstall.txt', 'w+')
    dateTime = datetime.datetime.now()
    verifiedFile.write("You installed at: ")
    verifiedFile.write(str(dateTime))
    verifiedFile.close()

    print(" ")
    print("*************** Initial Install was ran on your Linux OS and your site is back down ***************")

def macInstall():
    print("*************** Build the Server ***************")
    os.system('python3 run.py build')

    print("*************** Making Migrations ***************")
    os.system('sudo docker-compose run django python3 manage.py migrate --run-syncdb')

    print("*************** Set up a Root User ***************")
    os.system('sudo docker-compose run django python3 manage.py createsuperuser')

    print("*************** Spin up the Server ***************")
    os.system('python3 run.py up')

    print("*************** Spin the Server Down ***************")
    os.system('python3 run.py down')

    verifiedFile = open('verifiedInstall.txt', 'w+')
    dateTime = datetime.datetime.now()
    verifiedFile.write("You installed at: ")
    verifiedFile.write(str(dateTime))
    verifiedFile.close()


    print(" ")
    print("*************** Initial Install was ran on your MacOS and your site is back down ***************")

def windowsInstall():
    print("*************** Build the Server ***************")
    os.system('docker-compose build')

    print("*************** Spin up the Server ***************")
    os.system('docker-compose up')

    print("*************** Making Migrations ***************")
    os.system('docker-compose migrate')

    print("*************** Set up a Root User ***************")
    os.system('docker-compose run django python3 run.py admin')

    print("*************** Spin the Server Down ***************")
    os.system('docker-compose down')

    verifiedFile = open('verifiedInstall.txt', 'w+')
    dateTime = datetime.datetime.now()
    verifiedFile.write("You installed at: ")
    verifiedFile.write(str(dateTime))
    verifiedFile.close()

    print(" ")
    print("*************** Initial Install was ran on your Windows OS and your site is back down ***************")

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
        linuxInstall()
    elif get_platform() == "Windows":
        windowsInstall()
    elif get_platform() == "OS X":
        macInstall()
    else:
        print("Your Operating System is not supported")

if __name__ == "__main__":
    main()
