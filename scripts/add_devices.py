#!/usr/bin/env python

#########################################################################################
# This script takes a single argument, the filename of a device file as produced by
# Crashlytics.  It adds the devices in that file to the dev portal.
#########################################################################################

import sys
from common import envSetup, doCmd

envSetup()

filename = sys.argv[1]
cmd = "./add_devices.rb %s" % filename
print doCmd(cmd)