# The runVger.py script will start up the website and make any mirgations necessary
# 
# To execute this script type in the command line: python3 ./runVger
# Note: Must be in the /vger-devel1-dream-team directory to execute

import os

os.popen('docker-compose up')
os.system('cd src/vger')
os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 sudo docker-compose exec django python manage.py makemigrations')
os.system('HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 sudo docker-compose exec django python manage.py migrate')
os.system('cd ../..')
print("Website is up and migrations are complete.")
