import pickle

tf_model = pickle.load(open('./Logestic_Regression/tf_model.sav','rb'))
tf_vectorizer = pickle.load(open('./Logestic_Regression/tf_vectorizer.sav','rb'))
text = input('Enter a text: ')
x_transform = tf_vectorizer.transform([text])

print(text,':','pos' if tf_model.predict(x_transform)[0] ==1 else 'neg')