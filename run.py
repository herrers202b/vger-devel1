#!/usr/bin/env python3
import sys
import os

#Prints 
def usage():
    print("Usage: run.py\n" + 
            "\tmigrate \t- makes migrations and applies them\n" + 
            "\tup [-d] \t- spins up the djangosite [runs quietly]\n" + 
            "\tdown \t\t- brings the docker container down\n" +
            "\tbuild \t\t- builds docker-compose images\n" + 
            "\tadmin [name]\t- creates a new superuser [with given name]\n" + 
            "\tinspectdb \t- inspects the django database setups\n" + 
            "\town \t\t- changes current user to new owner of all subdirectors\n" + 
            "\tstartapp 'name'\t- creates a new app subdirectory with given name (required)\n" +
            "\ttest \t\t- runs all test files in project apps, optional app name to test specific app\n" + 
            "\tpab \t\t- pulls all remote branches\n" +
            "\tkill \t\t- kills all running docker containers\n" +
            "\tdbflush \t- flushes the current database froom the system\n")

import sys
import os

def main():
    
    # Starts the server
    if 'up'.strip() in sys.argv:
        os.system("sudo docker-compose run django manage.py collectstatic --noinput --clear")
        if '-d'.strip() in sys.argv:
            os.system("sudo docker-compose up -d")
        else:
            os.system("sudo docker-compose up")

    # Allows us to run a docker-compose down.
    elif 'down'.strip() in sys.argv:
        os.system("sudo docker-compose down")

    # Builds the containers
    elif 'build'.strip() in sys.argv:
        os.system("sudo docker-compose build")

    # Does the migrations
    elif 'migrate'.strip() in sys.argv:
        os.system("sudo docker-compose run django python3 manage.py makemigrations base")
        os.system("sudo docker-compose run django python3 manage.py makemigrations user")
        os.system("sudo docker-compose run django python3 manage.py migrate base")
        os.system("sudo docker-compose run django python3 manage.py migrate user")
        
    # Creates a superuser
    elif 'admin'.strip() in sys.argv:
        if len(sys.argv) == 3:
            os.system("sudo docker-compose run django python3 manage.py createsuperuser " + sys.argv[2])
        else:
            os.system("sudo docker-compose run django python3 manage.py createsuperuser")

    # Creates a superuser
    elif 'inspectdb'.strip() in sys.argv:
        os.system("sudo docker-compose run django python3 manage.py inspectdb")

    #makes current user owner of all subdirectories/files
    elif 'own'.strip() in sys.argv:
        os.system("sudo chown -R $USER:$USER .")

    #creates a new app subdirectory in django with given name
    elif 'startapp'.strip() in sys.argv:
        if len(sys.argv) == 3:
            os.system("sudo docker-compose run django python3 manage.py startapp " + sys.argv[2])
        else:
            usage()

    #runs the projects test files
    elif 'test'.strip() in sys.argv:
        if len(sys.argv) == 3:
            os.system("sudo docker-compose run django python3 manage.py test " + sys.argv[2])
        else:
            os.system("sudo docker-compose run django python3 manage.py test")
    elif 'pab'.strip() in sys.argv:
        os.system("git branch -r | grep -v '\->' | while read remote; do git branch --track \"${remote#origin/}\" \"$remote\"; done")

    elif 'kill'.strip() in sys.argv:
        os.system("sudo docker kill $(sudo docker ps -a -q)")
        os.system("sudo docker rm $(sudo docker ps -a -q)")
    
    elif 'dbflush'.strip() in sys.argv:
        os.system("sudo docker kill $(sudo docker ps -a -q)")
        os.system("sudo docker rm $(sudo docker ps -a -q)")
        #os.system("sudo docker-compose run django python3 manage.py flush")
        os.system("sudo chown -R $USER:$USER .")
        os.system("sudo rm -rf data/")
        os.system("sudo rm src/vger/db.sqlite3")
        os.system("sudo docker-compose run django python3 manage.py makemigrations")
        os.system("sudo docker-compose run django python3 manage.py migrate")
    else:   
        usage()



# end program    
if __name__=="__main__":
    main()
