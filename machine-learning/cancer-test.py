#分类 —— 威斯康辛州乳腺癌数据
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

from sklearn.datasets import load_breast_cancer

cancer_dataset = load_breast_cancer()
print(f"cancer.keys() : {cancer_dataset.keys()}")
print(f"cancer.shape : {cancer_dataset['data'].shape}")
print(f"cancer.desc : {cancer_dataset['DESCR']}")
