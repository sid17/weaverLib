from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
import json
import unicodedata
import sys
import os
import clientManager as CM
import time
import weaverWrapperFn as wp
import yaml
import ast
clientIP='172.31.33.213'
clientPort=2002
numThreads=2
threadPoolObj=CM.weaverThreadManager(clientIP,clientPort,numThreads)

def callWrapperFn(thread,fnName,params):
	print fnName
	if fnName=='returnNodesForward':
		rV=wp.returnNodesForward(thread,**params)
		return rV
	elif fnName=='getNode':
		rV=wp.getNode(thread,**params)
		return rV
	elif fnName=='oneHopGraphml':
		rV=wp.oneHopGraphml(thread,**params)
		return rV
	elif fnName=='returnNodesBackward':
		rV=wp.returnNodesBackward(thread,**params)
		return rV
	elif fnName=='returnNodeOneHopBackward':
		rV=wp.returnNodeOneHopBackward(thread,**params)
		return rV
	elif fnName=='returnNodeOneHopForward':
		rV=wp.returnNodeOneHopForward(thread,**params)
		return rV
	elif fnName=='InsertNode':
		rV=wp.InsertNode(thread,**params)
		return rV
	elif fnName=='InsertRelationUndirected':
		rV=wp.InsertRelationUndirected(thread,**params)
		return rV
	elif fnName=='oneHop':
		rV=wp.oneHop(thread,**params)
		return rV
	elif fnName=='returnPathMinMax':
		rV=wp.returnPathMinMax(thread,**params)
		return rV 

def execFn(request):
	if request.method=='GET':
		print 'Received Request'
		data=request.body
		data=ast.literal_eval(data)
		thread,index=threadPoolObj.getThread()
		print thread,index
		while not thread:
			time.sleep(10)
			thread,index=threadPoolObj.getThread()
		print 'Got Thread'+str(index)
		params=data["params"]
		fnName=data["fnName"]
		fnRetVal=callWrapperFn(thread,fnName,params)
		threadPoolObj.returnThread(index)
		print 'Return Thread'+str(index)
		return HttpResponse(json.dumps(fnRetVal), content_type="application/json")

