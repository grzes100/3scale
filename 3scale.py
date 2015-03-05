#
# 3scale test by M. Dawcewicz
#

import urllib2
import json
import sys

servers_url = "http://servers-api.va.3sca.net/servers/"
dc_url = "http://datacenters-api.va.3sca.net/datacenters/"

resp = urllib2.urlopen(dc_url)
DCs = json.loads(resp.read())

resp = urllib2.urlopen(servers_url + ".json")
servers = json.loads(resp.read())

if not (DCs and servers):
    print "Error"
    sys.exit(1)

# convert into a dictionary indexed by server ID
servers = dict([(srv['id'], dict([(k, v) for k, v in srv.items() if k != "id"])) for srv in servers])

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
