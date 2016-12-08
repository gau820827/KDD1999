import pandas as pd
import numpy as np

from sklearn import tree


# Read data
def readdata():
    xtrain = pd.read_csv("train.in", header=None).as_matrix()
    ytrain = pd.read_csv("train.out", header=None).as_matrix().reshape(-1,1)
    xtest = pd.read_csv("test.in", header=None).as_matrix()

    return xtrain[:, :-1], ytrain, xtest[:, :-1]

xtrain, ytrain, xtest = readdata()

clf = tree.DecisionTreeClassifier(class_weight="balanced")
clf = clf.fit(xtrain, ytrain)

labels = clf.predict(xtest)

print "id,label"
for idt, label in enumerate(labels):
    print "{},{}".format(idt+1, label)