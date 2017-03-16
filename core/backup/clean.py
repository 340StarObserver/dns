import os
import datetime
import json
import confmodel
import sys

# used to delete old zip data file in disc
# parameters:
# repositoryname 	: 	the name of backup repository
# indexstr 		: 	the name of index
def rmZipData(repositorylocation,indexstr):
	try:
		os.chdir(repositorylocation)
		os.system("/bin/rm %s-A.zip"%(indexstr))
		os.system("/bin/rm indices/%s-B.zip"%(indexstr))
		print "delete backup( %s ) success"%(indexstr)
	except:
		print "! fail to delete backup( %s )"%(indexstr)


# modify the file named "index"
def modifySnapshot(repositorylocation,indexstr):
	fb=None
	try:
		fb=open(repositorylocation+"/index","r")
		obj=json.loads(fb.read())
		obj['snapshots'].remove(indexstr)
		fb.close()
		fb=open(repositorylocation+"/index","w")
		fb.write(json.dumps(obj))
		print "modify %s/%s success"%(repositorylocation,indexstr)
	except Exception,e:
		print "!-- fail to modify %s/%s"%(repositorylocation,indexstr)
		print "reason : %s"%(str(e))
	finally:
		if fb!=None:
			fb.close()


# show help
def help():
	inform="this script used to delete old zip data file in disc"
	inform=inform+"\r\npython clean.py arg1"
	inform=inform+"\r\n\targ1 : which index you want to delete its zip data file"
	print inform


# entrance of this script
# steps:
# 1. delete zip file
# 2. modify the file named "index"
def entrance(configurefile):
	conf=confmodel.readconf(configurefile)
	#today=datetime.date.today()
	#thdate=today-datetime.timedelta(days=conf['deletelimit'])
	#indexstr="dns"+thdate.strftime("%Y%m%d")
	if len(sys.argv)<2:
		help()
		return
	indexstr=sys.argv[1]
	rmZipData(conf['repositorylocation'],indexstr)
	modifySnapshot(conf['repositorylocation'],indexstr)


if __name__ == '__main__':
	entrance("/home/seven/workspace/dns/conf/dns.conf")
