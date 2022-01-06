import cv2 as cv 
import numpy as np
import os
import random
import math
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
# %matplotlib
class HoG(object) :
    def __init__(self, img, cell_w, bin_count) :
        rows, cols = img.shape
        img = np.power(img / 255.0, 2.2) * 255
        self.img = img
        self.cell_w = cell_w
        self.bin_count = bin_count
        self.angle_unit = 180.0 / bin_count
        self.cell_x = int(rows / cell_w)
        self.cell_y = int(cols / cell_w)

    #求每个像素的x和y方向的梯度值和梯度方向
    def Pixel_gradient(self) :
        gradient_values_x = cv.Sobel(self.img, cv.CV_64F, 1, 0, ksize = 5)#x方向梯度
        gradient_values_y = cv.Sobel(self.img, cv.CV_64F, 0, 1, ksize = 5)#y方向梯度
        gradient_magnitude = np.sqrt(np.power(gradient_values_x, 2) + np.power(gradient_values_y, 2))#计算总梯度
#         gradient_angle = cv.phase(gradient_values_x, gradient_values_y, angleInDegrees=True)#计算梯度方向
        gradient_angle = np.arctan2( gradient_values_x, gradient_values_y )
        gradient_angle[ gradient_angle > 0 ] *= 180 / 3.14
        gradient_angle[ gradient_angle < 0 ] = ( gradient_angle[ gradient_angle < 0 ] + 3.14 ) * 180 / 3.14

        return gradient_magnitude, gradient_angle
    
    #求每个cell的x和y方向的梯度值和梯度方向
    def Cell_gradient(self, gradient) :
        cell = np.zeros((self.cell_x, self.cell_y, self.cell_w, self.cell_w))
        gradient_x = np.split(gradient, self.cell_x, axis = 0)
        for i in range(self.cell_x) :
            gradient_y = np.split(gradient_x[i], self.cell_y, axis = 1)
            for j in range(self.cell_y) :
                cell[i][j] = gradient_y[j]
        return cell

    
    #对每个梯度方向进行投票
    def Get_bins(self, cell_gradient, cell_angle) :
        bins = np.zeros((cell_gradient.shape[0], cell_gradient.shape[1], self.bin_count))
        for i in range(bins.shape[0]) :
            for j in range(bins.shape[1]) :
                tmp_unit = np.zeros(self.bin_count)
                cell_gradient_list = np.int8(cell_gradient[i][j].flatten())
                cell_angle_list = cell_angle[i][j].flatten()
                cell_angle_list = np.int8( cell_angle_list / self.angle_unit )#0-9
                cell_angle_list[ cell_angle_list >=9 ] = 0
#                 cell_angle_list = cell_angle_list.flatten()
#                 cell_angle_list = np.int8(cell_angle_list / self.angle_unit) % self.bin_count

                for m in range(len(cell_angle_list)) :
                    tmp_unit[cell_angle_list[m]] += int(cell_gradient_list[m])#将梯度值作为投影的权值
        
                bins[i][j] = tmp_unit
        return bins 
    
    #获取整幅图像的特征向量
    def Block_Vector(self) :
        gradient_magnitude, gradient_angle = self.Pixel_gradient()
        cell_gradient_values = self.Cell_gradient(gradient_magnitude)
        cell_angle = self.Cell_gradient(gradient_angle)
        bins = self.Get_bins(cell_gradient_values, cell_angle)
        
        block_vector = []
        for i in range(self.cell_x - 1) :
            for j in range(self.cell_y - 1) :
                feature = []
                feature.extend(bins[i][j])
                feature.extend(bins[i + 1][j])
                feature.extend(bins[i][j + 1])
                feature.extend(bins[i + 1][j + 1])
                
                mag = lambda vector : math.sqrt(sum(i ** 2 for i in vector))
                magnitude = mag(feature)
                if magnitude != 0 :
                    normalize = lambda vector, magnitude: [element / magnitude for element in vector]
                    feature = normalize(feature, magnitude)
                    
                block_vector.extend(feature)
        return np.array(block_vector)    
    
class PCA() :
    def __init__(self, n_components) :
        self.n_components = n_components
        
    def fit(self, X) :
        def deMean(X) :
            return X - np.mean(X, axis = 0)
        
        def calcCov(X) :
            return np.cov(X, rowvar = False)
        
        def deEigenvalue(cov) :
            return np.linalg.eig(cov)
        
        n, self.d = X.shape
        assert self.n_components <= self.d
        assert self.n_components <= n
        
        X = deMean(X)
        cov = calcCov(X) 
        eigenvalue, featurevector = deEigenvalue(cov)
        index = np.argsort(eigenvalue)
        n_index = index[-self.n_components : ]
        self.w = featurevector[ : , n_index]
        
        return self
    def transform(self, X) :
        n, d = X.shape
        assert d == self.d
        return np.dot(X, self.w)

