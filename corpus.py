
import pandas
import copy
import sigfig
import pickle
import random
import jsonpickle
from nltk import FreqDist

# Designed to be easy to use and modify
# not to be fast

class Corpus(object):
    def __init__(self):
        self.__data = dict()
    def __getitem__(self, key):
        return self.__data[key]
    def __setitem__(self, key, value):
        self.__data[key] = value
    def __delitem__(self, key):
        del self.__data[key]
    def __add__(self, obj):
        output = self.Copy()
        for key in obj.Labels():
            if key not in output.Labels(): output[key] = []
            output[key] = output[key] + obj[key]
        return output
    def __len__(self): 
        size = 0
        for label in self.Labels():
            size = size + len(self[label])
        return size
    def __iter__(self):
        return iter(self.__data)
    def __contains__(self, key):
        return key in self.__data
    def AddEntry(self, label, text): # Add entry to corpus
        if label not in self.Labels(): self[label] = []
        self[label].append(text)
    def Labels(self): # Get all labels in corpus
        return set(self.__data.keys())
    def Relabel(self, src, tgt): # Change label from src to tgt
        if src not in self.Labels(): raise RuntimeError(f"Label {src} not in corpus")
        if tgt in self.Labels(): raise RuntimeError(f"Label {tgt} already in corpus")
        self[tgt] = self[src]
        del self[src]
    def Merge(self, src, tgt): # Add all entries from src label to the tgt label, then delete src label
        if src not in self.Labels(): raise RuntimeError(f"Label {src} not in corpus")
        if tgt not in self.Labels(): raise RuntimeError(f"Label {tgt} not in corpus")
        self[tgt] = self[tgt] + self[src]
        del self[src]
    def Stats(self): # Display stats of corpus
        print("===========================================")
        print(f"Labels in dataset: {self.Labels()}")
        size = len(self)
        print(f"Total size of dataset: {size}")
        for label in self.Labels():
            percentage = sigfig.round((len(self[label]) / size) * 100, sigfigs = 2)
            print(f"Label: {label}, amount: {len(self[label])} ({percentage}%)")
        print("===========================================")
    def Copy(self): # Create carbon copy
        return copy.deepcopy(self)
    def Save(self, filename): # Save (pickle)
        with open(filename, "wb") as file:
            pickle.dump(self.__data, file, -1)
    def Load(filename): # Load (pickle)
        with open(filename, "rb") as file:
            data = pickle.load(file)
            output = Corpus()
            output.__data = data
            return output
    def SaveJSON(self, filename): # Save (JSON)
        with open(filename, "w") as file:
            json = jsonpickle.encode(self.__data)
            file.write(json)
    def LoadJSON(filename): # Load (JSON)
        with open(filename, "r") as file:
            json = file.read()
            data = jsonpickle.decode(json)
            output = Corpus()
            output.__data = data
            return output
    def Repetitions(self): # Get number of repetitions in corpus
        sents = set()
        for label in self.Labels():
            sents.update( self[label] )
        return len(self) - len( sents )
    def Strip(self): # Remove all repeating entries
        output = Corpus()
        repetitions = Corpus()
        sent_to_label = dict()
        for label in self.Labels():
            for sent in self[label]:
                if sent not in sent_to_label: sent_to_label[sent] = set()
                sent_to_label[sent].add(label)
        for sent in sent_to_label:
            if len(sent_to_label[sent]) > 1: 
                for label in sent_to_label[sent]:
                    repetitions.AddEntry(label, sent)
            else:
                label = next(iter(sent_to_label[sent]))
                output.AddEntry(label, sent)
        return (output, repetitions)
    def Truncate(self, size_per_label):
        for label in self.Labels():
            random.shuffle(self[label])
            size = min(len(self[label]), size_per_label)
            self[label] = self[label][0:size-1]
    def Balance(self, total_size):
        size_per_label = int(total_size / len(self.Labels()))
        self.Truncate(size_per_label)
    def Transform(self, func):
        for label in self.Labels():
            for i, text in enumerate(self[label]):
                self[label][i] = func(self[label][i])
    def Split(self, train_percentage, test_percentage, validation_percentage):
        train_percentage = abs(train_percentage)
        test_percentage = abs(test_percentage)
        validation_percentage = abs(validation_percentage)
        if (train_percentage + test_percentage + validation_percentage) > 1: raise RuntimeError("Sum of percentages above 1") 
        train = Corpus()
        test = Corpus()
        validation = Corpus()
        for label in self.Labels():
            train_size = len(self[label]) * train_percentage
            test_size = len(self[label]) * test_percentage
            validation_size = len(self[label]) * validation_percentage
            random.shuffle(self[label])
            for i, text in enumerate(self[label]):
                if i < train_size:
                    train.AddEntry(label, text)
                elif i < train_size + test_size:
                    test.AddEntry(label, text)
                elif i < train_size + test_size + validation_size:
                    validation.AddEntry(label, text)
        return train, test, validation
    def Dataset(self):
        output = []
        for label in self.Labels():
            for text in self[label]:
                output.append( (text, label) )
        return output
    def DatasetXY(self):
        x = []
        y = []
        for label in self.Labels():
            for text in self[label]:
                x.append(text)
                y.append(label)
        return x, y
    def Vocabulary(self, tokenizer): # tokenizer(text) -> [ token1, token2, ... ]
        all_tokens = []
        for label in self.Labels():
            for text in self[label]:
                lokal_tokens = tokenizer(text)
                for token in lokal_tokens:
                    all_tokens.append(token)
        return FreqDist(all_tokens)
    def PrintCSV(self, filename, style = False):
        # style=False -> text,sentiment
        # style=True -> text,label1,label2
        data = self.Dataset()
        all_labels = list(self.Labels())
        with open(filename, "w") as file:
            if style:
                # Header
                file.write("text")
                for label in all_labels: file.write(f",{label}")
                file.write("\n")
                # Content
                for (text, label) in data:
                    file.write(text)
                    for l in all_labels:
                        if l == label: file.write(",1")
                        else: file.write(",0")
                    file.write("\n")
            else:
                file.write("text,sentiment\n")
                for (text, label) in data: file.write(f"{text},{label}\n")
    def ImportCSV(filename, label_text, label_sentiment):
        # Supports only style=False -> text,sentiment 
        f = pandas.read_csv(filename)
        output = Corpus()
        for i in f.iterrows():
            text = i[1][label_text]
            label = i[1][label_sentiment]
            output.AddEntry(label, text)
        return output
