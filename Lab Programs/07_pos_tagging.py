import nltk

from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

text = "The quick brown fox jumps over the lazy dog"

words = word_tokenize(text)
tags = nltk.pos_tag(words)

print(tags)