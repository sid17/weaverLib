from weaver import client
from threading import Lock
clientLock=Lock()
class weaverThreadManager:
	def __init__(self,clientIP,clientPort,numThreads):
		self.clientIP = clientIP
		self.clientPort = clientPort
		self.threadPool = []
		self.createPool(numThreads)

	def _create_weaver_client(self):
		try:
			c = client.Client(self.clientIP, self.clientPort)
			return c
		except:
			print 'Connection to Client Failed, Check if the weaver instance is running'
			return None

	def createPool(self,numThreads):
		with clientLock:
			for i in range(numThreads):
				c = self._create_weaver_client()
				if c:
					self.threadPool.append(c)
				else:
					return False

	def getThread(self):
		with clientLock:
			if self.threadPool:
				c = self.threadPool[-1]
				self.threadPool.pop()
				return c
			else:
				return self._create_weaver_client()

	def returnThread(self,c):
		with clientLock:
			self.threadPool.append(c)
