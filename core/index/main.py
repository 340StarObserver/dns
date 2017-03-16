# the driver program that can read all data files and push data into elasticsearch

import confmodel
import logmodel
import elasticmodel
import metaAnalyzer
import treemodel
import datetime

# steps:
# 1. read configuration
# 2. create logger manager
# 3. get paths of all data file
# 4. initialize the index and type
# 5. analyse each file,and put data into elasticsearch
# parameter:
# configurefile 	: 	the absoluate path of your configure file
def entrance(configurefile):
	conf=confmodel.readconf(configurefile)

	today=datetime.date.today()
	yesterday=today-datetime.timedelta(days=1)
	logger=logmodel.createlogger(conf['log_dir']+str(yesterday)+".log")
	logger.debug("read configure file successfully")

	metafiles=metaAnalyzer.getpathlist(conf['data_dir']+str(yesterday)+"/",logger)
	
	indexstr="dns"+yesterday.strftime("%Y%m%d")
	elasticmodel.initIndex(conf['host'],conf['port'],indexstr,logger)
	elasticmodel.initType(conf['host'],conf['port'],indexstr,"querydata","question",logger)
	elasticmodel.initType(conf['host'],conf['port'],indexstr,"dnsdata","name",logger)

	conn=elasticmodel.getconnect(conf['host'],conf['port'])
	query_size=elasticmodel.docsize(conn,indexstr,"querydata")
	query_startid=query_size+1
	data_size=elasticmodel.docsize(conn,indexstr,"dnsdata")
	data_startid=data_size+1

	logger.debug("start analysing file and putting data into elasticsearch")
	query_total=0
	data_total=0
	treemap=treemodel.DnsTree()
	for file in metafiles:
		datalist=metaAnalyzer.readfile(file,logger,treemap)
		query_total+=len(datalist)
		query_startid=elasticmodel.addbatch(conn,indexstr,"querydata",datalist,conf['batch_size'],query_startid,logger)
		del datalist[:]
	reslist=treemap.listFormat()
	data_total=len(reslist)
	elasticmodel.addbatch(conn,indexstr,"dnsdata",reslist,conf['batch_size'],data_startid,logger)
	del reslist[:]
	logger.debug("All done")
	logger.debug("%s querydata pushed : %d"%(indexstr,query_total))
	logger.debug("%s dnsdata pushed : %d"%(indexstr,data_total))

if __name__ == '__main__':
	entrance("/home/seven/workspace/dns/conf/dns.conf")
