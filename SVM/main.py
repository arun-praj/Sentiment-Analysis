import pickle

model = pickle.load(open('./SVM/model.sav','rb'))
vectorizer = pickle.load(open('./SVM/vectorizer.sav','rb'))

text = input('Enter your review: ')
vectorize_text = vectorizer.transform([text])
out = model.predict(vectorize_text)
print(text,":","pos" if out ==1 else "neg")