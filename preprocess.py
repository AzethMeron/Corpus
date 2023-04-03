
import re
import nltk

# Does it make sense to make preprocessor a class, since it will mosty likely have only constant attributes, which could be just global variables?
# Probably not, although if at some point necessity for an internal variable for instance appears, class objects will allow it and global variables would not
class Preprocessor:
    def __init__(self):
        self.__tokenizer = None
        self.__lemmatizer = None
        self.__stopwords = None
        self.__interpuntion = None
        self.__token_url = "URL"
        self.__token_user = "USER"
    def __strip_urls(self, text):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls = re.findall(regex,text)
        for url in urls:
            text = text.replace(url[0], self.__token_url)
        return text
    def Tokenize(self, text):
        pass
    def Preprocess(self, text):
        text = text.lower()
        #
        return text