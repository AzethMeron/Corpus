
import pandas
from corpus import Corpus

dir = "Corpus 3/"
f = pandas.read_csv(f"{dir}go_emotions_dataset.csv")

labels = set(["admiration","amusement","anger","annoyance","approval","caring","confusion","curiosity","desire","disappointment","disapproval","disgust","embarrassment","excitement","fear","gratitude","grief","joy","love","nervousness","optimism","pride","realization","relief","remorse","sadness","surprise","neutral"])

dataset = Corpus()
unclear = Corpus()

for i in f.iterrows():
    row = i[1]
    text = row['text']
    if bool(row['example_very_unclear']): 
        unclear.AddEntry("unclear", text)
    else:
        labelset = set()
        for label in labels:
            if bool(row[label]):
                labelset.update(set([label]))
        if len(labelset) > 1: 
            unclear.AddEntry("unclear", text)
        else:
            for label in labelset:
                dataset.AddEntry(label, text)

dataset.Save(f"{dir}c3dataset")
unclear.Save(f"{dir}c3unclear")