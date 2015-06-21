import hashlib
def _get_unique_id(node_handle):
    m = hashlib.md5(node_handle.encode())
    return str(str(int(m.hexdigest(), 16))[0:16])

def ProcessNodeData(dataObj,name):
    data=dict(dataObj)
    for key,val in data.iteritems():
        data[key]=getValFromWeaver(val)
    data['caption']=name
    data['handle']=name
    if data['labels'][0][1:8]=='Concept':
        data['type']='Concept'
    else:
        data['type']='Media'
    return data

def ProcessEdgeData(edge,edgeProps):
    props=dict(edge.properties)
    if 'edgeDirection' in edgeProps:
        if edgeProps['edgeDirection']=='B':
            props['source']=edge.end_node
            props['target']=edge.start_node
        else:
            props['source']=edge.start_node
            props['target']=edge.end_node

    for key,val in props.iteritems():
        props[key]=getValFromWeaver(val)
    props['type']=getValFromWeaver(edge.properties['label'])
    props['handle']=edge.handle
    return props

def getValFromWeaver(val):
    return val[0]

def mergeProps(l1,l2):
    l2=getValFromWeaver(l2)
    l1=l1.split(',')
    l2=l2.split(',')
    l3=list()
    l3=l1+list(set(l2)-set(l1))
    return ",".join(l3)

def getUpdatedProperty(newProps,oldProps):
    for key,val in newProps.iteritems():
            updateVal=val
            if key in oldProps:
                updateVal=mergeProps(newProps[key],oldProps[key])
            newProps[key]=updateVal

    return newProps