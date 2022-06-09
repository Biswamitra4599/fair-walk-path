import re
import numpy as np
import pickle

adj_list = [[] for i in range(4039)]
gender_list = [77]*4039
gender_dist = dict()
gender_wise_neighbour_indices = []

def fillupmat(nodeid):
    circle_file = open(str(nodeid)+".circles",'r')
    y=[]
    for circle in circle_file:
        x=re.split(r'[ \t]+',circle)
        y+=[int(a) for a in x[1:]]

    for i in y:
        adj_list[nodeid].append(i)
        adj_list[i].append(nodeid)
    circle_file.close()

    edge_file = open(str(nodeid)+'.edges','r')
    for edge in edge_file:
        vertices = edge.split(' ')
        adj_list[int(vertices[0])].append(int(vertices[1]))
        adj_list[int(vertices[1])].append(int(vertices[0]))
    edge_file.close()

    #assigning gender
    feature_file = open(str(nodeid)+'.feat','r')
    ego_feature_file = open(str(nodeid)+'.egofeat','r')
    feature_names_file = open(str(nodeid)+'.featnames','r')
    gender_index = 77
    for line in feature_names_file:
        if line.split(' ')[1].split(';')[0] == 'gender':
            gender_index = int(line.split(' ')[0])
            break
    
    count_gender77 = 0
    count_gender78 = 0
    for row in feature_file:
        feature_data = row.split(' ')
        node = int(feature_data[0])
        if feature_data[gender_index+1] == '1':
            gender_list[node] = 77
            count_gender77+=1
        else:
            gender_list[node] = 78
            count_gender78 += 1
    
    gender_dist[nodeid] = (count_gender77,count_gender78)
    #assigning gender to ego node
    row = ego_feature_file.readline()
    feature_data = row.split(' ')
    node = int(feature_data[0])
    if row[gender_index+1] == '1':
            gender_list[node] = 77
    else:
            gender_list[node] = 78

def get_gender_wise_neighbours(adj_list):
    for nodeid in range(len(adj_list)):
        gender77_list = []
        gender78_list = []
        for i in range(len(adj_list[nodeid])):
            if(gender_list[adj_list[nodeid][i]]==77):
                gender77_list.append(i)
            else:
                gender78_list.append(i)
        gender_wise_neighbour_indices.append((gender77_list,gender78_list))

def get_gender_dist(adj_list):
    for i in range(len(adj_list)):
        count_gender77 = len(gender_wise_neighbour_indices[i][0])
        count_gender78 = len(gender_wise_neighbour_indices[i][1])
        gender_dist[i] = (count_gender77,count_gender78)



def fairwalk(adj_list,walk_len,walk_num):
    fairwalk_traces = []
    for nodeid in range(len(adj_list)):
        if len(adj_list[nodeid]) != 0:
            traces = []
            for j in range(walk_num):
                walk = []
                current_node = nodeid
                for step in range(walk_len):
                    r = np.random.randint(77,79)
                    random_neighbor = None
                    try:
                        if r==77:
                            group77_neighbours = gender_wise_neighbour_indices[current_node][0]
                            if len(group77_neighbours) == 0:
                                random_neighbor = np.random.choice(gender_wise_neighbour_indices[current_node][1])
                            else:
                                random_neighbor = np.random.choice(group77_neighbours)
                        else:
                            group78_neighbours = gender_wise_neighbour_indices[current_node][1]
                            if len(group78_neighbours) == 0:
                                random_neighbor = np.random.choice(gender_wise_neighbour_indices[current_node][0])
                            else:
                                random_neighbor = np.random.choice(group78_neighbours)
                    except:
                        pass
                    walk.append(adj_list[current_node][random_neighbor])
                    current_node = adj_list[current_node][random_neighbor]
                traces.append(walk)
            fairwalk_traces.append(traces)
    return fairwalk_traces

def main():
    egos = [0,107,348,414,686,698,1684,1912,3437,3980]
    for ego_node in egos:
        fillupmat(ego_node)
    
    get_gender_wise_neighbours(adj_list)
    get_gender_dist(adj_list)
    fair_traces = fairwalk(adj_list,80,2)

    #dump the traces
    pickle.dump(fair_traces,open("fair_traces","wb"))
    for traces in fair_traces:
        for walk in traces: 
            print(walk)

if __name__ == '__main__':
    main()