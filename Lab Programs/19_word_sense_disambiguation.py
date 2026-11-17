import nltk

from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('punkt_tab')

sentence = "I went to the bank to deposit money"

word = "bank"

tokens = word_tokenize(sentence)

sense = lesk(tokens, word)

if sense:
    print("Word:", word)
    print("Meaning:", sense.definition())
    print("Synset:", sense.name())
else:
    print("No meaning found")