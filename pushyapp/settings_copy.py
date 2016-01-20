# Pushy Settings
#
# For start functionality
#   add to /etc/rc.local
#       nohup /absolute/path/to/file/run.py > /dev/null 2>&1 &
#
# make executable:
#   sudo chmod 755 run.py
#
# May need to change ownership of cam.py to root for access to hardware.
# Default root permissions for opencv camera interfacing:
#   sudo chown root:root /absolute/path/to/file/pushyapp/cam.py
#   sudo chmod 700
#
#   sudo visudo
#   (under %sudo):
#   yourusername ALL=(ALL) NOPASSWD: /absolute/path/to/file/pushyapp/cam.py
#   (at end):
#   yourusername ALL=(ALL:ALL) ALL

users = ['James Kominick']
key = 'yoursecretapikey'

import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
