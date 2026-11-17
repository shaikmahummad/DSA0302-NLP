import nltk

from nltk.tag import RegexpTagger

patterns = [
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*ly$', 'RB'),
    (r'.*ous$', 'JJ'),
    (r'.*s$', 'NNS'),
    (r'.*', 'NN')
]

tagger = RegexpTagger(patterns)

sentence = "The boys are playing happily".split()

print(tagger.tag(sentence))