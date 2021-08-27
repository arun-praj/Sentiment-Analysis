# Feature Extraction Methods

    - Bag of word model
    - Bag of N-Grams model
    - TF-IDF model
    - Word2Vec
    - WOrd Embedding (Vectorization)

# Bags of wrods model.

    - The bag of word model is simple to understand and impelement. It is a way of extracting features from the text for use in machine learning algorithms. It has seen greate success in problems such as: NLP,Information retrieval from documents, Document Classifications.
    * Feature Extraction Process: input text -> clean text -> tokenize -> build vocabulary -> generate vectors -> ml algorithm.
        - Tokenization oberve and find out the frequency of each token.
        - Treate each sentence as separate docuement and make a list of words for all documents including punctuations.
        - bag of words =['word1','word2','word3','word4','word5','word6','word7','word8','word0','word10']
        - Vectors convert text that can be used by the ml algorith.
        - We take the first document (word1 word2 word3 word4) and checks the ferquency of words from the 10 unique words.
        - word1: 1
        - word2: 1
        - word3: 1
        - word4: 1
        - word5, word6, word7, word8, word9, word10:0
        - Same as for other document (sentences.) [1,1,1,1,0,0,0,0,0,0]
        - In this approach , each word or token is call a 'gram'. Creating a vocabulary of two-word pairs is called a bigram model. eg ('word1 word2','word2 word3')

    # Vectorization
        - The process of converting NLP text into numbers is called vectorization in ML.
            - eg:
                - couting the no. of times each word appear in a document.
                - calculating the frequnecy that each word appers in a document out of all the words in that doucment.

    # Bag of words implementation
        - Count Vectorizer
        - TF-IDF Vectorizer
        - N-Grams

# TF-IDF Algorithm or word ferquency algorithm.

    - Term Frequency - Inverse Document Frequency
        * Term Frequency: This measures the frequency of a word in a doucment.
            - When we are vectorizing the documents, we check for each words counts. In worst case if the term doesn't exist in the docuemnt, then the particular TF value is 0 and in other extreme case, if all the words in the documents are same then it will be 1. The final value of the normalised TF value will be in the range if [0 to 1].
        * Term frequency is how often a word appears in a document, divided by how many words there are.
        * Inverse Document Frequency: It is how unique or rate a word is.(loge(total no. of document/no. of document with term t in it.))
        * TF-IDF weight is the product of term frequency and inverse document frequency.
    - This is a technique to quantify a word in docuemnts, we generally compute a weight to each word which signifies the importance of the word in document and corpus. This method is widely used technique in Information Retrieval and Text Mining.
    - Its easy for us to understand the sentence but computer can only understand any data inly in the form of numerical value. So, we vectorize all of the text so computer can understand the text better.
    * t -> term (word)
    * d -> docuemnt (set of words)
    * n-> count of corpus
        - corpus -> total document set
