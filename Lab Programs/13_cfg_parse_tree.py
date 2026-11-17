import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'a' | 'the'
N -> 'boy' | 'ball'
V -> 'kicked' | 'saw'
""")

parser = nltk.ChartParser(grammar)

sentence = "the boy kicked a ball".split()

for tree in parser.parse(sentence):
    print(tree)
    tree.pretty_print()
