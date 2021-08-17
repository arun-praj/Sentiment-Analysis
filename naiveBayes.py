# from preprocesser import cleaner
import pandas as pd
import numpy as np
from collections import defaultdict # defaultdict prevents from key error in dictionaries

from preprocesser import cleaner,stemmer

class NaiveBayes:
    """Implementation of Naive Bayes algorith from scratch."""

    def __init__(self, unique_classes):
        self.classes = unique_classes # unique classes such as 0,1 for sentiment

    def addToBow(self,example,dict_index):
        """
            Bow means Bag of words
        """
        if isinstance(example, np.ndarray):
            example = example[0]
        # example=example[0]
        
        # print(dict_index)
        for token_word in example.split(): #for every word in preprocessed example
            self.bow_dicts[dict_index][token_word]+=1 #increment in its count
        
    def train(self, dataset, labels,stem = False,clean = False):
        self.examples = dataset
        self.labels = labels
        self.bow_dicts = np.array(defaultdict(lambda: 0) for index in range(self.classes.shape[0]))

        #only convert to numpy arrays if initially not passed as numpy arrays 
        if not isinstance(self.examples, np.ndarray):
            self.examples = np.array(self.examples)
        if not isinstance(self.examples, np.ndarray):
            self.examples = np.array(self.examples)
        
        ps = stemmer.PorterStemmer()
        for cat_index, category in enumerate(self.classes):
            # classes = [1,2,3,4]

            all_cat_examples = self.examples[self.labels == category] 
            #filter all examples of categories
            # first for category 1 then 2 then 3 and so on....
            # processed_example = all_cat_examples
            # get examples processed
            cleaned_examples = [cleaner(cat_example) for cat_example in all_cat_examples]

            # if clean:
            #     processed_example = [cleaner(cat_example) for cat_example in all_cat_examples]
            # if stem:
            #     processed_example = [ps.stem_now(sentence) for sentence in processed_example]
            
            cleaned_examples = pd.DataFrame(data = cleaned_examples)

            np.apply_along_axis(self.addToBow, 1, cleaned_examples, cat_index)
            # return cleaned_examples
            # return isinstance(cleaned_examples,np.ndarray)

# nb = NaiveBayes(['a', 'b'])