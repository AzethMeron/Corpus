
import pandas
import copy
import sigfig
import pickle
import random
import jsonpickle

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
        self[tgt] = self[src]
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
                if sent not in sent_to_label: sent_to_label[sent] = []
                sent_to_label[sent].append(label)
        for sent in sent_to_label:
            if len(sent_to_label[sent]) > 1: 
                for label in sent_to_label[sent]:
                    repetitions.AddEntry(label, sent)
            else:
                label = sent_to_label[sent][0]
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
        

# This function was designed to be used with Corpus 2
# Due to differences in structure, each corpus available online requires it's own loading function, sadly
# Leaving as example "how-to"
def parse_csv(filename):
    f = pandas.read_csv(filename)
    output = Corpus()
    for i in f.iterrows():
        text = i[1]['text']
        label = i[1]['label']
        output.AddEntry(label, text)
    return output