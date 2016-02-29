#!/usr/bin/env python

from common import envSetup, doCmd
from config import DELIVER_WD

def downloadMetadata(): 
    curdir = os.path.abspath(os.curdir)
    os.chdir(DELIVER_WD)
    cmd = "echo y|deliver download_metadata"
    doCmd(cmd)

def main():
    envSetup()
    downloadMetadata()
 
if __name__ == "__main__":
    print "Download Metadata Script"
    exit(main())