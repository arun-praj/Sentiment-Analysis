#imports
from sklearn.datasets import fetch_20newsgroups
# we will use sklearn for only dataset, algorithm is implemented by ourselves
# we wont be using naive bayes from sklearn
import pandas as pd
import numpy as np
from naiveBayes import NaiveBayes
from preprocesser import cleaner, stemmer


categories=['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med'] 
newsgroups_train=fetch_20newsgroups(subset='train',categories=categories)
# There are altogether 20 categories

train_data = newsgroups_train.data
train_labels = newsgroups_train.target

unique_classes = np.unique(train_labels) #unique classes for our model
# print(unique_classes)

nb = NaiveBayes(unique_classes)

lst = nb.train(train_data,train_labels,stem=False)
# # lst
# print(lst)

# print(pd.DataFrame(data=lst).head(4))