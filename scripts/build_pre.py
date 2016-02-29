#!/usr/bin/env python

#
# This script runs before every build, developer and continuous integration.
#
# Should be run in the current directory, like so
#
# cd $SRCROOT/scripts/
# ./build_pre.py


from common import buildXcConfig, envSetup

envSetup()

def main():
    envSetup()
    buildXcConfig()
 
if __name__ == "__main__":
    print "Xcode Pre-Build Script"
    exit(main())

