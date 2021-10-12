def P2_3():
    dict1 = {}
    with open('data1.txt', 'r') as file:
        lst1 = list(file.readlines())
        lst = list()
        for line in lst1:
            #print(type(line))
            line = line.strip('\n')
            line = line.split()
            line = list(line)
            lst.append(line)
        lst = lst[1: len(lst) - 1]
        #print(lst)
    tmpNames = []
    tmpScores = []
    for information in lst:
        #print(information)
        tmpNames.append(information[0])
        New_lst = information[1 : ]
        w = (1 + 2 + 3 + 2.5)
        sum_scores = (1 / w) * (1 * int(New_lst[0]) + 2 * int(New_lst[1]) + 3 * int(New_lst[2]) + 2.5 * int(New_lst[3]))
        tmpScores.append(sum_scores)
    #print(tmpScores)

    for i in range(3) :
        dict1[tmpNames[i]] = tmpScores[i]
        dict = sorted(dict1.items(), key=lambda x: x[1], reverse=True)
    #print(d_sort)
    tmpNames = list()
    tmpScores = list()
    for i in dict :
        tmpNames.append(i[0])
        tmpScores.append(i[1])
    for i in range(len(tmpScores)) :
        tmpScores[i] = round(tmpScores[i], 1)
    return tmpNames, tmpScores


if __name__ == "__main__":
    tmpNames, tmpScores = P2_3()
    print(tmpNames)
    print(tmpScores)