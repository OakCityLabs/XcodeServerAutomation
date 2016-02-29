#!/usr/bin/env python

#
# This script runs after every build, developer and continuous integration.
#
# Should be run in the current directory, like so
#
# cd $SRCROOT/scripts/
# ./build_post.py

print "Xcode Post-Build Script"

from common import envSetup

envSetup()