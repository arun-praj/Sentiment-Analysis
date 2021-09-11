from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def stemmerr(sentence):
    words = [stemmer.stem(word) for word in sentence.split(' ')]
    sentence = ' '.join(words)
    return sentence

def lemaa(sentence):
    words = [lemmatizer.lemmatize(word) for word in sentence.split(' ')]
    sentence = ' '.join(words)
    return sentence

def porter_stemmer(sentence):
    return stemmerr(lemaa(sentence))

sent1 = 'goes gone going'
# sent1 ='walk walking walked'
sent1 = porter_stemmer(sent1)
print(sent1)