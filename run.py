#!/home/james/projects/pushy/pbenv/bin/python
# update to your virtualenv

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from pushyapp import pushy

pushy.start()