class DataSet(object) :
    def __init__(self, root, division) :
        self.root = root
        self.division = division
        
    def data_segmentation(self, car, dog, face, snake) :
        #将每一类图片分割成训练集和测试集，四种类分别设置标签是[1, 2, 3， 4]方便后续的性能评估
        train_car, test_car = car[ : int(car.shape[0] * self.division)], car[int(car.shape[0] * self.division) : ]
        train_car_target, test_car_target = np.full(len(train_car) , 1, dtype = np.int64), np.full(len(test_car) , 1, dtype = np.int64)
        train_dog, test_dog = dog[ : int(dog.shape[0] * self.division)], dog[int(dog.shape[0] * self.division) : ]
        train_dog_target, test_dog_target = np.full(len(train_dog) , 2, dtype = np.int64), np.full(len(test_dog) , 2, dtype = np.int64)
        train_face, test_face = face[ : int(face.shape[0] * self.division)], face[int(face.shape[0] * self.division) : ]
        train_face_target, test_face_target = np.full(len(train_face) , 3, dtype = np.int64), np.full(len(test_face) , 3, dtype = np.int64)
        train_snake, test_snake = snake[ : int(snake.shape[0] * self.division)], snake[int(snake.shape[0] * self.division) : ]
        train_snake_target, test_snake_target = np.full(len(train_snake) , 4, dtype = np.int64), np.full(len(test_snake) , 4, dtype = np.int64)

        #将四类图片拼接成一个大的矩阵
        train_data = np.concatenate([train_car, train_dog, train_face, train_snake])
        test_data = np.concatenate([test_car, test_dog, test_face, test_snake])
        train_target = np.concatenate([train_car_target, train_dog_target, train_face_target, train_snake_target])
        test_target = np.concatenate([test_car_target, test_dog_target, test_face_target, test_snake_target])
        
        #以索引方式打乱训练集
        index = [i for i in range(len(train_data))]
        random.shuffle(index)
        train_data = train_data[index]
        train_target = train_target[index]
        
        return train_data, train_target, test_data, test_target
    
    def datasets(self) :
        #读取每类图片的名字
        image_car = list(sorted(os.listdir(os.path.join(self.root, 'car'))))
        image_dog = list(sorted(os.listdir(os.path.join(self.root, 'dog'))))
        image_face = list(sorted(os.listdir(os.path.join(self.root, 'face'))))
        image_snake = list(sorted(os.listdir(os.path.join(self.root, 'snake'))))
        
        #储存图片
        car = np.zeros((4000, 256, 256), dtype = np.uint8)
        dog = np.zeros((4000, 256, 256), dtype = np.uint8)
        face = np.zeros((4000, 256, 256), dtype = np.uint8)
        snake = np.zeros((4000, 256, 256), dtype = np.uint8)
        
        #读取车、狗、人脸、蛇的图片，进行resize至256 * 256
        for i in range(4000) :
            img = cv.imread(os.path.join(self.root, 'car', image_car[i]), cv.IMREAD_GRAYSCALE)
            img = cv.resize(img, (256, 256), cv.INTER_CUBIC)
            car[i] = img
        for i in range(4000) :
            img = cv.imread(os.path.join(self.root, 'dog', image_dog[i]), cv.IMREAD_GRAYSCALE)
            img = cv.resize(img, (256, 256), cv.INTER_CUBIC)
            dog[i] = img    
        for i in range(4000) :
            img = cv.imread(os.path.join(self.root, 'face', image_face[i]), cv.IMREAD_GRAYSCALE)
            img = cv.resize(img, (256, 256), cv.INTER_CUBIC)
            face[i] = img
        for i in range(4000) :
            img = cv.imread(os.path.join(self.root, 'snake', image_snake[i]), cv.IMREAD_GRAYSCALE)
            img = cv.resize(img, (256, 256), cv.INTER_CUBIC)
            snake[i] = img
        print(car.shape, dog.shape, face.shape, snake.shape)
        #分割
        train_data, train_target, test_data, test_target = self.data_segmentation(car, dog, face, snake)
        return train_data, train_target, test_data, test_target
    
