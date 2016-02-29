#!/usr/bin/env python

from common import envSetup, buildXcConfig
    
def main():
    envSetup()
    buildXcConfig()
 
if __name__ == "__main__":
    print "Build xcconfig Script"
    print 
    print "  Before running this script, run download_profiles.py to insure provisioning profiles are up to date." 
    print
    exit(main())