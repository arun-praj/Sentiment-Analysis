class AbstractStemmer:
    pass


class PorterStemmer(AbstractStemmer):
    """
    tutorial from: https://medium.com/analytics-vidhya/building-a-stemmer-492e9a128e84
    """
    consonants = "bcdfghjklmnpqrstwxz"
    special_case = "y"
    vowels = "aeiou"

    def _divide_into_groups(self, word):
        """
            Divides each word according to vowel and consonents
            eg. tree -> [t,r,ee]
        """
        groups = []
        preceding = ""
        for index,letter in enumerate(word.lower()):
            if preceding == "":
                preceding = letter
            else:
                if self._compare_same_class(preceding,letter):
                    preceding += letter
                else:
                    groups.append(preceding)
                    preceding  = letter
                    if index == len(word)-1:
                        groups.append(letter)
            
        return groups

    def _compare_same_class(self,letter1, letter2):
        if letter1 in self.consonants and letter2 in self.consonants:
            return True
        elif letter1 in self.vowels and letter2 in self.vowels:
            return True
        else:
            return False
        return False

    def _determine_class(self,letter):
        if letter[0] in self.consonants:
            return 'C'
        return 'V'

    def _encode_word(self,word):
        divided_list = self._divide_into_groups(word)
        classified = [self._determine_class(letter) for letter in divided_list]
        return classified
        print(dict(zip(divided_list, classified)))
        
    def _determine_m(self, word):
        class_list = self._encode_word(word)
        if len(class_list) < 2:
            return 0
        if class_list[0] == 'C':  # if first elment is C remove it
            class_list = class_list[1:]
        if class_list[-1] == 'V': # if last elment is V remove it
            class_list = class_list[:len(class_list) - 1]

        m = len(class_list) // 2 if (len(class_list) / 2) >= 1 else 0
        print(m)
        


   

p = PorterStemmer()
p._determine_m("oaten")

