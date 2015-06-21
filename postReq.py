import json
import yaml
import urllib,requests
import ast
def PostWeaverQuery(fnName,params):
		query=dict(fnName=fnName,params=params)
		myport=3232
		data=json.dumps(query)
		myURL = "http://127.0.0.1:%s/weaverWrapper/execFn/" % (myport)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.get(myURL, data=data,headers=headers)
		response=yaml.safe_load(r.text)
		return response

if __name__ == '__main__':

	fnName='returnNodesForward'
	params=dict(src='watching',path_len_min=1,path_len_max=2)
	result=PostWeaverQuery(fnName,params)
	print fnName,result
	print type(result)

	fnName='returnNodesBackward'
	params=dict(src='watching_planit_params_2',path_len_min=1,path_len_max=2)
	result=PostWeaverQuery(fnName,params)
	print fnName,result
	print type(result)
#
#
#	fnName='returnNodeOneHopBackward'
#	params=dict(src='standing_human',properties={})
#	result=PostWeaverQuery(fnName,params)
#	print fnName,result
#	print type(result)
#
#	fnName='returnNodeOneHopForward'
#	params=dict(src='standing_human',properties={})
#	result=PostWeaverQuery(fnName,params)
#	print fnName,result
#	print type(result)
#
#	fnName='getNode'
#	params=dict(node='standing_human')
#	result=PostWeaverQuery(fnName,params)
#	print fnName,result
#	print type(result)
#
#	fnName='oneHopGraphml'
#	params=dict(name='phone',num=5,edgeProps={'edgeDirection':'F'})
#	result=PostWeaverQuery(fnName,params)
#	print fnName,result
#	print type(result)
#
#	fnName='InsertNode'
#        params=dict(Id='1',nodeProps={})
#        result=PostWeaverQuery(fnName,params)
#        print fnName,result
#        print type(result)
#
#        fnName='InsertNode'
#        params=dict(Id='2',nodeProps={})
#        result=PostWeaverQuery(fnName,params)
#        print fnName,result
#        print type(result)
#
#
#        fnName='InsertRelationUndirected'
#        params=dict(src='1',dst='2',edgeProps={'label':'dummy','source_text':'dummy','source_url':'dummy'})
#        result=PostWeaverQuery(fnName,params)
#        print fnName,result
#        print type(result)
#
#
#
#	fnName='oneHop'
#	params=dict(node='phone',edgeProps={'edgeDirection':'F'})
#	result=PostWeaverQuery(fnName,params)
#	print fnName,result
#	print type(result)
#
#	fnName='returnPathMinMax'
#	params=dict(src='standing_human',dest='volume',path_len_min=0,path_len_max=2)
#	result=PostWeaverQuery(fnName,params)
#	print fnName,result
#	print type(result)
#
#
