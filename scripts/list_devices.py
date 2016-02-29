#!/usr/bin/env python

import sys
from common import envSetup, doCmd

envSetup()

cmd = "./list_devices.rb"
print doCmd(cmd)
