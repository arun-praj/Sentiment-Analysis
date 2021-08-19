import pickle

lr_model = pickle.load(open('./Logestic_Regression/lr_model.sav','rb'))
cv_vectorizer = pickle.load(open('./Logestic_Regression/cv_vectorizer.sav','rb'))

# testing
text = input('Enter a text: ')
x_transform = cv_vectorizer.transform([text])

print(text,':','pos' if lr_model.predict(x_transform)[0] ==1 else 'neg')