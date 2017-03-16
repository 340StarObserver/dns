# used to read configuration of this program,
# it return a dictionary of <key,value>

import ConfigParser
import sys

def readconf(filename):
	data={}
	config=ConfigParser.ConfigParser()
	try:
		config.read(filename)
		data['data_dir']=config.get("dns", "data_dir")
		data['log_dir']=config.get("dns", "log_dir")
		data['batch_size']=int(config.get("dns", "batch_size"))
		data['host']=config.get("dns","host")
		data['port']=int(config.get("dns","port"))
		data['repositoryname']=config.get("backup","repositoryname")
		data['repositorylocation']=config.get("backup","repositorylocation")
		data['snapshotSpeed']=config.get("backup","snapshotSpeed")
		data['restoreSpeed']=config.get("backup","restoreSpeed")
		data['backuplimit']=int(config.get("backup","backuplimit"))
		data['deletelimit']=int(config.get("backup","deletelimit"))
	except StandardError, e:
		print "failed to read conf,reason is %s"%(e)
		sys.exit(1)
	except:
		print "failed to read conf,may be your path is not exist"
		sys.exit(1)
	return data
