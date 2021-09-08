from nltk.stem.porter import *
stemmer = PorterStemmer()

def porter_stemmer(sentence):
    words = [stemmer.stem(word) for word in sentence.split(' ')]
    sentence = ' '.join(words)
    return sentence
