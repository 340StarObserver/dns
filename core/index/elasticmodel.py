from elasticsearch import helpers
from elasticsearch import Elasticsearch
from datetime import date
import urllib2
import json
import sys

# create a connect to elasticsearch
# parameter "host","port" are the host and the port of elasticsearch
def getconnect(host,port):
	es=Elasticsearch("%s:%d"%(host,port))
	return es


# get the number of documents of a type
# parameters:
# "es" 			: 	the connection with elasticsearch
# "indexstr" 		: 	determine which index
# "typestr" 		: 	determine which type
def docsize(es,indexstr,typestr):
	try:
		res=es.count(index=indexstr,doc_type=typestr)
		return res['count']
	except:
		return 0


# add more than one document in a batch request
# parameters:
# "es" 			: 	the connection with elasticsearch
# "indexstr" 		: 	determine which index
# "typestr" 		: 	determine which type
# "data" 		: 	a list of dictionaries,each dictionary is one document
# "batchsize" 		: 	how many documents are added in one request
# "startid" 		: 	the _id start begin with what
# "logger" 		: 	your logger
# return value:
# it is the startid of next add.for example,"startid"=1,len(data)=50,the return value will be 51
def addbatch(es,indexstr,typestr,data,batchsize,startid,logger):
	i=0
	actions=[]
	for d in data:
		action={}
		action['_index']=indexstr
		action['_type']=typestr
		action['_source']=d
		action['_source']['pagingid']=startid+i
		actions.append(action)
		i+=1
		del action
		if i%batchsize==0:
			helpers.bulk(es,actions)
			del actions[:]
			logger.debug("%s : %s pushed: %d"%(indexstr,typestr,i))
	if i%batchsize>0:
		helpers.bulk(es,actions)
		del actions[:]
		logger.debug("%s : %s pushed: %d"%(indexstr,typestr,i))
	return startid+i


# initialize the settings of index
# parameters:
# host,port 		: 	the host and port of elasticsearch
# indexstr 		: 	the index
# logger 		: 	the logger
def initIndex(host,port,indexstr,logger):
	jsonsetting='{"settings": {"analysis": {"tokenizer": {"domain_name_tokenizer": {"delimiter": ".", "type": "PathHierarchy", "reverse": true}}, "analyzer": {"domain_name_analyzer": {"filter": "lowercase", "type": "custom", "tokenizer": "domain_name_tokenizer"}}}}}'
	url="http://%s:%d/%s"%(host,port,indexstr)
	req=urllib2.Request(url)
	try:
		res=urllib2.urlopen(req)
		logger.debug("index( dns ) already exists")
	except:
		logger.debug("index( dns ) not exists,it will be created")
		req=urllib2.Request(url,jsonsetting)
		res=urllib2.urlopen(req)
		fd=json.loads(res.read())
		if fd['acknowledged']==True:
			logger.debug("index( dns ) successfully create and init settings")
		else:
			logger.debug("index( dns ) failed to create and inti settings")
			sys.exit(1)


# initialize the settings of type
# parameters:
# host,port 		: 	the host and port of elasticsearch
# indexstr 		: 	the index
# typestr 		: 	the type
# term 		: 	the term which use domain_name_analyzer
# logger 		: 	the logger
def initType(host,port,indexstr,typestr,term,logger):
	jsonsetting='{"properties": {"%s": {"type": "string", "analyzer": "domain_name_analyzer"}}}'%(term)
	url_1="http://%s:%d/%s/_mapping/%s"%(host,port,indexstr,typestr)
	req=urllib2.Request(url_1)
	w=False
	try:
		res=urllib2.urlopen(req)
		if len(res.read())!=2:
			logger.debug("type( %s : %s ) already exists"%(indexstr,typestr))
			w=True
		else:
			logger.debug("type( %s : %s ) not exists,it will be created"%(indexstr,typestr))
			url_2="http://%s:%d/%s/_mapping/%s"%(host,port,indexstr,typestr)
			req=urllib2.Request(url_2,jsonsetting)
			res=urllib2.urlopen(req)
			fd=json.loads(res.read())
			if fd['acknowledged']==True:
				logger.debug("type( %s : %s ) successfully create and init settings"%(indexstr,typestr))
				w=True
	except:
		pass
	if w==False:
		logger.debug("type( %s : %s ) failed to create and inti settings"%(indexstr,typestr))
		sys.exit(1)
