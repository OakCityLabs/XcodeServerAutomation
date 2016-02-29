#!/usr/bin/env python

from common import find_uuid_adhoc, find_uuid_development, find_uuid_appstore

print "Development:", find_uuid_development()
print "AdHoc:", find_uuid_adhoc()
print "AppStore:", find_uuid_appstore()