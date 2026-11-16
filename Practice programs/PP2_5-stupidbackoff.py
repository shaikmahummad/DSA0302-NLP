from collections import Counter

corpus = [
    "i love python",
    "i love python",
    "i love machine learning",
    "python is easy",
    "machine learning is useful"
]

unigrams = Counter()
bigrams = Counter()
trigrams = Counter()

for sentence in corpus:
    words = sentence.split()
    unigrams.update(words)

    for i in range(len(words) - 1):
        bigrams[(words[i], words[i + 1])] += 1

    for i in range(len(words) - 2):
        trigrams[(words[i], words[i + 1], words[i + 2])] += 1


def get_score(sequence):
    words = sequence.lower().split()

    if len(words) != 3:
        print("Enter exactly three words.")
        return

    w1, w2, w3 = words

    if trigrams[(w1, w2, w3)] > 0:
        score = trigrams[(w1, w2, w3)]
        level = "Trigram"
    elif bigrams[(w2, w3)] > 0:
        score = bigrams[(w2, w3)] * 0.4
        level = "Bigram"
    else:
        score = unigrams[w3] * 0.16
        level = "Unigram"

    print("Sequence:", sequence)
    print("Level used:", level)
    print("Score:", score)


get_score("i love python")
get_score("we love python")
get_score("we enjoy python")