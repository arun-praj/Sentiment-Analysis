from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from naive_bayes import NaiveBayes

training_set=pd.read_csv('Naive_Bayes/labeledTrainData.tsv',sep='\t')

#getting training set examples labels
y_train=training_set['sentiment'].values
x_train=training_set['review'].values
print ("Unique Classes: ",np.unique(y_train))
print ("Total Number of Training Examples: ",x_train.shape)

train_data,test_data,train_labels,test_labels=train_test_split(x_train,y_train,shuffle=True,test_size=0.25,random_state=42,stratify=y_train)
classes=np.unique(train_labels)
print(classes)
# print('train_data',train_data[0]) # string
# print('test_data',test_data[0]) # string
# print('train_tabels',train_labels) # 0 or 1


# Training phase....
# classes are 0 and 1 only

nb=NaiveBayes(classes)
print ("------------------Training In Progress------------------------")
print ("Training Examples: ",train_data.shape)
nb.train(train_data,train_labels)
print ('------------------------Training Completed!')

# Testing phase 

pclasses=nb.test(test_data)
test_acc=np.sum(pclasses==test_labels)/float(test_labels.shape[0])
print ("Test Set Examples: ",test_labels.shape[0])
print ("Test Set Accuracy: ",test_acc)

# testing
test=pd.read_csv('Naive_bayes/testData.tsv',sep='\t')
Xtest=test.review.values

#generating predictions....
# pclasses=nb.test(Xtest) 
# print(pclasses)


# test
test_array = ['not good','fine','not bad','i used to love it','its sucks']
classes = nb.test(test_array)
for sentence,classes in zip(test_array,classes):
    print(sentence,':','pos' if classes ==1 else 'neg')



test_string = input('Enter new string')
classes = nb.test([test_string])
for sentence,classes in zip(test_string,classes):
    print(sentence,':','pos' if classes ==1 else 'neg')


x = input('Enter a text: ')

print(x,':','pos' if nb.test([x]) ==1 else 'neg')