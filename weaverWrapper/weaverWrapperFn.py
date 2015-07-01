import json
import utils as utils
from weaver import client
import datetime
colorred = "\033[01;31m{0}\033[00m"
colorgrn = "\033[1;36m{0}\033[00m"

def oneHopGraphml(c,name='phone',num=5,edgeProps={'edgeDirection':'F'}):
    retVal=dict()
    retVal['nodes']=list()
    retVal['edges']=list()
    nodeList=list()
    nodename=name
    try:
        onehop=c.traverse(nodename).out_edge(edgeProps).node().execute()
        print 'Node Found, traversing one hop neighbors'
    except client.WeaverError:
        print dir(client.WeaverError)
	print client.WeaverError.message
        return False

    nodeOb=c.get_node(node=name)
    retVal['nodes'].append(utils.ProcessNodeData(nodeOb.properties,name))
    counter=0
    nodeList.append(name)

    for node in onehop:
        counter=counter+1
        nodeOb=c.get_node(node=node)
        data=dict(nodeOb.properties)
        retVal['nodes'].append(utils.ProcessNodeData(nodeOb.properties,node))
        nodeList.append(node)
        if counter==num:
            break

    edges=c.get_edges(node=nodename,properties=edgeProps)

    for edge in edges:
        if edge.start_node in nodeList and edge.end_node in nodeList:
            retVal['edges'].append(utils.ProcessEdgeData(edge,edgeProps))

    return retVal

def getNode(c,node='phone'):
	node=c.get_node(node=node)
	return node.properties

def InsertNode(c,Id='floor',CreatedAt=datetime.datetime.now(),nodeProps={}):
    nodeProps['created_at']=CreatedAt
    if not Id:
        print colorred.format('undefined concept node handle')
        return
    c.begin_tx()
    c.create_node(Id)
    c.set_node_properties(node=Id,properties=nodeProps)
    try:
        c.end_tx()
        print 'created a new node'
        print Id,nodeProps
        return True
    except client.WeaverError:
        print 'node already exists'
        print Id,nodeProps
        nodeProps.pop("created_at", None)
        oldProps=c.get_node(node=Id).properties
        c.begin_tx()
        c.set_node_properties(node=Id,properties=utils.getUpdatedProperty(nodeProps,oldProps))
        try:
            c.end_tx()
            return True
        except client.WeaverError:
            print 'Internal Error, contact the system administrator:Node'
            return False

def updateNodeProps(Id,nodeProps):
    c.begin_tx()
    c.set_node_properties(node=Id,properties=nodeProps)
    try:
        c.end_tx()
        return True
    except client.WeaverError:
        print 'Internal Error, contact the system administrator:Node'
        return False


#Creating a new Concept Relationship in RoboBrain
def InsertRelation(c,CreatedAt=datetime.datetime.now(),src='1',dst='2',edgeDirection='F',edgeProps={}):
    if not src:
        print colorred.format('Source undefined')
        return
    if not dst:
        print colorred.format('Destination undefined')
        return

    edgeProps['created_at']=CreatedAt
    edgeProps['edgeDirection']=edgeDirection
    edges=c.get_edges(node=src,properties={'label':edgeProps['label'],'source_text':edgeProps['source_text'],'source_url':edgeProps['source_url'],'edgeDirection':edgeProps['edgeDirection']},nbrs=[dst])  # all the edges at a particular node
    if len(edges)==1:
        handle=edges[0].handle
        edgeProps.pop("created_at", None)
        oldProps=edges[0].properties
        c.begin_tx()
        newProps=utils.getUpdatedProperty(edgeProps,oldProps)
        print handle,newProps
        c.set_edge_properties(edge=handle,properties=newProps)
        try:
            c.end_tx()
            print 'edge exists:'
            print src,dst,edgeProps
            return True
        except client.WeaverError:
            print 'Internal Error, contact the system administrator:Edge'
            return False

    elif len(edges)==0:
        c.begin_tx()
        newEdge=c.create_edge(src,dst)
        c.set_edge_properties(node=src,edge=newEdge,properties=edgeProps)
        try:
            c.end_tx()
            print 'created  new edge'
            print src,dst,edgeProps
            return True
        except:
            print 'there is some internal error, contact the system administrator:Edge'
            return False
    else:
        print 'There cannot be two edges which have the exact same properties'
        return False


def InsertRelationUndirected(c,CreatedAt=datetime.datetime.now(),src='1',dst='2',edgeProps={}):
    return InsertRelation(c,CreatedAt=CreatedAt,src=src,dst=dst,edgeDirection='F',edgeProps=edgeProps) and InsertRelation(c,CreatedAt=CreatedAt,src=dst,dst=src,edgeDirection='B',edgeProps=edgeProps)