def micro_f1(pred, target) :
    #第一类
    target1 = target.copy()
    pred1 = pred.copy()
    target1 = target1 == 1
    pred1 = pred1 == 1
    TP1 = np.sum(target1[pred1 == 1] == 1)
    FN1 = np.sum(target1[pred1 == 0] == 1)
    FP1 = np.sum(target1[pred1 == 1] == 0)
    TN1 = np.sum(target1[pred1 == 0] == 0)
    
    #第二类
    target2 = target.copy()
    pred2 = pred.copy()
    target2 = target2 == 2
    pred2 = pred2 == 2
    TP2 = np.sum(target2[pred2 == 1] == 1)
    FN2 = np.sum(target2[pred2 == 0] == 1)
    FP2 = np.sum(target2[pred2 == 1] == 0)
    TN2 = np.sum(target2[pred2 == 0] == 0)
    
    #第三类
    target3 = target.copy()
    pred3 = pred.copy()
    target3 = target3 == 3
    pred3 = pred3 == 3
    TP3 = np.sum(target3[pred3 == 1] == 1)
    FN3 = np.sum(target3[pred3 == 0] == 1)
    FP3 = np.sum(target3[pred3 == 1] == 0)
    TN3 = np.sum(target3[pred3 == 0] == 0)
    
    #第四类
    target4 = target.copy()
    pred4 = pred.copy()
    target4 = target4 == 4
    pred4 = pred4 == 4
    TP4 = np.sum(target4[pred4 == 1] == 1)
    FN4 = np.sum(target4[pred4 == 0] == 1)
    FP4 = np.sum(target4[pred4 == 1] == 0)
    TN4 = np.sum(target4[pred4 == 0] == 0)
    
    TP = TP1 + TP2 + TP3 + TP4
    FN = FN1 + FN2 + FN3 + FN4
    FP = FP1 + FP2 + FP3 + FP4
    TN = TN1 + TN2 + TN3 + TN4
    
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * precision * recall / (precision + recall) 
    
    confusion_matrix =np.array([[np.sum(pred[target == 1] == 1), np.sum(pred[target == 1] == 2), np.sum(pred[target == 1] == 3), np.sum(pred[target == 1] == 4)],
                                [np.sum(pred[target == 2] == 1), np.sum(pred[target == 2] == 2), np.sum(pred[target == 2] == 3), np.sum(pred[target == 2] == 4)],
                                [np.sum(pred[target == 3] == 1), np.sum(pred[target == 3] == 2), np.sum(pred[target == 3] == 3), np.sum(pred[target == 3] == 4)],
                                [np.sum(pred[target == 4] == 1), np.sum(pred[target == 4] == 2), np.sum(pred[target == 4] == 3), np.sum(pred[target == 4] == 4)]])
    
    return precision, recall, f1, TP1, TP2, TP3, TP4, confusion_matrix

dataset = DataSet(root = 'data', division = 0.875)
train_data, train_target, test_data, test_target = dataset.datasets()

# 绘制混淆矩阵
def plot_confusion_matrix(cm, classes, title = 'Confusion matrix', cmap = plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]) :
        for j in range(cm.shape[1]) :
            plt.text(j, i, f'{cm[i][j]}', horizontalalignment="center", color="white" if cm[i][j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    
# print(train_data.shape, train_target.shape, test_data.shape, test_target.shape)
# print(test_target, train_target)
#HoG特征获取
train_feature = []
test_feature = []
for i in range(len(train_data)) :
    hog = HoG(train_data[i], 32, 9)
    temp_feature = hog.Block_Vector()
    train_feature.append(temp_feature)
    
for i in range(len(test_data)) :
    hog = HoG(test_data[i], 32, 9)
    temp_feature = hog.Block_Vector()
    test_feature.append(temp_feature)

train_feature = np.array(train_feature)
test_feature = np.array(test_feature)
# print(train_feature.shape, test_feature.shape)
#PCA降维
pca = PCA(n_components = 100)
pca.fit(train_feature)
train_reduction = pca.transform(train_feature)
test_reduction = pca.transform(test_feature)
print(train_reduction.shape)
print(test_reduction.shape)
#模型训练和预测
clf = svm.SVC()
clf.fit(train_reduction, train_target)
print(clf.score(test_reduction, test_target))
print(clf.score(train_reduction, train_target))
pred = clf.predict(test_reduction)
precision, recall, f1, TP1, TP2, TP3, TP4, confusion_matrix = micro_f1(pred, test_target)
print( precision, recall, f1, TP1, TP2, TP3, TP4, confusion_matrix)
#绘制混淆矩阵
plot_confusion_matrix(cm = confusion_matrix, classes = ['car', 'dog', 'face', 'snake'])