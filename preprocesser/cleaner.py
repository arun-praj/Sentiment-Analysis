import string,re
from time import perf_counter
from bs4 import BeautifulSoup
import emoji,contractions as cn

def cleaner(text_arg:"String"):
    """
        Parameters:
        ______________________________
        text_arg: String argument

        Goal:
        ______________________________
        1. converting all letters to lower or upper case
        2. converting numbers into words or removing numbers
        3. removing punctuations (.,!?*), accent marks and other diacritics
        4. removing white spaces
        5. expanding abbreviations
        6. removing stop words, sparse terms, and particular words
        7. text canonicalization

        Returns:
        ______________________________
        processed_string:String
    """

    # remove html tag
    soup = BeautifulSoup(text_arg, "html.parser")
    processed_string = soup.get_text()
    text_arg = re.sub('\[[^]]*\]', '', processed_string)
    
    # remove URLS
    processed_string = re.sub('http[s]?://\S+', '', processed_string)

    # remove hashtags
    processed_string = re.sub('#+',"",processed_string)

    # convert emoji to text
    processed_string = emoji.demojize(processed_string)

    # remove contractions . eg: I've : I have
    processed_string = cn.fix(processed_string)

    # remove special characters
    processed_string = re.sub(r'\W',' ',processed_string)

    # to lower
    processed_string = processed_string.lower()

    # remove all single characters
    processed_string = re.sub(r'\s+[a-zA-Z]\s+',' ',processed_string)

    # remove letter repetation
    processed_string = re.sub(r'(.)\1+',r'\1\1',processed_string)

    # remove punctuation
    processed_string = ''.join(ch for ch in processed_string if ch not in string.punctuation)

    #replace username
    replace_username_with = "user"
    processed_string = re.sub('B\@\w+',replace_username_with,processed_string)

    # remove multiple white space
    processed_string = re.sub('(\s+)',' ',processed_string)

    return processed_string

