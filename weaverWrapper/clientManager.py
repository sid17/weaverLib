from weaver import client
class weaverThreadManager:
	def __init__(self,clientIP,clientPort,numThreads):
		self.clientIP = clientIP
		self.clientPort = clientPort
		self.numThreads=numThreads
		self.threadPool=list()
		self.threadStatus=list()
		self.createPool(numThreads)
	def createPool(self,numThreads):
		for i in range(numThreads):
			try:
				c=client.Client(self.clientIP,self.clientPort)
				self.threadPool.append(c)
				self.threadStatus.append(False)
			except:
				print 'Connection to Client Failed, Check if the weaver instance is running'
				assert False
	def getThread(self):
		for i in range(self.numThreads):
			if (not self.threadStatus[i]):
				self.threadStatus[i]=True
				return self.threadPool[i],i
		return False,0

	def returnThread(self,i):
		self.threadStatus[i]=False



