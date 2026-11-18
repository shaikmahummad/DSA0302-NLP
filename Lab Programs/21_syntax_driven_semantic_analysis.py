import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N | Det Adj N | N
VP -> V NP | V
Det -> 'the' | 'a' | 'an'
Adj -> 'young' | 'beautiful' | 'intelligent'
N -> 'student' | 'teacher' | 'book' | 'dog'
V -> 'reads' | 'likes' | 'teaches'
""")

sentence = input("Enter a sentence: ").lower()
tokens = nltk.word_tokenize(sentence)

parser = RecursiveDescentParser(grammar)

for tree in parser.parse(tokens):
    print("\nSyntax Tree:")
    tree.pretty_print()

    print("\nNoun Phrases and Their Meanings:")
    for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
        phrase = " ".join(subtree.leaves())
        print("\nNoun Phrase:", phrase)

        for word in phrase.split():
            if word in ['the', 'a', 'an']:
                continue

            synsets = wordnet.synsets(word, pos=wordnet.NOUN)

            if synsets:
                print(word, ":", synsets[0].definition())
            else:
                print(word, ": Meaning not found")

    break
else:
    print("Sentence does not match the grammar.")