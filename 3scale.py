#
# 3scale test by M. Dawcewicz
#

import urllib2
import json
import sys
import argparse

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("proxy", help="proxy server",nargs="?")
parser.add_argument("-u", "--http_user", help="HTTP user name")
parser.add_argument("-p", "--http_passwd", help="HTTP password")

args = parser.parse_args()

if args.proxy:
    servers_url = "http://%s/servers/" % (args.proxy)
    dc_url = "http://%s/datacenters/" % (args.proxy)

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, "http://"+args.proxy, args.http_user, args.http_passwd)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
else:
    servers_url = "http://servers-api.va.3sca.net/servers/"
    dc_url = "http://datacenters-api.va.3sca.net/datacenters/"


# retrieve datacenters
try:
    resp = urllib2.urlopen(dc_url)
    DCs = json.loads(resp.read())
except urllib2.URLError as e:
    print "Error '%s' while trying to read %s" %(e.reason,dc_url)
    sys.exit(1)


# retrieve servers
try:
    resp = urllib2.urlopen(servers_url + ".json")
    servers = json.loads(resp.read())
except urllib2.URLError as e:
    print "Error '%s' while trying to read %s" %(e.reason,servers_url)
    sys.exit(2)

if not (DCs and servers):
    print "Error. Exiting..."
    sys.exit(10)

# convert into a dictionary indexed by server ID
servers = dict([(srv['id'], dict([(k, v) for k, v in srv.items() if k != "id"])) for srv in servers])

# print the results
for DC in DCs:
    print "- Datacenter:\t%s" % (DC['name'])

    print "- Servers:"
    if 'servers' in DC:
        for srvid in DC['servers'].split(","):
            srvid = int(srvid)
            if srvid in servers:
                print "- %-20s: %s" % (servers[srvid]["name"], servers[srvid]["description"])
            else:
                print "- %-20s: Description unknown (ID: %i)" % ("Name unknown", srvid)
    else:
        print "- None found"
