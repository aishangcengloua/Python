import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Lab5.dat')


def CalcDistance(x, y):
    return np.sum(np.square(x - y))


def get_farthest_k_center(X, K):
    row, col = X.shape
    centroids = np.zeros((K, col))
    # 第一个点
    index = int(np.random.uniform(0, row))
    centroids[0, :] = X[index, :]
    # 第二个点
    distance = np.zeros(row)
    for i in range(row):
        distance[i] = CalcDistance(X[i, :], centroids[0, :])
    max_index = np.argmax(distance)
    centroids[1, :] = X[max_index, :]
    # 第三个点及以后，
    # 然后再选择距离前两个点的最短距离最大的那个点作为第三个初始类簇的中心点
    j = 1
    while j <= K - 2:
        distance = np.zeros(row)
        for i in range(row):
            distance1 = CalcDistance(centroids[j - 1, :], X[i, :])
            distance2 = CalcDistance(centroids[j, :], X[i, :])
            distance[i] = min(distance1, distance2)
            max_index = np.argmax(distance)
        centroids[j + 1, :] = X[max_index, :]
        j += 1
    return centroids


def cal_Silhouette_Coeff(X, cidx, K):
    c, b = [], [0] * (K - 1)
    distance_a, distance_b = 0, np.zeros(K - 1)
    for i in range(K):
        subX = X[cidx == 1 + i]  # 获取每个簇类
        length = len(subX)
        for j in range(length):
            distance_a = CalcDistance(subX[j, :], subX[:, :]) / (length)  # 凝聚度
            for k in range(K):  # 求最近簇
                if k < i:
                    b[k] = CalcDistance(subX[j, :], X[cidx == k + 1, :]) / len(X[cidx == k + 1])
                elif k > i:
                    b[k - 1] = CalcDistance(subX[j, :], X[cidx == k + 1, :]) / len(X[cidx == k + 1])
            distance_b = np.min(b)  # 分离度
        c.append((distance_b - distance_a) / max(distance_a, distance_b))

    return sum(c) / len(c)


def calSSE(X, cidx, ctrs):
    SSE = 0
    for i, ctr in enumerate(ctrs):
        SSE += np.sum(np.square(X[np.where(cidx == i + 1)] - ctr))

    return SSE / X.shape[0]


def kmeans(X, K):
    center_point = get_farthest_k_center(X, K)  # 初始化簇点
    cluter = np.zeros(X.shape[0])  # 建立簇类初始化为0
    item = 5
    while item > 0:  # 迭代
        for i in range(X.shape[0]):  # 计算每一组数据与每个簇心的欧氏距离，距离最小者记为此组数据为所标类别
            distance = center_point
            distance = np.sum(np.square(distance - X[i]), axis=1)  # 注意x， y都计算所以要求和，注意求和维度
            cluter[i] = np.argmin(distance) + 1  # 最小值的下标

        New_center_point = np.zeros((K, 2), dtype=np.float64)

        for i in range(K):  # 更新簇点，取每一簇类的平均值作为新簇心
            subX = X[np.where(cluter == i + 1)]
            length = len(subX)
            if length > 0:  # 防止分母出现0
                New_center_point[i] = np.mean(subX, axis=0)
            else:
                New_center_point[i] = center_point[i]

        if (New_center_point == center_point).all():  # 当新簇点与之前的簇心近似相等时退出迭代
            break

        center_point = New_center_point
        item -= 1
    return cluter, center_point  # 返回每一组数据所对应的簇类和簇心


SSE = []
C = []
mark = ['r', 'c', 'y', 'k', 'm', 'g']

plt.ion()
for K in range(2, 7):
    cidx, ctrs = kmeans(data, K)
    print(f'K为{K}时的簇心 : \n {ctrs}')
    SSE.append(calSSE(data, cidx, ctrs))  # 手肘法求最好分类的K值
    C.append(cal_Silhouette_Coeff(data, cidx, K))  # 求轮廓系数

    plt.subplot(2, 3, K - 1)
    for i in range(K):
        plt.scatter(data[np.where(cidx == i + 1), 0], data[np.where(cidx == i + 1), 1], marker='.', color=mark[i])  # 作图
    plt.scatter(ctrs[:, 0], ctrs[:, 1], marker='*', color='g')  # 做出簇心
    plt.title(f'K is {K}')
    plt.tight_layout()
    plt.xticks([]), plt.yticks([])

plt.figure(), plt.plot(list(range(2, 7)), SSE, '+--')
plt.figure(), plt.plot(list(range(2, 7)), C, '+--'), plt.grid(), plt.xticks([2, 3, 4, 5, 6]), plt.xlim(2, 6)
plt.ioff()
plt.show()