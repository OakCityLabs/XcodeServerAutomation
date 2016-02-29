#!/usr/bin/env python

#
# This script runs before continuous integration builds, not developer builds.
#
# Should be run in the current directory, like so
#
# cd $XCS_SOURCE_DIR/<projectname>/scripts/
# ./bot_pre.py

from config import XCCONFIG
from common import envSetup, tagRevision
from download_profiles import downloadProfiles

envSetup()

print "Xcode Bot Pre-Integration Script"

# touch the xcconfig file, to make xcode happy that it exists
open(XCCONFIG, 'w').close()

# Update provisioning profiles from the dev portal
downloadProfiles()
tagRevision()
