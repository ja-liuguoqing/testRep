import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

X, y = mglearn.datasets.make_forge()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


fig, axes = plt.subplots(1, 3, figsize=(10, 3))
for n_neighbors, ax in zip([1,3,9], axes):
    knc = KNeighborsClassifier(n_neighbors=n_neighbors)
    knc.fit(X_train, y_train)
    mglearn.plots.plot_2d_separator(knc, X_train, fill=True, eps=0.5, ax=ax, alpha=.4)
    mglearn.discrete_scatter(X[: 0], X[: 1], y, ax=ax)
    y_predict = knc.predict(X_test)
    print(f"prediction : {y_predict}")
    print(f"prediction : {y_test}")
    print(f"Test set score : {knc.score(X_test, y_test):.2f}")