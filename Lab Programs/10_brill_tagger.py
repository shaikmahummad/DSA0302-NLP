import nltk

from nltk.corpus import treebank
from nltk.tag import RegexpTagger, UnigramTagger, BrillTaggerTrainer
from nltk.tag.brill import WordRule, PosRule

nltk.download('treebank')

train_data = treebank.tagged_sents()[:3000]

initial_tagger = RegexpTagger([
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*s$', 'NNS'),
    (r'.*', 'NN')
])

templates = [
    WordRule(PosRule, (True,)),
]

trainer = BrillTaggerTrainer(initial_tagger, templates)
tagger = trainer.train(train_data, max_rules=10)

sentence = "The company is growing rapidly".split()

print(tagger.tag(sentence))