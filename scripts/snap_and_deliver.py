#!/usr/bin/env python

import os
import glob

from common import doCmd, envSetup
from config import SNAPSHOT_WD, STORE_SNAPSHOTS, DELIVER_WD

def snapAndDeliver(): 
    curdir = os.path.abspath(os.curdir)

    os.chdir(SNAPSHOT_WD)
    print doCmd("snapshot")

    os.chdir(curdir)
    os.chdir(STORE_SNAPSHOTS)
    doCmd("frameit silver")

    for d in glob.glob("*-*"):
        # nuke all the non-framed pics
        cmd = "find %s -name \*.png -not -name \*framed.png -exec rm  {} \;" % d
        print doCmd(cmd)
    
    # Ship it!
    os.chdir(curdir)
    os.chdir(DELIVER_WD)
    cmd = "deliver -f run"
    print doCmd(cmd)

def main():
    envSetup()
    snapAndDeliver()
    
if __name__ == "__main__":
    print "Snap and Deliver Script"
    exit(main())