import numpy as np

def P2_4():
    tmpList = []
    data = list(np.load('data2.npy'))
    #data = data[ : len(data)]
    #print(len(data))
    dict1 = {}
    for i in range(len(data)) :
        if data[i] not in dict1.keys() :
            dict1[data[i]] = 1
        else :
            dict1[data[i]] += 1
    for i in dict1.keys() :
        if dict1[i] > 1 :
            tmpList.append(i)
    tmpList = sorted(tmpList)
    
    return tmpList

if __name__ == "__main__":
    tmpList = P2_4()
    print(tmpList)