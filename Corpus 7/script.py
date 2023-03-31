
import pandas
from corpus import Corpus

dir = "Corpus 7/"

def func(fin, fout):
    f = pandas.read_csv(f"{dir}{fin}")
    dataset = Corpus()
    for i in f.iterrows():
        row = i[1]
        label = row['sentiment']
        text = row['tweet_text']
        dataset.AddEntry(label, text)
    dataset.Save(f"{dir}{fout}")
    dataset.Stats()

func("minnesota_classified.csv", "c7minnesota")
func("training-dataset.csv", "c7training")