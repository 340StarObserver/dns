import urllib2
import json
import sys
import os
import datetime
import confmodel

# restore data from backup
# parameters:
# host,port 		: 	the host and port of elasticsearch
# repositoryname 	: 	the name of backup repository
# indexstr 		: 	the name of index
def restore(host,port,repositoryname,indexstr	):
	settings='{"indices":"%s"}'%(indexstr)
	url="http://%s:%d/_snapshot/%s/%s/_restore?wait_for_completion=true"%(host,port,repositoryname,indexstr)
	req=urllib2.Request(url,settings)
	try:
		res=urllib2.urlopen(req)
		print "restore index( %s ) success"%(indexstr)
		return True
	except:
		print "!-- fail to restore index( %s ), may be already exists"%(indexstr)
		return False


# decompress the backup in disc
def decompress(repositorylocation,indexstr):
	try:
		os.chdir(repositorylocation)
		os.system("unzip %s-A.zip"%(indexstr))
		os.system("unzip indices/%s-B.zip"%(indexstr))
		os.system("/bin/rm %s-A.zip"%(indexstr))
		os.system("/bin/rm indices/%s-B.zip"%(indexstr))
		return True
	except:
		return False


# delete a backup
# parameters:
# host,port 		: 	the host and port of elasticsearch
# repositoryname 	: 	the name of backup repository
# indexstr 		: 	the name of index
def deleteBackup(host,port,repositoryname,indexstr):
	url="http://%s:%d/_snapshot/%s/%s"%(host,port,repositoryname,indexstr)
	req=urllib2.Request(url)
	req.get_method=lambda:'DELETE'
	try:
		res=urllib2.urlopen(req)
		fd=json.loads(res.read())
		if fd['acknowledged']==True:
			print "delete backup( %s ) success"%(indexstr)
		else:
			print "!-- fail to delete backup( %s )"%(indexstr)
	except:
		print "!-- fail to delete backup( %s )"%(indexstr)


# entrance to restore data from backup
# steps:
# 1. decompress the backup
# 2. restore data
# 3. delete the backup
def entrance(configurefile):
	if len(sys.argv)<2:
		help()
		return
	indexstr=sys.argv[1]
	conf=confmodel.readconf(configurefile)
	if decompress(conf['repositorylocation'],indexstr)==True:
		res=restore(conf['host'],conf['port'],conf['repositoryname'],indexstr)
		if res==True:
			deleteBackup(conf['host'],conf['port'],conf['repositoryname'],indexstr)
			os.chdir(conf['repositorylocation'])
			os.system("/bin/rm -rf indices/%s"%(indexstr))
	else:
		print "failed to decompress backup( %s ) in disc"%(indexstr)


# show help
def help():
	inform="this script used to restore data from backup repository"
	inform=inform+"\r\npython restore.py arg1"
	inform=inform+"\r\n\targ1 : which index you want to restore"
	print inform


if __name__ == '__main__':
	entrance("/home/seven/workspace/dns/conf/dns.conf")