def oneHop(c,node='watching',edgeProps={'edgeDirection':'F','label':'ACTIVITY_PARAMS','paramtype':'pi'}):
    onehop=c.traverse(node).out_edge(edgeProps).node().execute()
    return onehop


def returnPathMinMax(graphClient,src='standing_human',dest='volume',path_len_min=0,path_len_max=5,nodeListDisplay=False,path_len_exact=False,displayPath=False):
    
    # path lies from path_length_min to path_length_max, we return all path in this range if path_length_exact=False
    # return path=path_length_max if path_length_exact

    nodename1=src
    nodename2=dest
    paths=graphClient.discover_paths(start_node=nodename1,end_node=nodename2, path_len=path_len_max)
    edges=graphClient.enumerate_paths(paths, nodename1, nodename2, 5)
    flag=0
    counter_ED=0
    all_path=list()
    for edge in edges:
        possible_path=list()
        if nodeListDisplay:
            counter_ED=1
            length=len(edge)
            possible_path=list()
            possible_path.append(edge[0].start_node)
            for i in range(0,length):
                possible_path.append(edge[i].end_node)
        else:
            for ed in edge:
                v1=dict(ed.properties)
                v1['source']=ed.start_node
                v1['target']=ed.end_node
                possible_path.append(v1)

        if len(possible_path)-counter_ED>=path_len_min:
                if path_len_exact:
                    if len(possible_path)-1==path_len_max:
                        flag=1
                        all_path.append(possible_path)
                        if displayPath:
                            for node in possible_path:
                                print node,
                            print
                else:
                    flag=1
                    all_path.append(possible_path)
                    if displayPath:
                        for node in possible_path:
                            print node,
                        print 

    return all_path

def CollectNodesRecursive(graphClient,graphDir,visited,hopLengthNodes,hopPoint,path_len_max):
    hopLengthNodes[hopPoint]=list()
    for node in hopLengthNodes[hopPoint-1]:
        if node in visited:
            pass
        else:
            visited[node]=1
            oneHop=graphClient.traverse(node).out_edge({'edgeDirection':graphDir}).node().execute()
            for n1 in oneHop:
                hopLengthNodes[hopPoint].append(n1)

    if hopPoint==path_len_max:
        return hopLengthNodes
    else:
        return CollectNodesRecursive(graphDir,visited,hopLengthNodes,hopPoint+1,path_len_max)

def CollectNodes(graphClient,graphDir,src='standing_human',path_len_max=5,properties={}):
    visited=dict()
    hopPoint=1
    hopLengthNodes=dict()
    edge_props = dict()
    hopLengthNodes[hopPoint-1]=list()
    start=src
    hopLengthNodes[hopPoint-1].append(start)
    retValFinal=dict()
    if not path_len_max==1:
        retValFinal=CollectNodesRecursive(graphDir,visited,hopLengthNodes,hopPoint,path_len_max)
    else:
        hopLengthNodes[hopPoint]=list()
        edge_props['edgeDirection']=graphDir
        oneHop=graphClient.traverse(start).out_edge(edge_props=properties).node().execute()
        for node in oneHop:
            hopLengthNodes[hopPoint].append(node)
        retValFinal=hopLengthNodes
    
    return retValFinal


def CollectNodesModified(graphClient,graphDir,src='standing_human',path_len_min=1,path_len_max=5,properties={}):
    start=src
    retValFinal=dict()
    # print 'Collect Nodes Modified src:,path_len:,path_len_max:',src,path_len_min,path_len_max
    for num_hops in range(path_len_min,path_len_max+1):
        query = graphClient.traverse(start)
        for i in range(num_hops):
            query = query.out_edge({'edgeDirection':graphDir}).node()
        newList=list(query.execute())
        retValFinal[num_hops]=newList

    return retValFinal


def returnNodesForward(graphClient,src='standing_human',path_len_min=1,path_len_max=5):
    return CollectNodesModified(graphClient,graphDir='F',src=src,path_len_min=path_len_min,path_len_max=path_len_max,properties={})

def returnNodesBackward(graphClient,src='laptop',path_len_min=1,path_len_max=5):
    return CollectNodesModified(graphClient,graphDir='B',src=src,path_len_min=path_len_min,path_len_max=path_len_max,properties={})

def returnNodeOneHopBackward(graphClient,src='standing_human',properties={}):   
    return CollectNodes(graphClient,graphDir='B',src=src,path_len_max=1,properties=properties)

def returnNodeOneHopForward(graphClient,src='standing_human',properties={}):    
    return CollectNodes(graphClient,graphDir='F',src=src,path_len_max=1,properties=properties)
