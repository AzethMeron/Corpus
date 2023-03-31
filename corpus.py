
import pandas
import copy
import sigfig
import pickle
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
    def AddEntry(self, label, text):
        if label not in self.Labels(): self[label] = []
        self[label].append(text)
    def Labels(self):
        return set(self.__data.keys())
    def Relabel(self, src, tgt):
        if src not in self.Labels(): raise RuntimeError(f"Label {src} not in corpus")
        if tgt in self.Labels(): raise RuntimeError(f"Label {tgt} already in corpus")
        self[tgt] = self[src]
        del self[src]
    def Merge(self, src, tgt):
        if src not in self.Labels(): raise RuntimeError(f"Label {src} not in corpus")
        if tgt not in self.Labels(): raise RuntimeError(f"Label {tgt} not in corpus")
        self[tgt] = self[src]
        del self[src]
    def Stats(self):
        print("===========================================")
        print(f"Labels in dataset: {self.Labels()}")
        size = len(self)
        print(f"Total size of dataset: {size}")
        for label in self.Labels():
            percentage = sigfig.round((len(self[label]) / size) * 100, sigfigs = 2)
            print(f"Label: {label}, amount: {len(self[label])} ({percentage}%)")
        print("===========================================")
    def Copy(self):
        return copy.deepcopy(self)
    def Save(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.__data, file, -1)
    def Load(filename):
        with open(filename, "rb") as file:
            data = pickle.load(file)
            output = Corpus()
            output.__data = data
            return output
    def Repetitions(self):
        sents = set()
        for label in self.Labels():
            sents.update( self[label] )
        return len(self) - len(sents)

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