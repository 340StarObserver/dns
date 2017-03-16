import urllib2
import json
import sys
import confmodel

# create a backup repository and initialize its settings
# parameters:
# host,port 			: 	the host and port of elasticsearch
# repositoryname 		: 	the name of backup repository
# repositorylocation 		: 	the absoluate path of backup repository
# backupSpeed 		: 	the max speed of backup
# restoreSpeed 		: 	the max speed of restore
def initRepository(host,port,repositoryname,repositorylocation,backupSpeed,restoreSpeed):
	settings='{"type":"fs","settings":{"location":"%s","max_snapshot_bytes_per_sec":"%s","max_restore_bytes_per_sec":"%s"}}'%(repositorylocation,backupSpeed,restoreSpeed)
	url="http://%s:%d/_snapshot/%s"%(host,port,repositoryname)
	req=urllib2.Request(url,settings)
	req.get_method=lambda:'PUT'
	try:
		res=urllib2.urlopen(req)
		feedback=json.loads(res.read())
		if feedback['acknowledged']==True:
			print "init repository success"
		else:
			print "!-- fail to init repository"
	except Exception,e:
		print "!-- fail to init repository"
		print "reason : %s"%(str(e))
		sys.exit(1)


# the entrance to create and init the backup repository
def entrance(configurefile):
	conf=confmodel.readconf(configurefile)
	initRepository(conf['host'],conf['port'],conf['repositoryname'],conf['repositorylocation'],conf['snapshotSpeed'],conf['restoreSpeed'])


if __name__ == '__main__':
	entrance("/home/seven/workspace/dns/conf/dns.conf")
