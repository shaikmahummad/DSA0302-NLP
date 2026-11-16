import nltk

patterns = [
    (r"^(I|you|he|she|we|they)$", "PRP"),
    (r".*ing$", "VBG"),
    (r".*ly$", "RB"),
    (r".*", "NN")
]

tagger = nltk.RegexpTagger(patterns)

sentence = "I love NLP"
tokens = nltk.word_tokenize(sentence)

print(tagger.tag(tokens))