import re 
def preprocess_string(str_arg):
    
    """"
        Parameters:
        ----------
        str_arg: example string to be preprocessed
        
        What the function does?
        -----------------------
        Preprocess the string argument - str_arg - such that :
        1. everything apart from letters is excluded
        2. multiple spaces are replaced by single space
        3. str_arg is converted to lower case 
        
        Example:
        --------
        Input :  Menu is absolutely perfect,loved it!
        Output:  ['menu', 'is', 'absolutely', 'perfect', 'loved', 'it']
        

        Returns:
        ---------
        Preprocessed string 
        
    """
    
    cleaned_str=re.sub('[^a-z\s]+',' ',str_arg,flags=re.IGNORECASE) #every char except alphabets is replaced
    cleaned_str=re.sub('(\s+)',' ',cleaned_str) #multiple spaces are replaced by single space
    cleaned_str=cleaned_str.lower() #converting the cleaned string to lower case
    
    return cleaned_str # eturning the preprocessed string in tokenized form