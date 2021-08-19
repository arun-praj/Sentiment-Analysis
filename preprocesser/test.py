from cleaner import cleaner
from stopword import removing_stopwords

text = '<h1>Hello world</h1> ,my, name is hero and he is god, they said to me.'
text = cleaner(text)
text = removing_stopwords(text)

print(text)