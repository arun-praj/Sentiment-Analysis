from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score,f1_score
from sklearn.linear_model import LogisticRegression
import pandas as pd

# laod dataset
training_set=pd.read_csv('Naive_Bayes/labeledTrainData.tsv',sep='\t')

# train_test_split
y_train=training_set['sentiment'].values
x_train=training_set['review'].values
train_data,test_data,train_labels,test_labels=train_test_split(x_train,y_train,shuffle=True,
test_size=0.25,random_state=42,stratify=y_train)
# vectorization
cv= CountVectorizer(binary=True, analyzer = 'word', min_df = 10, max_df = 0.95)
cv.fit_transform(train_data)
train_feature_set=cv.transform(train_data)
test_feature_set=cv.transform(test_data)
train_feature_set.shape[1]

# Logistic Regression. Training phase....

# classes are 0 and 1 only
lr_model = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)
print ("------------------Training In Progress------------------------")
print ("Training Examples: ",train_data.shape)
# model.fit(train_data,train_labels)
lr_model.fit(train_feature_set,train_labels)
print ('------------------------Training Completed!')

# Testing phase 
y_pred = lr_model.predict(test_feature_set)
accuracy_scores = round(accuracy_score(test_labels,y_pred),3)
print("Accuracy: ",accuracy_scores)
print("F1: ",round(f1_score(test_labels, y_pred),3))

# testing
x = input('Enter a text: ')
x_transform = cv.transform([x])

print(x,':','pos' if lr_model.predict(x_transform)[0] ==1 else 'neg')