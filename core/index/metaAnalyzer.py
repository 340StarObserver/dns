# used to analyse metadata files

import os
import struct
import socket
import dnslib
import time
import sys

# this function calculate all files' names in the direction of "datadir"
# parameter "datadir"  is an absolute path
# the return value is a list,such as ["datadir/1.txt","datadir/2.txt","datadir/3.txt"]
def getpathlist(datadir,logger):
	res=[]
	try:
		res=os.listdir(datadir)
		n=len(res)
		i=0
		while i<n:
			res[i]=datadir+res[i]
			i+=1
		return res
	except:
		logger.error("!-- not found medata direction : "+datadir)
		sys.exit(1)


# read a binary file and analyse
# parameters:
# 	"path" is the filename and path of a file
# 	"logger" is a log manager
#	"treemap" is a binary tree that store information about dns
# return value:
# 	a list of dictionaries,each dictionary includes(time,srcip,srcport,dstip,dstport,question)
def readfile(path,logger,treemap):
	longsize=8
	intsize=4
	shortsize=2
	reslist=[]
	count=0
	with open(path,"rb") as f:
		while True:
			chunkbuf=f.read(intsize)
			if len(chunkbuf)<4:
				break
			req_flag=socket.ntohl(struct.unpack("!I", chunkbuf)[0])

			chunkbuf=f.read(longsize)
			timesec=struct.unpack("Q", chunkbuf)[0]
			chunkbuf=f.read(longsize)
			timeusec = struct.unpack("Q", chunkbuf)[0]

			chunkbuf=f.read(intsize)
			srcint=struct.unpack("!L", chunkbuf)[0]
			srcstr=socket.inet_ntoa(chunkbuf)
			chunkbuf=f.read(intsize)
			dstint=struct.unpack("!L", chunkbuf)[0]
			dststr=socket.inet_ntoa(chunkbuf)

			chunkbuf=f.read(shortsize)
			sport=socket.ntohs(struct.unpack("!H", chunkbuf)[0])
			chunkbuf=f.read(shortsize)
			dport=socket.ntohs(struct.unpack("!H", chunkbuf)[0])

			chunkbuf=f.read(intsize)
			buflen=socket.ntohl(struct.unpack("!L", chunkbuf)[0])
			if(buflen<=1460):
				buf=f.read(buflen)
			else:
				logger.error("Error : buflen %d %d"%(buflen,socket.ntohl(buflen)))
				break
			try:
				dns=dnslib.DNSRecord.parse(buf)
				if req_flag==20:
					for r in dns.questions:
						tmp={}
						tmp['time']=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timesec))
						tmp['srcip']=srcstr
						tmp['srcport']=sport
						tmp['dstip']=dststr
						tmp['dstport']=dport
						tmp['question']=str(r.qname)
						reslist.append(tmp)
						del tmp
					for r in dns.rr:
						treemap.push(str(r.rname),timesec,r.rtype,r.rclass,r.ttl,str(r.rdata))
					for r in dns.auth:
						treemap.push(str(r.rname),timesec,r.rtype,r.rclass,r.ttl,str(r.rdata))
					for r in dns.ar:
						try:
							treemap.push(str(r.rname),timesec,r.rtype,r.rclass,r.ttl,str(r.rdata))
						except:
							pass
			except dnslib.dns.DNSError as err:
				logger.error("My Error : %s"%(str(err)))
			except :
				logger.error("Unexpected Error")
			count=count+1
			if count%50000==0:
				logger.debug("deal line: %d"%(count))
	logger.debug("finish analyse: %s"%(path))
	return reslist
