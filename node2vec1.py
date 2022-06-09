import pickle
import numpy as np
import os
import tensorflow as tf


d = 10 #num of dimensions of embedding
v = 7998 #num of nodes in the graph
w = 4 #window size in skip-gram

#list of tupples --> [(x1(list),y1(scalar)), (x2,y2), (x3,y3), ...]
#x is list of context nodes
#y is center node
#data = pickle.load(open("new_data","rb"))
data = pickle.load(open(os.getcwd()+"\\facebook\\new_data","rb"))

data_x,data_y = [],[]

for row in data:
    data_x.append(row[0])
    data_y.append(row[1])



x = np.array(data_x)#[:100000]
oneHX = np.zeros((x.shape[0],v),dtype=np.int8)
for i in range(2*w):
    oneHX[np.arange(x.shape[0]), x[:,i]] += 1


#embedding
model = tf.keras.Sequential()
model.add(tf.keras.layers.Input(shape=oneHX.shape,dtype=np.int8))
model.add(tf.keras.layers.Dense(shape=(v,d),activation = newAct))

