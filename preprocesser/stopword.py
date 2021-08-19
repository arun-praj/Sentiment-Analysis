from nltk.corpus import stopwords  

def removing_stopwords(sentence):
    stop_wr=set(stopwords.words('english'))

    filter_tokens = [word for word in sentence.split(' ') if word.lower() not in stop_wr]
    filtered_text = ' '.join(filter_tokens)

    return filtered_text