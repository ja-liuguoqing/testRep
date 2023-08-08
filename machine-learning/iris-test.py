#分类 —— 鸢尾花的种类
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=112)
iris_dataset = load_iris()
#训练的输入 测试的输入 训练的输出 测试的输出
X_train, X_test, y_train, y_test = train_test_split(
    iris_dataset['data'],#数据
    iris_dataset['target'],#对应标签
    random_state=0
)
"""
print(f"X_train shape : {X_train.shape}")
print(f"X_test shape : {X_test.shape}")
print(f"y_train shape : {y_train.shape}")
print(f"y_test shape : {y_test.shape}")
"""
knn.fit(X_train, y_train)
X_new = np.array([[5, 2.9, 1, 0.2]])

y_predict = knn.predict(X_test)
print(f"prediction : {y_predict}")
print(f"Test set score : {np.mean(y_test == y_predict):.2f}")