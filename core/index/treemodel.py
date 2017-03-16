import time
import Queue

# a class that it is a binary tree node which store dns data
# the key is "name"
# the value is "dtime,dtype,dclass,dttl,ddata"
# the left child is "left"
# the right child is "right"
class TreeNode():
	# constructor
	def __init__(self,name,dtime,dtype,dclass,dttl,ddata):
		self.name=name
		self.dtime=dtime
		self.dtype=dtype
		self.dclass=dclass
		self.dttl=dttl
		self.ddata=ddata
		self.left=None
		self.right=None

	# get its left child
	def getLeft(self):
		return self.left

	# get its right child
	def getRight(self):
		return self.right

	# set its left child
	def setLeft(self,left):
		self.left=left

	# set its right child
	def setRight(self,right):
		self.right=right

	# get its name
	def getName(self):
		return self.name

	# update its value only when time is smaller than the previous
	def updateValue(self,dtime,dtype,dclass,dttl,ddata):
		if dtime<self.dtime:
			self.dtime=dtime
			self.dtype=dtype
			self.dclass=dclass
			self.dttl=dttl
			self.ddata

	# get the format of dictionary which compare its key and value
	def dictFormat(self):
		packet={}
		packet['time']=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.dtime))
		packet['name']=self.name
		packet['type']=self.dtype
		packet['class']=self.dclass
		packet['ttl']=self.dttl
		packet['data']=self.ddata
		return packet


##################################################


# a treemap whose nodes store information about dns
class DnsTree():
	# constructor
	def __init__(self):
		self.root=None

	# push a new node into the tree
	# if exists a node which has the same name,then update its value
	def push(self,name,dtime,dtype,dclass,dttl,ddata):
		if self.root==None:
			self.root=TreeNode(name,dtime,dtype,dclass,dttl,ddata)
			return
		parent=None
		cur=self.root
		t=0
		while cur!=None:
			t=cmp(name,cur.getName())
			if t==0:
				cur.updateValue(dtime,dtype,dclass,dttl,ddata)
				return
			parent=cur
			if t<0:
				cur=cur.getLeft()
			else:
				cur=cur.getRight()
		newnode=TreeNode(name,dtime,dtype,dclass,dttl,ddata)
		if t<0:
			parent.setLeft(newnode)
		else:
			parent.setRight(newnode)

	# get the format of list
	# use BFS,when producing the list,del the node at the same time
	def listFormat(self):
		reslist=[]
		q=Queue.Queue()
		cur=self.root
		if cur!=None:
			q.put(cur)
		while q.empty()==False:
			cur=q.get()
			if cur.getLeft()!=None:
				q.put(cur.getLeft())
			if cur.getRight()!=None:
				q.put(cur.getRight())
			reslist.append(cur.dictFormat())
			del cur
		self.root=None
		return reslist
