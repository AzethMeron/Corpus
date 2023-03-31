# Python library for text corpus (NLP)
Repository created for my project on university while i'm working on dataset. 

Corpuses (csv/txt files) are taken from kaggle, links in Link.txt. 

I'm not adding bibliography because it's too early in development.

# Corpus class
Corpus class is created as unified model of text corpus, because online resources usually have very different structures and labeling. 

For each corpus we use, we convert it into Corpus class, allowing us to perform operations on it easily (like combining sets, truncating, stripping repetitions)

It's supposed to be used from live interpreter, manually.

```python
from corpus import Corpus
c = Corpus.Load("Corpus 2/c2") # Load corpus from file (WARNING ABOUT IT LATER)
c.Stats() # Display statistics
d = c.Copy() # Create carbon copy of corpus c
c.Truncate(2000) # Change the corpus, so every label has AT MOST 2000 entries (selection of entries is random!)
c.Balance(2000) # Change the corpus, so total size of dataset is around 2000 (selection of entries is random!)
e = c + d # Combine sets c and d
e.Transform(lambda t: t.upper()) # Change all texts to uppercase
joyful_texts = c['joy'] # Get all texts from 'joy' category (returns list)
len(joyful_texts) # Number of 'joy' texts
joyful_texts[10] # Get 11th element from joyful_texts list
c.SaveJSON("tmp.json")
```

Corpus.Save and Corpus.Load use python pickling and thus it's platform- and version-dependant. Use Corpus.SaveJSON and Corpus.LoadJSON instead fo long-term storage.

Internally, Corpus uses dictionary-of-lists, where labels (like joy, anger) are used as keys and texts are stored in the list under given key. Visualization:
```python
data = {
	'joy': [
		'i am feeling rather triumphant that i decided to disagree with davids notion that the real peak was further on and decided to give the side trail a chance', 
		'i can feel some kind of acceptance in the song which is why i gave the photo a kind of ecstatic ascension to a higher level of conscience aesthetic like a rapture of sort'
		], 
	'anger': [
		'i swamp uncaring unfeeling fucked up apathetic humanbeings who wont pull their heads out of their asses long enough to turn around and look at me and say i see you', 
		'i feel disgusted by the ugliness of the current society'
		]
	}
```

Loading csv file into Corpus depends on the structure given by corpus creators, so there's no universal code for that. Here's example for corpus 2 (which can be used in 2 more i think, with slight changes)
```python
from corpus import Corpus
import pandas
def parse_csv(filename):
    f = pandas.read_csv(filename)
    output = Corpus()
    for i in f.iterrows():
        text = i[1]['text']
        label = i[1]['label']
        output.AddEntry(label, text)
    return output

training = parse_csv("Corpus 2/training.csv")
```