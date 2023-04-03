
# Does it make sense to make preprocessor a class, since it will mosty likely have only constant attributes, which could be just global variables?
# Probably not, although if at some point necessity for an internal variable for instance appears, class objects will allow it and global variables would not
class Preprocessor:
    def _init__(self):
        self.__tokenizer = None
        self.__lemmatizer = None
        self.__stopwords = None
        self.__interpuntion = None
    def Tokenize(self, text):
        pass
    def Preprocess(self, text);
        text = text.lower()
        #
        return text