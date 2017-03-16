import urllib2
import json
import datetime
import os
import sys
import confmodel
from elasticsearch import Elasticsearch

# judge whether an index need to backup
# parameters:
# host,port 		: 	the host and port of elasticsearch
# indexstr 		: 	the name of index
def needBackup(host,port,indexstr):
	es=Elasticsearch("%s:%d"%(host,port))
	count1=0
	count2=0
	try:
		count1=es.count(index=indexstr,doc_type="querydata")['count']
		count2=es.count(index=indexstr,doc_type="dnsdata")['count']
	except:
		pass
	return count1+count2>0


# make a snapshot backup for an index
# parameters:
# host,port 		: 	the host and port of elasticsearch
# repositoryname 	: 	the name of backup repository
# indexstr 		: 	the name of index
def backup(host,port,repositoryname,indexstr):
	settings='{"indices":"%s"}'%(indexstr)
	url="http://%s:%d/_snapshot/%s/%s?wait_for_completion=true"%(host,port,repositoryname,indexstr)
	req=urllib2.Request(url,settings)
	req.get_method=lambda:'PUT'
	try:
		res=urllib2.urlopen(req)
		print "backup index( %s ) success"%(indexstr)
		return True
	except:
		print "!-- fail to backup index( %s ), may be this backup already exists"%(indexstr)
		return False


# delete a index
# parameters:
# host,port 		: 	the host and port of elasticsearch
# indexstr 		: 	the name of index
def deleteIndex(host,port,indexstr):
	url="http://%s:%d/%s"%(host,port,indexstr)
	req=urllib2.Request(url)
	req.get_method=lambda:'DELETE'
	try:
		res=urllib2.urlopen(req)
		fd=json.loads(res.read())
		if fd['acknowledged']==True:
			print "delete index( %s ) from elasticsearch success"%(indexstr)
		else:
			print "!-- fail to delete index( %s ) from elasticsearch"%(indexstr)
	except:
		print "!-- fail to delete index( %s ) from elasticsearch"%(indexstr)


# compress the backup in disc
# cmd1 	: 	zip the data files of this index
# cmd2 	: 	zip other files of this index
# cmd3 	: 	delete the original data files
# cmd4 	: 	delete the original other files
def compress(repositorylocation,indexstr):
	os.chdir(repositorylocation)
	cmd1="zip %s-A.zip *%s.dat"%(indexstr,indexstr)
	cmd2="zip -r indices/%s-B.zip indices/*%s"%(indexstr,indexstr)
	cmd3="/bin/rm *%s.dat"%(indexstr)
	cmd4="/bin/rm -rf indices/%s"%(indexstr)
	os.system(cmd1)
	os.system(cmd2)
	os.system(cmd3)
	os.system(cmd4)


# the entrance of make a snapshot
# steps:
# 1. read configure file, determine which index to be backup
# 2. judge whether that index necessary to be backup
# 3. export that index to disc
# 4. delete that index from elasticsearch
# 5. compress the backup
def entrance(configurefile):
	indexstr=None
	willcompress=None
	willdelete=None
	right=True
	try:
		indexstr=sys.argv[2]
		willcompress=sys.argv[4]
		willdelete=sys.argv[6]
	except:
		right=False
	if right==False:
		help(configurefile)
		return
	conf=confmodel.readconf(configurefile)
	if needBackup(conf['host'],conf['port'],indexstr)==True:
		res=backup(conf['host'],conf['port'],conf['repositoryname'],indexstr)
		if res==True:
			if willdelete=="true":
				deleteIndex(conf['host'],conf['port'],indexstr)
			if willcompress=="true":
				compress(conf['repositorylocation'],indexstr)
	else:
		print "index( %s ) has no data,so not need to backup it"%(indexstr)


# show help
def help(configurefile):
	inform="""This script used to export an index to backup repository
sysopsis : python export.py -i arg1 -c arg2 -d arg3
	arg1 : the name of an index
	arg2 : true -> will compress, false -> will not
	arg3 : true -> will delete index from elasticsearch, false -> will not
some other configure terms are at %s
	"""%(configurefile)
	print inform


if __name__ == '__main__':
	entrance("/home/seven/workspace/dns/conf/dns.conf")
