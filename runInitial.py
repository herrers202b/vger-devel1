import os
import sys

# Builds the Docker images,
# creates necessary directories with appropriate ownership,
# spins up the system to build empty databases,
# and spin the system back down.

# Mac, Linux
# 1. Build the server
# 2. Set up a root user
# 3. Spin the server up
# 4. Spin the server down

# Windows
# 1. Build the server
# 2. Spin the server up
# 3. Spin the server down

def linuxInstall():
    print("*************** Build the Server ***************")
    os.system('python3 run.py build')

    print("*************** Set up a Root User ***************")
    os.system('python3 run.py admin')

    print("*************** Spin up the Server ***************")
    os.system('python3 run.py up')

    print("*************** Spin the Server Down ***************")
    os.system('python3 run.py down')
    print("Initial Innstall was ran on your Linux OS and your site is back down.")

def macInstall():
    print("*************** Build the Server ***************")
    os.system('python3 run.py build')

    print("*************** Set up a Root User ***************")
    os.system('python3 run.py admin')

    print("*************** Spin up the Server ***************")
    os.system('python3 run.py up')

    print("*************** Spin the Server Down ***************")
    os.system('python3 run.py down')
    print("Initial Install was ran on your MacOS and your site is back down.")

def windowsInstall():
    print("*************** Build the Server ***************")
    os.system('docker-compose build')

    print("*************** Spin up the Server ***************")
    os.system('docker-compose up')

    print("*************** Spin the Server Down ***************")
    os.system('docker-compose down')
    print("Initial Install was ran on your Windows OS and your site is back down.")

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
