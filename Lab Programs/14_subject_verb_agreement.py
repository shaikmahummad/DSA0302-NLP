import nltk

grammar = nltk.CFG.fromstring("""
S -> SG | PL
SG -> NP_SG VP_SG
PL -> NP_PL VP_PL
NP_SG -> 'he' | 'she'
NP_PL -> 'they' | 'we'
VP_SG -> 'runs' | 'plays'
VP_PL -> 'run' | 'play'
""")

parser = nltk.ChartParser(grammar)

sentences = [
    "he runs",
    "they run",
    "she plays",
    "we play",
    "he run"
]

for sentence in sentences:
    tokens = sentence.split()
    trees = list(parser.parse(tokens))

    if trees:
        print(sentence, ": Grammatically Valid")
    else:
        print(sentence, ": Grammatically Invalid")