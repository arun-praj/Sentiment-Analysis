from sklearn.datasets import fetch_20newsgroups

categories=['sci.med']
newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)

train_data=newsgroups_train.data #getting all trainign examples
train_labels=newsgroups_train.target #getting training labels
print ("Total Number of Training Examples: ",len(train_data))
print("Total Number of Training Labels: ", len(train_labels))
print(train_labels)
# for d in train_data:
#     print(d,"\n")