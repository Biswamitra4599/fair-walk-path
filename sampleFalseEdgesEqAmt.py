import os
import numpy as np
import re

adj_list = np.zeros(shape=(4039,4039),dtype=np.int8)

def fillupmat(nodeid):
    circle_file = open(str(nodeid)+".circles",'r')
    y=[]
    for circle in circle_file:
        x=re.split(r'[ \t]+',circle)
        y+=[int(a) for a in x[1:]]

    for i in y:
        adj_list[nodeid][i] = 1
        adj_list[i][nodeid] = 1
    circle_file.close()

    edge_file = open(str(nodeid)+'.edges','r')
    for edge in edge_file:
        vertices = edge.split(' ')
        adj_list[int(vertices[0])][int(vertices[1])] = 1
        adj_list[int(vertices[1])][int(vertices[0])] = 1 
    edge_file.close()


def sample_false_edges_equal_amount():
    egos = [0,107,348,414,686,698,1684,1912,3437,3980]
    for ego_node in egos:
        fillupmat(ego_node)

    falseEdgeSamples = {}
    
    for i in range(adj_list.shape[0]):
        trueEdgeCount = np.count_nonzero(adj_list[i]==1)
        if trueEdgeCount > 0:
            falseEdgeList = np.where(adj_list[i] == 0)
            falseEdgeSample = np.random.choice(falseEdgeList[0],trueEdgeCount)
        falseEdgeSamples[i] = falseEdgeSample
    
    return falseEdgeSamples


