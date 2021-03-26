# The closeVger.py script will close down the website 
# # 
# To execute this script type in the command line: python3 ./closeVger
# To execute this script type in the command line: python3 ./closeVger.py
# Note: Must be in the /vger-devel1-dream-team directory to execute

import os

os.system('docker compose down')
print("Website is now offline.")