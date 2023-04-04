
import re
import nltk
import string
from nltk.tokenize import word_tokenize

# Does it make sense to make preprocessor a class, since it will mosty likely have only constant attributes, which could be just global variables?
# Probably not, although if at some point necessity for an internal variable for instance appears, class objects will allow it and global variables would not
class Preprocessor:
    def __init__(self):
        self.__token_url = "URL"
        self.__token_user = "USER"
    def __strip_urls(self, text):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls = re.findall(regex,text)
        for url in urls:
            text = text.replace(url[0], self.__token_url)
        return text
    def __strip_users(self, text):
        for word in text.split():
            if(word[0] == "@"):
                text = text.replace(word, self.__token_user)
        return text
    def __strip_stopwords(self, text):
        stopwords = set(nltk.corpus.stopwords.words('english'))
        words = []
        for word in self.WordTokenize(text):
            if word not in stopwords:
                words.append(word)
        return ' '.join(words)
    def __lemmatize(self, text):
        words = []
        lemmatize = nltk.WordNetLemmatizer().lemmatize
        for word in self.WordTokenize(text):
            words.append( lemmatize(word) )
        return ' '.join(words)
    def __strip_punctuation(self, text):
        punctuation = string.punctuation
        return text.translate(str.maketrans('', '', punctuation))
    def WordTokenize(self, text):
        return word_tokenize(text)
    def Preprocess(self, text):
        text = text.lower()
        text = self.__strip_urls(text)
        text = self.__strip_users(text)
        text = self.__lemmatize(text)
        text = self.__strip_punctuation(text)
        text = self.__strip_stopwords(text)
        return text