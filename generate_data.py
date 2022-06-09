import pickle

fair_traces = pickle.load(open("fair_traces","rb"))

data = []
windowSize = 4
walkLen = 80

for traces in fair_traces:
    for walk in traces:
        i = 0
        while(i + 2*windowSize +1 <= walkLen):
            new_x = []
            new_x += walk[i:i+windowSize]
            new_y = walk[i+windowSize]
            new_x += walk[i+windowSize+1:i + 2*windowSize +1]
            i += 1
            data.append((new_x,new_y))

pickle.dump(data,open("new_data","wb"))

for row in data:
    print(row)



