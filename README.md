# Feature Extraction Methods

    - Bag of word model
    - Bag of N-Grams model
    - TF-IDF model
    - Word2Vec
    - WOrd Embedding (Vectorization)

# Bag of words

    - sent1 = good boy
    - sent2 = good girl
    - sent3 = boy girl good
    - words/frequency
        - good-> 3
        - boy -> 2
        - girl-> 2
    - Vectors
    | sn    | good | boy | girl | o/p |
    | ----- | ---- | --- | ---- | --- |
    | sent1 | 1    | 0   | 0    |     |
    | sent2 | 1    | 0   | 1    |     |
    | sent3 | 1    | 1   | 1    |     |

# Bags of words model.

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

    - Term Frequency = (no.of repeated words in sentece/no.of words in sentece)
    - IDF = log(no.of sentences / no.of sentences containing words)
    - TF-IDF = TF*IDF
        - sent1 = good boy
        - sent2 = good girl
        - sent3 = boy girl good
        - words/frequency
            - good-> 3
            - boy -> 2
            - girl-> 2
            TF->
            | sn   | sent1 | sent2 | sent3 |
            | ---- | ----- | ----- | ----- |
            | good | 1/2   | 1\2   | 1/3   |
            | boy  | 1/2   | 0     | 1/3   |
            | girl | 0     | 1\2   | 1/3   |
            IDF->
            | words | IDF        |
            | ----- | ---------- |
            | good  | log(3/3)=0 |
            | boy   | log(3/2)   |
            | girl  | log(3/2) |
            TF_IDF->
            | sn    | f1   | f2            | f3            | o/p |
            | ----- | ---- | ------------- | ------------- | --- |
            |       | good | boy           | girl          |     |
            | sent1 | 0    | 1/2\*log(3/2) | 0             |     |
            | sent2 | 0    | 0             | 1/2\*log(3/2) |     |
            | sent3 |      |               |               |     |

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

# TF_IDF problems:

    - bow and tf-idf approach semantic information is not stored.
    - TF_IDF impportance to uncommon words.
    - chance of overfitting

# Word2Vec

    - Each word is basically represented as a vector of 32 or more dimension instead of a singular number.
    - Here the semantic information and relation between different words is also preserved.

# How to convert Text to Vectorizer

    - We can use either CountVectorizer or TfidfTransfomer
    - In this project we use TfidfVectorizer (uses bothCountVectorizer and TfidfTransfomer)

# Tokenization:

    - breakup the sentence into words.(sentence into list)
    - nltk is analysis of words not sentences.

# Stop words

    - That does add any meaning.

# Stemming and Lemmatization

    - process of reducing infected words to their word stem
    - eg: going,goes,gone -> go

# CountVectorizer

    - Convert all sentences into vectors.
    - Bags of Words
    -

# CountVectorizer vs. TD-IDF

    -
