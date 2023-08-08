#回归 —— 波士顿房价
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

from sklearn.datasets import load_boston

X, y = mglearn.datasets.load_extended_boston()
print(f"X.shape : {X.shape}")