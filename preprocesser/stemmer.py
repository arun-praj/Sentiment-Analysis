class AbstractStemmer:
    pass


class PorterStemmer(AbstractStemmer):
    """
    A Stemmer class
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
        """
            [C] VC * {m} [V]
            ie. m is the numbers of VC.
        """
        class_list = self._encode_word(word)
        if len(class_list) < 2:
            return 0
        if class_list[0] == 'C':  # if first elment is C remove it
            class_list = class_list[1:]
        if class_list[-1] == 'V': # if last elment is V remove it
            class_list = class_list[:len(class_list) - 1]

        m = len(class_list) // 2 if (len(class_list) / 2) >= 1 else 0
        return m

    def _check_endswith(self, stem, letters):
        """
            *v --> stem ends with letters sucn as S,L,T
        """
        for letter in letters:
            if stem.endswith(letter):
                return True
        return False
    def _check_vowel(self, stem):
        """
            *v* --> stem contains a vowel in between
        """
        for letter in stem:
            if letter in self.vowels:
                return True
        return False

    def _check_double_consonant(self, stem):
        """
            *d — stem ends with a double consonant of any type.
        """
        if stem[-1] in self.consonants and stem[-2] in self.consonants:
            return True
        return False
    
    def _check_o(self, stem):
        """
            *o — stem ends with cvc (consonant followed by vowel followed by consonant) where second 
            consonant is not W, X or Y (see, weird y again!).
        """
        if len(stem) <= 3:
            return False

        if stem[-3] in self.consonants and stem[-2] in self.vowels and stem[-1] in self.consonants:
            return True
        return False


    #PorterStemming Starts
    def _porter_step_1(self, word):
        """
            Deals with plurals and past participles
        """
        stem = word
        step2b = False

            #step1a
        #      SSES -> SS                         caresses  ->  caress
        #      IES  -> I                          ponies    ->  poni
        #                                           ties      ->  ti
        #      SS   -> SS                         caress    ->  caress
        #      S    -> epsolon                           cats      ->  cat

        if stem.endswith('sses'):
            stem = stem[:-2]
        elif stem.endswith('ies'):
            stem = stem[:-2]
        elif not stem.endswith('ss') and stem.endswith('s'):
            stem = stem[:-1]
    
        # Step 1b,

        # (m>0) EED -> EE                    feed      ->  feed
        #                                 agreed    ->  agree
        # (*v*) ED  ->                       plastered ->  plaster
        #                                 bled      ->  bled
        # (*v*) ING ->                       motoring  ->  motor
        #                                 sing      ->  sing
        # if steps 2 or 3 of 1b passes, another (sub)sub step has to be done
        # — this step will add letters.
        # Why? To be able to generalize better in further steps.

        if len(stem) > 4:
            if stem.endswith('eed') and self._determine_m(stem) > 0:
                stem = stem[:-1]
            elif stem.endswith('ed'):
                stem = stem[:-2]
                if not self._check_vowel(stem):
                    stem = word
                else:
                    step2b = True

            elif stem.endswith('ing'):
                stem = stem[:-3]
                if not self._check_vowel(stem):
                    stem = word
                else:
                    step2b = True
                
        # Step 1b,2
        # (if step 1b is true)
        # AT -> ATE                       conflat(ed)  ->  conflate
        # BL -> BLE                       troubl(ed)   ->  trouble
        # IZ -> IZE                       siz(ed)      ->  size
        # (*d and not (*L or *S or *Z))
        #        -> single letter
        #                                     hopp(ing)    ->  hop
        #                                     tann(ed)     ->  tan
        #                                     fall(ing)    ->  fall
        #                                     hiss(ing)    ->  hiss
        #                                     fizz(ed)     ->  fizz
        #      m=1 and *o) -> E               fail(ing)    ->  fail
        #                                     fil(ing)     ->  file
        if step2b:
            if stem.endswith('at') or stem.endswith('bl') or stem.endswith('iz'):
                stem += "e"
            elif self._check_double_consonant(stem) and not self._check_endswith(stem, "lsz"):
                stem = stem[:-1]
            elif self._determine_m(stem) == 1 and self._check_o(stem):
                stem += "e"

        #     Step 1c
        #     (*v*) Y -> I                    happy        ->  happi
        #                                 sky          ->  sky
        if self._check_vowel(stem) and stem.endswith('y'):
            stem = stem[:-1] + "i"

        return stem

    def _porter_step_2(self, stem):
        # Step 2

        # (m>0) ATIONAL ->  ATE           relational     ->  relate
        # (m>0) TIONAL  ->  TION          conditional    ->  condition
        #                                 rational       ->  rational
        # (m>0) ENCI    ->  ENCE          valenci        ->  valence
        # (m>0) ANCI    ->  ANCE          hesitanci      ->  hesitance
        # (m>0) IZER    ->  IZE           digitizer      ->  digitize
        # (m>0) ABLI    ->  ABLE          conformabli    ->  conformable
        # (m>0) ALLI    ->  AL            radicalli      ->  radical
        # (m>0) ENTLI   ->  ENT           differentli    ->  different
        # (m>0) ELI     ->  E             vileli        - >  vile
        # (m>0) OUSLI   ->  OUS           analogousli    ->  analogous
        # (m>0) IZATION ->  IZE           vietnamization ->  vietnamize
        # (m>0) ATION   ->  ATE           predication    ->  predicate
        # (m>0) ATOR    ->  ATE           operator       ->  operate
        # (m>0) ALISM   ->  AL            feudalism      ->  feudal
        # (m>0) IVENESS ->  IVE           decisiveness   ->  decisive
        # (m>0) FULNESS ->  FUL           hopefulness    ->  hopeful
        # (m>0) OUSNESS ->  OUS           callousness    ->  callous
        # (m>0) ALITI   ->  AL            formaliti      ->  formal
        # (m>0) IVITI   ->  IVE           sensitiviti    ->  sensitiv
        pair_tests = [('ational','ate'), ('tional','tion'), ('enci','ence'), ('anci','ance'), ('izer', 'ize'),
                      ('abli','able'), ('alli','al'), ('entli', 'ent'), ('eli', 'e'), ('ousli', 'ous'), ('ization', 'ize'),
                      ('ation', 'ate'), ('ator', 'ate'), ('alism', 'al'), ('iveness', 'ive'), ('fulness', 'ful'),
                      ('ousness', 'ous'), ('aliti','al'), ('ivit', 'ive'), ('biliti','ble')]

        if self._determine_m(stem) > 0:
            for termination, substitute in pair_tests:
                if stem.endswith(termination):
                    stem =  stem[: -len(termination)] + substitute
                    break
        return stem

    def _porter_step_3(self, stem):

        #  Step 3

        # (m>0) ICATE ->  IC              triplicate     ->  triplic
        # (m>0) ATIVE ->                  formative      ->  form
        # (m>0) ALIZE ->  AL              formalize      ->  formal
        # (m>0) ICITI ->  IC              electriciti    ->  electric
        # (m>0) ICAL  ->  IC              electrical     ->  electric
        # (m>0) FUL   ->                  hopeful        ->  hope
        # (m>0) NESS  ->                  goodness       ->  good
        pair_tests = [('icate','ic'),('ative',''),('alize','al'),('iciti','ic'),('ical','ic'),('ful',''),('ness','')]

        if self._determine_m(stem) > 0:
            for termination, substitute in pair_tests:
                if stem.endswith(termination):
                    stem =  stem[: -len(termination)] + substitute
                    break
        return stem

    def _porter_step_4(self, stem):
        """
        Remove suffixes
        """
        #     Step 4

        # (m>1) AL    ->                  revival        ->  reviv
        # (m>1) ANCE  ->                  allowance      ->  allow
        # (m>1) ENCE  ->                  inference      ->  infer
        # (m>1) ER    ->                  airliner       ->  airlin
        # (m>1) IC    ->                  gyroscopic     ->  gyroscop
        # (m>1) ABLE  ->                  adjustable     ->  adjust
        # (m>1) IBLE  ->                  defensible     ->  defens
        # (m>1) ANT   ->                  irritant       ->  irrit
        # (m>1) EMENT ->                  replacement    ->  replac
        # (m>1) MENT  ->                  adjustment     ->  adjust
        # (m>1) ENT   ->                  dependent      ->  depend
        # (m>1 and (*S or *T)) ION ->     adoption       ->  adopt
        # (m>1) OU    ->                  homologou      ->  homolog
        # (m>1) ISM   ->                  communism      ->  commun
        # (m>1) ATE   ->                  activate       ->  activ
        # (m>1) ITI   ->                  angulariti     ->  angular
        # (m>1) OUS   ->                  homologous     ->  homolog
        # (m>1) IVE   ->                  effective      ->  effect
        # (m>1) IZE   ->                  bowdlerize     ->  bowdler
        suffixes_1 = ['al','ance','ence','er','ic','able','ible','ant','ement','ment','ent']
        special_case = 'ion'
        suffixes_2 = ['ou','ism','ate','iti','ous','ive','ize']

        if self._determine_m(stem) > 1:
            for suffix in suffixes_1:
                if stem.endswith(suffix):
                    return stem[: -len(suffix)]
            if stem.endswith(special_case):
                temp = stem[: -len(special_case)]
                if self._check_endswith(temp, "st"):
                    return temp
            for suffix in suffixes_2:
                if stem.endswith(suffix):
                    return stem[: -len(suffix)]
        return stem

    def _porter_step_5(self, stem):
        # Step 5a

        #     (m>1) E     ->                  probate        ->  probat
        #                                     rate           ->  rate
        #     (m=1 and not *o) E ->           cease          ->  ceas

        # Step 5b

        #     (m > 1 and *d and *L) -> single letter
        #                                     controll       ->  control
        #                                     roll           ->  roll

        #step 5a
        if self._determine_m(stem) > 1 and stem.endswith('e') and len(stem) > 4:
            stem = stem[:-1]
        elif self._determine_m(stem) == 1 and not self._check_o(stem) and stem.endswith('e') and len(stem) > 4:
            stem = stem[:-1]
        #step5b
        if self._determine_m(stem) > 1 and self._check_endswith(stem, "dl") and len(stem) > 4:
            stem = stem[:-1]
        return stem
    
    def stem_now(self, sentence):
        """
            input: A string sentence
        """
        stem_words = []
        for stem in sentence.split():
            stem = self._porter_step_1(stem)
            stem = self._porter_step_2(stem)
            stem = self._porter_step_3(stem)
            stem = self._porter_step_4(stem)
            stem = self._porter_step_5(stem)
            stem_words.append(stem)
        
        return " ".join(stem_words)

# p = PorterStemmer()
# print(p._porter_step_4("aaa"))

